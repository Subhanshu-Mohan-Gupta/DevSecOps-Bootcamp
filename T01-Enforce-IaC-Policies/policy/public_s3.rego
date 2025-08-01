package main

deny[msg] {
  rc := input.resource_changes[_]
  rc.type == "aws_s3_bucket"
  rc.change.after.acl == "public-read"

  msg := sprintf("S3 bucket '%v' should not have public-read ACL", [rc.name])
}




