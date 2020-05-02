console.log('Loading function');

var AWS = require('aws-sdk');
var iotdata = new AWS.IotData({endpoint: 'a5dhqdjw6qpyv-ats.iot.ap-southeast-2.amazonaws.com'});

exports.handler = async (event, context, callback) => {
   
    var params = {
    topic: 'awsiot_to_localgateway',
    payload: JSON.stringify({message: "Turn On - Light"}),
    qos: 0
    };
    
    iotdata.publish(params, function(err, data) {
    if(err){
    console.log(err);
    }
    else{
    console.log("Success, I guess.");
    context.succeed();
    }
    });
    callback();
};
