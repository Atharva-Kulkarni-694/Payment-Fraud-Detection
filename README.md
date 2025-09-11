"""
# 🔍 Fraud Detection System for Payments

A complete end-to-end fraud detection system built with Python that processes payment transactions in real-time and identifies potentially fraudulent activities using machine learning.

## 🚀 Features

- **Real-time fraud detection** using XGBoost ML model
- **RESTful API** for transaction processing
- **Interactive dashboard** with Streamlit
- **Database integration** (PostgreSQL/File-based)
- **Comprehensive logging** and monitoring
- **Scalable architecture** with streaming support

## 📁 Project Structure

```
fraud_detection_system/
├── data/
│   ├── generate_data.py           # Sample data generation
│   ├── transactions.csv           # Generated sample data
│   └── processed_transactions.json # Processed transactions storage
├── ml_model/
│   ├── preprocessing.py           # Feature engineering
│   ├── train_model.py            # Model training
│   ├── predict.py                # Prediction logic
│   ├── model.pkl                 # Trained model
│   └── preprocessor.pkl          # Feature preprocessor
├── api/
│   └── main.py                   # FastAPI application
├── ui/
│   └── app.py                    # Streamlit dashboard
├── database/
│   └── db_connection.py          # Database management
├── utils/
│   ├── config.py                 # Configuration
│   └── logger.py                 # Logging utilities
├── run.py                        # Main setup script
├── requirements.txt              # Dependencies
└── README.md                     # This file
```

## ⚙️ Installation & Setup

### 1. Clone and Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt
```

### 2. Initialize the System

```bash
# Run the setup script (generates data, trains model, initializes database)
python run.py
```

This will:
- Create project directories
- Generate 10,000 sample transactions
- Train the fraud detection model
- Initialize the database

### 3. Start the Services

#### Start the API Server
```bash
# Start FastAPI server
python api/main.py

# Or using uvicorn directly
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

#### Start the Dashboard
```bash
# Start Streamlit dashboard (in a new terminal)
streamlit run ui/app.py
```

## 🔧 Usage

### API Endpoints

#### Check Transaction
```bash
curl -X POST "http://localhost:8000/check_transaction" \
     -H "Content-Type: application/json" \
     -d '{
       "user_id": "user_123",
       "amount": 299.99,
       "location": "New York",
       "device": "mobile"
     }'
```

Response:
```json
{
  "prediction": "SAFE",
  "confidence": 0.123,
  "risk_score": 12.3,
  "transaction_id": "user_123"
}
```

#### Get Statistics
```bash
curl "http://localhost:8000/stats"
```

Response:
```json
{
  "total_transactions": 1250,
  "fraud_detected": 63,
  "safe_transactions": 1187,
  "fraud_rate": 5.04,
  "avg_confidence": 0.187
}
```

### Dashboard Features

Access the dashboard at `http://localhost:8501` to view:
- **Real-time metrics**: Total transactions, fraud rate, confidence scores
- **Visual charts**: Fraud distribution, confidence histograms
- **Transaction table**: Recent transactions with fraud predictions

## 🤖 Machine Learning Model

### Features Used
- **Transaction amount** and amount patterns
- **Time-based features**: Hour, day of week, weekend/night flags
- **User behavior**: Average spending, transaction frequency
- **Location and device** encoding
- **Statistical features**: Log amounts, rounded amounts

### Model Performance
The XGBoost classifier achieves:
- **High accuracy** on fraud detection
- **Low false positive rate** to minimize customer friction
- **Fast prediction times** for real-time processing

## 🗄️ Database Options

### File-based Storage (Default)
- No setup required
- Uses JSON files for simple deployment
- Suitable for development and small-scale usage

### PostgreSQL (Optional)
```python
# Set environment variable to use PostgreSQL
export DB_HOST=localhost
export DB_USER=your_username
export DB_PASSWORD=your_password
```

## 📊 Sample Data

The system generates realistic synthetic data with:
- **95% normal transactions**: Regular amounts, common locations, business hours
- **5% fraudulent transactions**: Unusual amounts, suspicious timing, uncommon locations
- **User behavior patterns**: Consistent spending habits per user

## 🧪 Testing

### Manual Testing
```python
from ml_model.predict import fraud_predictor

# Test a transaction
transaction = {
    "user_id": "test_user",
    "amount": 1500.00,
    "location": "Unknown",
    "device": "desktop"
}

result = fraud_predictor.predict_single_transaction(transaction)
print(result)
```

### API Testing
```bash
# Test with curl
curl -X POST "http://localhost:8000/check_transaction" \
     -H "Content-Type: application/json" \
     -d '{"user_id":"test","amount":50,"location":"NYC","device":"mobile"}'
```

## 🚀 Deployment

### Docker Deployment (Coming Soon)
```dockerfile
# Dockerfile will be available in future updates
FROM python:3.9-slim
# ... deployment configuration
```

### Cloud Deployment
- **AWS**: Deploy using EC2, RDS, and API Gateway
- **Google Cloud**: Use Cloud Run, Cloud SQL, and Cloud Functions
- **Azure**: Deploy with App Service and Azure SQL Database

## 📈 Monitoring & Alerts

### Logging
- All transactions are logged with fraud predictions
- Fraud events generate warning-level logs
- Log files: `fraud_detection.log`

### Metrics Tracking
- Transaction volume and fraud rates
- Model confidence scores
- Processing performance metrics

## 🔧 Configuration

Environment variables in `utils/config.py`:
```python
DB_HOST=localhost          # Database host
DB_PORT=5432              # Database port
DB_NAME=fraud_detection   # Database name
DB_USER=postgres          # Database user
DB_PASSWORD=password      # Database password
MODEL_PATH=ml_model/model.pkl  # Model file path
API_PORT=8000             # API server port
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙋‍♂️ Support

For questions or issues:
- Check the logs in `fraud_detection.log`
- Ensure all dependencies are installed
- Verify the model is trained (`ml_model/model.pkl` exists)
- Check API server is running on port 8000
"""