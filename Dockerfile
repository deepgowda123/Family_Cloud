# Use a lightweight Python base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies (for SQLite and other libs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential sqlite3 && \
    rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=5000

# Expose port
EXPOSE 5000

# Command to run the app
CMD ["python", "app.py"]
