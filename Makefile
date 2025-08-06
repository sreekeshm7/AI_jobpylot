# AI JobPylot - Development Makefile

.PHONY: help install test run clean docker-build docker-run docker-stop lint format

# Default target
help:
	@echo "AI JobPylot - Development Commands"
	@echo "=================================="
	@echo "install      - Install dependencies"
	@echo "test         - Run tests"
	@echo "run          - Run the application"
	@echo "clean        - Clean cache and temporary files"
	@echo "docker-build - Build Docker image"
	@echo "docker-run   - Run with Docker Compose"
	@echo "docker-stop  - Stop Docker containers"
	@echo "lint         - Run linting"
	@echo "format       - Format code"
	@echo "setup        - Complete setup (install + env setup)"

# Install dependencies
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

# Run tests
test:
	@echo "Running tests..."
	python -m pytest tests/ -v
	python test_hybrid_ats.py

# Run the application
run:
	@echo "Starting AI JobPylot..."
	python main.py

# Run with uvicorn (development)
dev:
	@echo "Starting development server..."
	uvicorn main:app --host 0.0.0.0 --port 8001 --reload

# Clean cache and temporary files
clean:
	@echo "Cleaning cache and temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf build/
	rm -rf dist/

# Docker commands
docker-build:
	@echo "Building Docker image..."
	docker build -t ai-jobpylot .

docker-run:
	@echo "Starting with Docker Compose..."
	docker-compose up -d

docker-stop:
	@echo "Stopping Docker containers..."
	docker-compose down

docker-logs:
	@echo "Showing Docker logs..."
	docker-compose logs -f

# Code quality
lint:
	@echo "Running linting..."
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

format:
	@echo "Formatting code..."
	black .
	isort .

# Complete setup
setup: install
	@echo "Setting up environment..."
	@if [ ! -f .env ]; then \
		echo "Creating .env file from template..."; \
		cp env.example .env; \
		echo "Please edit .env file with your OpenAI API key"; \
	else \
		echo ".env file already exists"; \
	fi
	@echo "Setup complete! Edit .env file with your OpenAI API key"

# Health check
health:
	@echo "Checking application health..."
	curl -f http://localhost:8001/health || echo "Application not running"

# API documentation
docs:
	@echo "Opening API documentation..."
	@if command -v xdg-open > /dev/null; then \
		xdg-open http://localhost:8001/docs; \
	elif command -v open > /dev/null; then \
		open http://localhost:8001/docs; \
	else \
		echo "API docs available at: http://localhost:8001/docs"; \
	fi

# Quick start
quickstart: setup run 