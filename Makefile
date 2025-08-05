# Makefile for SerialVisionUI
# Windows compatible makefile

.PHONY: help install install-dev test clean build run format lint

# Default target
help:
	@echo "Available commands:"
	@echo "  install     - Install dependencies"
	@echo "  install-dev - Install development dependencies"  
	@echo "  test        - Run tests"
	@echo "  clean       - Clean build artifacts"
	@echo "  build       - Build executable"
	@echo "  run         - Run the application"
	@echo "  format      - Format code with black"
	@echo "  lint        - Run linting with flake8"

# Install dependencies
install:
	pip install -r requirements.txt

# Install development dependencies
install-dev:
	pip install -r requirements.txt
	pip install -e .[dev]

# Run tests
test:
	python -m pytest tests/ -v

# Clean build artifacts
clean:
	if exist build rmdir /s /q build
	if exist dist rmdir /s /q dist
	if exist *.egg-info rmdir /s /q *.egg-info
	for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"

# Build executable with PyInstaller
build:
	pyinstaller main.spec

# Run the application
run:
	python app.py

# Format code with black (if available)
format:
	black src/ tests/ --line-length 88

# Run linting with flake8 (if available) 
lint:
	flake8 src/ tests/ --max-line-length=88
