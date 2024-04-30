import boto3
from datetime import datetime
import uuid

# Initialize a DynamoDB client
dynamodb = boto3.resource('dynamodb')

# Reference your DynamoDB table
table = dynamodb.Table('backend-logging')

def log_to_dynamodb(level, message):
    # Create a unique ID for each log entry
    log_id = str(uuid.uuid4())
    # Current timestamp
    timestamp = datetime.utcnow().isoformat()

    # Put the log entry into the DynamoDB table
    table.put_item(
        Item={
            'log_id': log_id,
            'timestamp': timestamp,
            'level': level,
            'message': message
        }
    )

def read_logs():
    # Scan the table to read all items
    response = table.scan()

    # Print out each item
    for item in response['Items']:
        print(item)


# Example usage
# log_to_dynamodb('INFO', 'This is a log message from my app')
read_logs()

