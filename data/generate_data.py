import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

def generate_transaction_data(n_samples=10000):
    """Generate synthetic payment transaction data"""
    
    np.random.seed(42)
    random.seed(42)
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Generate base data
    user_ids = [f"user_{i:05d}" for i in range(1, 5001)]
    locations = ["New York", "San Francisco", "London", "Tokyo", "Paris", "Berlin", "Sydney", "Toronto"]
    devices = ["mobile", "desktop", "tablet"]
    
    data = []
    
    for i in range(n_samples):
        # Normal transaction patterns
        is_fraud = np.random.random() < 0.05  # 5% fraud rate
        
        if is_fraud:
            # Fraudulent patterns
            amount = np.random.exponential(500) + 100  # Higher amounts
            user_id = np.random.choice(user_ids)
            location = np.random.choice(locations)
            device = np.random.choice(devices)
            # Unusual hours
            hour = np.random.choice([2, 3, 4, 23, 0, 1])
        else:
            # Normal patterns
            amount = np.random.gamma(2, 50)  # Lower amounts
            user_id = np.random.choice(user_ids)
            location = np.random.choice(locations[:4])  # More common locations
            device = np.random.choice(devices, p=[0.6, 0.3, 0.1])  # Mobile more common
            # Normal hours
            hour = np.random.choice(range(8, 22))
        
        timestamp = datetime.now() - timedelta(
            days=np.random.randint(0, 30),
            hours=hour,
            minutes=np.random.randint(0, 60)
        )
        
        data.append({
            'user_id': user_id,
            'amount': round(amount, 2),
            'location': location,
            'device': device,
            'timestamp': timestamp,
            'is_fraud': is_fraud
        })
    
    df = pd.DataFrame(data)
    df.to_csv('data/transactions.csv', index=False)
    print(f"Generated {n_samples} transactions and saved to data/transactions.csv")
    return df

if __name__ == "__main__":
    generate_transaction_data()