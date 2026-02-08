# Haskellito Backend Dockerfile
# Provides Python + GHCi in a sandboxed environment

FROM python:3.11-slim

# Install GHC (provides GHCi)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ghc \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for running the application
RUN useradd -m -s /bin/bash haskellito

# Set working directory
WORKDIR /app

# Copy requirements first for better caching (build context = repo root)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire backend
COPY backend .

# Switch to non-root user
USER haskellito

# Expose the API port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
