# Terraform Configuration for AWS Data Pipeline
# This creates the infrastructure for the data pipeline

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Data Lake S3 Buckets
resource "aws_s3_bucket" "bronze" {
  bucket = "${var.project_name}-bronze-${var.environment}"

  versioning {
    enabled = true
  }

  lifecycle_rule {
    enabled = true

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    expiration {
      days = 365
    }
  }

  tags = var.common_tags
}

resource "aws_s3_bucket" "silver" {
  bucket = "${var.project_name}-silver-${var.environment}"

  versioning {
    enabled = true
  }

  lifecycle_rule {
    enabled = true

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    expiration {
      days = 365
    }
  }

  tags = var.common_tags
}

resource "aws_s3_bucket" "gold" {
  bucket = "${var.project_name}-gold-${var.environment}"

  versioning {
    enabled = true
  }

  tags = var.common_tags
}

resource "aws_s3_bucket" "artifacts" {
  bucket = "${var.project_name}-artifacts-${var.environment}"

  versioning {
    enabled = true
  }

  tags = var.common_tags
}

# IAM Role for Glue Jobs
resource "aws_iam_role" "glue_role" {
  name = "${var.project_name}-glue-role-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "glue.amazonaws.com"
        }
      }
    ]
  })

  tags = var.common_tags
}

resource "aws_iam_role_policy_attachment" "glue_s3" {
  role       = aws_iam_role.glue_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_role_policy_attachment" "glue_cloudwatch" {
  role       = aws_iam_role.glue_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonGlueServiceRole"
}

# Glue Database
resource "aws_glue_catalog_database" "data_lake" {
  name = "${var.project_name}_db_${var.environment}"
}

# Glue Job for Transformation
resource "aws_glue_job" "transform_job" {
  name         = "${var.project_name}-transform-${var.environment}"
  role_arn     = aws_iam_role.glue_role.arn
  glue_version = "4.0"
  worker_type  = "G.1X"
  number_of_workers = var.glue_workers

  command {
    script_location = "s3://${aws_s3_bucket.artifacts.bucket}/jobs/transform.py"
    python_version  = "3"
  }

  default_arguments = {
    "--job-language" = "python"
    "--env"          = var.environment
  }

  tags = var.common_tags
}

# CloudWatch Alarms
resource "aws_cloudwatch_metric_alarm" "glue_job_failure" {
  alarm_name          = "${var.project_name}-glue-failure-${var.environment}"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "1"
  metric_name         = "glue.driver.progress"
  namespace           = "AWS/Glue"
  period              = "300"
  statistic           = "Minimum"
  threshold           = "0"
  alarm_description   = "Alert if Glue job fails"
  alarm_actions       = [aws_sns_topic.alerts.arn]

  dimensions = {
    JobName = aws_glue_job.transform_job.name
  }
}

# SNS Topic for Alerts
resource "aws_sns_topic" "alerts" {
  name = "${var.project_name}-alerts-${var.environment}"
}

resource "aws_sns_topic_subscription" "email" {
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "email"
  endpoint  = var.alert_email
}
