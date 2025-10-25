#!/bin/bash

# WhatsApp Messaging Utility - Quick Deployment Script
# This script helps you deploy to different platforms

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    if ! command_exists python3; then
        print_error "Python 3 is not installed"
        exit 1
    fi
    
    if ! command_exists pip; then
        print_error "pip is not installed"
        exit 1
    fi
    
    print_success "Prerequisites check passed"
}

# Function to setup environment
setup_environment() {
    print_status "Setting up environment..."
    
    # Copy environment file if it doesn't exist
    if [ ! -f "backend/.env" ]; then
        if [ -f "backend/.env.example" ]; then
            cp backend/.env.example backend/.env
            print_warning "Created .env file from .env.example"
            print_warning "Please edit backend/.env with your actual credentials"
        else
            print_error ".env.example file not found"
            exit 1
        fi
    fi
    
    print_success "Environment setup completed"
}

# Function to install dependencies
install_dependencies() {
    print_status "Installing dependencies..."
    
    cd backend
    pip install -r requirements.txt
    cd ..
    
    print_success "Dependencies installed"
}

# Function to run tests
run_tests() {
    print_status "Running tests..."
    
    cd backend
    if [ -d "tests" ]; then
        python -m pytest tests/ -v
    else
        print_warning "No tests found, skipping..."
    fi
    cd ..
    
    print_success "Tests completed"
}

# Function to deploy with Docker
deploy_docker() {
    print_status "Deploying with Docker..."
    
    if ! command_exists docker; then
        print_error "Docker is not installed"
        exit 1
    fi
    
    if ! command_exists docker-compose; then
        print_error "Docker Compose is not installed"
        exit 1
    fi
    
    # Build and start services
    docker-compose up -d --build
    
    print_success "Docker deployment completed"
    print_status "Your API should be available at http://localhost:8000"
}

# Function to deploy to Railway
deploy_railway() {
    print_status "Deploying to Railway..."
    
    if ! command_exists railway; then
        print_error "Railway CLI is not installed"
        print_status "Install it with: npm install -g @railway/cli"
        exit 1
    fi
    
    cd backend
    railway login
    railway init
    railway up
    cd ..
    
    print_success "Railway deployment completed"
}

# Function to deploy to Heroku
deploy_heroku() {
    print_status "Deploying to Heroku..."
    
    if ! command_exists heroku; then
        print_error "Heroku CLI is not installed"
        print_status "Install it from: https://devcenter.heroku.com/articles/heroku-cli"
        exit 1
    fi
    
    cd backend
    heroku create your-whatsapp-api
    git init
    git add .
    git commit -m "Initial commit"
    git push heroku main
    cd ..
    
    print_success "Heroku deployment completed"
}

# Function to deploy to Google Cloud
deploy_gcloud() {
    print_status "Deploying to Google Cloud..."
    
    if ! command_exists gcloud; then
        print_error "Google Cloud SDK is not installed"
        print_status "Install it from: https://cloud.google.com/sdk/docs/install"
        exit 1
    fi
    
    cd backend
    gcloud app deploy
    cd ..
    
    print_success "Google Cloud deployment completed"
}

# Function to show help
show_help() {
    echo "WhatsApp Messaging Utility - Deployment Script"
    echo ""
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  docker      Deploy using Docker Compose"
    echo "  railway     Deploy to Railway"
    echo "  heroku      Deploy to Heroku"
    echo "  gcloud      Deploy to Google Cloud Platform"
    echo "  setup       Setup environment and install dependencies"
    echo "  test        Run tests"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 setup    # Setup environment and install dependencies"
    echo "  $0 docker   # Deploy with Docker"
    echo "  $0 railway  # Deploy to Railway"
}

# Main script logic
main() {
    case "${1:-help}" in
        "docker")
            check_prerequisites
            setup_environment
            install_dependencies
            run_tests
            deploy_docker
            ;;
        "railway")
            check_prerequisites
            setup_environment
            install_dependencies
            run_tests
            deploy_railway
            ;;
        "heroku")
            check_prerequisites
            setup_environment
            install_dependencies
            run_tests
            deploy_heroku
            ;;
        "gcloud")
            check_prerequisites
            setup_environment
            install_dependencies
            run_tests
            deploy_gcloud
            ;;
        "setup")
            check_prerequisites
            setup_environment
            install_dependencies
            print_success "Setup completed!"
            print_status "Next steps:"
            print_status "1. Edit backend/.env with your credentials"
            print_status "2. Run: $0 test"
            print_status "3. Run: $0 docker (or your preferred deployment method)"
            ;;
        "test")
            check_prerequisites
            run_tests
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

# Run main function with all arguments
main "$@"