resource "aws_s3_bucket" "example" {
  bucket = "my-public-bucket"
  acl    = "public-read"
}
