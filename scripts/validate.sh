#!/bin/bash

# XARF Validation Script - No Node.js dependencies required
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
    
    if ! command -v python3 &> /dev/null; then
        missing_tools+=("python3")
    fi
    
    if [ ${#missing_tools[@]} -ne 0 ]; then
        print_status $RED "❌ Missing required tools: ${missing_tools[*]}"
        echo "Please install:"
        echo "  macOS: brew install jq python3"
        echo "  Ubuntu: apt-get install jq python3"
        exit 1
    fi
    
    print_status $GREEN "✅ All dependencies available"
}

# Validate JSON syntax
validate_json_syntax() {
    local file=$1
    if ! jq --exit-status . "$file" >/dev/null 2>&1; then
        print_status $RED "❌ Invalid JSON syntax: $file"
        return 1
    fi
    return 0
}

# Validate JSON files in directory
validate_directory() {
    local dir=$1
    local description=$2
    local error_count=0
    
    print_status $BLUE "🔍 Validating $description..."
    
    while IFS= read -r -d '' file; do
        if ! validate_json_syntax "$file"; then
            ((error_count++))
        fi
    done < <(find "$dir" -name "*.json" -print0)
    
    if [ $error_count -eq 0 ]; then
        print_status $GREEN "✅ All $description files are valid JSON"
    else
        print_status $RED "❌ Found $error_count invalid JSON files in $description"
        return 1
    fi
    
    return 0
}

# Basic schema validation (checks required fields exist)
validate_schema_structure() {
    local file=$1
    
    # Check if it's a JSON Schema
    if jq -e '.["$schema"]' "$file" >/dev/null 2>&1; then
        # Check required JSON Schema fields
        if ! jq -e '.["$id"]' "$file" >/dev/null 2>&1; then
            print_status $YELLOW "⚠️  Schema missing \$id: $file"
        fi
        if ! jq -e '.title' "$file" >/dev/null 2>&1; then
            print_status $YELLOW "⚠️  Schema missing title: $file"
        fi
        if ! jq -e '.description' "$file" >/dev/null 2>&1; then
            print_status $YELLOW "⚠️  Schema missing description: $file"
        fi
    fi
    
    return 0
}

# Check sample has required XARF fields
validate_sample_structure() {
    local file=$1
    local error_count=0
    
    # Required XARF fields
    local required_fields=("xarf_version" "report_id" "timestamp" "reporter" "source_identifier" "class" "type")
    
    for field in "${required_fields[@]}"; do
        if ! jq -e ".$field" "$file" >/dev/null 2>&1; then
            print_status $RED "❌ Sample missing required field '$field': $file"
            ((error_count++))
        fi
    done
    
    return $error_count
}

# Format JSON files
format_json() {
    print_status $BLUE "🎨 Formatting JSON files..."
    
    local formatted_count=0
    
    while IFS= read -r -d '' file; do
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
        fi
    done < <(find "$ROOT_DIR" -name "*.json" -not -path "*/node_modules/*" -print0)
    
    if [ $formatted_count -eq 0 ]; then
        print_status $GREEN "✅ All JSON files already properly formatted"
    else
        print_status $GREEN "✅ Formatted $formatted_count JSON files"
    fi
}

# Main validation function
main() {
    print_status $BLUE "🚀 XARF Validation Suite"
    echo ""
    
    check_dependencies
    
    local validation_errors=0
    
    # Validate schemas
    if ! validate_directory "$ROOT_DIR/schemas" "schema"; then
        ((validation_errors++))
    fi
    
    # Validate samples
    if ! validate_directory "$ROOT_DIR/samples" "sample"; then
        ((validation_errors++))
    fi
    
    # Additional schema structure checks
    print_status $BLUE "🔍 Checking schema structure..."
    while IFS= read -r -d '' file; do
        validate_schema_structure "$file"
    done < <(find "$ROOT_DIR/schemas" -name "*.json" -print0)
    
    # Additional sample structure checks
    print_status $BLUE "🔍 Checking sample structure..."
    local sample_errors=0
    while IFS= read -r -d '' file; do
        validate_sample_structure "$file"
        sample_errors=$((sample_errors + $?))
    done < <(find "$ROOT_DIR/samples/v4" -name "*.json" -print0)
    
    if [ $sample_errors -gt 0 ]; then
        ((validation_errors++))
    fi
    
    # Handle command line arguments
    case "${1:-validate}" in
        "format")
            format_json
            ;;
        "validate"|"")
            # Already done above
            ;;
        *)
            echo "Usage: $0 [validate|format]"
            exit 1
            ;;
    esac
    
    echo ""
    if [ $validation_errors -eq 0 ]; then
        print_status $GREEN "🎉 All validations passed!"
        exit 0
    else
        print_status $RED "❌ Validation failed with $validation_errors error(s)"
        exit 1
    fi
}

main "$@"