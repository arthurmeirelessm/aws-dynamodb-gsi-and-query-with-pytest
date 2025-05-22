resource "aws_ecr_repository" "meu_repositorio" {
  name                 = "meu-repositorio"
  image_tag_mutability = "MUTABLE"  # Ou "IMMUTABLE" se quiser impedir sobrescrita de tags
  force_delete         = true       # Remove o repositório mesmo se tiver imagens

  image_scanning_configuration {
    scan_on_push = true            # Ativa varredura de vulnerabilidades ao enviar imagens
  }

  encryption_configuration {
    encryption_type = "AES256"   
  }

  tags = {
    Ambiente = "dev"
    Projeto  = "meu-projeto"
  }
}
