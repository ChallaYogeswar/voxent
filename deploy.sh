#!/bin/bash

# VOXENT Production Deployment Script

set -e

echo "🚀 Starting VOXENT deployment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install docker-compose first."
    exit 1
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data/input_calls
mkdir -p data/voice_dataset
mkdir -p logs
mkdir -p config

# Build and start services
echo "🐳 Building and starting services..."
docker-compose up --build -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
sleep 30

# Check service health
echo "🔍 Checking service health..."
if curl -f http://localhost:5000/status > /dev/null 2>&1; then
    echo "✅ VOXENT is running successfully!"
    echo "🌐 Web interface: http://localhost:5000"
    echo "📊 Status endpoint: http://localhost:5000/status"
else
    echo "❌ Service health check failed. Check logs with: docker-compose logs"
    exit 1
fi

echo "🎉 Deployment completed successfully!"
