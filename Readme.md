## How to Run

### 1. **Build and Start All Services**

From the project root, run:

```bash
docker-compose up --build -d #run in bkg
```

This will start:
- Zookeeper
- Kafka
- Spark (or Python consumer)
- MongoDB
- Web app

---

### 2. **Send Reviews to Kafka**

Open a new terminal and run the producer:

```bash
docker-compose exec kafka bash
cd /app/kafka
python producer.py
```

This will send reviews to the `amazon_reviews` Kafka topic.

---

### 3. **Check the Consumer**

- **Spark consumer:** Logs will appear in the Spark container.
- **Python consumer:** You can run it with:

  ```bash
  docker-compose exec kafka bash
  cd /app/kafka
  python consumer.py
  ```

  You should see output for each review received and its sentiment.

---

### 4. **View the Dashboard**

Open your browser and go to:

```
http://localhost:5000
```

You should see the Amazon Reviews Dashboard update as reviews are processed.

---

### 5. **Check MongoDB (Optional)**

To inspect stored reviews:

```bash
docker-compose exec mongodb mongosh -u admin -p password --authenticationDatabase reviews_db
use reviews_db
db.<your_collection>.find().pretty()
 #hanaa this is not working 
```

Replace `<your_collection>` with your actual collection name.

---

## Stopping the App

Press `Ctrl+C` in the terminal running Docker Compose, or run:

```bash
docker-compose down
```

---

## Customization

- Edit `kafka/producer.py` to change the data source.
- Edit `kafka/consumer.py` or `spark/spark_streaming.py` for custom processing.
- Edit `web_app/` for dashboard changes.

---

**Enjoy streaming and analyzing Amazon reviews!**