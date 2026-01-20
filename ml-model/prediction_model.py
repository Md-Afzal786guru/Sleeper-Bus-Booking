# prediction_model.py - Booking Confirmation Prediction Model
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import json
from datetime import datetime

class BookingPredictionModel:
    """
    Predicts the probability of booking confirmation based on historical data
    
    Features considered:
    - Day of week
    - Time of booking
    - Route segment
    - Seat type preference
    - Number of seats
    - Meal preference
    - Advance booking days
    - Season/Month
    """
    
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.label_encoders = {}
        self.feature_columns = [
            'day_of_week', 'booking_hour', 'route_segment', 
            'seat_type', 'num_seats', 'has_meal', 
            'advance_days', 'month', 'is_weekend', 'is_peak_hour'
        ]
        
    def generate_mock_dataset(self, n_samples=1000):
        """Generate mock historical booking data"""
        np.random.seed(42)
        
        data = {
            'booking_id': [f'BK{i:06d}' for i in range(n_samples)],
            'day_of_week': np.random.choice(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                                            'Friday', 'Saturday', 'Sunday'], n_samples),
            'booking_hour': np.random.randint(0, 24, n_samples),
            'route_segment': np.random.choice(['Ahmedabad-Vadodara', 'Ahmedabad-Surat', 
                                              'Ahmedabad-Mumbai', 'Vadodara-Mumbai', 
                                              'Surat-Mumbai'], n_samples),
            'seat_type': np.random.choice(['lower', 'upper'], n_samples),
            'num_seats': np.random.choice([1, 2, 3, 4], n_samples, p=[0.4, 0.3, 0.2, 0.1]),
            'has_meal': np.random.choice([0, 1], n_samples, p=[0.3, 0.7]),
            'advance_days': np.random.randint(0, 30, n_samples),
            'month': np.random.randint(1, 13, n_samples),
        }
        
        df = pd.DataFrame(data)
        
        # Create derived features
        df['is_weekend'] = df['day_of_week'].isin(['Saturday', 'Sunday']).astype(int)
        df['is_peak_hour'] = df['booking_hour'].isin([9, 10, 11, 18, 19, 20]).astype(int)
        
        # Generate target variable (confirmed: 1, cancelled: 0)
        # Higher confirmation probability for:
        # - Advance bookings
        # - Weekday travel
        # - Off-peak hours
        # - With meals (shows commitment)
        
        confirmation_prob = 0.5  # Base probability
        
        # Adjust based on features
        confirmation_prob += (df['advance_days'] > 7) * 0.15
        confirmation_prob += (df['is_weekend'] == 0) * 0.10
        confirmation_prob += (df['has_meal'] == 1) * 0.12
        confirmation_prob += (df['is_peak_hour'] == 0) * 0.08
        confirmation_prob += (df['num_seats'] == 1) * 0.05
        
        # Add some randomness
        noise = np.random.uniform(-0.15, 0.15, n_samples)
        confirmation_prob = np.clip(confirmation_prob + noise, 0, 1)
        
        df['confirmed'] = (confirmation_prob > 0.5).astype(int)
        df['confirmation_probability'] = confirmation_prob
        
        return df
    
    def preprocess_features(self, df, fit=False):
        """Encode categorical variables"""
        categorical_cols = ['day_of_week', 'route_segment', 'seat_type']
        
        for col in categorical_cols:
            if fit:
                self.label_encoders[col] = LabelEncoder()
                df[f'{col}_encoded'] = self.label_encoders[col].fit_transform(df[col])
            else:
                df[f'{col}_encoded'] = self.label_encoders[col].transform(df[col])
        
        # Update feature columns to use encoded versions
        encoded_features = [
            'day_of_week_encoded', 'booking_hour', 'route_segment_encoded', 
            'seat_type_encoded', 'num_seats', 'has_meal', 
            'advance_days', 'month', 'is_weekend', 'is_peak_hour'
        ]
        
        return df, encoded_features
    
    def train(self, df):
        """Train the prediction model"""
        print("Training Booking Confirmation Prediction Model...")
        
        # Preprocess
        df, encoded_features = self.preprocess_features(df, fit=True)
        
        X = df[encoded_features]
        y = df['confirmed']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Evaluate
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        
        print(f"Training Accuracy: {train_score*100:.2f}%")
        print(f"Testing Accuracy: {test_score*100:.2f}%")
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': encoded_features,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\nFeature Importance:")
        print(feature_importance)
        
        return {
            'train_accuracy': train_score,
            'test_accuracy': test_score,
            'feature_importance': feature_importance.to_dict('records')
        }
    
    def predict_confirmation_probability(self, booking_data):
        """
        Predict confirmation probability for a new booking
        
        Args:
            booking_data: dict with keys:
                - day_of_week
                - booking_hour
                - route_segment
                - seat_type
                - num_seats
                - has_meal
                - advance_days
                - month
        
        Returns:
            float: Confirmation probability (0-100%)
        """
        # Create dataframe from input
        df = pd.DataFrame([booking_data])
        
        # Add derived features
        df['is_weekend'] = df['day_of_week'].isin(['Saturday', 'Sunday']).astype(int)
        df['is_peak_hour'] = df['booking_hour'].isin([9, 10, 11, 18, 19, 20]).astype(int)
        
        # Preprocess
        df, encoded_features = self.preprocess_features(df, fit=False)
        
        X = df[encoded_features]
        
        # Predict probability
        probability = self.model.predict_proba(X)[0][1] * 100
        
        return round(probability, 2)

# Example usage
if __name__ == "__main__":

    predictor = BookingPredictionModel()

    print("Generating mock historical data...")
    mock_data = predictor.generate_mock_dataset(n_samples=1000)
    

    mock_data.to_csv('mock_booking_dataset.csv', index=False)
    print("\nMock dataset saved to 'mock_booking_dataset.csv'")
    print(f"Dataset shape: {mock_data.shape}")
    print(f"\nFirst 5 rows:")
    print(mock_data.head())
    
    # Train model
    print("\n" + "="*50)
    training_results = predictor.train(mock_data)
    
    # Test predictions
    print("\n" + "="*50)
    print("Sample Predictions:")
    
    test_cases = [
        {
            'day_of_week': 'Friday',
            'booking_hour': 14,
            'route_segment': 'Ahmedabad-Mumbai',
            'seat_type': 'lower',
            'num_seats': 2,
            'has_meal': 1,
            'advance_days': 10,
            'month': 3
        },
        {
            'day_of_week': 'Sunday',
            'booking_hour': 22,
            'route_segment': 'Ahmedabad-Surat',
            'seat_type': 'upper',
            'num_seats': 1,
            'has_meal': 0,
            'advance_days': 1,
            'month': 12
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        prob = predictor.predict_confirmation_probability(test_case)
        print(f"\nTest Case {i}:")
        print(f"  Route: {test_case['route_segment']}")
        print(f"  Day: {test_case['day_of_week']}")
        print(f"  Advance Days: {test_case['advance_days']}")
        print(f"  Has Meal: {'Yes' if test_case['has_meal'] else 'No'}")
        print(f"  → Confirmation Probability: {prob}%")

    insights = {
        'model_type': 'Random Forest Classifier',
        'training_samples': len(mock_data),
        'accuracy_metrics': {
            'train_accuracy': f"{training_results['train_accuracy']*100:.2f}%",
            'test_accuracy': f"{training_results['test_accuracy']*100:.2f}%"
        },
        'top_features': training_results['feature_importance'][:5]
    }
    
    with open('model_insights.json', 'w') as f:
        json.dump(insights, f, indent=2)
    
    print("\n" + "="*50)
    print("Model insights saved to 'model_insights.json'")