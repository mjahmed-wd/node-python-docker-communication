FROM python:3.9-slim

WORKDIR /app

# Install only runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    poppler-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create necessary directories
RUN mkdir -p file/converted_images

# Expose port
EXPOSE 5000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"] 