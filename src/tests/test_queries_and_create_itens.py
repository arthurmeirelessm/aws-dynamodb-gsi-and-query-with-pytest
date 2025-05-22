import pytest
import json
import random
from datetime import datetime, timezone, timedelta
from unittest.mock import AsyncMock, MagicMock
from queries_and_create_itens import QueriesAndCreateItens

@pytest.fixture
def mock_dynamodb_service():
     # Mock da tabela e do método put_item
     mock_table = AsyncMock()
     mock_table.put_item.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}

     # Mock do recurso DynamoDB
     mock_dynamodb = AsyncMock()
     mock_dynamodb.Table.return_value = mock_table

     # Context manager do session.resource
     mock_resource_context = AsyncMock()
     mock_resource_context.__aenter__.return_value = mock_dynamodb

     # Sessão DynamoDB mockada
     mock_session = MagicMock()
     mock_session.resource.return_value = mock_resource_context

     # Instância do serviço com sessão mockada
     svc = QueriesAndCreateItens()
     svc.session = mock_session

     return svc, mock_table

@pytest.mark.asyncio
async def test_success_single_item(mock_dynamodb_service):
     svc, mock_table = mock_dynamodb_service

     response = await svc.create_multiple_items_with_random_ids(1)
     body = json.loads(response["body"])

     assert response["statusCode"] == 200
     assert body["message"] == "Itens foram criados!"
     # Verifica que put_item foi chamado exatamente uma vez
     assert mock_table.put_item.call_count == 1
     # Verifica os campos do item enviado
     _, kwargs = mock_table.put_item.call_args
     item = kwargs.get("Item")
     assert item["id"].startswith("item-")
     assert "created_at" in item
     assert item["category"] in svc.CATEGORIES

@pytest.mark.asyncio
async def test_success_multiple_items(mock_dynamodb_service):
     svc, mock_table = mock_dynamodb_service
     count = 5

     response = await svc.create_multiple_items_with_random_ids(count)
     body = json.loads(response["body"])

     assert response["statusCode"] == 200
     assert body["message"] == "Itens foram criados!"
     # Verifica que put_item foi chamado exatamente 'count' vezes
     assert mock_table.put_item.call_count == count

@pytest.mark.asyncio
@pytest.mark.parametrize("invalid_count", ["1", None, 1.5, [], {}])
async def test_invalid_count_types(mock_dynamodb_service, invalid_count):
     svc, mock_table = mock_dynamodb_service

     response = await svc.create_multiple_items_with_random_ids(invalid_count)
     body = json.loads(response["body"])

     assert response["statusCode"] == 400
     assert body["message"] == "Valor de count não é inteiro"
     # put_item não deve ser chamado quando count é inválido
     mock_table.put_item.assert_not_called()

@pytest.mark.asyncio
async def test_put_item_exception_triggers_500(mock_dynamodb_service):
     svc, mock_table = mock_dynamodb_service
     # Simula erro no put_item
     mock_table.put_item.side_effect = Exception("DynamoDB falhou")

     response = await svc.create_multiple_items_with_random_ids(1)
     body = json.loads(response["body"])

     assert response["statusCode"] == 500
     assert "DynamoDB falhou" in body["error"]
