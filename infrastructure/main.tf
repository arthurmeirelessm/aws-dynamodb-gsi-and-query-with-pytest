provider "aws" {
  region = "us-east-1"
}

module "infrastructure" {
  source = "./modules"

  lambda_function_name = "GSItesting"
  dynamodb_table_name  = "GSI-dynamodb-table-testing"
  project_name         = "GSItesting-project"
  codebuild_role_arn   = ""
  ecr_repo_uri         = var.ecr_repo_uri
  buildspec_path       = var.buildspec_path
  tags                 = var.tags
  pipeline_name        = var.pipeline_name
  pipeline_role_arn    = var.pipeline_role_arn
  artifact_bucket_name = var.artifact_bucket_name
  codestar_connection_arn = var.codestar_connection_arn
  repo_owner           = var.repo_owner
  repo_name            = ""
  branch               = "main"
}

