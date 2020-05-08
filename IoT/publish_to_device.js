console.log('Loading function');

var AWS = require('aws-sdk');
var iotdata = new AWS.IotData({endpoint: 'a5dhqdjw6qpyv-ats.iot.ap-southeast-2.amazonaws.com'});


exports.handler = async (event, context, callback) => {
    
    let response = { 
        "isBase64Encoded": false,
        "statusCode": 200,  
        "headers": {
            "Access-Control-Allow-Origin" : "*", // Required for CORS support to work
            "Access-Control-Allow-Credentials" : true // Required for cookies, authorization headers with HTTPS 
        }, 
        "body": JSON.stringify({ status: "good from publish_to_device" })
    };
    const username  = event.requestContext.authorizer.claims['cognito:username'];

    let body = JSON.parse(event["body"])
    //let body =event["body"]
    var params = {
        topic: 'awsiot_to_localgateway/b1',
        payload: JSON.stringify(
            {
                "controller": {
                    "username": username,
                    "light": body.light,
                    "fan": body.fan,
                    "pump": body.pump,
                    "type": body.type
                }
            }),
        qos:1
    };

    console.log("event:", params)

    iotdata.publish(params, function(err, data) {
        if(err){
            console.log("error");
        }
        else{
            console.log("Success, I guess.");
        }
    });
    callback();
    return response;
};