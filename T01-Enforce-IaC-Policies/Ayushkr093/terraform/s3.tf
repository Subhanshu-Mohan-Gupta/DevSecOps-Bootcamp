# Public ACL
resource "aws_s3_bucket" "public_acl" {
  bucket = "${var.project_name}-public"

  tags = {
    Environment = var.environment
  }
}

# Separate ACL resource (recommended approach)
resource "aws_s3_bucket_acl" "public_acl" {
  bucket = aws_s3_bucket.public_acl.id
  acl    = var.insecure_acl
}

# Missing tag
resource "aws_s3_bucket" "missing_tag" {
  bucket = "${var.project_name}-no-tags"

  tags = {
    Name = "missing-environment"
  }
}

resource "aws_s3_bucket_acl" "missing_tag_acl" {
  bucket = aws_s3_bucket.missing_tag.id
  acl    = "private"
}

# Versioning disabled - FIXED
resource "aws_s3_bucket_versioning" "missing_tag_versioning" {
  bucket = aws_s3_bucket.missing_tag.id
  
  versioning_configuration {
    status = "Disabled"
  }
}

# Compliant bucket
resource "aws_s3_bucket" "compliant" {
  bucket = "${var.project_name}-secure"

  tags = {
    Environment = var.environment
  }
}

resource "aws_s3_bucket_acl" "compliant_acl" {
  bucket = aws_s3_bucket.compliant.id
  acl    = "private"
}

# Compliant versioning - FIXED
resource "aws_s3_bucket_versioning" "compliant_versioning" {
  bucket = aws_s3_bucket.compliant.id
  
  versioning_configuration {
    status = "Enabled"
  }
}

