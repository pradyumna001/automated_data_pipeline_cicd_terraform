# Terraform Outputs

output "bronze_bucket" {
  description = "Bronze layer S3 bucket"
  value       = aws_s3_bucket.bronze.id
}

output "silver_bucket" {
  description = "Silver layer S3 bucket"
  value       = aws_s3_bucket.silver.id
}

output "gold_bucket" {
  description = "Gold layer S3 bucket"
  value       = aws_s3_bucket.gold.id
}

output "artifacts_bucket" {
  description = "Artifacts S3 bucket"
  value       = aws_s3_bucket.artifacts.id
}

output "glue_job_name" {
  description = "Glue job name"
  value       = aws_glue_job.transform_job.name
}

output "glue_role_arn" {
  description = "Glue IAM role ARN"
  value       = aws_iam_role.glue_role.arn
}

output "sns_topic_arn" {
  description = "SNS topic ARN for alerts"
  value       = aws_sns_topic.alerts.arn
}
