# Use a lightweight Python image
FROM python:3.12-slim

# Set environment variable to prevent bytecode and enable logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory in the container
WORKDIR /app

# Install system dependencies (add other later if needed, like tesseract/poppler)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/aot/lists/*

# Copy only requirements first for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of your code
COPY . .

# Default command - interactive shll (for dev container or override via compose)
CMD [ "bash" ]

# Install Git
ARG INSTALL_GIT=true
RUN if [ "$INSTALL_GIT" = "true" ]; then apt-get update && apt-get install -y git; fi
