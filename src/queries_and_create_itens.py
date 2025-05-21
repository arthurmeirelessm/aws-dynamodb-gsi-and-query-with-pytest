import json
import aioboto3
import uuid
from datetime import datetime, timedelta, timezone
import random
from boto3.dynamodb.conditions import Key

class QueriesAndCreateItens:
    def __init__(self):
        self.session = aioboto3.Session()
        self.table_name = "GSI-dynamodb-table-testing"
        self.CATEGORIES = ["books", "electronics", "fashion", "games"]

    
    
    async def create_multiple_items_with_random_ids(self, count: int):
        try:
            if not isinstance(count, int):
                return {
                    "statusCode": 400,
                    "body": json.dumps({
                        "message": "Valor de count não é inteiro",
                    })
                }
            async with self.session.resource("dynamodb") as dynamodb:
                table = await dynamodb.Table(self.table_name)
                fixed_ids = [f"item-{i}" for i in range(1, 6)]

                for _ in range(count):
                    item = {
                        "id": random.choice(fixed_ids),
                        "created_at": (
                            datetime.now(timezone.utc) +
                            timedelta(seconds=random.randint(0, 300))
                        ).isoformat(),
                        "category": random.choice(self.CATEGORIES)
                    }
                    await table.put_item(Item=item)

            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "Itens foram criados!",
                })
            }

        except Exception as e:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": str(e)})
            }

    
    