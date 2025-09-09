from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime
import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from ml_model.predict import fraud_predictor
from database.db_connection import db_manager
from utils.logger import fraud_logger

app = FastAPI(title="Fraud Detection API", version="1.0.0")

class TransactionRequest(BaseModel):
    user_id: str
    amount: float
    location: str
    device: str
    timestamp: str = None

class TransactionResponse(BaseModel):
    prediction: str
    confidence: float
    risk_score: float
    transaction_id: str

@app.on_event("startup")
async def startup_event():
    """Initialize database and models on startup"""
    db_manager.create_tables()

@app.get("/")
async def root():
    return {
        "message": "Fraud Detection API is running",
        "endpoints": ["/check_transaction", "/stats"],
        "version": "1.0.0"
    }

@app.post("/check_transaction", response_model=TransactionResponse)
async def check_transaction(transaction: TransactionRequest):
    """Check if a transaction is fraudulent"""
    try:
        # Prepare transaction data
        transaction_data = {
            "user_id": transaction.user_id,
            "amount": transaction.amount,
            "location": transaction.location,
            "device": transaction.device,
            "timestamp": transaction.timestamp or datetime.now().isoformat()
        }
        
        # Get prediction
        result = fraud_predictor.predict_single_transaction(transaction_data)
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        # Log the transaction
        fraud_logger.log_transaction(
            transaction.user_id,
            result["prediction"],
            result["confidence"],
            transaction_data
        )
        
        # Store in database
        transaction_data.update(result)
        db_manager.insert_transaction(transaction_data)
        
        return TransactionResponse(
            prediction=result["prediction"],
            confidence=result["confidence"],
            risk_score=result["risk_score"],
            transaction_id=transaction.user_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def get_stats():
    """Get fraud detection statistics"""
    try:
        df = db_manager.get_transactions(1000)
        
        if df.empty:
            return {"message": "No transactions found"}
        
        fraud_count = len(df[df.get('prediction', '') == 'FRAUD'])
        total_count = len(df)
        
        stats = {
            "total_transactions": total_count,
            "fraud_detected": fraud_count,
            "safe_transactions": total_count - fraud_count,
            "fraud_rate": (fraud_count / total_count * 100) if total_count > 0 else 0,
            "avg_confidence": df['confidence'].mean() if 'confidence' in df.columns else 0
        }
        
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)    