# Haskellito Backend Dockerfile
# Provides Python + GHCi in a sandboxed environment with bubblewrap

FROM python:3.11-slim

# Install GHC and bubblewrap for sandboxing
RUN apt-get update && apt-get install -y --no-install-recommends \
    ghc \
    bubblewrap \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for GHCi processes
RUN useradd -m -s /bin/bash haskellito

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .

# Expose the API port
EXPOSE 8000

# Run as root so bubblewrap can create sandboxes
# GHCi processes will be sandboxed with minimal privileges
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
