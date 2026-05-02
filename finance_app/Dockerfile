# Use a slim Python 3.11 base image
FROM python:3.11-slim

# Set environment variables to prevent Python from writing .pyc files and to unbuffer output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for libraries like lxml and general build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the ports for FastAPI (8000) and Streamlit (8501)
EXPOSE 8000
EXPOSE 8501

# Use a shell script or a combined command to run both services. 
# Note: In a production environment, it is often better to run these in separate containers using Docker Compose.
# For a single-container deployment (like on some PaaS providers), this method works:
CMD ["sh", "-c", "uvicorn api.routes:app --host 0.0.0.0 --port 8000 & streamlit run app.py --server.port 8501 --server.address 0.0.0.0"]
