from sklearn.datasets import make_classification
import pandas as pd 
import boto3

def generate_data(n_samples, n_features, n_classes):
    X, y = make_classification(n_samples=n_samples, n_features=n_features, n_classes=n_classes, random_state=1)
    X = 1.0 + (X - X.min()) * (5.0 - 1.0) / (X.max() - X.min())
    return X

# create csv file from data
data = pd.DataFrame(generate_data(100, 4, 2))

# Send the data to S3
bucket = 'data-in-all'
key = 'iris/data.csv'
data.to_csv('/tmp/data.csv', index=False)
# initialize s3 client
s3 = boto3.client('s3')
# upload file to s3
s3.upload_file('/tmp/data.csv', bucket, key)
print(f'Uploaded {key} to s3://{bucket}/{key}')
