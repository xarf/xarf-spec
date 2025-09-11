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
    
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    print_status $BLUE "🐧 Detected Linux"
    
    if command -v apt-get &> /dev/null; then
        print_status $BLUE "📦 Installing dependencies via apt..."
        sudo apt-get update
        sudo apt-get install -y jq python3
    elif command -v yum &> /dev/null; then
        print_status $BLUE "📦 Installing dependencies via yum..."
        sudo yum install -y jq python3
    else
        print_status $YELLOW "⚠️  Please install jq and python3 manually"
    fi
else
    print_status $YELLOW "⚠️  Unsupported OS. Please install jq and python3 manually"
fi

# Test validation
print_status $BLUE "🧪 Testing validation script..."
if "$ROOT_DIR/scripts/validate.sh"; then
    print_status $GREEN "✅ Validation test passed!"
else
    print_status $YELLOW "⚠️  Validation test failed - this is expected if there are validation errors"
fi

echo ""
print_status $GREEN "🎉 Setup complete!"
echo ""
echo "Available commands:"
echo "  ./scripts/validate.sh         - Validate all JSON files"
echo "  ./scripts/validate.sh format  - Format all JSON files"
echo ""
echo "For CI/CD, the GitHub Actions workflow will run validation automatically."