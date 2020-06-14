from __future__ import print_function
  
import json
import boto3
import datetime

from boto3.dynamodb.conditions import Key, Attr
  
print('Loading function')

def lambda_handler(event, context):
    body = json.loads(event["Records"][0]["body"])
    print(body['broker-device'])
    # Client
    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
    table = dynamodb.Table('RegisteredDevices')
    response = table.query(
        KeyConditionExpression=Key('ID').eq(body['broker-device']))
    
    # TO DO Implement if empty functionality
    # if response['Items'][0]['User' == ''"   
    humidity = 'humidity'
    water = 'water'
    temp = 'temp'
    ph = 'ph'
    ldr = 'ldr'
    
    pidevice = response['Items'][0]['ID']
    user = response['Items'][0]['username']
    time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    print(time)
    
    filenameHumidity = '%s-%s-%s-%s.json' % (pidevice, user, time, humidity)
    filenameWater = '%s-%s-%s-%s.json' % (pidevice, user, time, water)
    filenameTemp = '%s-%s-%s-%s.json' % (pidevice, user, time, temp)
    filenamepH = '%s-%s-%s-%s.json' % (pidevice, user, time, ph)
    filenameLDR = '%s-%s-%s-%s.json' % (pidevice, user, time, ldr)
    
    directoryHumidity = '%s-%s/%s/%s' %(pidevice, user, humidity, filenameHumidity)
    directoryWater = '%s-%s/%s/%s' %(pidevice, user, water, filenameWater)
    directoryTemp = '%s-%s/%s/%s' %(pidevice, user, temp, filenameTemp)
    directorypH = '%s-%s/%s/%s' %(pidevice, user, ph, filenamepH)
    directoryLDR = '%s-%s/%s/%s' %(pidevice, user, ldr, filenameLDR)
    
    directory = {}
    directory['humidity'] = directoryHumidity
    directory['water'] = directoryWater
    directory['temp'] = directoryTemp
    directory['ph'] = directorypH
    directory['ldr'] = directoryLDR
    #Parse the JSON message 
    eventText = json.dumps(event)
    
    # Print the parsed JSON message to the console. You can view this text in the Monitoring tab in the AWS Lambda console or in the Amazon CloudWatch Logs console.
    print('Received event: ', eventText)
    
    data = {}
    data['humidity'] = {'pi-id': body['broker-device'], 'type': humidity, 'time': body['payload']['time'], 'value': body['payload']['data']['humidity']}
    data['water'] = {'pi-id': body['broker-device'], 'type': water, 'time': body['payload']['time'], 'value': body['payload']['data']['water']}
    data['temp'] = {'pi-id': body['broker-device'], 'type': temp, 'time': body['payload']['time'], 'value': body['payload']['data']['temp']}
    data['ph'] = {'pi-id': body['broker-device'], 'type': ph, 'time': body['payload']['time'], 'value': body['payload']['data']['ph']}
    data['ldr'] = {'pi-id': body['broker-device'], 'type': ldr, 'time': body['payload']['time'], 'value': body['payload']['data']['ldr']}
    
    s3_client = boto3.resource(
    's3',
    region_name='ap-southeast-2',
    )

    for (directory, directory_value), (data, data_value) in zip(directory.items(), data.items()):
        object = s3_client.Object('iot-plant-data', directory_value)
        response = object.put(Body=json.dumps(data_value))
  
    print(response)