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