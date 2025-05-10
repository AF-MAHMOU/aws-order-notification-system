# aws-order-notification-system
Event-driven order processing using AWS SNS, SQS, Lambda &amp; DynamoDB

📐 Architecture Overview
This system implements an event-driven architecture to process e-commerce orders using AWS managed services.

![sequence](https://github.com/user-attachments/assets/ff51eb09-a2d2-4196-90e3-d4487d9dc92b)

🧩 Components 
Amazon SNS (OrderTopic):
Publishes order notifications to subscribed SQS queues.

Amazon SQS (OrderQueue):
Buffers incoming order events; integrates with DLQ for failed deliveries.

AWS Lambda (ProcessOrder):
Consumes messages from SQS and processes orders.

Amazon DynamoDB (Orders):
Stores processed order data persistently.

Dead Letter Queue (DLQ):
Receives failed messages after 3 unsuccessful Lambda attempts.

⚙️ Setup Instructions
1. Prerequisites
AWS account with appropriate permissions

AWS CLI configured (optional for testing)

2. Infrastructure Deployment
🔸 DynamoDB Table
Name: Orders

Partition Key: orderId (String)

Attributes: userId, itemName, quantity, status, timestamp

🔸 SNS Topic
Name: OrderTopic

Action: Subscribe the SQS queue to this topic

🔸 SQS Queue
Name: OrderQueue

DLQ Configuration:

MaxReceiveCount: 3

Redrive policy: Enabled

🔸 Lambda Function
Name: ProcessOrder

Runtime: Python 3.12

Trigger: SQS Queue (OrderQueue)

IAM Role Permissions:

sqs:ReceiveMessage

dynamodb:PutItem

logs:* (CloudWatch)

3. Lambda Function Code
The complete implementation is in the lambda_function.py file. Ensure the function parses incoming JSON and writes to DynamoDB.

🧪 Testing the System
Publish a Test Message:
aws sns publish \
  --topic-arn arn:aws:sns:<REGION>:<ACCOUNT_ID>:OrderTopic \
  --message '{
    "orderId": "O1234",
    "userId": "U123",
    "itemName": "Laptop",
    "quantity": 1,
    "status": "new",
    "timestamp": "2025-05-03T12:00:00Z"
  }'
  
Verification Steps:
✅ Check SQS metrics (Messages sent/received)

✅ View Lambda logs in CloudWatch

✅ Scan the DynamoDB Orders table for entries

