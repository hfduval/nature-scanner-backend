import json
import uuid
import logging
import boto3
import os

def lambda_handler(event, context):
    try:
        s3_client = boto3.client('s3')

        id = str(uuid.uuid4())
        key = f"{id}.jpg"

        presigned_url = s3_client.generate_presigned_url('put_object',
                                                         Params={'Bucket': os.getenv('IMAGE_BUCKET'),
                                                                 'Key': key},
                                                         ExpiresIn=3600)

        response = {
            'statusCode': 200,
            'body': json.dumps({
                'url': presigned_url,
                'key': key,
            })
        }
    
    except Exception as e:
        logging.error(f"Error generating presigned URL: {e}")
        response = {
            'statusCode': 500,
            'body': 'Error generating presigned URL'
        }

    return response
