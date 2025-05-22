variable "lambda_function_name" {
  type        = string
  description = "Nome da função Lambda"
}

variable "dynamodb_table_name" {
  type        = string
  description = "Nome da tabela DynamoDB"
}

variable "project_name" {
  description = "Nome do projeto CodeBuild"
  type        = string
}

variable "codebuild_role_arn" {
  description = "ARN da role do CodeBuild"
  type        = string
}

variable "ecr_repo_uri" {
  description = "URI do repositório ECR (ex.: 123456789012.dkr.ecr.us-east-1.amazonaws.com/repo)"
  type        = string
}

variable "buildspec_path" {
  description = "Caminho para o arquivo buildspec.yml"
  type        = string
}

variable "tags" {
  description = "Tags aplicadas aos recursos"
  type        = map(string)
}

variable "pipeline_name" {
  description = "Nome do pipeline CodePipeline"
  type        = string
}

variable "pipeline_role_arn" {
  description = "ARN da role do CodePipeline"
  type        = string
}

variable "artifact_bucket_name" {
  description = "Nome do bucket S3 para armazenar os artefatos do pipeline"
  type        = string
}

variable "codestar_connection_arn" {
  description = "ARN da conexão CodeStar (GitHub/Bitbucket)"
  type        = string
}

variable "repo_owner" {
  description = "Dono do repositório (usuário ou organização)"
  type        = string
}

variable "repo_name" {
  description = "Nome do repositório no GitHub"
  type        = string
}

variable "branch" {
  description = "Branch a ser utilizado no pipeline (ex.: main, master, develop)"
  type        = string
}
