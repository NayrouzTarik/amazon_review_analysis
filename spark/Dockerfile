# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install Java and required packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    default-jdk \
    wget \
    procps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV SPARK_VERSION=3.4.0
ENV HADOOP_VERSION=3
ENV SPARK_HOME=/opt/spark
ENV PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH
ENV PATH=$SPARK_HOME/bin:$PATH

# Download and install Spark
RUN wget -q https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    tar -xzf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /opt/spark && \
    rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

# Create app directories
RUN mkdir -p /app/spark /app/ml_model /app/model /app/data

# Install Python dependencies for both Spark and ML model
RUN pip install --no-cache-dir \
    pyspark==${SPARK_VERSION} \
    findspark \
    nltk \
    pandas==1.5.3 \
    numpy==1.23.5 \
    scikit-learn==1.2.2 \
    matplotlib \
    seaborn \
    joblib \
    pytest

# Copy requirements and install dependencies
COPY ./spark/requirements.txt /app/spark/
RUN pip install --no-cache-dir -r /app/spark/requirements.txt

# Copy ML model requirements and install if exists
COPY ./ml_model/requirements.txt /app/ml_model/
RUN if [ -f "/app/ml_model/requirements.txt" ]; then pip install --no-cache-dir -r /app/ml_model/requirements.txt; fi

# Set working directory
WORKDIR /app

# Copy Spark streaming script
COPY ./spark/spark_streaming.py /app/spark/

# Copy ML model files
COPY ./ml_model/ /app/ml_model/

# Copy model if exists
COPY ./model/ /app/model/

# Create improved entrypoint script
RUN echo '#!/bin/bash\n\
echo "Checking for model file..."\n\
MODEL_PATH="/app/model/model.pkl"\n\
\n\
if [ -f "$MODEL_PATH" ]; then\n\
    echo "Model file exists at $MODEL_PATH"\n\
else\n\
    echo "Model file NOT found at $MODEL_PATH"\n\
    echo "Available files in /app/model:"\n\
    mkdir -p /app/model\n\
    ls -la /app/model/\n\
    echo "Available files in /app/ml_model:"\n\
    ls -la /app/ml_model/\n\
    echo "Attempting to train model..."\n\
    if [ -f "/app/ml_model/train_model.py" ]; then\n\
        cd /app/ml_model && python train_model.py\n\
        if [ $? -ne 0 ]; then\n\
            echo "Error: Model training failed"\n\
        else\n\
            echo "Model training completed"\n\
        fi\n\
    else\n\
        echo "Training script not found!"\n\
    fi\n\
fi\n\
\n\
echo "Starting Spark streaming application..."\n\
cd /app/spark\n\
python -m spark_streaming\n\
' > /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

# Define entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
