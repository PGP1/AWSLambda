import json
import boto3
import logging
import re
import pickle


"""
this function grabs the latest prediction from the model via the s3 bucket
"""

s3 = boto3.client('s3')

def iterate_bucket_items(bucket, prefix, ignore):
    """
    iterates over all objects in s3 bucket

    :param bucket: name of s3 bucket
    :return: dict of metadata for an object
    """
    pattern = re.compile("{}\/((?!{}).*)\/.*\.json".format(prefix, ignore))


    paginator = s3.get_paginator('list_objects_v2')
    operation_parameters = {'Bucket': bucket,
                            'Prefix': prefix}
                            
    types = ['prediction']
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


def lambda_handler(event, context):
    
    s3 = boto3.client('s3')
    
    # parse event body data for device id 
    # TODO: context.cognito_identity_id –> The authenticated Amazon Cognito identity.

    qs = event["body"]
    device_id = json.loads(qs)
    device_id = device_id["device_id"]
    
    print("device_id:", device_id)
    
    object = s3.get_object(Bucket='iot-plant-data',Key='c0cb03a49a754a17b07b85c4d4f19039-test/prediction/prediction.json')
    prediction = object['Body'].read()
    
    # jsonify
    prediction = json.loads(prediction)

    return {
        'statusCode': 200,
        'body': json.dumps(prediction)
    }
    
    


