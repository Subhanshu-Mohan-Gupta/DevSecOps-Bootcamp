# Fails multiple checks
resource "aws_instance" "bad_instance" {
  ami           = var.ami_id
  instance_type = var.bad_instance_type
  monitoring    = false

  root_block_device {
    volume_size = var.root_volume_size
    encrypted   = false
  }

  tags = {}
}

# Missing required tags
resource "aws_instance" "missing_tags" {
  ami           = var.ami_id
  instance_type = var.allowed_instance_type
  monitoring    = true

  root_block_device {
    volume_size = var.root_volume_size
    encrypted   = true
  }

  tags = {
    Project = var.project_name
  }
}

# Compliant
resource "aws_instance" "compliant" {
  ami           = var.ami_id
  instance_type = var.allowed_instance_type_2
  monitoring    = true

  root_block_device {
    volume_size = var.root_volume_size
    encrypted   = true
  }

  tags = {
    Environment = var.environment
    Owner       = var.owner
    Project     = var.project_name
  }
}
