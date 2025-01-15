import boto3
import pandas as pd
import numpy as np
import os
import logging
import joblib
from urllib.parse import urlparse

# Load the model from the local file system
def load_model(model_path):
    model = joblib.load(model_path)
    return model

# Make predictions using the loaded model
def make_prediction(model, input_data):
    input_data = np.array(input_data)
    predictions = model.predict(input_data)
    return predictions

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize the S3 client
s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Define relevant s3 buckets
    predictions_bucket = 'iris-predictions'  
    model_bucket = 'lambda-bucket-iris'  
    model_key = 'model.pkl'  # key = path to the model file in the model bucket
    
    # Download the model file from S3 to the /tmp directory
    model_path = '/tmp/model.pkl'
    s3.download_file(model_bucket, model_key, model_path)
    
    for record in event['Records']:
        # Get the bucket and key for the uploaded CSV file
        source_bucket = record['s3']['bucket']['name']
        source_key = record['s3']['object']['key']
        logger.info(f'Processing file from bucket: {source_bucket}, key: {source_key}')
    
        # Ensure the file is in the 'data/' folder
        if not source_key.startswith('data/'):
            logger.warning(f'File {source_key} is not in the data/ folder. Skipping.')
            continue
    
        # Download the CSV file from the source S3 bucket
        download_path = f'/tmp/{os.path.basename(source_key)}'
        s3.download_file(source_bucket, source_key, download_path)
    
        # Load the data from the CSV file
        data = pd.read_csv(download_path)
        input_data = data.values
        
        # Load the model from the local file system
        model = load_model(model_path)
        
        # Make predictions
        predictions = make_prediction(model, input_data)
        
        # Save predictions to a new CSV file
        predictions_df = pd.DataFrame(predictions, columns=['Prediction'])
        predictions_key = f'predictions/{os.path.basename(source_key)}'
        predictions_path = f'/tmp/{os.path.basename(predictions_key)}'
        predictions_df.to_csv(predictions_path, index=False)
        
        # Upload the predictions file to the predictions S3 bucket
        s3.upload_file(predictions_path, predictions_bucket, predictions_key)
        logger.info(f'Predictions saved to bucket: {predictions_bucket}, key: {predictions_key}')
