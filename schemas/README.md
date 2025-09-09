# XARF JSON Schema Definitions

This directory contains the authoritative JSON Schema definitions for XARF (eXtended Abuse Reporting Format) v4 and legacy v3 formats. These schemas serve as the single source of truth for what constitutes a valid XARF report.

## 📁 Directory Structure

```
schemas/
├── README.md                    # This documentation
├── v4/                         # XARF v4 schemas
│   ├── xarf-core.json          # Base schema with common fields
│   ├── xarf-v4-master.json     # Master schema with conditional validation
│   ├── messaging-class.json    # Messaging abuse (spam, bulk messaging)
│   ├── connection-class.json   # Network attacks (DDoS, login attacks)
│   ├── content-class.json      # Web content abuse (phishing, malware)
│   ├── infrastructure-class.json # Compromised systems (bots, C2)
│   ├── copyright-class.json    # IP infringement (DMCA, copyright)
│   ├── vulnerability-class.json # Security disclosures (CVEs, misconfigs)
│   └── reputation-class.json   # Threat intelligence (blocklists, reputation)
└── v3/                         # Legacy XARF v3 schemas
    └── xarf-v3-legacy.json     # XARF v3 format for backwards compatibility
```

## 🎯 Quick Start

### Validating XARF v4 Reports

Use the **master schema** for complete validation with class-specific rules:

```bash
# Using ajv-cli (Node.js)
npm install -g ajv-cli
ajv validate -s schemas/v4/xarf-v4-master.json -d your-report.json

# Using python-jsonschema
pip install jsonschema
jsonschema -i your-report.json schemas/v4/xarf-v4-master.json
```

### Validating Legacy XARF v3 Reports

```bash
ajv validate -s schemas/v3/xarf-v3-legacy.json -d your-v3-report.json
```

## 📋 Schema Overview

### XARF v4 Architecture

XARF v4 uses a **class-based architecture** with 7 primary abuse classes:

| Class | Purpose | Key Fields | Example Types |
|-------|---------|------------|---------------|
| **messaging** | Communication abuse | `protocol`, `smtp_from` | spam, bulk_messaging |
| **connection** | Network attacks | `destination_ip`, `protocol` | ddos, login_attack, port_scan |
| **content** | Web content abuse | `url`, `target_brand` | phishing, malware, fraud |
| **infrastructure** | Compromised systems | `malware_family`, `c2_server` | bot, compromised_server |
| **copyright** | IP infringement | `work_title`, `rights_holder` | copyright, trademark |
| **vulnerability** | Security disclosures | `service`, `cve_id` | cve, misconfiguration |
| **reputation** | Threat intelligence | `threat_type`, `confidence_score` | blocklist, ip_reclamation |

### Core Required Fields

All XARF v4 reports must include:

- `xarf_version` - Version string (e.g., "4.0.0")
- `report_id` - UUID v4 identifier
- `timestamp` - ISO 8601 datetime when abuse occurred
- `reporter` - Organization information (`org`, `contact`, `type`)
- `source_identifier` - IP, domain, or identifier of abuse source
- `class` - Primary abuse classification
- `type` - Specific abuse type within class

## 🔧 Schema Usage Guide

### 1. Parser Implementation

**Recommended approach for XARF parsers:**

```javascript
// 1. Load the master schema for complete validation
const masterSchema = require('./schemas/v4/xarf-v4-master.json');

// 2. Validate incoming reports
function validateXARFReport(report) {
  const ajv = new Ajv({
    allErrors: true,
    verbose: true,
    loadSchema: loadSchemaFunction // Load referenced schemas
  });
  
  const validate = ajv.compile(masterSchema);
  const valid = validate(report);
  
  if (!valid) {
    throw new Error(`Invalid XARF report: ${JSON.stringify(validate.errors)}`);
  }
  
  return report;
}

// 3. Handle both v3 and v4 formats
function parseXARFReport(data) {
  if (data.Version === "3" || data.Version === "3.0") {
    return convertV3ToV4(data); // Convert legacy format
  }
  
  if (data.xarf_version && data.xarf_version.startsWith("4.")) {
    return validateXARFReport(data);
  }
  
  throw new Error("Unknown XARF version");
}
```

### 2. Generator Implementation

**Creating valid XARF v4 reports:**

```python
import json
import uuid
from datetime import datetime
import jsonschema

def create_xarf_report(class_name, type_name, source_ip, **kwargs):
    report = {
        "xarf_version": "4.0.0",
        "report_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "reporter": {
            "org": kwargs.get("reporter_org", "Security Organization"),
            "contact": kwargs.get("reporter_contact", "abuse@example.com"),
            "type": kwargs.get("reporter_type", "automated")
        },
        "source_identifier": source_ip,
        "class": class_name,
        "type": type_name,
        **kwargs  # Additional class-specific fields
    }
    
    # Validate against master schema
    with open('schemas/v4/xarf-v4-master.json') as f:
        schema = json.load(f)
    
    jsonschema.validate(report, schema)
    return report

# Example usage
spam_report = create_xarf_report(
    class_name="messaging",
    type_name="spam", 
    source_ip="192.0.2.100",
    protocol="smtp",
    smtp_from="spam@example.com",
    subject="Buy now!",
    evidence_source="spamtrap"
)
```

### 3. Class-Specific Validation

For specialized use cases, you can validate against individual class schemas:

```bash
# Validate only messaging class fields
ajv validate -s schemas/v4/messaging-class.json -d messaging-report.json

# Validate only connection class fields  
ajv validate -s schemas/v4/connection-class.json -d ddos-report.json
```

## 📊 Validation Levels

### Strict Mode
- Fail on any unknown fields
- Require all optional recommended fields
- Enforce strict format validation

### Permissive Mode (Recommended)
- Validate known fields, warn on unknown fields  
- Allow missing optional fields
- Forward compatibility for new fields

### Legacy Mode
- Accept v3 format reports
- Convert to v4 structure automatically
- Generate warnings for deprecated patterns

## 🔄 V3 to V4 Migration

### Automatic Conversion

The v3 legacy schema includes mapping documentation for converting old reports:

```javascript
function convertV3ToV4(v3Report) {
  const v4Report = {
    xarf_version: "4.0.0",
    report_id: generateUUID(),
    legacy_version: "3",
    timestamp: v3Report.Report.Date,
    reporter: {
      org: v3Report.ReporterInfo.ReporterOrg,
      contact: v3Report.ReporterInfo.ReporterOrgEmail,
      type: "unknown"
    },
    source_identifier: v3Report.Report.SourceIp,
    source_port: v3Report.Report.SourcePort,
    // Map v3 types to v4 class/type combinations
    ...mapV3TypeToV4(v3Report.Report.ReportType),
    evidence: convertSamplesToEvidence(v3Report.Report.Samples)
  };
  
  return v4Report;
}

function mapV3TypeToV4(v3Type) {
  const mapping = {
    "Spam": { class: "messaging", type: "spam" },
    "Login-Attack": { class: "connection", type: "login_attack" },
    "Port-Scan": { class: "connection", type: "port_scan" },
    "DDoS": { class: "connection", type: "ddos" },
    "Phishing": { class: "content", type: "phishing" },
    "Malware": { class: "content", type: "malware" },
    "Botnet": { class: "infrastructure", type: "bot" },
    "Copyright": { class: "copyright", type: "copyright" }
  };
  
  return mapping[v3Type] || { class: "infrastructure", type: "unknown" };
}
```

## ⚡ Performance Guidelines

### Schema Loading
- Cache compiled schemas in production
- Load schemas asynchronously when possible
- Use schema references to avoid duplication

### Validation Optimization
- Validate incrementally (core → class-specific)
- Batch validate multiple reports when possible
- Use streaming validation for large evidence payloads

### Memory Management
- Limit evidence payload size (5MB per item, 15MB total)
- Use efficient base64 decoding libraries
- Clean up validation objects after use

## 🎨 Examples by Class

### Messaging Class - Email Spam
```json
{
  "xarf_version": "4.0.0",
  "report_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2024-01-15T14:30:25Z",
  "reporter": {
    "org": "SpamCop",
    "contact": "reports@spamcop.net",
    "type": "automated"
  },
  "source_identifier": "192.0.2.123",
  "source_port": 25,
  "class": "messaging",
  "type": "spam",
  "protocol": "smtp",
  "smtp_from": "fake@example.com",
  "subject": "Urgent: Verify Your Account",
  "evidence_source": "spamtrap",
  "evidence": [{
    "content_type": "message/rfc822",
    "description": "Complete spam email with headers",
    "payload": "base64-encoded-email-content"
  }],
  "tags": ["phishing:financial", "campaign:fake_bank_2024"]
}
```

### Connection Class - DDoS Attack
```json
{
  "xarf_version": "4.0.0", 
  "report_id": "987fcdeb-51a2-43d1-9f12-345678901234",
  "timestamp": "2024-01-15T10:20:30Z",
  "reporter": {
    "org": "DDoS Protection Service",
    "contact": "security@ddosprotect.com",
    "type": "automated"
  },
  "source_identifier": "198.51.100.75",
  "class": "connection",
  "type": "ddos",
  "destination_ip": "203.0.113.100",
  "destination_port": 80,
  "protocol": "tcp",
  "attack_vector": "syn_flood",
  "peak_pps": 250000,
  "duration_seconds": 2700,
  "evidence_source": "flow_analysis",
  "tags": ["attack:volumetric", "severity:high"]
}
```

### Content Class - Phishing Site
```json
{
  "xarf_version": "4.0.0",
  "report_id": "123e4567-e89b-12d3-a456-426614174000", 
  "timestamp": "2024-01-15T16:45:10Z",
  "reporter": {
    "org": "PhishTank",
    "contact": "admin@phishtank.com",
    "type": "automated"
  },
  "source_identifier": "203.0.113.45",
  "class": "content",
  "type": "phishing",
  "url": "http://fake-bank.example.com/login.php",
  "target_brand": "Example Bank",
  "target_category": "financial",
  "evidence_source": "crawler",
  "evidence": [{
    "content_type": "image/png",
    "description": "Screenshot of phishing page", 
    "payload": "base64-encoded-screenshot"
  }],
  "tags": ["phishing:banking", "target:example_bank"]
}
```

## 🚀 Integration Patterns

### Web Application Integration
```javascript
// Express.js endpoint for receiving XARF reports
app.post('/xarf/reports', async (req, res) => {
  try {
    const report = await validateXARFReport(req.body);
    
    // Route based on class
    switch (report.class) {
      case 'messaging':
        await handleSpamReport(report);
        break;
      case 'connection':
        await handleNetworkAttack(report);
        break;
      case 'content':
        await handleMaliciousContent(report);
        break;
      // ... other cases
    }
    
    res.json({ status: 'processed', report_id: report.report_id });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});
```

### Command Line Validation
```bash
#!/bin/bash
# validate-xarf.sh - Batch validation script

for file in reports/*.json; do
  echo "Validating $file..."
  if ajv validate -s schemas/v4/xarf-v4-master.json -d "$file"; then
    echo "✅ $file is valid"
  else
    echo "❌ $file is invalid"
  fi
done
```

### Python Validation Function
```python
import json
import jsonschema
from pathlib import Path

def validate_xarf_file(report_file, schema_dir="schemas/v4"):
    """Validate a XARF report file against the appropriate schema."""
    
    with open(report_file) as f:
        report = json.load(f)
    
    # Determine schema based on XARF version
    if report.get('xarf_version', '').startswith('4.'):
        schema_file = Path(schema_dir) / 'xarf-v4-master.json'
    elif report.get('Version') in ['3', '3.0']:
        schema_file = Path(schema_dir).parent / 'v3' / 'xarf-v3-legacy.json'
    else:
        raise ValueError(f"Unknown XARF version: {report.get('xarf_version')}")
    
    with open(schema_file) as f:
        schema = json.load(f)
    
    try:
        jsonschema.validate(report, schema)
        return True, None
    except jsonschema.exceptions.ValidationError as e:
        return False, str(e)

# Usage
is_valid, error = validate_xarf_file('spam-report.json')
if not is_valid:
    print(f"Validation failed: {error}")
```

## 🔍 Troubleshooting

### Common Validation Errors

**1. Missing Required Fields**
```
Error: Required property 'protocol' missing for messaging class
Solution: Add protocol field when class is 'messaging'
```

**2. Invalid UUID Format**
```  
Error: 'report_id' must be valid UUID v4
Solution: Use proper UUID generation: uuid4() or equivalent
```

**3. Invalid Timestamp Format**
```
Error: 'timestamp' must be ISO 8601 date-time
Solution: Use format like '2024-01-15T14:30:25Z'
```

**4. Evidence Size Limits**
```
Error: Evidence item exceeds 5MB limit
Solution: Compress or truncate evidence, use external references
```

### Schema Reference Issues

If schemas fail to load due to $ref resolution:

```bash
# Ensure all referenced schemas are accessible
ls schemas/v4/xarf-core.json  # Should exist
ls schemas/v4/messaging-class.json  # Should exist
# etc.
```

## 📚 Additional Resources

- **XARF v4 Technical Specification**: Complete field definitions and validation rules
- **XARF v4 Implementation Guide**: Integration patterns and best practices
- **Sample Reports**: Real-world examples in `/samples/v4/` directory
- **Parser Libraries**: Multi-language implementations (Python, JavaScript, Go, PHP, Java, Rust)

## 🤝 Contributing

To contribute to XARF schema development:

1. Review existing schemas for consistency
2. Test changes against sample reports
3. Update documentation for new fields
4. Ensure backwards compatibility
5. Submit pull requests with comprehensive tests

## 📄 License

These schemas are part of the XARF specification and are available under the MIT License for maximum compatibility with both open source and commercial implementations.

---

**The schemas in this directory are the authoritative source of truth for XARF validation. Parser implementations should reference these schemas directly rather than duplicating the validation logic.**