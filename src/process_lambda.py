import json
import logging
import boto3
import os
import requests


def lambda_handler(event, context):
    try:
        s3_client = boto3.client('s3')

        api_key = "..."
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        # fixme: 2400 is an existing image on the bucket for testing purposes, real img_id should be passed from
        #  function param
        img_id = "2400"
        key = f"{img_id}.jpg"

        presigned_url = s3_client.generate_presigned_url('get_object',
                                                         Params={'Bucket': os.getenv('IMAGE_BUCKET'),
                                                                 'Key': key},
                                                         ExpiresIn=3600)

        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "What animal species is in this image? If there are no animals in the image or if you are not sure, you can say 'Cannot identify Species'."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"{presigned_url}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        resp = {
            'statusCode': 200,
            'body': json.dumps(response.json())
        }

    except Exception as e:
        logging.error(f"Error generating presigned URL: {e}")
        resp = {
            'statusCode': 500,
            'body': 'Error generating presigned URL'
        }

    return resp
