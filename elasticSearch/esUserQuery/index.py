import sys, os, base64, datetime, hashlib, hmac, json
import requests # pip install requests
from aws_requests_auth.aws_auth import AWSRequestsAuth

def lambda_handler(event, context):

    username = event["requestContext"]["authorizer"]["claims"]["cognito:username"]
    
    body = json.loads(event["body"])
    
    deviceId = body["DeviceId"]
    
    accessKeyId = body["AccessKeyId"]
    
    secretKey = body["SecretKey"]
    
    sessionToken = body["SessionToken"]
    
    type = body["QueryType"]
    
    headers = { "Content-Type": "application/json" }
    
    auth = AWSRequestsAuth(aws_access_key=accessKeyId,
                    aws_secret_access_key=secretKey,
                    aws_host='search-plantly-es-cheap-my4i72dmshwihajjj2sbwqii3i.ap-southeast-2.es.amazonaws.com',
                    aws_token=sessionToken,
                    aws_region='ap-southeast-2',
                    aws_service='es')
    
    
    host = "https://search-plantly-es-cheap-my4i72dmshwihajjj2sbwqii3i.ap-southeast-2.es.amazonaws.com"
    url = host + "/" + deviceId + '-' + username + "/" + "_search"
    
    print("url", url)
    
    query = {
        "query": {
            "match": {
                "type": type
            }
        },
        "sort": [
            {
                "time.keyword": { "order": "desc" }
            }
        ]
    }
    
    print("query", query)
    
    response = requests.post(url,auth=auth, json=query, headers=headers)

    print("response", response.text)
    
    return {
        'statusCode': 200,
        'body': response.text
    }