# Cross-Modal Product Recommendation System - Makefile
# Windows PowerShell compatible commands

.PHONY: help install-backend install-frontend install start-backend start-frontend start stop clean

# Default target
help:
	@echo "Cross-Modal Product Recommendation System - Available Commands:"
	@echo ""
	@echo "Installation:"
	@echo "  make install              - Install both backend and frontend dependencies"
	@echo "  make install-backend      - Install Python backend dependencies"
	@echo "  make install-frontend     - Install Node.js frontend dependencies"
	@echo ""
	@echo "Running:"
	@echo "  make start                - Start both backend and frontend servers"
	@echo "  make start-backend        - Start FastAPI backend server"
	@echo "  make start-frontend       - Start Vite frontend server"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean                - Clean temporary files and caches"
	@echo ""

# Install all dependencies
install: install-backend install-frontend
	@echo "All dependencies installed successfully!"

# Install backend dependencies
install-backend:
	@echo "Installing Python backend dependencies..."
	@cd backend && python -m venv venv
	@cd backend && .\venv\Scripts\Activate.ps1 && pip install --upgrade pip
	@cd backend && .\venv\Scripts\Activate.ps1 && pip install -r requirements.txt
	@echo "Backend dependencies installed!"

# Install frontend dependencies
install-frontend:
	@echo "Installing frontend dependencies..."
	@cd frontend && npm install
	@echo "Frontend dependencies installed!"

# Start both servers
start:
	@echo "Starting Cross-Modal Product Recommendation System..."
	@echo "Backend will run on http://localhost:8000"
	@echo "Frontend will run on http://localhost:5173"
	@echo ""
	@echo "Starting backend server..."
	@start powershell -NoExit -Command "cd backend; .\venv\Scripts\Activate.ps1; python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
	@timeout /t 3 /nobreak >nul
	@echo "Starting frontend server..."
	@start powershell -NoExit -Command "cd frontend; npm run dev"
	@echo ""
	@echo "Both servers are starting in separate windows!"
	@echo "Access the application at http://localhost:5173"

# Start backend only
start-backend:
	@echo "Starting FastAPI backend server on http://localhost:8000..."
	@cd backend && .\venv\Scripts\Activate.ps1 && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Start frontend only
start-frontend:
	@echo "Starting Vite frontend server on http://localhost:5173..."
	@cd frontend && npm run dev

# Clean temporary files
clean:
	@echo "Cleaning temporary files and caches..."
	@if exist backend\__pycache__ rmdir /s /q backend\__pycache__
	@if exist backend\app\__pycache__ rmdir /s /q backend\app\__pycache__
	@if exist backend\app\api\__pycache__ rmdir /s /q backend\app\api\__pycache__
	@if exist backend\app\models\__pycache__ rmdir /s /q backend\app\models\__pycache__
	@if exist backend\app\utils\__pycache__ rmdir /s /q backend\app\utils\__pycache__
	@if exist frontend\node_modules\.vite rmdir /s /q frontend\node_modules\.vite
	@if exist frontend\dist rmdir /s /q frontend\dist
	@echo "Clean complete!"
