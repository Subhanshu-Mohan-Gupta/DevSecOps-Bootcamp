# 1. Configure Terraform and the AWS Provider
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# 2. Create the OIDC Identity Provider for GitHub
resource "aws_iam_openid_connect_provider" "github" {
  url = "https://token.actions.githubusercontent.com"
  client_id_list = [
    "sts.amazonaws.com"
  ]
  thumbprint_list = ["6938fd4d98bab03faadb97b34396831e3780aea1"]
}

# 3. Define the IAM Role for GitHub Actions to Assume (Deployment Role)
resource "aws_iam_role" "github_actions_deploy_role" {
  name = "github-actions-deploy-role"

  # Trust policy allowing GitHub's OIDC provider to assume this role.
  # It is scoped to your specific repository and main branch for security.
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Federated = aws_iam_openid_connect_provider.github.arn
        },
        Action = "sts:AssumeRoleWithWebIdentity",
        Condition = {
          StringEquals = {
            # Change this to your GitHub org/user and repo name!
            "token.actions.githubusercontent.com:sub" : "repo:GoutamTx/zero-trust-lambda:ref:refs/heads/main"
          }
        }
      }
    ]
  })
}

# 4. Define and Attach Permissions for the Deployment Role
resource "aws_iam_policy" "lambda_deploy_policy" {
  name        = "lambda-deploy-policy"
  description = "Policy for GitHub Actions to deploy the sample Lambda."
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "lambda:CreateFunction",
          "lambda:UpdateFunctionCode",
          "lambda:UpdateFunctionConfiguration",
          "lambda:GetFunction",
          "iam:PassRole"
        ],
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "deploy_policy_attachment" {
  role       = aws_iam_role.github_actions_deploy_role.name
  policy_arn = aws_iam_policy.lambda_deploy_policy.arn
}

# 5. Define the IAM Role for the Lambda to Use at Runtime (Execution Role)
resource "aws_iam_role" "lambda_execution_role" {
  name = "sample-lambda-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect    = "Allow",
        Principal = { Service = "lambda.amazonaws.com" },
        Action    = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}
