FROM python:3.11-slim

LABEL maintainer="Imposter-zx"
LABEL description="AegisScan Strategic v4.0 - Mission-Aware Adversarial Simulation Framework"
LABEL version="4.0.0"

WORKDIR /opt/aegisscan

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    nmap \
    tshark \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -e .

# Create non-root user
RUN useradd -m -u 1000 aegisscan && \
    chown -R aegisscan:aegisscan /opt/aegisscan

USER aegisscan

# Expose API port
EXPOSE 5000

# Default command (can be overridden)
CMD ["python", "main.py", "--help"]