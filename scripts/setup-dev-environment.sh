#!/bin/bash
# Development Environment Setup Script for Ledgerly
# =================================================

set -e

echo "🚀 Setting up Ledgerly development environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check prerequisites
echo "📋 Checking prerequisites..."

command -v docker >/dev/null 2>&1 || {
    print_error "Docker is required but not installed. Please install Docker Desktop."
    exit 1
}
print_status "Docker is installed"

command -v docker-compose >/dev/null 2>&1 || command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1 || {
    print_error "Docker Compose is required but not installed."
    exit 1
}
print_status "Docker Compose is available"

# Verify we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    print_error "Please run this script from the project root directory (where docker-compose.yml is located)"
    exit 1
fi

# Stop any running containers
echo "🛑 Stopping any existing containers..."
docker compose down 2>/dev/null || true

# Build images
echo "🏗️  Building Docker images..."
docker compose build

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs
mkdir -p output

# Start services
echo "🎯 Starting development services..."
docker compose up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service health
echo "🔍 Checking service health..."

services=("postgres" "minio" "redis")
for service in "${services[@]}"; do
    if docker compose ps "$service" | grep -q "healthy\|running"; then
        print_status "$service is ready"
    else
        print_warning "$service may still be starting up"
    fi
done

# Display access information
echo ""
echo "🎉 Development environment is ready!"
echo ""
echo "📊 Service URLs:"
echo "   • Frontend:  http://localhost:3000"
echo "   • Backend:   http://localhost:8000"
echo "   • API Docs:  http://localhost:8000/docs"
echo "   • MinIO:     http://localhost:9001 (admin/admin)"
echo "   • Database:  localhost:5432"
echo "   • Redis:     localhost:6379"
echo ""
echo "🔧 Useful commands:"
echo "   • View logs:        docker compose logs -f"
echo "   • Stop services:    docker compose down"
echo "   • Restart:          docker compose restart"
echo "   • Shell to backend: docker compose exec backend bash"
echo "   • Shell to DB:      docker compose exec postgres psql -U postgres -d ledgerly"
echo ""
echo "📝 Next steps:"
echo "   1. Visit http://localhost:3000 to see the frontend"
echo "   2. Visit http://localhost:8000/docs to see the API documentation"
echo "   3. Upload a Citi credit card statement to test the system"
echo ""

# Run basic connectivity tests
echo "🧪 Running basic connectivity tests..."

# Test backend health endpoint
if curl -f -s http://localhost:8000/health >/dev/null 2>&1; then
    print_status "Backend health check passed"
else
    print_warning "Backend health check failed - service may still be starting"
fi

# Test frontend
if curl -f -s http://localhost:3000 >/dev/null 2>&1; then
    print_status "Frontend accessibility check passed"
else
    print_warning "Frontend accessibility check failed - service may still be starting"
fi

# Test MinIO
if curl -f -s http://localhost:9000/minio/health/live >/dev/null 2>&1; then
    print_status "MinIO health check passed"
else
    print_warning "MinIO health check failed - service may still be starting"
fi

echo ""
print_status "Setup complete! Happy coding! 🚀"
