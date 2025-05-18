provider "aws" {
  region = "us-east-1"
}

module "infrastructure" {
  source = "./modules"

  lambda_function_name = "GSItesting"
  dynamodb_table_name  = "GSI-dynamodb-table-testing"
}
