provider "aws" {
  region     = "us-east-1"
  access_key = "fake"
  secret_key = "fake"
}

resource "aws_s3_bucket" "bad_bucket" {
  bucket = "my-insecure-bucket"
  acl    = "public-read"
}



