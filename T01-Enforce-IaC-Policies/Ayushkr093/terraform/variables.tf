variable "aws_region" {
  type        = string
  description = "AWS region"
  default     = "ap-south-1"
}

variable "ami_id" {
  type        = string
  description = "AMI ID for EC2"
  default     = "ami-020cba7c55df1f615"
}

variable "project_name" {
  type        = string
  description = "Project name prefix"
  default     = "rego-demo"
}

variable "environment" {
  type        = string
  description = "Environment name"
  default     = "dev"
}

variable "owner" {
  type        = string
  description = "Owner tag"
  default     = "devops-team"
}

variable "insecure_acl" {
  type        = string
  description = "ACL for testing public-read bucket"
  default     = "public-read"
}

variable "bad_instance_type" {
  type        = string
  description = "Non-compliant instance type"
  default     = "t3.micro"
}

variable "allowed_instance_type" {
  type        = string
  description = "Compliant instance type 1"
  default     = "t3.micro"
}

variable "allowed_instance_type_2" {
  type        = string
  description = "Compliant instance type 2"
  default     = "t4g.micro"
}

variable "root_volume_size" {
  type        = number
  description = "Size of root volume in GB"
  default     = 8
}
