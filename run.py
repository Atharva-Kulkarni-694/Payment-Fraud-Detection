import os
import sys
from datetime import datetime

def setup_project():
    """Set up the project structure and initialize components"""
    
    print("🚀 Setting up Fraud Detection System...")
    
    # Create necessary directories
    directories = [
        'data', 'ml_model', 'utils', 'database', 
        'api', 'ui', 'streaming', 'tests'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("✅ Project directories created")
    
    # Generate sample data if not exists
    if not os.path.exists('data/transactions.csv'):
        print("📊 Generating sample transaction data...")
        from data.generate_data import generate_transaction_data
        generate_transaction_data()
        print("✅ Sample data generated")
    else:
        print("✅ Sample data already exists")
    
    # Train model if not exists
    if not os.path.exists('ml_model/model.pkl'):
        print("🤖 Training fraud detection model...")
        from ml_model.train_model import train_fraud_model
        train_fraud_model()
        print("✅ Model trained and saved")
    else:
        print("✅ Model already exists")
    
    # Initialize database
    from database.db_connection import db_manager
    db_manager.create_tables()
    print("✅ Database initialized")
    
    print("\n🎯 System Setup Complete!")
    print("\n📋 Next Steps:")
    print("1. Start API server: python api/main.py")
    print("2. Start dashboard: streamlit run ui/app.py")
    print("3. Test API: curl -X POST http://localhost:8000/check_transaction -H 'Content-Type: application/json' -d '{\"user_id\":\"test_user\",\"amount\":299.99,\"location\":\"New York\",\"device\":\"mobile\"}'")

def test_system():
    """Test the fraud detection system"""
    print("\n🧪 Testing Fraud Detection System...")
    
    from ml_model.predict import fraud_predictor
    
    # Test transactions
    test_transactions = [
        {
            "user_id": "user_12345",
            "amount": 50.00,  # Normal amount
            "location": "New York",
            "device": "mobile",
            "timestamp": datetime.now().isoformat()
        },
        {
            "user_id": "user_67890",
            "amount": 2500.00,  # Suspicious amount
            "location": "Unknown Location",
            "device": "desktop",
            "timestamp": datetime.now().replace(hour=3).isoformat()  # Suspicious time
        }
    ]
    
    for i, transaction in enumerate(test_transactions, 1):
        print(f"\n🔍 Test Transaction {i}:")
        print(f"Amount: ${transaction['amount']}")
        print(f"Location: {transaction['location']}")
        print(f"Device: {transaction['device']}")
        
        result = fraud_predictor.predict_single_transaction(transaction)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"🎯 Prediction: {result['prediction']}")
            print(f"📊 Confidence: {result['confidence']:.3f}")
            print(f"⚠️ Risk Score: {result['risk_score']:.1f}%")

if __name__ == "__main__":
    # Setup the project
    setup_project()
    
    # Test the system
    test_system()