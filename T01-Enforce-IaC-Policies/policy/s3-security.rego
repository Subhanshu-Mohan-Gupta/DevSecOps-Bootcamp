package main

deny[msg] {
    resource := input.planned_values.root_module.resources[_]
    resource.type == "aws_s3_bucket"
    resource.values.acl == "public-read"
    msg := sprintf("S3 bucket '%s' has public-read ACL - security violation", [resource.name])
}

deny[msg] {
    resource := input.planned_values.root_module.resources[_]
    resource.type == "aws_s3_bucket"
    resource.values.acl == "public-read-write"
    msg := sprintf("S3 bucket '%s' has public-read-write ACL - security violation", [resource.name])
}

deny[msg] {
    resource := input.planned_values.root_module.resources[_]
    resource.type == "aws_s3_bucket"
    count(resource.values.server_side_encryption_configuration) == 0
    msg := sprintf("S3 bucket '%s' must have encryption enabled", [resource.name])
}
