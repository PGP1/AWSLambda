'use strict'

const AWS = require('aws-sdk');

AWS.config.update({ region: 'ap-southeast-2' })

exports.handler = async (event, context, callback) => {  
    
        
    const documentClient = new AWS.DynamoDB.DocumentClient({ region: 'ap-southeast-2' });

    let response = { statusCode: 200, body: "okay" }

    const username  = event.requestContext.authorizer.claims['cognito:username'];
    const email = event.requestContext.authorizer.claims.email;
    let device;
    
    try {
        device = JSON.parse(event.body).device
    } catch (err) {
        response.statusCode = 500;
        response.body = "Invalid device id";
        return response;
    }
    
    console.log(username, email, device)
    
    const params = {
        TableName: "UserDevices",
        Key: {
            User: username,
        },
        UpdateExpression: "ADD #devices :device",
        ExpressionAttributeNames: {
            '#devices': 'devices'
        },
        ExpressionAttributeValues: {
            ":device": documentClient.createSet([device])
        },
        ReturnValues: 'UPDATED_NEW'
    }

    try {
        if(device) {
            await documentClient.update(params).promise();
        } else {
            throw new Error("device cannot be null");
        }
    } catch(err) {
        response.statusCode = 500;
        response.body = err.message;
        return response;
    }

    response.statusCode = 200;
    response.body = "registerd ";

    return response;
}