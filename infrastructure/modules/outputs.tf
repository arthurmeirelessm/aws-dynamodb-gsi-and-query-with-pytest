output "lambda_function_name" {
  value = aws_lambda_function.this.function_name
}

output "dynamodb_table_name" {
  value = aws_dynamodb_table.this.name
}


output "codebuild_role_arn" {
  value = aws_iam_role.codebuild_role.arn
  description = "ARN da role do CodeBuild"
}


