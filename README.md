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


## 1 Pre-Requistites

An AWS Account and an API Gateway API route to call a function, you will also need an IAM role with appropriate privileges to execute Lambda functions and also save logs to Cloudwatch

https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway.html

## 2 Deployment

To deploy a Lambda function simply clone or copy the code to a zip file and upload to the AWS Lambda cloud console. Then link to it when you create a new route in API Gateway.

https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-getting-started-with-rest-apis.html

## 3 Testing

Lambda functions are tested using AWS Cloudwatch. Make sure you enable logging when you create an API. You will find each APi has its own "Log Group" and inside each Log Group are logs for a particular function called by a route.

However you can also do manual testing with either Postman or wscat.

3.1 Testing with Postman


3.2 Testing with wscat

