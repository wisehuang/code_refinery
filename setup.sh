#!/bin/bash

echo "Setting up Code Refinery project..."

# Setup backend
echo "Setting up backend..."
cd backend

# Check if uv is installed
if command -v uv &> /dev/null; then
    echo "Using uv for dependency management..."
    if [ -f pyproject.toml ]; then
        echo "Installing from pyproject.toml..."
        uv sync
    else
        echo "Installing from requirements.txt..."
        uv pip install -r requirements.txt
    fi
else
    echo "uv not found, using standard Python tools..."
    # Create virtual environment
    python3 -m venv venv
    source venv/bin/activate
    
    # Install dependencies
    pip install -r requirements.txt
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    cp env.example .env
    echo "Created .env file. Please edit it with your API keys:"
    echo "  OPENAI_API_KEY=your_openai_api_key_here"
    echo "  ANTHROPIC_API_KEY=your_anthropic_api_key_here"
    echo "  GOOGLE_API_KEY=your_google_api_key_here"
fi

cd ..

# Setup frontend
echo "Setting up frontend..."
cd frontend

# Install dependencies
npm install

cd ..

echo "Setup complete!"
echo ""
echo "To start the application:"
echo "1. Set your API keys in backend/.env"
if command -v uv &> /dev/null; then
    echo "2. In one terminal: cd backend && uv run uvicorn main:app --reload"
else
    echo "2. In one terminal: cd backend && source venv/bin/activate && uvicorn main:app --reload"
fi
echo "3. In another terminal: cd frontend && npm start"
echo ""
echo "The application will be available at:"
echo "- Frontend: http://localhost:3000"
echo "- Backend API: http://localhost:8000"
echo "- API Docs: http://localhost:8000/docs" 