from kafka import KafkaConsumer
import json
from textblob import TextBlob

def analyze_sentiment(review_text):
    """Analyze sentiment using TextBlob."""
    blob = TextBlob(review_text)
    return blob.sentiment.polarity  # Range: -1 (negative) to 1 (positive)

def update_sentiment_statistics(sentiment_label):
    """Update sentiment statistics (customize as needed)."""
    print(f"Updated Sentiment: {sentiment_label}")

def process_review(review):
    """Process a single review message."""
    reviewer = review.get('reviewerName', 'Unknown')
    text = review.get('reviewText', '')
    print(f"Received review from {reviewer}:\n{text}\n")

    sentiment_score = analyze_sentiment(text)
    print(f"Sentiment score for this review: {sentiment_score}")

    if sentiment_score > 0.1:
        sentiment_label = "Positive"
    elif sentiment_score < -0.1:
        sentiment_label = "Negative"
    else:
        sentiment_label = "Neutral"

    print(f"Sentiment Label: {sentiment_label}")
    update_sentiment_statistics(sentiment_label)

def main():
    consumer = KafkaConsumer(
        'amazon_reviews',
        bootstrap_servers=['kafka:9092'],
        auto_offset_reset='earliest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    print("Kafka consumer started. Waiting for messages...")
    for message in consumer:
        review = message.value
        print("DEBUG: Raw review message:", review)
        if isinstance(review, dict):
            process_review(review)
        else:
            print("Warning: Received message is not a dictionary.")

if __name__ == "__main__":
    main()