#!/bin/bash

# XARF Development Setup Script
# Sets up local development environment without Node.js dependencies

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

print_status $BLUE "🚀 Setting up XARF development environment..."
echo ""

# Check operating system
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    print_status $BLUE "🍎 Detected macOS"
    
    if ! command -v brew &> /dev/null; then
        print_status $YELLOW "⚠️  Homebrew not found. Please install it first:"
        echo "  /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        exit 1
    fi
    
    print_status $BLUE "📦 Installing dependencies via Homebrew..."
    brew install jq python3
    
    print_status $BLUE "🐍 Installing Python packages..."
    python3 -m pip install --user jsonschema
    
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    print_status $BLUE "🐧 Detected Linux"
    
    if command -v apt-get &> /dev/null; then
        print_status $BLUE "📦 Installing dependencies via apt..."
        sudo apt-get update
        sudo apt-get install -y jq python3 python3-pip
        
        print_status $BLUE "🐍 Installing Python packages..."
        python3 -m pip install --user jsonschema
    elif command -v yum &> /dev/null; then
        print_status $BLUE "📦 Installing dependencies via yum..."
        sudo yum install -y jq python3 python3-pip
        
        print_status $BLUE "🐍 Installing Python packages..."
        python3 -m pip install --user jsonschema
    else
        print_status $YELLOW "⚠️  Please install jq, python3, and 'pip install jsonschema' manually"
    fi
else
    print_status $YELLOW "⚠️  Unsupported OS. Please install jq, python3, and 'pip install jsonschema' manually"
fi

# Test validation
print_status $BLUE "🧪 Testing validation scripts..."
echo "Testing JSON formatting..."
if "$ROOT_DIR/scripts/format-json.sh" check; then
    print_status $GREEN "✅ JSON formatting test passed!"
else
    print_status $YELLOW "⚠️  JSON formatting test failed"
fi

echo "Testing schema validation..."
if python3 "$ROOT_DIR/scripts/validate-schemas.py" > /dev/null; then
    print_status $GREEN "✅ Schema validation test passed!"
else
    print_status $YELLOW "⚠️  Schema validation test failed - check for schema errors"
fi

echo ""
print_status $GREEN "🎉 Setup complete!"
echo ""
echo "Available commands:"
echo "  ./scripts/format-json.sh check       - Check JSON formatting"
echo "  ./scripts/format-json.sh format      - Format all JSON files"
echo "  python3 scripts/validate-schemas.py  - Validate samples against schemas"
echo ""
echo "For CI/CD, the GitHub Actions workflow will run validation automatically."
