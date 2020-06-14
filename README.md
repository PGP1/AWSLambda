# AWS Lambda
This repo is for version-controlling the API/Lambda functions that control the Plantly backend.

Plantly uses a micro-service architecture so the functions here belong to different micro-services and different APIs.

- IoT API - Bridge the MQTT communication between the raspberry pi and our AWS cloud
- Elasticsearch API - Fetch and write data to elasticsearch indexes (one index per user)
- getMyDevices API - Fetch and write device data to DynamoDB
- getUserData API - Fetch and write user Data to DynamoDB
- linkDevice - Standalone lambda function to link a device to a user ID
- getPrediction API - Websocket API for fetching model prediction data
- registerDevice - Standalone lambda function to register a device
- registerToDynamoDB - Link device to account on DynamoDB
- uploadAvatar - Update a user avatar on the front-end

## 1. Pre-Requistites

An AWS Account and an API Gateway API route to call a function, you will also need an IAM role with appropriate privileges to execute Lambda functions and also save logs to Cloudwatch

https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway.html

## 2. Deployment

### 2.1 Deploy Lambda

To deploy a Lambda function simply clone or copy the code to a zip file and upload to the AWS Lambda cloud console. 

### 2.2 Link function to an API in AWS API Gateway

You must then link to it when you create a new route in API Gateway.

https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-getting-started-with-rest-apis.html


## 3. Testing

Lambda functions are tested using AWS Cloudwatch. Make sure you enable logging when you create an API. You will find each APi has its own "Log Group" and inside each Log Group are logs for a particular function called by a route.

However you can also do manual testing with either Postman or wscat.

### 3.1 Testing with Postman

In postman enter the endpoint URL of a request in the address bar and choose the appropriate HTTP method from the drop-down.

In the authorization tab choose AWS Signature for the authorization Type. Enter your AWS IAM user's access key ID in the AccessKey input field. Enter your IAM user secret key in SecretKey. 

Alterntively you can use a Lambda token.

https://docs.aws.amazon.com/apigateway/latest/developerguide/call-api-with-api-gateway-lambda-authorization.html

Specify an appropriate AWS region that matches the region specified in the invocation URL. Enter execute-api in Service Name.

Choose the Headers tab. Optionally, delete any existing headers. This can clear any stale settings that may cause errors. Add any required custom headers. For example, if API keys are enabled, you can set the x-api-key:{api_key} name/value pair here.

Choose Send to submit the request and receive a response. You can check this response in Cloudwatch.


### 3.2 Testing with wscat

Download wscat from https://www.npmjs.com/package/wscat 

or install wscat by running the following command:

```npm install -g wscat```

To connect to your API, run the wscat command as shown in the following example.

```wscat -c wss://rumb30qq13.execute-api.ap-southeast-2.amazonaws.com/default```

Then you can send a json request like so:

```{"device":"c0cb03a49a754a17b07b85c4d4f19039", "username": "test"}```

And you should get something back such as:

```{"pi-id": "c0cb03a49a754a17b07b85c4d4f19039", "prediction": "low temp & low light", "type": "prediction", "time": "2020-06-14T09:36:16.209814"}```

### 3.3 Checking log output with Cloudwatch

If you can configured your Cloudwatch correctly you will find a Log Group named something like ```/aws/apigateway/rumb30qq13/default```

You can use this to check the invocation logs for output of your tests and general usage.

```	
2020-06-14T16:51:32.505+10:00
(OGxWOFh2ywMFQsA=) WebSocket API [rumb30qq13] received message from client [OGxWNcuwywMCFpA=]. Message: [
{
    "requestContext": {
        "routeKey": "$default",
        "messageId": "OGxWOcuxSwMCFpA=",
        "eventType": "MESSAGE",
        "extendedRequestId": "OGxWOFh2ywMFQsA=",
        "requestTime": "14/Jun/2020:06:51:32 +0000",
        "messageDirection": "IN",
        "stage": "default",
        "connectedAt": 1592117492425,
        "requestTimeEpoch": 1592117492502,
        "identity": {
            "cognitoIdentityPoolId": null,
            "cognitoIdentityId": null,
            "principalOrgId": null,
            "cognitoAuthenticationType": null,
            "userArn": null,
            "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
            "accountId": null,
            "caller": null,
            "sourceIp": "220.253.123.231",
            "accessKey": null,
            "cognitoAuthenticationProvider": null,
            "user": null
        },
        "requestId": "OGxWOFh2ywMFQsA=",
        "domainName": "rumb30qq13.execute-api.ap-southeast-2.amazonaws.com",
        "connectionId": "OGxWNcuwywMCFpA=",
        "apiId": "rumb30qq13"
    },
    "body": "{ \"device\": \"test132452\", \"username\": \"test7\"}",
    "isBase64Encoded": false
}
```
