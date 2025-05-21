import pytest
from unittest.mock import AsyncMock, MagicMock
import json
from queries_and_create_itens import QueriesAndCreateItens  # ajuste o caminho se necessário

@pytest.mark.asyncio
async def test_create_with_stubbed_client():
    # Mock da tabela com put_item como async
    mock_table = AsyncMock()
    mock_table.put_item.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}

    # Mock do resource().Table()
    mock_dynamodb = AsyncMock()
    mock_dynamodb.Table.return_value = mock_table

    # Simula o async context manager do session.resource()
    mock_resource_context = AsyncMock()
    mock_resource_context.__aenter__.return_value = mock_dynamodb

    mock_session = MagicMock()
    mock_session.resource.return_value = mock_resource_context

    # Substitui a session pela mockada
    svc = QueriesAndCreateItens()
    svc.session = mock_session

    response = await svc.create_multiple_items_with_random_ids("1")
    print("Response", response)

    assert response["statusCode"] == 200
    assert json.loads(response["body"])["message"] == "Itens foram criados!"
    mock_table.put_item.assert_called()
