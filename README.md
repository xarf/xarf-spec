# XARF v4 Specification

The eXtended Abuse Reporting Format (XARF) is a standard for reporting abuse incidents in a structured, machine-readable format. XARF v4 introduces a category-based architecture with seven main abuse categories and enhanced evidence handling.

## Documentation

- **[Introduction & Overview](docs/introduction.md)** - High-level overview and use cases
- **[Technical Specification](docs/specification.md)** - Complete technical reference
- **[Implementation Guide](docs/implementation-guide.md)** - Deployment and project management
- **[JSON Schemas](schemas/)** - Formal validation schemas for all XARF v4 categories and event types
- **[Sample Reports](samples/)** - Sample reports organized for all XARF v4 categories and event types


## Quick Start

```bash
# Install dependencies (jq, python3, jsonschema)
./scripts/setup.sh

# View a sample report
cat samples/v4/messaging-spam.json

# Check JSON formatting
./scripts/format-json.sh check

# Format all JSON files
./scripts/format-json.sh format

# Validate all samples against schemas
python3 scripts/validate-schemas.py

# Or using nix-shell (NixOS users)
nix-shell -p python3 python3Packages.jsonschema --run "python3 scripts/validate-schemas.py"

# Validate specific sample against its schema
python3 -c "
import json, jsonschema
with open('samples/v4/messaging-spam.json') as f: data = json.load(f)
with open('schemas/v4/types/messaging-spam.json') as f: schema = json.load(f)
jsonschema.validate(data, schema)
print('✅ Valid!')
"
```

## Parser Libraries

- **JavaScript**: [xarf-javascript](https://github.com/xarf/xarf-javascript)
- **Python**: [xarf-python](https://github.com/xarf/xarf-python) (Alpha)
- **Go**: Coming soon

## XARF v3 Compatibility

XARF v4 maintains backward compatibility with v3 reports. See the [Technical Specification](docs/specification.md#backwards-compatibility) for details.

## Contributing

XARF v4 is an open standard. We welcome contributions from the security community. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - See [LICENSE](LICENSE) for details.