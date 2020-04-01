from __future__ import print_function
  
import json
import boto3
  
print('Loading function')

def lambda_handler(event, context):
  
    # Parse the JSON message 
    eventPayload = json.dumps(event)
  
    # Print the parsed JSON message to the console. You can view this text in the Monitoring tab in the AWS Lambda console or in the Amazon CloudWatch Logs console.
    print('Received event: ', eventText)
  
    data = eventPayload
    s3_client = boto3.resource(
    's3',
    region_name='ap-southeast-2',
   
    )
    object = s3_client.Object('iot-plant-data', 'sensordata/pi-data.json')
    response = object.put(Body=data)
  
    print(response)