import joblib
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
import argparse # for command line arguments

def load_model(model_path):
    model = joblib.load(model_path)
    return model

def make_prediction(model, input_data):
    input_data = np.array(input_data)
    predictions = model.predict(input_data)
    return predictions

def make_data(n_samples, n_features, n_classes):
    X, y = make_classification(n_samples=n_samples, n_features=n_features, n_classes=n_classes, random_state=1)
    X = 1.0 + (X - X.min()) * (5.0 - 1.0) / (X.max() - X.min())
    return X

def make_csv():
    data = pd.DataFrame(make_data(100, 4, 2))
    path = 'iris-data.csv'
    pd.to_csv(data, path)
    return path

def main():
    
    model = load_model(model.pkl)
    input_data = pd.read_csv(make_csv())
    predictions = make_prediction(model, input_data)
    print(f"Predictions: {predictions}")

if __name__ == "__main__":
    main()
