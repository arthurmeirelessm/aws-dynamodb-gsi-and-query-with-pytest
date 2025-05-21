import asyncio
import json
from queries_and_create_itens import QueriesAndCreateItens

async def _async_handler(event, context):
    operation = event.get("operation")
    svc = QueriesAndCreateItens()
 
    if operation: 
            if operation == "create":
                return await svc.create_multiple_items_with_random_ids(event["count"])
            elif operation == "query":
                return await svc.query_by_id_between_dates()
            elif operation == "gsi_query":
                return await svc.gsi_query()
            else: 
                return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": json.dumps({"error": f"Invalid operation: {operation}"}),
                })
            }
    return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": json.dumps({"error": f"Operation not found"}),
                })
            }      
                

def lambda_handler(event, context):
    return asyncio.run(_async_handler(event, context))
