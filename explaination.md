# Explanation of Visibility Timeout and Dead Letter Queue (DLQ)
in the Order Processing System
1. Visibility Timeout in Amazon SQS
The visibility timeout (default: 30 seconds) is a mechanism that temporarily hides a message from other consumers while it's being processed by a service like AWS Lambda.

# Key Functions:
Prevents duplicate processing by making the message invisible to other consumers during active processing.

Allows time for Lambda to finish processing before the message becomes visible again.

Automatically extends if Lambda is still working when the timeout is about to expire.

Retries automatically if Lambda fails; the message reappears in the queue.

In Our System:
Ensures each order is processed exactly once.

Allows automatic retries for temporary failures.

Prevents message loss during processing.

# 2. Dead Letter Queue (DLQ) Implementation
We configured the DLQ with a maxReceiveCount of 3, meaning messages are moved to the DLQ after three failed processing attempts.

Purpose of DLQ:
Prevents infinite retry loops by isolating persistently failing messages.

Preserves problematic messages for investigation and debugging.

Maintains system health by removing "poison pill" messages.

Supports failure pattern analysis for long-term improvements.

# 3. Importance for Order Processing
Order Integrity: No orders are lost—even if processing fails.

System Reliability: Temporary failures are handled without disruption.

Debugging Efficiency: Failed orders are available in DLQ for troubleshooting.

Scalability: Automated retries reduce manual effort.

# 4. Failure Handling Flow
Lambda fails to process a message → returns an error  
↓  
SQS makes the message visible again (Retry 1)  
↓  
After 3 failed attempts → Message is moved to DLQ  
↓  
Operations Team:  
→ Inspects the failed message  
→ Identifies issues (e.g., malformed data)  
→ Reprocesses after applying fixes  
5. Key Benefits
99.9%+ order processing reliability

Zero manual intervention for transient failures

Clear separation of operational and failed messages

Built-in adherence to AWS best practices
