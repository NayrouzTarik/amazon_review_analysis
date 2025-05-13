FROM confluentinc/cp-kafka:7.3.0

# Copy files to the correct location
COPY kafka/producer.py /app/
COPY kafka/kafka_config.json /etc/kafka/

WORKDIR /app
CMD ["python", "/app/producer.py"]