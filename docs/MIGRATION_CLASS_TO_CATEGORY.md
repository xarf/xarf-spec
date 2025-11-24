# Migration Guide: "class" to "category" Field Change

## Overview

XARF v4 has been updated to use "category" instead of "class" for the primary abuse classification field. This change improves clarity and avoids potential naming conflicts with programming language keywords.

## What Changed

### Field Name
- **Old**: `"class": "messaging"`
- **New**: `"category": "messaging"`

### Affected Files
- All schema files in `schemas/v4/`
- All type-specific schemas in `schemas/v4/types/`
- All sample files in `samples/v4/`
- All documentation

## Migration Checklist

### For Report Generators
- [ ] Update JSON serialization to use `"category"` field
- [ ] Remove or deprecate `"class"` field usage
- [ ] Update any templates or code generation tools
- [ ] Test with updated schema validation

### For Report Parsers
- [ ] Update JSON deserialization to read `"category"` field
- [ ] Consider backward compatibility for transition period
- [ ] Update field mappings in database schemas
- [ ] Update API documentation

### For Validators
- [ ] Update schema validation to check `"category"`
- [ ] Update error messages referencing "class"
- [ ] Re-test all validation rules
- [ ] Update validation test suites

## Example Code Updates

### Python
```python
# Old
report["class"] = "messaging"

# New
report["category"] = "messaging"
```

### JavaScript/TypeScript
```javascript
// Old
const report = {
  class: "messaging",
  type: "spam"
};

// New
const report = {
  category: "messaging",
  type: "spam"
};
```

### Go
```go
// Old
type XARFReport struct {
    Class string `json:"class"`
}

// New
type XARFReport struct {
    Category string `json:"category"`
}
```

## Backward Compatibility

During the transition period, consider:

1. **Dual-field support**: Accept both `class` and `category` in parsers
2. **Migration warnings**: Log warnings when `class` is used
3. **Automatic conversion**: Map old `class` field to `category` internally
4. **Grace period**: Set a deprecation timeline (e.g., 6 months)

## Testing

Validate your migration:
```bash
# Check JSON syntax
python3 -m json.tool your-report.json

# Validate against schema
ajv validate -s schemas/v4/xarf-core.json -d your-report.json
```

## Support

For questions or issues related to this migration:
- Open an issue: https://github.com/xarf-project/xarf-spec/issues
- Check the specification: docs/specification.md

## Timeline

- **Change Date**: 2025-11-24
- **Recommended Migration**: Immediate
- **Suggested Grace Period**: 6 months for dual-field support
