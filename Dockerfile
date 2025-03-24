FROM python:3.11-slim

WORKDIR /app

# Copy dependencies file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/

# Expose port
EXPOSE 80

# Start command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]