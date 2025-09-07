FROM python:3.10-slim

# Increase timeout for large wheels like torch
ENV PIP_DEFAULT_TIMEOUT=1000

# Set working directory
WORKDIR /app

# Install system packages (needed for PyTorch & scientific libs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libopenblas-dev \
    libssl-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------
# Preinstall PyTorch (CPU version here)
# ------------------------------------------------------
RUN pip install --no-cache-dir --upgrade typing-extensions
RUN pip install --no-cache-dir torch==2.8.0 --index-url https://download.pytorch.org/whl/cpu

# Copy requirements first (for caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose Streamlit's default port
EXPOSE 8502

# Start the Streamlit app
CMD ["streamlit", "run", "app.py", \
     "--server.enableCORS", "false", \
     "--server.enableXsrfProtection", "false", \
     "--server.headless", "true", \
     "--server.port", "8502", \
     "--server.address", "0.0.0.0"]
