from kafka import KafkaProducer
import json
import time
import os

# Create Kafka producer
# Use localhost:29092 when running from host machine
producer = KafkaProducer(
    bootstrap_servers=['localhost:29092'],  # For running on host machine
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Adjust path for running from kafka directory
data_path = "/app/data/Data.json"
if not os.path.exists(data_path):
    # Try alternative path
    data_path = '../data/data.json'
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Could not find data file at {data_path}")

print(f"Loading data from {data_path}")

# Load data from JSON file
with open(data_path, 'r') as f:
    reviews = json.load(f)

# Topic name
topic_name = 'amazon_reviews'
print(f"Sending data to topic: {topic_name}")

# Send each review to Kafka topic
count = 0
for review in reviews:
    # Add sentiment label if not already present
    if 'sentiment' not in review:
        if 'overall' in review:
            review['sentiment'] = (
                "positive" if review['overall'] > 3
                else "neutral" if review['overall'] == 3
                else "negative"
            )
        else:
            review['sentiment'] = "neutral"  # Default
    
    # Send to Kafka
    producer.send(topic_name, value=review)
    
    # Print progress
    count += 1
    if count % 10 == 0:
        print(f"Sent {count} reviews so far...")
    
    # Small delay to avoid flooding
    time.sleep(0.1)

# Make sure all messages are sent
producer.flush()
print(f"All {count} reviews sent to Kafka topic '{topic_name}'")