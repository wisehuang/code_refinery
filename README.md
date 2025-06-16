# Code Refinery

AI-powered code refactoring service with modern frontend and backend architecture.

## 🚀 Features

- **Modern Frontend**: Next.js 15 with TypeScript and Tailwind CSS
- **Powerful Backend**: FastAPI with concurrent LLM processing
- **Advanced Code Editor**: Monaco Editor with syntax highlighting for 18+ languages
- **AI-Powered Refactoring**: Concurrent processing with OpenAI GPT-4, Anthropic Claude, and Google Gemini
- **Secure Authentication**: Token-based API authentication
- **Professional UI**: Clean, responsive design with error handling

## 🏗️ Architecture

### Frontend (Next.js 15)
- **Framework**: Next.js 15 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS 4
- **Code Editor**: Monaco Editor
- **State Management**: React hooks
- **Error Handling**: React Error Boundaries
- **Authentication**: Bearer token support

### Backend (FastAPI)
- **Framework**: FastAPI with Python 3.8+
- **LLM Integration**: OpenAI, Anthropic, Google Gemini APIs
- **Concurrent Processing**: asyncio for parallel LLM calls
- **Architecture**: Service layer pattern
- **Authentication**: Token-based security
- **Testing**: Comprehensive unit tests

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.8+ (with uv package manager preferred)
- Node.js 18+ 
- API Keys for OpenAI, Anthropic, and Google

### Quick Setup with Authentication

1. **Run the authentication setup script**
   ```bash
   python setup_auth.py
   ```
   This will guide you through setting up API tokens and authentication.

### Manual Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd code_refinery/backend
   ```

2. **Install dependencies**
   ```bash
   # Using uv (recommended, requires Python 3.12+)
   uv pip install -r requirements.txt
   # Or, to use the canonical pyproject.toml (recommended for development)
   uv pip install .
   # For editable/development install:
   uv pip install -e .
   
   # Or using pip (for compatibility)
   pip install -r requirements.txt
   ```
   > **Note:** `requirements.txt` is provided for compatibility, but `pyproject.toml` is the canonical source of dependencies.

3. **Set environment variables**
   ```bash
   # Copy example environment file
   cp env.example .env
   
   # Edit .env file with your values:
   # OPENAI_API_KEY=your_openai_api_key
   # ANTHROPIC_API_KEY=your_anthropic_api_key
   # GOOGLE_API_KEY=your_google_api_key
   # AUTH_ENABLED=true
   # API_TOKEN=your_secure_api_token
   ```

4. **Run the backend**
   ```bash
   # Using uv
   uv run uvicorn main:app --reload
   
   # Or using python
   python -m uvicorn main:app --reload
   ```

   Backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd ../frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure frontend authentication**
   ```bash
   # Create .env.local file
   echo "NEXT_PUBLIC_API_TOKEN=your_api_token_here" > .env.local
   ```

4. **Start development server**
   ```bash
   npm run dev
   ```

   Frontend will be available at `http://localhost:3000`

## 🔐 Authentication

The API uses Bearer token authentication to protect endpoints.

### Configuration Options

1. **Enabled with Token** (Recommended for production)
   ```bash
   AUTH_ENABLED=true
   API_TOKEN=sk-refinery-your-secure-token-here
   ```

2. **Disabled** (Development only)
   ```bash
   AUTH_ENABLED=false
   ```

### Authentication Status

The frontend displays real-time authentication status:
- 🔐 **Authenticated**: Token is valid and accepted
- ❌ **Failed**: Token is invalid or missing
- 🔓 **Not Required**: Authentication is disabled
- 🔄 **Checking**: Verifying authentication status

### Protected Endpoints

- `POST /refactor` - Code refactoring (requires authentication)
- `GET /supported-languages` - Language list (requires authentication)
- `GET /auth/status` - Authentication test (requires authentication)

### Public Endpoints

- `GET /` - API information (no authentication)
- `GET /health` - Health check (no authentication)

## 🧪 Testing

### Backend Tests
```bash
cd backend
# Using uv
uv run pytest tests/ -v

# Or using python
python -m pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📁 Project Structure

```
code_refinery/
├── backend/                 # FastAPI backend
│   ├── main.py             # FastAPI application entry point
│   ├── models.py           # Pydantic models
│   ├── auth.py             # Authentication module
│   ├── services/           # Business logic layer
│   │   ├── llm_service.py  # LLM API integrations
│   │   └── refactor_service.py # Refactoring orchestration
│   ├── tests/              # Backend tests
│   ├── .env.example        # Environment variables template
│   └── requirements.txt    # Python dependencies
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/           # Next.js app router
│   │   ├── components/    # React components
│   │   ├── services/      # API services
│   │   ├── types/         # TypeScript types
│   │   └── utils/         # Utility functions
│   ├── public/            # Static assets
│   └── package.json       # Node.js dependencies
├── setup_auth.py          # Authentication setup script
└── README.md              # This file
```

## 🎯 Supported Languages

- Python
- JavaScript/TypeScript
- Java
- C/C++
- C#
- Go
- Rust
- PHP
- Ruby
- Swift
- Kotlin
- Scala
- R
- SQL
- HTML/CSS

## 🔧 Configuration

### Environment Variables

**Backend:**
- `OPENAI_API_KEY`: OpenAI API key
- `ANTHROPIC_API_KEY`: Anthropic API key  
- `GOOGLE_API_KEY`: Google API key
- `AUTH_ENABLED`: Enable/disable authentication (true/false)
- `API_TOKEN`: Secret token for API authentication

**Frontend:**
- `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:8000)
- `NEXT_PUBLIC_API_TOKEN`: API token for authentication

## 🚀 Production Deployment

### Backend Deployment
```bash
# Set production environment variables
export AUTH_ENABLED=true
export API_TOKEN="your-production-secret-token"

# Build production image
cd backend
docker build -t code-refinery-backend .

# Or deploy to cloud platforms (Vercel, Railway, etc.)
```

### Frontend Deployment
```bash
# Set production environment variables
export NEXT_PUBLIC_API_TOKEN="your-production-secret-token"

# Build production version
cd frontend
npm run build
npm start

# Or deploy to Vercel/Netlify
npx vercel --prod
```

## 🔒 Security Notes

- **Never commit API tokens** to version control
- **Use strong, unique tokens** for production
- **Rotate tokens regularly** in production environments
- **Use HTTPS** in production deployments
- **Consider additional security measures** like rate limiting and IP restrictions for production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Monaco Editor](https://microsoft.github.io/monaco-editor/) for the code editing experience
- [Next.js](https://nextjs.org/) for the React framework
- [FastAPI](https://fastapi.tiangolo.com/) for the Python backend framework
- [Tailwind CSS](https://tailwindcss.com/) for the styling system 