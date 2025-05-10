import json
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Orders')

def lambda_handler(event, context):
    for record in event['Records']:
        try:
            # Step 1: Parse outer SQS body (SNS format)
            sns_payload = json.loads(record['body'])

            # Step 2: Parse inner SNS "Message" (stringified JSON)
            message = json.loads(sns_payload['Message'])

            # Step 3: Validate required fields
            required_fields = ['orderId', 'userId', 'itemName']
            if not all(field in message for field in required_fields):
                print("ERROR: Missing required fields in message")
                continue

            # Step 4: Set default values if not provided
            message.setdefault('quantity', 1)
            message.setdefault('status', 'new')
            message.setdefault('timestamp', datetime.utcnow().isoformat())

            # Step 5: Store to DynamoDB
            table.put_item(Item=message)
            print(f"Order {message['orderId']} stored successfully")

        except Exception as e:
            print(f"ERROR processing message: {str(e)}")
            raise  # Ensures retry / DLQ behavior

    return {
        'statusCode': 200,
        'body': json.dumps('Orders processed successfully')
    }
