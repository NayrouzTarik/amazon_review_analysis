from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, IntegerType

spark = SparkSession.builder \
    .appName("AmazonReviewsStreaming") \
    .getOrCreate()

schema = StructType([
    StructField("reviewText", StringType(), True),
    StructField("overall", IntegerType(), True)
])

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "amazon_reviews") \
    .load()

reviews = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

def classify_sentiment(rating):
    if rating >= 4:
        return "positive"
    elif rating == 3:
        return "neutral"
    else:
        return "negative"

from pyspark.sql.functions import udf
classify_sentiment_udf = udf(classify_sentiment, StringType())

reviews = reviews.withColumn("sentiment", classify_sentiment_udf(col("overall")))

query = reviews.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
