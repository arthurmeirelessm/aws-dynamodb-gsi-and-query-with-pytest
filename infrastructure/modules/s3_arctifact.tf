resource "aws_s3_bucket" "codepipeline_artifacts" {
  bucket = var.artifact_bucket
}


resource "aws_s3_bucket_versioning" "codepipeline_artifacts" {
  bucket = aws_s3_bucket.codepipeline_artifacts.id

  versioning_configuration {
    status = "Enabled"
  }
}