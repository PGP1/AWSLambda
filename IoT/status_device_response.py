import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

print('Loading function')


def lambda_handler(event, context):
    
    # Client
    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
    table = dynamodb.Table('RegisteredDevices')
    response = table.query(
        KeyConditionExpression=Key('ID').eq(event['broker-id']))
        
    pidevice = response['Items'][0]['ID']
    user = response['Items'][0]['User']
    filename = "{}-{}-resources.json".format(pidevice, user)
    directory_value = "{}-{}/resources/{}".format(pidevice, user, filename)
    
    # Push to S3
    s3_client = boto3.resource(
    's3',
    region_name='ap-southeast-2',
    )
    
    data = {}
    data['broker-id'] = event['broker-id']
    data['status'] = event['status']
    data['uptime'] = event['uptime']
    data['cpu-percent'] = event['cpu-percent']
    data['ram'] = event['ram']
    
    print("donddnod", directory_value)
    print(data)
    object = s3_client.Object('iot-plant-data', directory_value)
    response = object.put(Body=json.dumps(data))
    
    #print(response)