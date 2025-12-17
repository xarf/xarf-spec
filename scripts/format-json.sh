#!/bin/bash

# XARF JSON Formatting Script
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Check if required tools are available
check_dependencies() {
    print_status $BLUE "🔧 Checking dependencies..."
    
    local missing_tools=()
    
    if ! command -v jq &> /dev/null; then
        missing_tools+=("jq")
    fi
    
    if [ ${#missing_tools[@]} -ne 0 ]; then
        print_status $RED "❌ Missing required tools: ${missing_tools[*]}"
        echo "Please install:"
        echo "  macOS: brew install jq"
        echo "  Ubuntu: apt-get install jq"
        exit 1
    fi
    
    print_status $GREEN "✅ All dependencies available"
}

# Check JSON syntax (basic validation for formatting safety)
validate_json_syntax() {
    local file=$1
    if ! jq --exit-status . "$file" >/dev/null 2>&1; then
        print_status $RED "❌ Invalid JSON syntax: $file"
        return 1
    fi
    return 0
}

# Format JSON files
format_json() {
    print_status $BLUE "🎨 Formatting JSON files..."
    
    local formatted_count=0
    local error_count=0
    
    while IFS= read -r -d '' file; do
        # Skip files with invalid JSON syntax
        if ! validate_json_syntax "$file"; then
            ((error_count++))
            continue
        fi
        
        if jq --tab . "$file" > "${file}.tmp" 2>/dev/null; then
            if ! cmp -s "$file" "${file}.tmp"; then
                mv "${file}.tmp" "$file"
                print_status $GREEN "✅ Formatted: $file"
                ((formatted_count++))
            else
                rm "${file}.tmp"
            fi
        else
            rm -f "${file}.tmp"
            print_status $RED "❌ Failed to format: $file"
            ((error_count++))
        fi
    done < <(find "$ROOT_DIR" -name "*.json" -not -path "*/node_modules/*" -print0)
    
    echo ""
    if [ $error_count -gt 0 ]; then
        print_status $RED "❌ Failed to format $error_count file(s) due to syntax errors"
        print_status $YELLOW "💡 Run schema validation to see detailed error information"
        return 1
    elif [ $formatted_count -eq 0 ]; then
        print_status $GREEN "✅ All JSON files already properly formatted"
    else
        print_status $GREEN "✅ Formatted $formatted_count JSON files"
    fi
}

# Check if formatting is needed (without modifying files)
check_formatting() {
    print_status $BLUE "🔍 Checking JSON formatting..."
    
    local needs_formatting=0
    local error_count=0
    
    while IFS= read -r -d '' file; do
        # Skip files with invalid JSON syntax
        if ! validate_json_syntax "$file"; then
            ((error_count++))
            continue
        fi
        
        if jq --tab . "$file" > "${file}.tmp" 2>/dev/null; then
            if ! cmp -s "$file" "${file}.tmp"; then
                print_status $YELLOW "⚠️  Needs formatting: $file"
                ((needs_formatting++))
            fi
            rm "${file}.tmp"
        else
            rm -f "${file}.tmp"
            print_status $RED "❌ Failed to check: $file"
            ((error_count++))
        fi
    done < <(find "$ROOT_DIR" -name "*.json" -not -path "*/node_modules/*" -print0)
    
    echo ""
    if [ $error_count -gt 0 ]; then
        print_status $RED "❌ $error_count file(s) have syntax errors"
        return 1
    elif [ $needs_formatting -gt 0 ]; then
        print_status $RED "❌ $needs_formatting file(s) need formatting"
        print_status $YELLOW "💡 Run './scripts/format-json.sh format' to fix formatting"
        return 1
    else
        print_status $GREEN "✅ All JSON files are properly formatted"
        return 0
    fi
}

# Main function
main() {
    print_status $BLUE "🎨 XARF JSON Formatter"
    echo ""
    
    check_dependencies
    
    # Handle command line arguments
    case "${1:-check}" in
        "format")
            format_json
            ;;
        "check"|"")
            check_formatting
            ;;
        *)
            echo "Usage: $0 [check|format]"
            echo ""
            echo "Commands:"
            echo "  check   - Check if JSON files need formatting (default)"
            echo "  format  - Format all JSON files"
            exit 1
            ;;
    esac
}

main "$@"