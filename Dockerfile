# Use lightweight Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY src/ ./src/

# Health check (optional but recommended for Railway)


# Run the app
CMD ["sh", "-c", "cd /app && python -m src"]
