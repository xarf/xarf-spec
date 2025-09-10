# XARF Repository Architecture

## Single Source of Truth Principle

### 📋 xarf-spec (Specification Repository)
**Purpose**: Authoritative specification and reference materials
- `schemas/v4/` - **Official JSON schemas** (master schema + 7 class schemas)
- `samples/v4/` - **Documentation examples** (one clean example per class)
- `docs/` - Specification documentation
- `CHANGELOG.md` - Version history

### 🧪 xarf-parser-tests (Shared Test Suite)  
**Purpose**: Comprehensive test cases for all parser implementations
- `samples/valid/` - All valid test cases (comprehensive coverage)
- `samples/invalid/` - All invalid test cases (error conditions)
- `test-definitions/` - Language-agnostic test specifications
- Used via Git subtree in all parser repositories

### 🐍 xarf-parser-python (Python Implementation)
**Purpose**: Python-specific parser implementation
- `tests/shared/` - Git subtree from xarf-parser-tests
- `xarf/` - Parser implementation
- **NO local schemas** - references xarf-spec schemas via URL
- **NO local samples** - uses shared test suite

## Schema Distribution Strategy

### For Parser Development
```bash
# Parsers reference schemas from spec repo via URL
SCHEMA_BASE_URL = "https://raw.githubusercontent.com/xarf/xarf-spec/main/schemas/v4/"
MASTER_SCHEMA = SCHEMA_BASE_URL + "xarf-v4-master.json"
```

### For Testing
```bash
# Include shared test suite via Git subtree
git subtree add --prefix=tests/shared https://github.com/xarf/xarf-parser-tests.git main --squash

# Update test suite when needed
git subtree pull --prefix=tests/shared https://github.com/xarf/xarf-parser-tests.git main --squash
```

## Benefits
- ✅ **Single source of truth** - schemas maintained in one place
- ✅ **Consistent testing** - all parsers use identical test cases  
- ✅ **Easy maintenance** - schema updates propagate automatically
- ✅ **Version control** - clear separation of concerns
- ✅ **Offline development** - test cases available locally via subtree