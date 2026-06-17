#!/usr/bin/env python3
"""
XARF Schema Validation Script

This script validates all XARF sample files against their corresponding JSON schemas.
It uses the master schema which automatically routes to the correct type-specific schema
based on the category and type fields in each sample.
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Tuple, Any

try:
    import jsonschema
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:
    print("❌ Error: jsonschema library not installed")
    print("Install with: pip install jsonschema")
    sys.exit(1)

# Colors for output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'  # No Color

def print_status(color: str, message: str) -> None:
    """Print colored output"""
    print(f"{color}{message}{Colors.NC}")

def load_json_file(file_path: Path) -> Tuple[Dict[str, Any], str]:
    """Load and parse a JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f), ""
    except json.JSONDecodeError as e:
        return {}, f"Invalid JSON: {e}"
    except Exception as e:
        return {}, f"Error reading file: {e}"

def resolve_schema_refs(schema: Dict[str, Any], schema_dir: Path) -> Dict[str, Any]:
    """Resolve $ref references in schema to create a complete schema"""
    # Cache for referenced schemas to avoid reloading the same files multiple times
    # (e.g., xarf-core.json is referenced by 20+ type schemas)
    schema_cache: Dict[Path, Dict[str, Any]] = {}
    
    def resolve_ref(obj: Any, current_dir: Path) -> Any:
        if isinstance(obj, dict):
            if '$ref' in obj:
                ref_path = obj['$ref']
                if not ref_path.startswith('http') and not ref_path.startswith('#'):  # Local file reference (not internal JSON Schema reference)
                    ref_file = current_dir / ref_path
                    if ref_file in schema_cache:
                        return resolve_ref(schema_cache[ref_file], current_dir)
                    elif ref_file.exists():
                        ref_schema, error = load_json_file(ref_file)
                        if error:
                            raise ValueError(f"Failed to load schema reference '{ref_path}': {error}")
                        schema_cache[ref_file] = ref_schema
                        return resolve_ref(ref_schema, ref_file.parent)
                    else:
                        raise FileNotFoundError(f"Schema reference not found: {ref_path} (resolved to {ref_file})")
                return obj
            else:
                return {k: resolve_ref(v, current_dir) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [resolve_ref(item, current_dir) for item in obj]
        return obj
    
    return resolve_ref(schema, schema_dir)

def validate_sample_against_schema(sample_data: Dict[str, Any], resolved_schema: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate a sample against a resolved schema"""
    try:
        # Enable format validation (including UUID validation)
        validator = Draft202012Validator(resolved_schema, format_checker=FormatChecker())
    except jsonschema.SchemaError as e:
        return False, [f"Invalid schema: {e}"]
    except Exception as e:
        return False, [f"Schema validator creation failed: {e}"]
    
    try:
        errors = list(validator.iter_errors(sample_data))
        if errors:
            error_messages = []
            for error in errors:
                # Create a readable error path
                path = " → ".join(str(p) for p in error.absolute_path) if error.absolute_path else "root"
                error_messages.append(f"  • {path}: {error.message}")
            return False, error_messages
        return True, []
    except jsonschema.ValidationError as e:
        return False, [f"Validation failed: {e}"]
    except Exception as e:
        return False, [f"Unexpected validation error: {e}"]

def meta_validate_schemas(schemas_root: Path) -> Tuple[bool, int]:
    """Meta-validate every schema file against the JSON Schema draft 2020-12 meta-schema.

    This catches malformed schemas (e.g. non-schema values under "properties")
    that would otherwise only surface in downstream parser/validator implementations.
    """
    meta_validator = Draft202012Validator(Draft202012Validator.META_SCHEMA)
    schema_files = sorted(schemas_root.rglob("*.json"))

    print_status(Colors.BLUE, f"🧪 Meta-validating {len(schema_files)} schema files...")
    print()

    invalid = 0
    for schema_path in schema_files:
        rel = schema_path.relative_to(schemas_root.parent)
        schema_data, load_error = load_json_file(schema_path)
        if load_error:
            print_status(Colors.RED, f"❌ {rel}: {load_error}")
            invalid += 1
            continue

        errors = list(meta_validator.iter_errors(schema_data))
        if errors:
            invalid += 1
            print_status(Colors.RED, f"❌ {rel}: {len(errors)} meta-validation error(s)")
            for error in errors[:5]:
                path = "/".join(str(p) for p in error.absolute_path) if error.absolute_path else "root"
                print(f"  • /{path}: {error.message}")
            if len(errors) > 5:
                print(f"  • ... and {len(errors) - 5} more")
        else:
            print_status(Colors.GREEN, f"✅ {rel}")

    print()
    if invalid:
        print_status(Colors.RED, f"❌ {invalid} schema file(s) are not valid JSON Schema")
    else:
        print_status(Colors.GREEN, "🎉 All schema files are valid JSON Schema!")
    print()
    return invalid == 0, invalid


def get_sample_category_type(sample_data: Dict[str, Any]) -> Tuple[str, str]:
    """Extract category and type from sample data"""
    category = sample_data.get('category', '')
    sample_type = sample_data.get('type', '')
    return category, sample_type

def main():
    """Main validation function"""
    print_status(Colors.BLUE, "🔍 XARF Schema Validation")
    print()
    
    # Get script directory and project root
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent
    
    # Paths
    samples_dir = root_dir / "samples" / "v4"
    schemas_dir = root_dir / "schemas" / "v4"
    master_schema_path = schemas_dir / "xarf-v4-master.json"
    
    # Check required paths exist
    if not samples_dir.exists():
        print_status(Colors.RED, f"❌ Samples directory not found: {samples_dir}")
        return 1
    
    if not schemas_dir.exists():
        print_status(Colors.RED, f"❌ Schemas directory not found: {schemas_dir}")
        return 1
    
    if not master_schema_path.exists():
        print_status(Colors.RED, f"❌ Master schema not found: {master_schema_path}")
        return 1

    # Meta-validate all schema files (v3 and v4) before validating samples
    all_schemas_dir = root_dir / "schemas"
    schemas_valid, _ = meta_validate_schemas(all_schemas_dir)
    if not schemas_valid:
        print_status(Colors.RED, "❌ Schema files failed meta-validation; fix them before validating samples")
        return 1

    # Get all sample files
    sample_files = list(samples_dir.glob("*.json"))
    if not sample_files:
        print_status(Colors.YELLOW, "⚠️  No sample files found")
        return 0
    
    print_status(Colors.BLUE, f"📋 Found {len(sample_files)} sample files to validate")
    print()
    
    # Load and resolve master schema once
    print_status(Colors.BLUE, "🔧 Loading and resolving master schema...")
    master_schema, schema_error = load_json_file(master_schema_path)
    if schema_error:
        print_status(Colors.RED, f"❌ Failed to load master schema: {schema_error}")
        return 1
    
    try:
        resolved_master_schema = resolve_schema_refs(master_schema, master_schema_path.parent)
    except FileNotFoundError as e:
        print_status(Colors.RED, f"❌ Missing schema file: {e}")
        return 1
    except ValueError as e:
        print_status(Colors.RED, f"❌ Schema parsing error: {e}")
        return 1
    except Exception as e:
        print_status(Colors.RED, f"❌ Unexpected error resolving schema references: {e}")
        return 1
    
    print()
    
    # Validation results
    validation_results = []
    total_samples = len(sample_files)
    valid_samples = 0
    
    # Validate each sample against resolved master schema
    for sample_path in sorted(sample_files):
        sample_name = sample_path.name
        
        print_status(Colors.CYAN, f"🔎 Validating {sample_name}")
        
        # Load sample file
        sample_data, sample_error = load_json_file(sample_path)
        if sample_error:
            print_status(Colors.RED, f"❌ Failed to load {sample_name}: {sample_error}")
            validation_results.append((sample_name, False, [f"Load error: {sample_error}"]))
            continue
        
        # Get category and type for information
        category, sample_type = get_sample_category_type(sample_data)
        if category and sample_type:
            print(f"   Category: {category}, Type: {sample_type}")
        else:
            print_status(Colors.YELLOW, f"⚠️  Warning: {sample_name} missing category or type fields")
            if not category:
                print("   Missing: category")
            if not sample_type:
                print("   Missing: type")
        
        # Validate against resolved master schema
        is_valid, errors = validate_sample_against_schema(sample_data, resolved_master_schema)
        
        if is_valid:
            print_status(Colors.GREEN, f"✅ Valid: {sample_name}")
            valid_samples += 1
        else:
            print_status(Colors.RED, f"❌ Invalid: {sample_name}")
            for error in errors:
                print(error)
        
        print()  # Empty line for readability
        
        validation_results.append((sample_name, is_valid, errors))
    
    # Print summary
    print_status(Colors.BLUE, "📊 Validation Summary")
    print(f"Total samples: {total_samples}")
    print(f"Valid samples: {valid_samples}")
    print(f"Invalid samples: {total_samples - valid_samples}")
    
    if valid_samples == total_samples:
        print_status(Colors.GREEN, "🎉 All samples validate successfully against their schemas!")
        return 0
    else:
        print_status(Colors.RED, f"❌ {total_samples - valid_samples} sample(s) failed validation")
        print()
        print_status(Colors.YELLOW, "Failed samples:")
        for sample_name, is_valid, errors in validation_results:
            if not is_valid:
                print(f"  • {sample_name}")
        return 1

if __name__ == "__main__":
    sys.exit(main())