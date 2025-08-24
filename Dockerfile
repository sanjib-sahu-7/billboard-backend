# Use official Python image
FROM python:3.10-slim

# Install dependencies for Tesseract
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy project files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose Flask port
EXPOSE 5000

# Start app
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]

