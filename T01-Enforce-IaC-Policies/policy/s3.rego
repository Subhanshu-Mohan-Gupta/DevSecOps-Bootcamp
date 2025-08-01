package main

deny[msg] {
  resource := input.resource.aws_s3_bucket[_]
  resource.acl == "public-read"
  msg := "❌ S3 bucket ACL should not be public-read."
}
