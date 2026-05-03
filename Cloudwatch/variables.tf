variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "alert_email" {
  description = "Email address to receive SNS alerts before deletion"
  type        = string
}

variable "dry_run" {
  description = "If true, scan only — no deletions will happen"
  type        = string
  default     = "true"
}

variable "approval_window_hours" {
  description = "Hours to wait after SNS alert before deletion"
  type        = string
  default     = "24"
}
