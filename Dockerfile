# Use official Python image, slim version for smaller size
FROM python:3.9-slim

# Set working directory in container to /app
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code
COPY . .

# Create a non-root user for security
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser:appuser /app
USER appuser

# Create volume for DB and logs persistence
VOLUME ["/app/data"]

# Expose ports 8501 for Streamlit + 8000 for Prometheus
EXPOSE 8501 8000

# Command to start the app (Prometheus starts automatically in app)
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]
