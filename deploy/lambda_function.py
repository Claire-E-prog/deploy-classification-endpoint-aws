import boto3
import pandas as pd
import joblib
# Native python
import os
import io
import logging



# Load the model from the local file system
def load_model(bucket_name,model_key):
    model_path = '/tmp/model.pkl'
    s3.download_file(bucket_name, model_key, model_path)
    return joblib.load(model_path)

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

# Initialize the S3 client
s3 = boto3.client('s3')

def handler(event, context):
    try:
        # log incoming event 
        logger.info(f'Recieved event: {event}')

        # Parse the S3 event
        record = event['Records'][0]
        input_bucket = record['s3']['bucket']['name']
        input_key = record['s3']['object']['key']

        # Define the output bucket and output key (hard code or cinfigure in environment variables)
        output_bucket = os.environ.get('OUTPUT_BUCKET', 'default-output-bucket')
        output_key = f'processed/ {os.path.basename(input_key)}'

        # Define the model bucket and key (hard code or configure as environment variables)
        model_bucket = os.environ.get('MODEL_BUCKET', 'default-model-bucket')
        model_key = os.environ.get('MODEL_KEY', 'default/path/to/model.pkl')

        # Log event
        logger.info(f'Processing file s3://{input_bucket}/{input_key}')

        # Load model from S3
        model = load_model(model_bucket, model_key)

        # Download input CSV file from S3
        response = s3.get_object(Bucket=input_bucket, Key=input_key)
        input_csv = response['Body'].read().decode('utf-8')
        df = pd.read_csv(io.StringIO(input_csv))
        logger.info('Input csv loaded successfully')

        # Inference
        logger.info('Running predictions...')
        predictions = make_prediction(model, df)

        # predictions to csv:
        predictions_df = pd.DataFrame(predictions, columns=['Predictions'])
        output_csv = io.StringIO()
        predictions_df.to_csv(output_csv, index=False)
        """
        ensures that the pointer for the in-memory file is reset to the 
        start so that the entire CSV data can be read and uploaded to S3. 
        It's an essential step when working with file-like objects in memory.
        """
        output_csv.seek(0)
        logger.info('Predictions generated and converted to csv')

        # Upload output csv to S3
        s3.put_object(
            Bucket=output_bucket,
            Key=output_key,
            Body=output_csv.getvalue()
        )

        logger.info(f'Predictions successfully loaded to s3://{output_bucket}/{output_key}')
        return{
            'statusCode': 200,
            'body': f'Woohoo!'
        }
    except Exception as e:
        logger.error(f'Error processing file: {str(e)}')
        return{
            'statusCode': 500,
            'body': f'Error processing file: {str(e)}'
        }
