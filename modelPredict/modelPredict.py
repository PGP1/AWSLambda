import tensorflow as tf

model_url = "updated_model"

imported = tf.saved_model.loader.load(export_dir=model_url, tags=None)


def model_predict(dictOfVals):

    def predict_fn(x):
        example = tf.train.Example()
        example.features.feature['water_level'].float_list.value.extend([x['water_level']])
        example.features.feature['temperature_level'].float_list.value.extend([x['temperature_level']])
        example.features.feature['ldr'].float_list.value.extend([x['ldr']])
        example.features.feature['pH'].float_list.value.extend([x['pH']])
        example.features.feature['humidity'].float_list.value.extend([x['humidity']])
        return imported.signatures["predict"](examples=tf.constant([example.SerializeToString()]))


    class_names = ['normal','low light','high light', 'low temp','low temp & low light',
                  'low temp & high light','high temp','high temp & low light',
                   'high temp & high light','low water','low water & low light',
                   'low water & high light', 'low water & low temp',
                   'low water & low temp & low light', ' low water & low temp & high light',
                   'low water & high temp','low water & high temp & low light',
                   'low water & high temp & high light','low ph','high ph','low light & low ph'
                   'low light & high ph','low temp & low ph','high light & low ph','high light & high ph',
                   'low temp & low ph','low temp & high ph', 
                   'low temp & low light & low ph', 'low temp & low light & high ph',
                   'low temp & high light & low ph', 'low temp & high light & high ph',
                   'high temp & low ph', 'high temp & high ph', 'high temp & low light & low ph',
                   'high temp & low light & high ph','high temp & high light & low ph',
                   'high temp & high light & high ph', 'low water & low ph', 'low water & high ph',
                   'low water & low light & low ph', 'low water & low light & high ph', 
                   'low water & high light & low ph', 'low water & high light & high ph',
                   'low water & low temp & low ph', 'low water & low temp & high ph',
                   'all levels are low','low water & low temp & low light & high ph',
                   'low water & low temp & high light & low ph',
                   'low water & low temp & high light & high ph',
                   'low water & high temp & low ph','low water & high temp & high ph',
                   'low water & high temp & low light & low ph' ,
                   'low water & high temp & low light & hight ph' ,
                   'low water & high temp & high light & low ph' ,
                   'low water & high temp & high light & high ph' ]

  
    id_name=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25
                ,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48
                ,49,50,51,52,53]


    def input_fn(features, batch_size=256):
        return tf.data.Dataset.from_tensor_slices(dict(features)).batch(batch_size)

    predictions = predict_fn(dictOfVals)

    class_id = predictions['class_ids'][0]
    probs = predictions['probabilities']
    init = tf.global_variables_initializer()

    with tf.Session() as sess:
        
        sess.run(init)
        print(sess.run(class_id).item())
        c_id = sess.run(class_id).item()
        
        print(sess.run(probs)[0][c_id])
        
        probability = sess.run(probs)[0][c_id]
        
        print(predictions['class_ids'])
        model_response = 'Prediction is "{}" ({:.1f}%)'.format(class_names[c_id], 100 * probability)

        print(model_response)

        return model_response
