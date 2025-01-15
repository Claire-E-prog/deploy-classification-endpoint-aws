FROM public.ecr.aws/lambda/python:3.12

# Copy requirements.txt
COPY ../requirements-dev.txt ${LAMBDA_TASK_ROOT}/requirements.txt

# Install the specified packages
RUN pip install -r ${LAMBDA_TASK_ROOT}/requirements.txt

# Copy function code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.lambda_handler" ]