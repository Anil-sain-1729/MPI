import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
# from sklearn.ensemble import RandomForestClassifier  # Optional upgrade

def preprocess(df):
    # Nothing to drop, only encode categorical if needed
    # Here 'Sex' is already numeric (0/1), so nothing to encode
    # Fill missing numeric values with median
    df = df.fillna(df.median(numeric_only=True))
    return df

def train_and_evaluate():
    # Load training data
    train_data = pd.read_csv("Titanic_train.csv")
    
    # Separate features and target
    y_train = train_data["Survived"]
    X_train = preprocess(train_data.drop(columns=["Survived"]))
    
    # Train Decision Tree
    model = DecisionTreeClassifier(max_depth=5, random_state=42)
    model.fit(X_train, y_train)
    
    # Load test data
    test_data = pd.read_csv("Titanic_test.csv")
    X_test = preprocess(test_data)
    
    # Predict
    preds = model.predict(X_test)
    
    return preds

if __name__ == "__main__":
    preds = train_and_evaluate()
    
    # This will calculate the accuracy of your code
    true_labels = pd.read_csv("Titanic_test_labels.csv")["Survived"]
    acc = accuracy_score(true_labels, preds)
    
    print(f"The model accuracy: {acc*100:.2f}%")
