'use strict'

const AWS = require('aws-sdk');

AWS.config.update({ region: 'us-east-2' })

exports.handler = async (event, context, callback) => {  

    const documentClient = new AWS.DynamoDB.DocumentClient({ region: 'ap-southeast-2' });
    

    let response = { statusCode: null, body: "" }

    event = JSON.parse(event.body)

    const id = event.id;
   
    const params = {
        TableName: "RegisteredDevices",
        Item: {
            ID: id,
        },
        Expected: {
            'ID':{
            Exists: false
            }
        }
    }

    try {
        if(id) {
            await documentClient.put(params).promise();
        } else {
            throw new Error("id key cannot be null");
        }
    } catch(err) {
        response.statusCode = 500;
        response.body = err.message;
        return response;
    }

    response.statusCode = 200;
    response.body = "registerd " + id;

    return response;
}