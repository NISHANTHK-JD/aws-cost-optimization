output "lambda_function_name" {
  description = "Name of the deployed Lambda function"
  value       = aws_lambda_function.ebs_cleanup.function_name
}

output "lambda_function_arn" {
  description = "ARN of the Lambda function"
  value       = aws_lambda_function.ebs_cleanup.arn
}

output "sns_topic_arn" {
  description = "ARN of the SNS alert topic"
  value       = aws_sns_topic.alerts.arn
}

output "cloudwatch_log_group" {
  description = "CloudWatch Log Group for Lambda logs"
  value       = aws_cloudwatch_log_group.lambda_logs.name
}

output "eventbridge_rule_name" {
  description = "EventBridge rule that triggers the Lambda"
  value       = aws_cloudwatch_event_rule.daily_trigger.name
}
