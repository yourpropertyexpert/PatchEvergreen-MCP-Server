FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV HOST=0.0.0.0

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
# Install pydantic first with specific version to avoid fastmcp compatibility issues
RUN pip3 install --no-cache-dir "pydantic==2.9.2" && \
    pip3 install --no-cache-dir -r requirements.txt && \
    pip3 install --no-cache-dir --upgrade asgiref

# Copy application files
COPY mcp_server_sse.py .
COPY SKILL.md .
COPY mcp_server.py .

# Expose port 8000
EXPOSE 8000d

# Health check - verify the server is responding
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python3 -c "import requests; requests.get('http://localhost:8000/.well-known/skills', timeout=5)" || exit 1

# Run the SSE server
CMD ["python3", "mcp_server_sse.py"]
