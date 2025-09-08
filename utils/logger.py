import logging
import json
from datetime import datetime
from typing import Dict, Any

class FraudLogger:
    def __init__(self, log_file="fraud_detection.log"):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def log_transaction(self, transaction_id: str, prediction: str, confidence: float, transaction_data: Dict[str, Any]):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "transaction_id": transaction_id,
            "prediction": prediction,
            "confidence": confidence,
            "transaction_data": transaction_data
        }
        
        if prediction == "FRAUD":
            self.logger.warning(f"FRAUD DETECTED: {json.dumps(log_entry)}")
        else:
            self.logger.info(f"SAFE TRANSACTION: {json.dumps(log_entry)}")

fraud_logger = FraudLogger()