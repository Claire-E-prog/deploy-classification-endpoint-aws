import os

# Environment Variables
os.environ['OUTPUT_BUCKET'] = 'data-out-all'
os.environ['MODEL_BUCKET'] = 'saved-models-all'
os.environ['MODEL_KEY'] = 'iris/model.pkl'

# Invoke Lambda Function
from lambda_function import handler
import json

event = {
    "Records":[
        {
            "s3":{
                "bucket":{
                    "name": "data-in-all"
                },
                "object":{
                    "key": "iris/data.csv"
                }
            }
        }
    ]
}
# no context but if there was put it here
context = {}

# call handler
response = handler(event, context)
print(response)