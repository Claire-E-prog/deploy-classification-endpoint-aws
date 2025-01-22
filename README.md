# Deploy Classification Model Pipeline

This project demonstrates the process of deploying a simple classification model for inference using **AWS Lambda** triggered on a data upload to s3 and returns predictions to another S3 bucket. 
## Overview

The project includes:
1. **Creating a Classification Model**: Build and save a simple model using the Iris dataset.
2. **Deploying the Model as a Lambda Endpoint**: 
   - Triggered by a file upload to an S3 bucket.
   - Generates predictions and saves the results in another S3 bucket.
3. **Exploring Deployment Methods**:
   - Zip file upload with Lambda Layers.
   - Docker-based deployment.

---

## Steps in the Project

### 1. **Train and Save the Model**
- Create a simple classification model using the Iris dataset.
- Save the trained model as a `.pkl` file for reuse.

### 2. **Set Up Lambda Deployment**
- Develop a Lambda function that:
  - Loads the trained model.
  - Processes new data uploaded as a `.csv` file to S3.
  - Outputs predictions as a `.csv` file to another S3 bucket.
- Configure AWS IAM permissions for:
  - Lambda execution.
  - S3 read/write access.

### 3. **Deploy the Model**
- Create a `requirements.txt` file for dependencies.
- Package the Lambda function as a zip file
- Package necessary files and dependencies as Lambda Layers.
- Upload the zip file to AWS Lambda, confiure S3 trigger and add layers.

---

## Key Learnings

### **Challenges with Zip Deployment**
- **Memory Constraints**: Packaging libraries like `scikit-learn` exceeded Lambda’s limits, even with layers.
                          Initial exploration revealed significant challenges in deploying ML models using zip uploads:
                          - Lambda layers alone are insufficient for dependencies like `scikit-learn`.
                          - Docker provides a more scalable and flexible solution for ML model deployment.
- **Architecture-Specific Layers**: Found a pre-built `pandas` layer compatible with `arm64`. Useful for functions
  limited to pandas as a requirement.

### **Solution**
- **Containerize the Endpoint**:
  - Build a Docker image for the model endpoint.
  - Push the Docker image to an AWS Elastic Container Registry (ECR).
  - Use the container as the source for the Lambda function.

---

## File Structure

```plaintext
.
├── develop/                 
│   ├── train_model.py    
|   └── model.pkl   
├── deploy/
│   ├── lambda_function.py # Lambda handler and model loader
│   ├── requirements.txt   
│   └── Dockerfile                   
└── README.md             
