FROM debian:12-slim

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential=12.9 \
    cmake=3.25.1-1 \
    debhelper=13.11.4 \
    dpkg-dev=1.21.22 \
    pkg-config=1.8.1-1 \
    && rm -rf /var/lib/apt/lists/*

# Copy the library source and consumer
COPY app/ /app/

# Set environment
ENV DEBIAN_FRONTEND=noninteractive
