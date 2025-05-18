import json
import pytest
from unittest.mock import patch, AsyncMock

import lambda_function

@pytest.fixture(autouse=True)
def mock_queries_and_create_items():
    """
    Garante que toda instância de QueriesAndCreateItens seja mockada com AsyncMock.
    """
    with patch("lambda_function.QueriesAndCreateItens") as MockClass:
        instance = MockClass.return_value
        instance.create_multiple_items_with_random_ids = AsyncMock()
        instance.query_by_id_between_dates      = AsyncMock()
        instance.gsi_query                       = AsyncMock()
        yield instance


def make_event(op):
    return {"operation": op}


# Testes do handler assíncrono (_async_handler)
@pytest.mark.asyncio
async def test_async_handler_create(mock_queries_and_create_items):
    mock_queries_and_create_items.create_multiple_items_with_random_ids.return_value = {
        "statusCode": 200,
        "body": json.dumps({"message": "create ok"})
    }

    response = await lambda_function._async_handler(make_event("create"), None)

    mock_queries_and_create_items.create_multiple_items_with_random_ids.assert_awaited_once()
    assert response["statusCode"] == 200
    assert json.loads(response["body"])['message'] == "create ok"
    

@pytest.mark.asyncio
async def test_async_handler_invalid_operation(mock_queries_and_create_items):
    response = await lambda_function._async_handler(make_event("dffads"), None)

    mock_queries_and_create_items.create_multiple_items_with_random_ids.assert_not_awaited()
    mock_queries_and_create_items.query_by_id_between_dates.assert_not_awaited()
    mock_queries_and_create_items.gsi_query.assert_not_awaited()
    
    body = json.loads(response["body"])        
    message_json = json.loads(body["message"]) 

    assert response["statusCode"] == 400
    assert message_json["error"] == "Invalid operation: dffads"

    

@pytest.mark.asyncio
async def test_async_handler_query(mock_queries_and_create_items):
    mock_queries_and_create_items.query_by_id_between_dates.return_value = {
        "statusCode": 200,
        "body": json.dumps({"message": "query ok"})
    }

    response = await lambda_function._async_handler(make_event("query"), None)

    mock_queries_and_create_items.query_by_id_between_dates.assert_awaited_once()
    assert response["statusCode"] == 200
    assert json.loads(response["body"])['message'] == "query ok"


@pytest.mark.asyncio
async def test_async_handler_gsi(mock_queries_and_create_items):
    mock_queries_and_create_items.gsi_query.return_value = {
        "statusCode": 200,
        "body": json.dumps({"message": "gsi ok"})
    }

    response = await lambda_function._async_handler(make_event("gsi_query"), None)

    mock_queries_and_create_items.gsi_query.assert_awaited_once()
    assert response["statusCode"] == 200
    assert json.loads(response["body"])['message'] == "gsi ok"


# Test do entrypoint síncrono (lambda_handler)
def test_sync_entrypoint(monkeypatch):
    # Prepara um retorno fictício do async handler sem rodar um loop real
    expected = {"statusCode": 204, "body": json.dumps({"msg": "sync"})}

    async def fake_async(event, context):
        return expected

    monkeypatch.setattr(lambda_function, '_async_handler', fake_async)

    # Chama o entrypoint síncrono
    result = lambda_function.lambda_handler(make_event("whatever"), None)
    assert result is expected
