import os
import sys
import json
import pandas as pd
import joblib
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

# Download NLTK resources if needed
nltk.download('stopwords')
nltk.download('wordnet')

# Add the directory containing preprocessing.py to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from preprocessing import preprocess_text
except ImportError as e:
    print(f"Error importing preprocessing module: {e}")
    raise

def load_data():
    """Load data from JSON file or create sample data"""
    data_paths = [
        '../data/Data.json',  # Relative path when running from ml_model directory
        '/app/data/Data.json'  # Docker container path
    ]

    for path in data_paths:
        if os.path.exists(path):
            print(f"Loading data from {path}")
            try:
                # Try to load as JSON Lines format
                data = pd.read_json(path, lines=True)
                print(f"Successfully loaded data with {len(data)} rows")
                print(f"Columns in data: {data.columns.tolist()}")
                return data
            except Exception as e:
                print(f"Error loading data as JSON lines: {str(e)}")
                try:
                    # Try to load as regular JSON
                    with open(path, 'r') as f:
                        raw_data = json.load(f)

                    # Handle various possible JSON structures
                    if isinstance(raw_data, list):
                        data = pd.DataFrame(raw_data)
                    elif isinstance(raw_data, dict):
                        if 'reviews' in raw_data:
                            data = pd.DataFrame(raw_data['reviews'])
                        else:
                            data = pd.DataFrame([raw_data])
                    print(f"Successfully loaded data with {len(data)} rows")
                    print(f"Columns in data: {data.columns.tolist()}")
                    return data
                except Exception as e2:
                    print(f"Error loading data as regular JSON: {str(e2)}")

    # Create sample data if loading fails
    print("Creating sample data for model training")
    data = pd.DataFrame({
        'reviewerID': ['u1', 'u2', 'u3', 'u4', 'u5'],
        'asin': ['p1', 'p2', 'p3', 'p4', 'p5'],
        'reviewText': [
            'This product is amazing!',
            'I really like this product',
            'Not worth the money',
            'Terrible experience with this item',
            'Works as expected, good value'
        ],
        'overall': [5, 4, 2, 1, 3],
        'reviewTime': ['2025-05-01', '2025-05-02', '2025-05-03', '2025-05-04', '2025-05-05']
    })

    return data

def train_and_save_model():
    """Train sentiment analysis model and save to multiple locations"""
    print("Starting model training...")

    # Load and prepare data
    data = load_data()

    # Map column names to standardized names
    column_mappings = {
        'text': 'review_text',
        'reviewText': 'review_text',
        'review': 'review_text',
        'content': 'review_text',
        'stars': 'rating',
        'overall': 'rating',
        'score': 'rating',
        'rating': 'rating'
    }

    # Rename columns based on mappings
    for original, standard in column_mappings.items():
        if original in data.columns and standard not in data.columns:
            data[standard] = data[original]
            print(f"Mapped column '{original}' to '{standard}'")

    # Ensure required columns exist
    if 'review_text' not in data.columns:
        print("Error: Could not find any suitable text column. Available columns:")
        print(data.columns)
        return None

    if 'rating' not in data.columns:
        print("Error: Could not find any suitable rating column. Available columns:")
        print(data.columns)
        return None

    # Make sure rating is numeric
    data['rating'] = pd.to_numeric(data['rating'], errors='coerce')

    # Remove any rows with missing values in key columns
    data = data.dropna(subset=['review_text', 'rating'])

    # Define sentiment based on rating (rating >= 4 is positive)
    data['sentiment'] = (data['rating'] >= 4).astype(int)

    print(f"Training model on {len(data)} reviews")
    print(f"Positive reviews: {sum(data['sentiment'])} ({sum(data['sentiment'])*100/len(data):.1f}%)")

    # Create a pipeline with preprocessing and classifier
    model = Pipeline([
        ('vectorizer', TfidfVectorizer(preprocessor=preprocess_text, max_features=5000)),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ])

    # Train the model
    print("Training model...")
    model.fit(data['review_text'], data['sentiment'])

    # Save the model to multiple locations to ensure it's accessible
    model_paths = [
        '../model/model.pkl',       # Relative path when run from ml_model directory
        '/app/model/model.pkl',     # Docker container path
        '/app/ml_model/model.pkl'   # Alternative Docker path
    ]

    # Create directories if they don't exist
    for path in model_paths:
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            try:
                os.makedirs(directory, exist_ok=True)
                print(f"Created directory: {directory}")
            except Exception as e:
                print(f"Error creating directory {directory}: {str(e)}")

    # Save model to all paths
    for path in model_paths:
        try:
            joblib.dump(model, path)
            print(f"Model saved to {path}")
        except Exception as e:
            print(f"Error saving model to {path}: {str(e)}")

    print("Model training and saving complete!")
    return model

if __name__ == "__main__":
    train_and_save_model()
