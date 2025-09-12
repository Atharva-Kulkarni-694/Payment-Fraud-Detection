import pandas as pd
import numpy as np
import joblib
import os
import sys
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import xgboost as xgb

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from ml_model.preprocessing import TransactionPreprocessor

class FraudDetectionModel:
    def __init__(self, model_type="xgboost"):
        self.model_type = model_type
        self.model = None
        self.threshold = 0.5
        
        if model_type == "xgboost":
            self.model = xgb.XGBClassifier(
                objective='binary:logistic',
                eval_metric='logloss',
                random_state=42,
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1
            )
    
    def train(self, X_train, y_train):
        """Train the fraud detection model"""
        self.model.fit(X_train, y_train)
        return self
    
    def predict(self, X):
        """Predict fraud probability"""
        predictions = self.model.predict(X)
        probabilities = self.model.predict_proba(X)[:, 1]
        return predictions, probabilities
    
    def save_model(self, filepath):
        """Save trained model"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        model_data = {
            'model': self.model,
            'model_type': self.model_type,
            'threshold': self.threshold
        }
        joblib.dump(model_data, filepath)
    
    @classmethod
    def load_model(cls, filepath):
        """Load trained model"""
        model_data = joblib.load(filepath)
        instance = cls(model_data['model_type'])
        instance.model = model_data['model']
        instance.threshold = model_data['threshold']
        return instance

def train_fraud_model():
    """Train and save fraud detection model"""
    # Create directories
    os.makedirs('ml_model', exist_ok=True)
    
    # Load data
    if not os.path.exists('data/transactions.csv'):
        print("No data found. Generating sample data...")
        from data.generate_data import generate_transaction_data
        generate_transaction_data()
    
    df = pd.read_csv('data/transactions.csv')
    print(f"Loaded {len(df)} transactions")
    
    # Initialize preprocessor
    preprocessor = TransactionPreprocessor()
    
    # Preprocess
    X, y = preprocessor.prepare_features(df, fit_scaler=True)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Train model
    print("Training XGBoost model...")
    model = FraudDetectionModel("xgboost")
    model.train(X_train, y_train)
    
    # Evaluate
    y_pred, y_prob = model.predict(X_test)
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save model and preprocessor
    model.save_model('ml_model/model.pkl')
    joblib.dump(preprocessor, 'ml_model/preprocessor.pkl')
    
    print("✅ Model trained and saved successfully!")
    return model

if __name__ == "__main__":
    train_fraud_model()