FROM python:3.11-slim

# Install system dependencies
# Playwright needs these system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers (Chromium only to save space/time, unless others needed)
RUN playwright install --with-deps chromium

# Copy application code
COPY src/ src/
COPY main.py .

# Environment setup
ENV PYTHONUNBUFFERED=1

# Command to run the application
# Note: For Render, this is overridden by render.yaml usually, but good default.
CMD ["python", "src/main.py"]
