import boto3
import os
import json
import logging
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ec2 = boto3.client("ec2")
sns = boto3.client("sns")

SNS_TOPIC_ARN         = os.environ.get("SNS_TOPIC_ARN", "")
DRY_RUN               = os.environ.get("DRY_RUN", "true").lower() == "true"
APPROVAL_WINDOW_HOURS = int(os.environ.get("APPROVAL_WINDOW_HOURS", "24"))


def get_unused_volumes():
    """Return all EBS volumes in 'available' state (not attached to any EC2)."""
    response = ec2.describe_volumes(
        Filters=[{"Name": "status", "Values": ["available"]}]
    )
    volumes = response.get("Volumes", [])
    logger.info(f"Found {len(volumes)} unused EBS volumes")
    return volumes


def get_orphaned_snapshots():
    """Return snapshots not associated with any existing volume or AMI."""
    # Get all current volume IDs
    all_volumes = ec2.describe_volumes()["Volumes"]
    active_volume_ids = {v["VolumeId"] for v in all_volumes}

    # Get all snapshots owned by this account
    snapshots = ec2.describe_snapshots(OwnerIds=["self"])["Snapshots"]

    orphaned = []
    for snap in snapshots:
        volume_id = snap.get("VolumeId", "")
        if volume_id and volume_id not in active_volume_ids:
            orphaned.append(snap)

    logger.info(f"Found {len(orphaned)} orphaned snapshots")
    return orphaned


def send_alert(volumes, snapshots):
    """Send SNS notification before deletion."""
    vol_ids   = [v["VolumeId"] for v in volumes]
    snap_ids  = [s["SnapshotId"] for s in snapshots]

    message = (
        f"EBS Cost Optimizer — Pre-Deletion Alert\n"
        f"{'='*50}\n"
        f"Timestamp : {datetime.utcnow().isoformat()} UTC\n"
        f"DRY RUN   : {DRY_RUN}\n\n"
        f"Unused EBS Volumes ({len(vol_ids)}):\n"
        + "\n".join(f"  - {v}" for v in vol_ids) +
        f"\n\nOrphaned Snapshots ({len(snap_ids)}):\n"
        + "\n".join(f"  - {s}" for s in snap_ids) +
        f"\n\nApproval window: {APPROVAL_WINDOW_HOURS} hours\n"
        f"If DRY_RUN=false, these resources will be deleted after the window."
    )

    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject="[AWS Cost Optimizer] Pre-Deletion Alert",
        Message=message
    )
    logger.info("SNS alert sent successfully")


def delete_volumes(volumes):
    """Delete unused EBS volumes and log each action."""
    deleted, failed = [], []
    for vol in volumes:
        vol_id = vol["VolumeId"]
        try:
            ec2.delete_volume(VolumeId=vol_id)
            logger.info(f"DELETED volume: {vol_id}")
            deleted.append(vol_id)
        except Exception as e:
            logger.error(f"FAILED to delete volume {vol_id}: {e}")
            failed.append(vol_id)
    return deleted, failed


def delete_snapshots(snapshots):
    """Delete orphaned snapshots and log each action."""
    deleted, failed = [], []
    for snap in snapshots:
        snap_id = snap["SnapshotId"]
        try:
            ec2.delete_snapshot(SnapshotId=snap_id)
            logger.info(f"DELETED snapshot: {snap_id}")
            deleted.append(snap_id)
        except Exception as e:
            logger.error(f"FAILED to delete snapshot {snap_id}: {e}")
            failed.append(snap_id)
    return deleted, failed


def lambda_handler(event, context):
    logger.info(f"Starting EBS Cost Optimizer | DRY_RUN={DRY_RUN}")

    volumes   = get_unused_volumes()
    snapshots = get_orphaned_snapshots()

    if not volumes and not snapshots:
        logger.info("No unused resources found. Nothing to clean up.")
        return {"statusCode": 200, "body": "No unused resources found"}

    # Always send alert first
    if SNS_TOPIC_ARN:
        send_alert(volumes, snapshots)

    result = {
        "dry_run"            : DRY_RUN,
        "volumes_found"      : len(volumes),
        "snapshots_found"    : len(snapshots),
        "volumes_deleted"    : [],
        "snapshots_deleted"  : [],
        "volumes_failed"     : [],
        "snapshots_failed"   : [],
    }

    if DRY_RUN:
        logger.info("DRY RUN mode — no resources deleted")
        result["message"] = "DRY RUN complete. Set DRY_RUN=false to enable deletion."
    else:
        vol_deleted, vol_failed   = delete_volumes(volumes)
        snap_deleted, snap_failed = delete_snapshots(snapshots)

        result["volumes_deleted"]   = vol_deleted
        result["snapshots_deleted"] = snap_deleted
        result["volumes_failed"]    = vol_failed
        result["snapshots_failed"]  = snap_failed
        result["message"]           = "Cleanup complete"

    logger.info(f"Result: {json.dumps(result, indent=2)}")
    return {"statusCode": 200, "body": json.dumps(result)}
