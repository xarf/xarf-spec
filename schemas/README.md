# XARF JSON Schema Definitions

This directory contains the authoritative JSON Schema definitions for XARF (eXtended Abuse Reporting Format) v4 and legacy v3 formats. These schemas serve as the single source of truth for what constitutes a valid XARF report.

## 📁 Directory Structure

```
schemas/
├── README.md                    # This documentation
├── v4/                         # XARF v4 schemas
│   ├── xarf-core.json          # Base schema with common fields
│   ├── xarf-v4-master.json     # Master schema with conditional validation
│   └── types/                  # Type-specific schemas (22 total)
│       ├── messaging-spam.json
│       ├── messaging-bulk-messaging.json
│       ├── connection-login-attack.json
│       ├── connection-port-scan.json
│       ├── connection-ddos.json
│       ├── connection-ddos-amplification.json
│       ├── connection-auth-failure.json
│       ├── vulnerability-cve.json
│       ├── vulnerability-open.json
│       ├── vulnerability-misconfiguration.json
│       ├── content-phishing.json
│       ├── content-malware.json
│       ├── infrastructure-bot.json
│       ├── infrastructure-compromised-server.json
│       ├── reputation-blocklist.json
│       ├── reputation-threat-intelligence.json
│       ├── copyright-copyright.json
│       ├── copyright-p2p.json
│       ├── copyright-cyberlocker.json
│       ├── copyright-ugc-platform.json
│       ├── copyright-link-site.json
│       └── copyright-usenet.json
└── v3/                         # Legacy XARF v3 schemas
    └── xarf-v3-legacy.json     # XARF v3 format for backwards compatibility
```

## 🎯 Quick Start

### Validating XARF v4 Reports

Use the **master schema** for complete validation with type-specific rules:

```bash
# Install dependencies
./scripts/setup.sh

# Validate all schemas and samples  
./scripts/validate.sh

# Using python-jsonschema directly
python3 -c "
import json, jsonschema
with open('samples/v4/messaging-spam.json') as f: data = json.load(f)
with open('schemas/v4/xarf-v4-master.json') as f: schema = json.load(f)
jsonschema.validate(data, schema)
print('✅ Valid!')
"
```

### Validating Against Specific Type Schemas

```bash
# Validate messaging spam report
python3 -c "
import json, jsonschema
with open('samples/v4/messaging-spam.json') as f: data = json.load(f)
with open('schemas/v4/types/messaging-spam.json') as f: schema = json.load(f)
jsonschema.validate(data, schema)
print('✅ Valid against type-specific schema!')
"
```

## 📋 Schema Architecture

### XARF v4 Type-Specific Architecture

XARF v4 uses a **type-specific architecture** with 22 dedicated schemas across 7 abuse classes:

| Class | Type-Specific Schemas | Purpose |
|-------|----------------------|---------|
| **messaging** (2) | `messaging-spam`, `messaging-bulk-messaging` | Communication abuse |
| **connection** (5) | `connection-login-attack`, `connection-port-scan`, `connection-ddos`, `connection-ddos-amplification`, `connection-auth-failure` | Network attacks |
| **vulnerability** (3) | `vulnerability-cve`, `vulnerability-open`, `vulnerability-misconfiguration` | Security vulnerabilities |
| **content** (2) | `content-phishing`, `content-malware` | Malicious web content |
| **infrastructure** (2) | `infrastructure-bot`, `infrastructure-compromised-server` | Compromised systems |
| **reputation** (2) | `reputation-blocklist`, `reputation-threat-intelligence` | Threat intelligence |
| **copyright** (6) | `copyright-copyright`, `copyright-p2p`, `copyright-cyberlocker`, `copyright-ugc-platform`, `copyright-link-site`, `copyright-usenet` | Intellectual property infringement |

### Core Schema Structure

All schemas extend the base `xarf-core.json` schema:

1. **xarf-core.json** - Common fields required by all reports
2. **Type-specific schemas** - Additional validation for each abuse type
3. **xarf-v4-master.json** - Conditional validation routing to correct type schema

### Required Fields (from xarf-core.json)

All XARF v4 reports must include:

- `xarf_version` - Version string (e.g., "4.0.0") 
- `report_id` - UUID v4 identifier
- `timestamp` - ISO 8601 datetime when abuse occurred
- `reporter` - Organization information (`org`, `contact`, `type`)
- `source_identifier` - IP, domain, or identifier of abuse source
- `category` - Primary abuse classification  
- `type` - Specific abuse type within category

## 🔧 Schema Usage Guide

### 1. Master Schema Validation (Recommended)

The master schema automatically validates against the correct type schema:

```python
import json
import jsonschema

def validate_xarf_report(report_data):
    """Validate XARF report against master schema."""
    with open('schemas/v4/xarf-v4-master.json') as f:
        master_schema = json.load(f)
    
    try:
        jsonschema.validate(report_data, master_schema)
        return True, None
    except jsonschema.exceptions.ValidationError as e:
        return False, str(e)

# Usage
with open('samples/v4/messaging-spam.json') as f:
    report = json.load(f)

is_valid, error = validate_xarf_report(report)
if not is_valid:
    print(f"Validation failed: {error}")
```

### 2. Type-Specific Validation

For focused validation or development:

```python
def validate_specific_type(report_data, category_name, type_name):
    """Validate against specific type schema."""
    schema_file = f'schemas/v4/types/{category_name}-{type_name.replace("_", "-")}.json'
    
    with open(schema_file) as f:
        schema = json.load(f)
    
    jsonschema.validate(report_data, schema)
    return True

# Example
validate_specific_type(report, "messaging", "spam")
```

### 3. Creating Valid Reports

```python
import json
import uuid
from datetime import datetime

def create_xarf_report(category_name, type_name, source_identifier, **kwargs):
    """Create a valid XARF v4 report."""
    report = {
        "xarf_version": "4.0.0",
        "report_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "reporter": {
            "org": kwargs.get("reporter_org", "Security Organization"),
            "contact": kwargs.get("reporter_contact", "abuse@example.com"),
            "type": kwargs.get("reporter_type", "automated")
        },
        "source_identifier": source_identifier,
        "category": category_name,
        "type": type_name,
        **{k: v for k, v in kwargs.items() if not k.startswith('reporter_')}
    }
    
    # Validate against master schema
    validate_xarf_report(report)
    return report

# Example: Create spam report
spam_report = create_xarf_report(
    category_name="messaging",
    type_name="spam",
    source_identifier="192.0.2.100", 
    protocol="smtp",
    smtp_from="spam@example.com",
    subject="Buy now!",
    evidence_source="spamtrap"
)
```

## 🎨 Examples by Type

### Messaging - Spam
```json
{
  "xarf_version": "4.0.0",
  "report_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2024-01-15T14:30:25Z",
  "reporter": {
    "org": "Anti-Spam Service",
    "contact": "reports@antispam.example",
    "type": "automated"
  },
  "source_identifier": "192.0.2.123",
  "source_port": 25,
  "category": "messaging",
  "type": "spam",
  "protocol": "smtp",
  "smtp_from": "fake@example.com",
  "subject": "Urgent: Verify Your Account",
  "evidence_source": "spamtrap"
}
```

### Connection - DDoS
```json
{
  "xarf_version": "4.0.0",
  "report_id": "987fcdeb-51a2-43d1-9f12-345678901234", 
  "timestamp": "2024-01-15T10:20:30Z",
  "reporter": {
    "org": "DDoS Protection Service",
    "contact": "security@ddosprotect.example",
    "type": "automated"
  },
  "source_identifier": "198.51.100.75",
  "category": "connection",
  "type": "ddos",
  "protocol": "tcp",
  "first_seen": "2024-01-15T10:15:00Z",
  "attack_vector": "syn_flood",
  "peak_pps": 250000,
  "duration_seconds": 2700
}
```

### Copyright - P2P
```json
{
  "xarf_version": "4.0.0",
  "report_id": "p2p-1234-5678-9012-abcdef123456",
  "timestamp": "2024-01-15T16:00:00Z",
  "reporter": {
    "org": "P2P Monitoring Service", 
    "contact": "p2p-reports@copyright.example",
    "type": "automated"
  },
  "source_identifier": "192.0.2.100",
  "category": "copyright",
  "type": "p2p",
  "p2p_protocol": "bittorrent",
  "swarm_info": {
    "info_hash": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
    "magnet_uri": "magnet:?xt=urn:btih:da39a3ee5e6b4b0d3255bfef95601890afd80709"
  },
  "work_title": "Copyrighted Movie 2024",
  "rights_holder": "Film Studio Corp"
}
```

## ⚡ Validation Tools

### Command Line Validation
```bash
# Validate all samples against schemas
./scripts/validate.sh

# Format all JSON files
./scripts/validate.sh format

# Manual validation with Python
python3 -c "
import json, jsonschema
with open('your-report.json') as f: data = json.load(f)
with open('schemas/v4/xarf-v4-master.json') as f: schema = json.load(f)
jsonschema.validate(data, schema)
print('✅ Report is valid!')
"
```

### Batch Validation Script
```bash
#!/bin/bash
# validate-reports.sh

for file in reports/*.json; do
  echo "Validating $file..."
  if python3 -c "
import json, jsonschema, sys
try:
  with open('$file') as f: data = json.load(f)
  with open('schemas/v4/xarf-v4-master.json') as f: schema = json.load(f)
  jsonschema.validate(data, schema)
  print('✅ Valid')
except Exception as e:
  print(f'❌ Invalid: {e}')
  sys.exit(1)
"; then
    echo "✅ $file is valid"
  else 
    echo "❌ $file is invalid"
  fi
done
```

## 🔍 Troubleshooting

### Common Validation Errors

**1. Missing Required Fields**
```
Error: 'protocol' is a required property
Solution: Add required fields per type schema
```

**2. Invalid Type/Class Combination**
```
Error: No schema found for category 'messaging' type 'invalid_type'
Solution: Use valid type from type-specific schemas
```

**3. Source Port Requirements**  
```
Error: 'source_port' is required when source_identifier is IP
Solution: Include source_port for IP-based sources (CGNAT environments)
```

**4. Evidence Validation**
```
Error: Evidence payload exceeds size limits
Solution: Limit evidence items to 5MB each, 50 items total
```

## 🚀 Integration Patterns

### Web API Endpoint
```javascript
// Express.js XARF report receiver
app.post('/xarf/reports', async (req, res) => {
  try {
    const report = req.body;
    
    // Validate against master schema
    await validateXARFReport(report);
    
    // Route based on class and type
    const handler = getHandlerForType(report.category, report.type);
    await handler.process(report);
    
    res.json({ 
      status: 'processed', 
      report_id: report.report_id 
    });
  } catch (error) {
    res.status(400).json({ 
      error: 'Invalid XARF report',
      details: error.message 
    });
  }
});
```

### Stream Processing
```python
import json
import jsonschema

def process_xarf_stream(reports_stream):
    """Process stream of XARF reports with validation."""
    
    # Load master schema once
    with open('schemas/v4/xarf-v4-master.json') as f:
        master_schema = json.load(f)
    
    validator = jsonschema.Draft202012Validator(master_schema)
    
    for report_data in reports_stream:
        try:
            # Validate
            validator.validate(report_data)
            
            # Route to appropriate handler
            handler_key = f"{report_data['category']}:{report_data['type']}"
            if handler_key in handlers:
                handlers[handler_key](report_data)
            else:
                logger.warning(f"No handler for {handler_key}")
                
        except jsonschema.exceptions.ValidationError as e:
            logger.error(f"Invalid XARF report: {e}")
```

## 📚 Additional Resources

- **Complete Sample Set**: Each type schema has a corresponding sample in `samples/v4/`
- **Master Schema**: `schemas/v4/xarf-v4-master.json` for comprehensive validation
- **Core Schema**: `schemas/v4/xarf-core.json` for common field definitions
- **Type Documentation**: Each type schema includes detailed field descriptions

## 🤝 Contributing

To contribute to XARF schema development:

1. **Test against samples**: Ensure schema changes validate existing samples
2. **Maintain compatibility**: Avoid breaking changes to core fields  
3. **Update documentation**: Include field descriptions and examples
4. **Validate thoroughly**: Use `./scripts/validate.sh` before submitting
5. **Follow conventions**: Match existing schema patterns and naming

## 📄 License

These schemas are part of the XARF specification and are available under the MIT License for maximum compatibility with both open source and commercial implementations.

---

**The schemas in this directory are the authoritative source of truth for XARF validation. Parser implementations should reference these schemas directly rather than duplicating the validation logic.**