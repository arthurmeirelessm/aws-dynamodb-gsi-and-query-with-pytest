import json
import aioboto3
import uuid
import datetime
import random
from boto3.dynamodb.conditions import Key

class QueriesAndCreateItens:
    def __init__(self):
        self.session = aioboto3.Session()
        self.table_name = "GSI-dynamodb-table-testing"
        self.CATEGORIES = ["books", "electronics", "fashion", "games"]

    async def gsi_query(self):
        try:
            async with self.session.resource("dynamodb") as dynamodb:
                table = dynamodb.Table(self.table_name)
                category_to_query = "books"

                response = await table.query(
                    IndexName="GSICategoryIndex",
                    KeyConditionExpression=Key("category").eq(category_to_query)
                )
                items = response.get("Items", [])

            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": f"{len(items)} itens encontrados para categoria '{category_to_query}'",
                    "items": items
                })
            }

        except Exception as e:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": str(e)})
            }

    
    async def create_multiple_items_with_random_ids(self):
        try:
            async with self.session.resource("dynamodb") as dynamodb:
                table = dynamodb.Table(self.table_name)
                fixed_ids = [f"item-{i}" for i in range(1, 6)]

                for _ in range(50):
                    item = {
                        "id": random.choice(fixed_ids),
                        "created_at": (
                            datetime.datetime.utcnow()
                            + datetime.timedelta(seconds=random.randint(0, 300))
                        ).isoformat(),
                        "category": random.choice(self.CATEGORIES)
                    }
                    await table.put_item(Item=item)

            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "50 itens com IDs fixos inseridos com sucesso para teste de query!",
                    "ids_usados": fixed_ids
                })
            }

        except Exception as e:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": str(e)})
            }

    
    
    async def query_by_id_between_dates(self):
        target_id = "item-3"
        start_dt = "2025-05-16T03:37:55.498413"
        end_dt   = "2025-05-18T03:38:07.381326"

        try:
            async with self.session.resource("dynamodb") as dynamodb:
                table = await dynamodb.Table(self.table_name)

                response = await table.query(
                    KeyConditionExpression=(
                        Key("id").eq(target_id) &
                        Key("created_at").between(start_dt, end_dt)
                    ),
                    ScanIndexForward=True
                )
                items = response.get("Items", [])

            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": (
                        f"{len(items)} itens encontrados para ID '{target_id}' "
                        f"entre {start_dt} e {end_dt}"
                    ),
                    "items": items
                })
            }

        except Exception as e:
            return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
