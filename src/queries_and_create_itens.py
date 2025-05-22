import json
import aioboto3
import uuid
import os
from datetime import datetime, timedelta, timezone
import random
from dotenv import load_dotenv
from boto3.dynamodb.conditions import Key


load_dotenv()

class QueriesAndCreateItens:
    def __init__(self):
        self.session = aioboto3.Session()
        self.region = os.getenv("AWS_DEFAULT_REGION")
        self.table_name = os.getenv("TABLE_NAME")
        self.aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.CATEGORIES = ["books", "electronics", "fashion", "games"]

    
    
    async def create_multiple_items_with_random_ids(self, count: int):
        print(count)
        try:
            if not isinstance(count, int):
                return {
                    "statusCode": 400,
                    "body": json.dumps({
                        "message": "Valor de count não é inteiro",
                    })
                }
            async with self.session.resource(
                "dynamodb",
                region_name=self.region,
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
            ) as dynamodb:
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

    
    