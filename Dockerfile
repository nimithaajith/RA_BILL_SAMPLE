# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install system dependencies for Python packages
RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libopenblas-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

    

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY requirements2.txt .
RUN pip install --no-cache-dir -r requirements2.txt

# Copy the Django project code
COPY . .

# Expose port 8000 
EXPOSE 8000
EXPOSE 6379
EXPOSE 80
