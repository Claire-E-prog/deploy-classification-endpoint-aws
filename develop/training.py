from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_iris
import joblib


data = load_iris()

def preprocessing(data):
    X = data['data']
    y = data['target']
    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2)

    return X_train, X_test, y_train, y_test

def train_model(data):
    X_train, X_test, y_train, y_test = preprocessing(data)
    print("preprocessing done")
    model = RandomForestClassifier(n_estimators=100, random_state= 1)
    model.fit(X_train, y_train)
    print("model trained")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return model, accuracy

model, accuracy = train_model(data)
print(f'Accuracy: {accuracy}')

# Test the model
# input_data = [5.1, 3.5, 1.4, 0.2]
# print(f'raw output {model.predict([input_data])}')
# add code to convert output from model.predict to class label
# label = data['target_names'][model.predict([input_data])]
# print(f'Class label: {label}')

# Save the model locally
joblib.dump(model, 'model.pkl')
print("Model saved to model.pkl")

