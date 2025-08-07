provider "aws" {
  region                      = "us-east-1"
  access_key                  = "fake"
  secret_key                  = "fake"
  skip_credentials_validation = true
  skip_requesting_account_id = true
}

resource "aws_s3_bucket" "bad_bucket" {
  bucket = "my-insecure-bucket"
  acl    = "public-read"
}



