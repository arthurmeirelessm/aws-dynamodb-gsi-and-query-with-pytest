# Código build (projeto CodeBuild)
resource "aws_codebuild_project" "this" {
  name          = var.project_name
  service_role  = var.codebuild_role_arn
  description   = "Build project for ${var.project_name}"

  artifacts {
    type = "CODEPIPELINE"
  }

  environment {
    compute_type                = "BUILD_GENERAL1_SMALL"
    image                       = "aws/codebuild/standard:5.0"
    type                        = "LINUX_CONTAINER"
    privileged_mode             = true

    environment_variable {
      name  = "ECR_REPO_URI"
      value = var.ecr_repo_uri
      type  = "PLAINTEXT"
    }
  }

  source {
    type            = "CODEPIPELINE"
    buildspec       = var.buildspec_path
  }

  tags = var.tags
}