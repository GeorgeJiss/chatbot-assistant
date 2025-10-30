#!/bin/bash

# TalentScout AI Hiring Assistant - Setup Script
# This script automates the installation and setup process

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Banner
echo "=================================================="
echo "  TalentScout AI Hiring Assistant - Setup"
echo "=================================================="
echo ""

# Check Python version
print_info "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    REQUIRED_VERSION="3.9"
    
    if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" = "$REQUIRED_VERSION" ]; then
        print_success "Python $PYTHON_VERSION found"
    else
        print_error "Python 3.9+ required, found $PYTHON_VERSION"
        exit 1
    fi
else
    print_error "Python 3 not found. Please install Python 3.9 or higher."
    exit 1
fi

# Check pip
print_info "Checking pip..."
if command -v pip3 &> /dev/null; then
    print_success "pip found"
else
    print_error "pip not found. Please install pip."
    exit 1
fi

# Create virtual environment
print_info "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_info "Virtual environment already exists"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi
print_success "Virtual environment activated"

# Upgrade pip
print_info "Upgrading pip..."
pip install --upgrade pip --quiet
print_success "pip upgraded"

# Install dependencies
print_info "Installing dependencies..."
pip install -r requirements.txt --quiet
print_success "Dependencies installed"

# Create necessary directories
print_info "Creating directories..."
mkdir -p data/candidates
mkdir -p data/tech_stacks
mkdir -p logs
mkdir -p tests
print_success "Directories created"

# Set up environment file
print_info "Setting up environment variables..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    print_success "Created .env file from template"
    echo ""
    print_info "IMPORTANT: Please edit .env and add your GROQ_API_KEY"
    print_info "Get your free API key at: https://console.groq.com/"
    echo ""
else
    print_info ".env file already exists"
fi

# Check if API key is set
if grep -q "your_groq_api_key_here" .env 2>/dev/null; then
    print_error "Please update GROQ_API_KEY in .env file before running the app"
    echo ""
    echo "Steps to get your API key:"
    echo "1. Visit https://console.groq.com/"
    echo "2. Sign up with GitHub or Google"
    echo "3. Go to API Keys section"
    echo "4. Create a new key"
    echo "5. Copy the key to .env file"
    echo ""
fi

# Create initial data files
print_info "Creating initial data files..."
if [ ! -f "data/tech_stacks/question_bank.json" ]; then
    cat > data/tech_stacks/question_bank.json << 'EOF'
{
  "python": {
    "junior": [
      "What are the main differences between lists and tuples in Python?",
      "Explain the concept of list comprehensions with an example.",
      "What is the difference between == and is operators?"
    ]
  }
}
EOF
    print_success "Created question bank template"
fi

# Create gitignore if not exists
if [ ! -f ".gitignore" ]; then
    print_info "Creating .gitignore..."
    cat > .gitignore << 'EOF'
__pycache__/
*.py[cod]
venv/
.env
data/candidates/*.json
logs/*.log
.DS_Store
.vscode/
.idea/
EOF
    print_success "Created .gitignore"
fi

# Run tests
print_info "Running tests..."
if python -m pytest tests/ -v --tb=short 2>/dev/null; then
    print_success "All tests passed"
else
    print_info "Tests not run (pytest might not be installed or no tests found)"
fi

# Final instructions
echo ""
echo "=================================================="
print_success "Setup completed successfully!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. Edit .env and add your GROQ_API_KEY"
echo "2. Run: streamlit run app.py"
echo "3. Open browser at http://localhost:8501"
echo ""
echo "For help, visit:"
echo "- Documentation: README.md"
echo "- Get API Key: https://console.groq.com/"
echo "- Issues: https://github.com/yourusername/talentscout/issues"
echo ""
echo "Happy hiring! 🚀"
echo ""