import json
import boto3

dynamodb = boto3.resource('dynamodb')

device_table = dynamodb.Table('RegisteredDevices')
user_table = dynamodb.Table('UserDevices')
def lambda_handler(event, context):
    username = event["requestContext"]["authorizer"]["claims"]["cognito:username"]

    event = json.loads(event["body"])
    
    device = device_table.get_item(
        Key={
            'ID': event["ID"]
        }
    )

    user = user_table.get_item(
        Key={
            'User': username
        }
    )
    
    check = False
    try:
        if(device['Item']['username'].strip() == username and event["ID"] in user["Item"]["devices"]):
            check = True
        if(check == False):
            raise Exception
    except Exception as e:
        return {
            'statusCode': 403,
            'body': json.dumps("You don't own the device")
        }
        
    if(check == True):
        device_table.update_item(
            Key={
                'ID': event["ID"]
            },
            UpdateExpression='SET username = :val',
            ExpressionAttributeValues={
                ':val': ' '
            }
        )
        user_table.update_item(
            Key={
                'User': username,
            },
            UpdateExpression="DELETE devices :id",
            ExpressionAttributeValues={
                ':id': set([event["ID"]])
            }
        )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Unlinked successfully')
    }
