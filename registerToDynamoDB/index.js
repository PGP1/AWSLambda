var aws = require('aws-sdk');
var ddb = new aws.DynamoDB({apiVersion: '2012-10-08'});

exports.handler = async (event, context) => {
    console.log(event);

    let date = new Date();

    const tableName = "UserDevices";
    const region = "ap-southeast-2";
    const defaultAvi = 'https://upload.wikimedia.org/wikipedia/commons/7/7c/Profile_avatar_placeholder_large.png';
    
    console.log("table=" + tableName + " -- region=" + region);

    aws.config.update({region: region});
    const documentClient = new aws.DynamoDB.DocumentClient({ region: region });

    // If the required parameters are present, proceed
    if (event.request.userAttributes.sub) {

        // -- Write data to DDB
        let ddbParams = {
            Item: {
                'id': event.request.userAttributes.sub,
                '__typename': 'User',
                'picture': defaultAvi,
                'User': event.userName,
                'email': event.request.userAttributes.email,
                'createdAt': date.toISOString()
            },
            TableName: tableName
        };

        // Call DynamoDB
        try {
            await documentClient.put(ddbParams).promise()
            console.log("Success");
        } catch (err) {
            console.log("Error", err);
        }

        console.log("Success: Everything executed correctly");
        context.done(null, event);

    } else {
        // Nothing to do, the user's email ID is unknown
        console.log("Error: Nothing was written to DDB or SQS");
        context.done(null, event);
    }
};