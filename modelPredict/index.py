import json
import math
import modelPredict
from decimal import * 
import urllib.parse
import boto3
import re

s3 = boto3.client('s3')

def iterate_bucket_items(bucket, prefix, ignore):
    """
    Generator that iterates over all objects in a given s3 bucket

    See http://boto3.readthedocs.io/en/latest/reference/services/s3.html#S3.Client.list_objects_v2 
    for return data format
    :param bucket: name of s3 bucket
    :return: dict of metadata for an object
    """
    pattern = re.compile("{}\/((?!{}).*)\/.*\.json".format(prefix, ignore))


    paginator = s3.get_paginator('list_objects_v2')
    operation_parameters = {'Bucket': bucket,
                            'Prefix': prefix}
                            
    types = ['ldr', 'water', 'ph', 'temp', 'humidity']
    types.remove(ignore)
    
    page_iterator = paginator.paginate(**operation_parameters)

    get_last_modified = lambda obj: int(obj['LastModified'].strftime('%s'))

    for page in page_iterator:
        if page['KeyCount'] > 0:
            print("latest", sorted(page['Contents'], key=get_last_modified))
            for item in sorted(page['Contents'], key=get_last_modified):
                key = item['Key']
                if(pattern.match(key)):
                    type = key.split("/")[1]
                    if(type in types):
                        types.remove(type)
                        yield item

def formatWater(waterVal):
    
    fval = float(float(waterVal)/100)*2

    fDec = str(float(fval)).split('.')[1]
    waterScaled = 0
        
    if float(fDec) >= 5:
        waterScaled = math.ceil(fval)
    if float(fDec) < 5 and float(fDec) > 0:
        waterScaled = math.floor(fval)
    elif float(fDec) == 0:
        waterScaled = fval
    
    return waterScaled


def lambda_handler(event, context):
    #1 - Get the bucket name
    print(event)
    message = json.loads(event["Records"][0]["Sns"]["Message"])

    bucket = message['Records'][0]['s3']['bucket']['name']

    #2 - Get the file/key name
    key = urllib.parse.unquote_plus(message['Records'][0]['s3']['object']['key'], encoding='utf-8')
    print(bucket)
    data = key.split("/")
    folder = data[0]
    currentMeasure = data[1]
    print("currentMeasure : " , currentMeasure)
    try:
        #3 - Fetch the file from S3
        response = s3.get_object(Bucket=bucket, Key=key)
        print("response", response)
        #4 - Deserialize the file's content
        text = response["Body"].read().decode()
        data = json.loads(text)
        
    
        features = ['water_level', 'temperature_level', 'ldr', 'pH','humidity']
        feat_data = {}
        feat_data[currentMeasure] = data['value']
    
        # response = s3.get_object(Bucket=bucket, Key='ghzy567-test7/LDR')

        # #4 - Deserialize the file's content
        # text = response["Body"].read().decode()
        # data = json.loads(text)

        
        for i in iterate_bucket_items(bucket, folder, ignore=currentMeasure):
            print("i", i)
            page_key = i["Key"].split("/")[1]
            temp = s3.get_object(Bucket=bucket, Key=i["Key"])
            bod = temp["Body"].read().decode()
            da = json.loads(bod)
            feat_data[page_key] = da["value"]


        #5 - Print the content
        print("feat_data", feat_data)
       
        feat_data['water_level'] = formatWater(feat_data['water'])
        feat_data['temperature_level'] = feat_data['temp']
        feat_data['pH'] = feat_data['ph']
        
        del feat_data['ph']
        del feat_data['temp']
        del feat_data['water']
        
        print("formatted feat_data", feat_data)
        #6 - Parse and print the transactions
        
        prediction = modelPredict.predict(feat_data)

    except Exception as e:
        print(e)
        raise e
        




