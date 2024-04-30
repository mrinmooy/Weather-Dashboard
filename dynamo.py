import boto3
from datetime import datetime
import uuid

session = boto3.Session(
    aws_access_key_id='AKIA6GBMF4I4QCV5LOZX',
    aws_secret_access_key='qEOiz3R3E5Ku4vnxXrV3R/Q7Cj8bOmthXhtCPmPl',
    region_name='us-east-1'  # e.g., 'us-west-2'
)




# Initialize a DynamoDB client
dynamodb = session.resource('dynamodb')

# Reference your DynamoDB table
table = dynamodb.Table('backend-logging')

def delete_log(log_id):
    # Delete the log entry from the DynamoDB table based on its log_id
    response = table.delete_item(
        Key={
            'log_id': log_id
        }
    )
    # Optionally print the response status to confirm deletion
    print(f"Deleted log with ID: {log_id}")
    print(response)

def add_log(city):
    # Create a unique ID for each log entry
    log_id = str(uuid.uuid4())
    # Current timestamp
    timestamp = datetime.utcnow().isoformat()

    # Put the log entry into the DynamoDB table
    table.put_item(
        Item={
            'log_id': log_id,
            'city': city,
            'timestamp': timestamp
        }
    )
    print(f"Log added for {city} at {timestamp}")

def read_logs():
    # Scan the table to read all items
    response = table.scan()

    # Print out each item
    for item in response['Items']:
        print(item)

# Example usage
# add_log('New York')
# delete_log('a2047e42-d6ae-47a1-ad99-4462cd6ebc97')
read_logs()
#lets see if this works