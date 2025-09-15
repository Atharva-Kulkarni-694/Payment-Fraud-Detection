import psycopg2
import pandas as pd
from pymongo import MongoClient
from typing import List, Dict, Any
import json
import os
import sys
from datetime import datetime

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.config import config

class DatabaseManager:
    def __init__(self, use_postgres=False):  # Changed default to False for simplicity
        self.use_postgres = use_postgres
        if use_postgres:
            try:
                self.conn = psycopg2.connect(
                    host=config.DB_HOST,
                    port=config.DB_PORT,
                    database=config.DB_NAME,
                    user=config.DB_USER,
                    password=config.DB_PASSWORD
                )
            except Exception as e:
                print(f"PostgreSQL connection failed: {e}")
                print("Switching to file-based storage...")
                self.use_postgres = False
                self.transactions = []
        else:
            # Simple file-based storage as fallback
            self.transactions = []
            self.db_file = "data/processed_transactions.json"
            self._load_transactions()
    
    def _load_transactions(self):
        """Load transactions from file"""
        try:
            if os.path.exists(self.db_file):
                with open(self.db_file, 'r') as f:
                    self.transactions = json.load(f)
        except Exception as e:
            print(f"Error loading transactions: {e}")
            self.transactions = []
    
    def _save_transactions(self):
        """Save transactions to file"""
        try:
            os.makedirs(os.path.dirname(self.db_file), exist_ok=True)
            with open(self.db_file, 'w') as f:
                json.dump(self.transactions, f, default=str)
        except Exception as e:
            print(f"Error saving transactions: {e}")
    
    def create_tables(self):
        if self.use_postgres:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(50),
                    amount DECIMAL(10,2),
                    location VARCHAR(100),
                    device VARCHAR(50),
                    timestamp TIMESTAMP,
                    is_fraud BOOLEAN,
                    prediction VARCHAR(20),
                    confidence DECIMAL(5,4),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            self.conn.commit()
        else:
            # File-based storage doesn't need table creation
            pass
    
    def insert_transaction(self, transaction_data: Dict[str, Any]):
        if self.use_postgres:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO transactions (user_id, amount, location, device, timestamp, is_fraud, prediction, confidence)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                transaction_data.get('user_id'),
                transaction_data.get('amount'),
                transaction_data.get('location'),
                transaction_data.get('device'),
                transaction_data.get('timestamp'),
                transaction_data.get('is_fraud'),
                transaction_data.get('prediction'),
                transaction_data.get('confidence')
            ))
            self.conn.commit()
        else:
            # Add to file-based storage
            transaction_data['created_at'] = datetime.now().isoformat()
            self.transactions.append(transaction_data)
            self._save_transactions()
    
    def get_transactions(self, limit=1000) -> pd.DataFrame:
        if self.use_postgres:
            query = "SELECT * FROM transactions ORDER BY created_at DESC LIMIT %s"
            return pd.read_sql_query(query, self.conn, params=(limit,))
        else:
            # Return from file-based storage
            recent_transactions = self.transactions[-limit:] if len(self.transactions) > limit else self.transactions
            return pd.DataFrame(recent_transactions)

db_manager = DatabaseManager()