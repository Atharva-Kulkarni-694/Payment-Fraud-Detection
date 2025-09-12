import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import os

class TransactionPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_columns = []
    
    def create_features(self, df):
        """Engineer features from raw transaction data"""
        df = df.copy()
        
        # Time-based features
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        df['day_of_week'] = pd.to_datetime(df['timestamp']).dt.dayofweek
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        df['is_night'] = ((df['hour'] >= 22) | (df['hour'] <= 6)).astype(int)
        
        # Amount-based features
        df['log_amount'] = np.log1p(df['amount'])
        df['amount_rounded'] = (df['amount'] % 1 == 0).astype(int)
        
        # User behavior (simplified)
        user_stats = df.groupby('user_id')['amount'].agg(['mean', 'std', 'count']).reset_index()
        user_stats.columns = ['user_id', 'user_avg_amount', 'user_std_amount', 'user_transaction_count']
        user_stats['user_std_amount'] = user_stats['user_std_amount'].fillna(0)
        df = df.merge(user_stats, on='user_id', how='left')
        
        # Encode categorical variables
        categorical_cols = ['location', 'device']
        for col in categorical_cols:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
                df[f'{col}_encoded'] = self.label_encoders[col].fit_transform(df[col].astype(str))
            else:
                # Handle unseen categories
                known_categories = set(self.label_encoders[col].classes_)
                df[col] = df[col].apply(lambda x: x if x in known_categories else 'unknown')
                
                # Add 'unknown' to encoder if not present
                if 'unknown' not in known_categories:
                    self.label_encoders[col].classes_ = np.append(self.label_encoders[col].classes_, 'unknown')
                
                df[f'{col}_encoded'] = self.label_encoders[col].transform(df[col].astype(str))
        
        return df
    
    def prepare_features(self, df, fit_scaler=False):
        """Prepare final feature matrix"""
        df = self.create_features(df)
        
        feature_cols = [
            'amount', 'log_amount', 'amount_rounded',
            'hour', 'day_of_week', 'is_weekend', 'is_night',
            'user_avg_amount', 'user_std_amount', 'user_transaction_count',
            'location_encoded', 'device_encoded'
        ]
        
        # Handle missing values
        df[feature_cols] = df[feature_cols].fillna(0)
        
        if fit_scaler:
            X_scaled = self.scaler.fit_transform(df[feature_cols])
            self.feature_columns = feature_cols
        else:
            X_scaled = self.scaler.transform(df[feature_cols])
        
        return X_scaled, df['is_fraud'].values if 'is_fraud' in df.columns else None