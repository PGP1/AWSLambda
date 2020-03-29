'use strict'

const AWS = require('aws-sdk');

AWS.config.update({ region: 'us-east-2' })

exports.handler = async (event, context, callback) => {  

    const documentClient = new AWS.DynamoDB.DocumentClient({ region: 'us-east-2' });

    const { username, password } = event; 

    let response = { statusCode: null, body: "" }

    let createJSON = (data) => {
        return JSON.stringify(data)
    }

    const params = {
        TableName: "piot-account",
        Item: {
            username: username,
            password: password,
            device: []
        }
    }

    try {
        const data = await documentClient.put(params).promise();
    } catch(err) {
        response.statusCode = 500;
        response.body = createJSON(err);
        return response;
    }

    response.statusCode = 200;
    response.body = "created";

    return response;
}