output "s3_bucket_names" {
  value = [
    aws_s3_bucket.public_acl.bucket,
    aws_s3_bucket.missing_tag.bucket,
    aws_s3_bucket.compliant.bucket
  ]
}

output "ec2_instance_ids" {
  value = [
    aws_instance.bad_instance.id,
    aws_instance.missing_tags.id,
    aws_instance.compliant.id
  ]
}
