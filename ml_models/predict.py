import pandas as pd
import joblib
import os
import sys
from typing import Dict, Any

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from ml_model.train_model import FraudDetectionModel

class FraudPredictor:
    def __init__(self):
        self.model = None
        self.preprocessor = None
        self.load_models()
    
    def load_models(self):
        """Load trained model and preprocessor"""
        try:
            self.model = FraudDetectionModel.load_model('ml_model/model.pkl')
            self.preprocessor = joblib.load('ml_model/preprocessor.pkl')
            print("✅ Models loaded successfully")
        except FileNotFoundError as e:
            print(f"Models not found: {e}")
            print("Please train the model first by running: python ml_model/train_model.py")
    
    def predict_single_transaction(self, transaction_data: Dict[str, Any]):
        """Predict fraud for a single transaction"""
        if self.model is None or self.preprocessor is None:
            return {"error": "Models not loaded"}
        
        try:
            # Convert to DataFrame
            df = pd.DataFrame([transaction_data])
            
            # Preprocess
            X, _ = self.preprocessor.prepare_features(df)
            
            # Predict
            prediction, probability = self.model.predict(X)
            
            result = {
                "prediction": "FRAUD" if prediction[0] == 1 else "SAFE",
                "confidence": float(probability[0]),
                "risk_score": float(probability[0]) * 100
            }
            
            return result
            
        except Exception as e:
            return {"error": f"Prediction failed: {str(e)}"}

# Global instance
fraud_predictor = FraudPredictor()