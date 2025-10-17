import boto3
import json
from urllib.parse import unquote_plus

def lambda_handler(event, context):
    textract = boto3.client('textract')
    
    # Get AWS account ID and region dynamically
    account_id = context.invoked_function_arn.split(':')[4]
    region = context.invoked_function_arn.split(':')[3]
    
    # Get S3 event details
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = unquote_plus(event['Records'][0]['s3']['object']['key'])
    
    # Debug logging
    print(f"Processing file: s3://{bucket}/{key}")
    print(f"Account ID: {account_id}, Region: {region}")
    
    # Start Textract job
    response = textract.start_document_text_detection(
        DocumentLocation={
            'S3Object': {
                'Bucket': bucket,
                'Name': key
            }
        },
        NotificationChannel={
            'SNSTopicArn': f'arn:aws:sns:{region}:{account_id}:textract-completion-topic',
            'RoleArn': f'arn:aws:iam::{account_id}:role/TextractServiceRole'
        }
    )
    
    return {'statusCode': 200, 'body': f"Started job: {response['JobId']}"}
