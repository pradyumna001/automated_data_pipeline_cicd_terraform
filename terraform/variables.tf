# Terraform Variables

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "data-pipeline"
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "glue_workers" {
  description = "Number of Glue workers"
  type        = number
  default     = 10
}

variable "alert_email" {
  description = "Email for alerts"
  type        = string
  default     = "alerts@example.com"
}

variable "common_tags" {
  description = "Common tags for all resources"
  type        = map(string)
  default = {
    Project     = "data-pipeline"
    ManagedBy   = "Terraform"
    Environment = "dev"
  }
}
