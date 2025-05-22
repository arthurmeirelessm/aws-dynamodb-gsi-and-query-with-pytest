resource "aws_codepipeline" "this" {
  name     = var.pipeline_name
  role_arn = var.pipeline_role_arn

  artifact_store {
    type     = "S3"
    location = var.artifact_bucket_name
  }

  stage {
    name = "Source"

    action {
      name             = "GitHubSource"
      category         = "Source"
      owner            = "AWS"
      provider         = "CodeStarSourceConnection"
      version          = "1"
      output_artifacts = ["source_output"]

      configuration = {
        ConnectionArn    = var.codestar_connection_arn
        FullRepositoryId = "${var.repo_owner}/${var.repo_name}"
        BranchName       = var.branch
        DetectChanges    = "false"
      }
    }
  }

  stage {
    name = "Build"

    action {
      name             = "Build"
      category         = "Build"
      owner            = "AWS"
      provider         = "CodeBuild"
      input_artifacts  = ["source_output"]
      output_artifacts = ["build_output"]
      version          = "1"

      configuration = {
        ProjectName = aws_codebuild_project.this.name
      }
    }
  }

  tags = var.tags
}
