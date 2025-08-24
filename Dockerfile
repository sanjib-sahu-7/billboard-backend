FROM python:3.10-slim

# Install dependencies for Tesseract and OpenCV
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Verify tesseract is installed correctly (build-time debug)
RUN tesseract --version

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose Flask port
EXPOSE 5000

# Start app with gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "--timeout", "300", "--log-level", "debug", "app:app"]
