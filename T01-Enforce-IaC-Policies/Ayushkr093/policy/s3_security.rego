package main

import future.keywords.contains
import future.keywords.if

# S3: No public ACL (public-read)
deny contains msg if {
  resource := input.planned_values.root_module.resources[_]
  resource.type == "aws_s3_bucket_acl"
  acl := resource.values.acl
  acl == "public-read"
  msg := sprintf("S3 bucket ACL '%s' should not be public-read", [resource.name])
}

# S3: No public ACL (public-read-write)
deny contains msg if {
  resource := input.planned_values.root_module.resources[_]
  resource.type == "aws_s3_bucket_acl"
  acl := resource.values.acl
  acl == "public-read-write"
  msg := sprintf("S3 bucket ACL '%s' should not be public-read-write", [resource.name])
}

# S3: Versioning enabled
deny contains msg if {
  resource := input.planned_values.root_module.resources[_]
  resource.type == "aws_s3_bucket_versioning"
  versioning_config := resource.values.versioning_configuration[0]
  versioning_config.status != "Enabled"
  msg := sprintf("S3 bucket versioning '%s' must have status 'Enabled', got '%s'", [resource.name, versioning_config.status])
}

# S3: Environment tag required
deny contains msg if {
  resource := input.planned_values.root_module.resources[_]
  resource.type == "aws_s3_bucket"
  tags := object.get(resource.values, "tags", {})
  not object.get(tags, "Environment", null)
  msg := sprintf("S3 bucket '%s' must have the 'Environment' tag", [resource.name])
}
