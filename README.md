# 💰 AWS Cost Optimization Automation
### Automated FinOps & SecOps Solution for Unused EBS Volumes & Orphaned Snapshots

![AWS](https://img.shields.io/badge/AWS-Lambda%20%7C%20CloudWatch%20%7C%20SNS%20%7C%20IAM-orange?style=for-the-badge&logo=amazon-aws)
![Terraform](https://img.shields.io/badge/Terraform-IaC-purple?style=for-the-badge&logo=terraform)
![Python](https://img.shields.io/badge/Python-3.9-blue?style=for-the-badge&logo=python)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=for-the-badge)

---

## 📌 Problem Statement

In large AWS environments, **unused EBS volumes** and **orphaned snapshots** silently accumulate over time — especially after EC2 instances are terminated — leading to unnecessary cloud storage costs that are often overlooked.

This project delivers a **fully automated, serverless solution** to detect and clean up these resources on a scheduled basis, with built-in compliance controls and security alerts — saving up to **30% on monthly AWS storage costs**.

---

## 🏗️ Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│                    AWS Cloud Environment                       │
│                                                                │
│  ┌─────────────────┐     triggers      ┌──────────────────┐  │
│  │  CloudWatch      │ ──────────────► │  AWS Lambda       │  │
│  │  EventBridge     │   (Scheduled)    │  (Python 3.9)     │  │
│  │  (Cron Rule)     │                  │                   │  │
│  └─────────────────┘                  └────────┬─────────┘  │
│                                                 │             │
│                    ┌────────────────────────────┤             │
│                    │                            │             │
│                    ▼                            ▼             │
│           ┌──────────────┐            ┌──────────────────┐   │
│           │  AWS SNS      │            │  EC2 / EBS        │   │
│           │  (Alert +     │            │  Volumes &        │   │
│           │  Approval)    │            │  Snapshots        │   │
│           └──────────────┘            └──────────────────┘   │
│                                                                │
│  ┌─────────────────┐     ┌──────────────────────────────┐    │
│  │  CloudWatch Logs │     │  IAM Role (Least Privilege)  │    │
│  │  (Audit Trail)   │     │  + AWS Config (Compliance)   │    │
│  └─────────────────┘     └──────────────────────────────┘    │
│                                                                │
│  [All infrastructure provisioned via Terraform]               │
└──────────────────────────────────────────────────────────────┘
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **Auto-Detection** | Scans all regions for unattached EBS volumes and orphaned snapshots |
| ⏰ **Scheduled Execution** | CloudWatch EventBridge cron triggers Lambda at regular intervals |
| 📧 **SNS Pre-Deletion Alerts** | Notifies team before deletion — supports manual approval gate |
| 🔐 **Least Privilege IAM** | Lambda has only the minimum permissions needed |
| 📋 **Audit Logging** | CloudWatch Logs records every deleted resource for compliance |
| 🏗️ **Terraform IaC** | 100% infrastructure-as-code — no manual AWS console setup |
| 💰 **Cost Savings** | Achieved 30% reduction in monthly AWS storage costs |

---

## 🛠️ Tech Stack

- **AWS Lambda** — Serverless compute for scan & cleanup logic
- **Python 3.9** — Lambda function runtime
- **AWS CloudWatch EventBridge** — Scheduled trigger (cron)
- **AWS SNS** — Pre-deletion notification & approval alerts
- **AWS IAM** — Least-privilege role for Lambda execution
- **AWS CloudWatch Logs** — Full audit trail of all actions
- **Terraform** — Infrastructure provisioning (IaC)

---

## 📁 Project Structure

```
aws-cost-optimization/
├── terraform/
│   ├── main.tf              # Core AWS resource definitions
│   ├── lambda.tf            # Lambda function + trigger config
│   ├── iam.tf               # IAM role with least-privilege policy
│   ├── cloudwatch.tf        # EventBridge cron rule + Log Group
│   ├── sns.tf               # SNS topic + subscription
│   ├── variables.tf         # Input variables
│   └── outputs.tf           # Output values
├── lambda/
│   ├── handler.py           # Main Lambda function (Python)
│   └── requirements.txt     # Python dependencies
├── docs/
│   └── architecture.png     # Architecture diagram
└── README.md
```

---

## 🚀 How It Works — Step by Step

### Step 1: Scheduled Trigger
CloudWatch EventBridge fires a cron event at a defined interval (e.g., daily at 2 AM UTC).

### Step 2: Lambda Scans AWS
The Python Lambda function uses `boto3` to:
- List all EBS volumes with state = `available` (not attached to any EC2)
- List all snapshots not associated with any existing volume or AMI

### Step 3: SNS Notification
Before any deletion, an SNS alert is sent to the configured email/Slack with:
- Resource IDs found
- Region
- Estimated cost savings
- Approval window (configurable)

### Step 4: Cleanup & Logging
After the approval window, resources are deleted. Every action is logged to CloudWatch with:
- Timestamp
- Resource ID
- Region
- Action taken (Deleted / Skipped)

---

## ⚙️ Setup & Deployment

### Prerequisites
- AWS CLI configured (`aws configure`)
- Terraform >= 1.0 installed
- Python 3.9+

### Deploy with Terraform

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/aws-cost-optimization.git
cd aws-cost-optimization/terraform

# Initialize Terraform
terraform init

# Preview changes
terraform plan

# Deploy infrastructure
terraform apply
```

### Lambda Environment Variables

| Variable | Description |
|---|---|
| `SNS_TOPIC_ARN` | ARN of the SNS topic for alerts |
| `DRY_RUN` | Set `true` to scan without deleting (safe mode) |
| `APPROVAL_WINDOW_HOURS` | Hours to wait before deletion after alert |
| `REGIONS` | Comma-separated AWS regions to scan |

---

## 🔐 Security & Compliance

- IAM Role follows **least-privilege principle** — Lambda can only describe/delete EBS volumes and snapshots
- **No wildcard `*` permissions** in IAM policy
- CloudWatch Logs retention set to **90 days** for audit compliance
- SNS approval gate ensures **no surprise deletions**
- Compatible with **AWS Config rules** for continuous compliance monitoring

---

## 📊 Results Achieved

| Metric | Before | After |
|---|---|---|
| Monthly EBS storage cost | Baseline | **-30% reduction** |
| Manual cleanup effort | Weekly manual review | **Zero manual work** |
| Compliance audit readiness | Manual log checks | **Automated audit trail** |
| Alert response time | N/A | **< 5 minutes via SNS** |

---

## 🎯 Key Learnings

- How to build event-driven serverless architectures on AWS
- FinOps principles: identifying and eliminating cloud waste programmatically
- DevSecOps: embedding security (least privilege, audit logging) into automation
- Terraform best practices: modular IaC, remote state, and variable management

---

## 👤 Author

**Nishanth Kumar J** — DevOps Engineer  
📧 nishanthk211969@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/nishanthkumar-janarthanam-5a60b219a)
