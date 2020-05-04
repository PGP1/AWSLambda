console.log('Loading function');

var AWS = require('aws-sdk');
var iotdata = new AWS.IotData({endpoint: 'a5dhqdjw6qpyv-ats.iot.ap-southeast-2.amazonaws.com'});

exports.handler = async (event, context, callback) => {
     
    console.log(event["body"]);
    
    let response = { 
        "isBase64Encoded": false,
        "statusCode": 200,  
        "headers": {
            "Access-Control-Allow-Origin" : "*", // Required for CORS support to work
            "Access-Control-Allow-Credentials" : true // Required for cookies, authorization headers with HTTPS 
        }, 
        "body": JSON.stringify({ status: "good" })
    }
    
    const username  = event.requestContext.authorizer.claims['cognito:username'];

    let body = JSON.parse(event.body);

    var params = {
        topic: 'status_request/b1',
        payload: JSON.stringify({
            "ID": body.id,
            "username": username
        }),
        qos: 0
    };
    
    iotdata.publish(params, function(err, data) {
        if(err){
            console.log(err);
        }
        else{
            console.log("Success, I guess.");
        }
    });
    
    return response;
};
