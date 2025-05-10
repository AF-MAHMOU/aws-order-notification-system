# AWS Order Notification System
**Event-driven order processing using AWS SNS, SQS, Lambda & DynamoDB**

## 📐 Architecture Overview
This system implements an event-driven architecture to process e-commerce orders using AWS managed services.

# Architecture Diagram

![architecture diagram](https://github.com/user-attachments/assets/6ea19a1a-c98f-4357-b4d5-7edcbc1d808f)


## 🧩 Components
| Service | Purpose | Key Features |
|---------|---------|--------------|
| **Amazon SNS (OrderTopic)** | Notification hub | Fanout to multiple subscribers |
| **Amazon SQS (OrderQueue)** | Message buffer | DLQ integration, 30s visibility timeout |
| **AWS Lambda (ProcessOrder)** | Order processor | Python 3.12, SQS-triggered |
| **DynamoDB (Orders)** | Data storage | orderId partition key |
| **Dead Letter Queue** | Error handling | Catches messages after 3 failures |

## ⚙️ Setup Instructions

### Prerequisites
- AWS account with IAM permissions
- AWS CLI (optional for testing)

### Infrastructure Deployment
1. **DynamoDB Table**
   ```bash
   aws dynamodb create-table \
     --table-name Orders \
     --attribute-definitions AttributeName=orderId,AttributeType=S \
     --key-schema AttributeName=orderId,KeyType=HASH \
     --billing-mode PAY_PER_REQUEST
   
# SNS Topic
aws sns create-topic --name OrderTopic
SQS Queue with DLQ

# Create DLQ first
aws sqs create-queue --queue-name OrderQueue-DLQ

# Main queue with redrive policy
aws sqs create-queue --queue-name OrderQueue \
  --attributes '{
    "RedrivePolicy": "{
      \"deadLetterTargetArn\":\"arn:aws:sqs:REGION:ACCOUNT_ID:OrderQueue-DLQ\",
      \"maxReceiveCount\":\"3\"
    }"
  }'
  
# 🐍 Lambda Function
See complete code: lambda_function.py

  Key responsibilities:

   -Parse SQS messages

   -Validate required fields (orderId, userId, itemName)

   -Write to DynamoDB

   -Handle errors with retries

# 🧪 Testing
aws sns publish \
  --topic-arn arn:aws:sns:REGION:ACCOUNT_ID:OrderTopic \
  --message '{
    "orderId": "O1234",
    "userId": "U123",
    "itemName": "Laptop",
    "quantity": 1,
    "status": "new",
    "timestamp": "2025-05-03T12:00:00Z"
  }'
  
# Verification Checklist:

✅ SQS queue shows message count

✅ Lambda CloudWatch logs show processing

✅ DynamoDB contains new order

✅ DLQ remains empty (success case)
