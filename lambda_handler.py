import json
import boto3
import os

s3 = boto3.client('s3')
S3_BUCKET = os.getenv('S3_BUCKET', 'your-bucket')

def handler(event, context):
    # simple proxy that stores JSON body to S3
    body = event.get('body') or json.dumps(event)
    key = f"events/{context.aws_request_id}.json" if context else "events/local_event.json"
    s3.put_object(Bucket=S3_BUCKET, Key=key, Body=body)
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'saved', 's3_key': key})
    }
