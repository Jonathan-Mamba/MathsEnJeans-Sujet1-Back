# Use lightweight Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY src/ ./src/

# Expose port (Railway assigns PORT env var, but default to 8000)
EXPOSE ${PORT:-8000}

# Health check (optional but recommended for Railway)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/', timeout=5)"

# Run the app - use PORT env variable for Railway compatibility
CMD ["sh", "-c", "python ./src"]
