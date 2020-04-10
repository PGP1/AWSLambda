'use strict'

const AWS = require('aws-sdk');

AWS.config.update({ region: 'ap-southeast-2' })

exports.handler = async (event, context, callback) => {  

    const documentClient = new AWS.DynamoDB.DocumentClient({ region: 'ap-southeast-2' });

    let response = { statusCode: 200, headers: {
        "Access-Control-Allow-Origin" : "*", // Required for CORS support to work
        "Access-Control-Allow-Credentials" : true // Required for cookies, authorization headers with HTTPS 
    }, body: "okay" }

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
        let registeredParams = {
            TableName: "RegisteredDevices", 
            Key: {
                ID: device
            },
            ExpressionAttributeValues: {
                ":username": username
            }
        }
        let fetch = await documentClient.get(registeredParams).promise();
        
        let notLinked = Object.keys(fetch).length > 0 && !(fetch.Item.username);
        
        if(notLinked) {
            await documentClient.update(params).promise();
            registeredParams.UpdateExpression = `SET username = if_not_exists(username, :username)`;
            await documentClient.update(registeredParams).promise();
        } else {
            throw new Error("Device isn't available");
        }
    } catch(err) {
        response.statusCode = 500;
        response.body = err.message;
        return response;
    }

    response.statusCode = 200;
    response.body = "registered ";

    return response;
}