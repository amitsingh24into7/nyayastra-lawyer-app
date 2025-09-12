# ===============================
# Stage 1: Build stage
# ===============================
FROM python:3.10-slim AS build

# Set working directory
WORKDIR /app

# Increase timeout for large wheels like PyTorch
ENV PIP_DEFAULT_TIMEOUT=1000

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libopenblas-dev \
    libssl-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements for caching
COPY requirements.txt .

# Install Python dependencies including PyTorch
RUN pip install --no-cache-dir --upgrade typing-extensions && \
    pip install --no-cache-dir torch==2.8.0 --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt
RUN pip install streamlit-option-menu==0.3.6    

# Copy app code
COPY . .

# ===============================
# Stage 2: Runtime stage
# ===============================
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy installed packages from build stage
COPY --from=build /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=build /usr/local/bin /usr/local/bin

# Copy app code
COPY --from=build /app /app

# Expose Streamlit port
EXPOSE 8502

# Start Streamlit app
CMD ["streamlit", "run", "app.py", \
     "--server.enableCORS=false", \
     "--server.enableXsrfProtection=false", \
     "--server.headless=true", \
     "--server.port=8502", \
     "--server.address=0.0.0.0"]