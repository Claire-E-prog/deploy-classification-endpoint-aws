import boto3
import pandas as pd
import joblib
# Native python
import os
import io
import logging


# Load the model from the local file system
def load_model(bucket_name, model_key):
    try:
        logger.info(f"Starting model download from s3://{bucket_name}/{model_key}")
        model_path = '/tmp/model.pkl'
        s3.download_file(bucket_name, model_key, model_path)
        logger.info("Model downloaded successfully to /tmp/model.pkl")
        return joblib.load(model_path)
    except Exception as e:
        logger.error(f"Error downloading or loading model: {str(e)}")
        raise
# Make predictions using the loaded model
def make_prediction(model, input_data):
    predictions = model.predict(input_data)
    return predictions
"""
Why Use logger Instead of print?
Log Levels:
With logger, you can log messages with different severity levels (DEBUG, INFO, WARNING, ERROR, CRITICAL).
Example: logger.info("This is an info message.") vs. logger.error("This is an error message.").

"""
# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.StreamHandler()
# Initialize the S3 client
s3 = boto3.client('s3')

def handler(event, context):
    try:
        # Log incoming event
        logger.info(f"Received event: {event}")
        logger.info(f"Lambda context: {context}")

        # parse the S3 event
        if 'Records' not in event or not event['Records']:
            raise ValueError("Invalid event structure. 'Records' key is missing or empty.")
        
        record = event['Records'][0]
        input_bucket = record['s3']['bucket']['name']
        input_key = record['s3']['object']['key']
        logger.info(f"Input bucket: {input_bucket}, Input key: {input_key}")

        # get environment variables
        output_bucket = os.environ.get('OUTPUT_BUCKET')
        model_bucket = os.environ.get('MODEL_BUCKET')
        model_key = os.environ.get('MODEL_KEY')

        if not output_bucket or not model_bucket or not model_key:
            raise ValueError("Environment variables OUTPUT_BUCKET, MODEL_BUCKET, and MODEL_KEY must be set.")

        output_key = f"iris/{os.path.basename(input_key)}"
        logger.info(f"Output bucket: {output_bucket}, Output key: {output_key}")
        logger.info(f"Model bucket: {model_bucket}, Model key: {model_key}")

        # Load the model
        logger.info("Downloading model...")
        model = load_model(model_bucket, model_key)
        logger.info("Model downloaded successfully.")

        # Download input CSV file
        logger.info("Downloading input CSV...")
        response = s3.get_object(Bucket=input_bucket, Key=input_key)
        input_csv = response['Body'].read().decode('utf-8')
        df = pd.read_csv(io.StringIO(input_csv))
        logger.info("Input CSV loaded successfully.")

        # Run predictions
        logger.info("Running predictions...")
        predictions = make_prediction(model, df)

        # Convert predictions to CSV
        predictions_df = pd.DataFrame(predictions, columns=['Predictions'])
        output_csv = io.StringIO()
        predictions_df.to_csv(output_csv, index=False)
        logger.info(f'created predictions csv: {output_csv.getvalue()}')
        output_csv.seek(0)  # Reset pointer
        logger.info("Predictions converted to CSV.")

        # Upload the processed file to S3
        logger.info(f"Uploading processed file to s3://{output_bucket}/{output_key}...")
        s3.put_object(
            Bucket=output_bucket,
            Key=output_key,
            Body=output_csv.getvalue()
        )
        logger.info("File uploaded successfully.")
        
        return {
            'statusCode': 200,
            'body': "Woohoo!"
        }
    
    except Exception as e:
        logger.error(f"Error processing file from bucket: {input_bucket}, key: {input_key}. Exception: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"Error processing file: {str(e)}"
        }
