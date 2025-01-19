import boto3
# Save the model to S3
s3 = boto3.client('s3')

def upload_model_to_s3(file_path, bucket_name, s3_path):
    s3 = boto3.client('s3')
    s3.upload_file(file_path, bucket_name, s3_path)
    print(f"Uploaded {file_path} to s3://{bucket_name}/{s3_path}")


file_path = '/Users/clairevans/Documents/ML_Ops/iris/develop/model.pkl'
bucket_name = 'saved-models-all'
s3_path = 'iris/model.pkl'

upload_model_to_s3(file_path, bucket_name, s3_path)

