// see also: https://www.npmjs.com/package/parse-multipart
var multipart = require("parse-multipart");
const AWS = require('aws-sdk');

const BUCKET_NAME = 'plantly-avatar';
const IAM_USER_KEY = '81rkz7+9L9og4xxxxxMdg/w00TxzS0vE';
const IAM_USER_SECRET = '81rkz7+9L9og4xxxxxMdg/w00TxzS0vE';

// "exports.handler" must match the entrypoint defined in the lambda Config.
exports.handler = function(event,context,callback){

    const documentClient = new AWS.DynamoDB.DocumentClient({ region: 'ap-southeast-2' });

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
    var bodyBuffer = Buffer.from(event['body'].toString(),'base64');
    var boundary = multipart.getBoundary(event.headers['content-type']);

    var file = multipart.Parse(bodyBuffer,boundary)[0];
    
    console.log("f", file)
   
    let s3bucket = new AWS.S3({
       accessKeyId: IAM_USER_KEY,
       secretAccessKey: IAM_USER_SECRET,
       Bucket: BUCKET_NAME,
    });
     
    var re = /(?:\.([^.]+))?$/;

    var ext = re.exec(file.filename)[1];
    let random = Math.floor(Math.random() * 1000);

    let params = {
        Bucket: BUCKET_NAME,
        Key: `${username}/profile${random}.${ext}`,
        Body: file.data,
    };
 
    s3bucket.upload(params, function (err, data) {
        if (err) {
            console.log('error in callback');
            response.statusCode = 403;
            response.body = JSON.stringify(err);
        }
        
        let param = {
                TableName: "UserDevices",
                Key: {
                    User: username,
                },
                UpdateExpression: "SET #avatar = :url",
                ExpressionAttributeNames: {
                    '#avatar': 'picture'
                },
                ExpressionAttributeValues: {
                    ":url": `https://plantly-avatar.s3-ap-southeast-2.amazonaws.com/${username}/profile${random}.${ext}`
                },
                ReturnValues: 'UPDATED_NEW'
            }
        
        documentClient.update(param).promise();
            
        callback(null, response);
    });
    
    
    return response;

}
