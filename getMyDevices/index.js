'use strict'

const AWS = require('aws-sdk');

AWS.config.update({ region: 'ap-southeast-2' })

exports.handler = async (event, context, callback) => {  
    

    const documentClient = new AWS.DynamoDB.DocumentClient({ region: 'ap-southeast-2' });

    let response = { statusCode: 200,  headers: {
        "Access-Control-Allow-Origin" : "*", // Required for CORS support to work
        "Access-Control-Allow-Credentials" : true // Required for cookies, authorization headers with HTTPS 
    }, body: "okay" }
    

    const username  = event.requestContext.authorizer.claims['cognito:username'];

    const params = {
        TableName: "UserDevices",
        Key: {
            User: username,
        }
    }

    try {
        let fetch = await documentClient.get(params).promise();
        response.body = JSON.stringify(fetch.Item.devices.values);
        return response;
    } catch(err) {
        response.statusCode = 500;
        response.body = err.message;
        return response;
    }
}