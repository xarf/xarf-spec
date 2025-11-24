# XARF v4 Type-Specific Schemas

This directory contains individual JSON schemas for each XARF v4 event type, providing granular validation and clear documentation of requirements for specific abuse scenarios.

## Benefits of Type-Specific Schemas

- **🔍 Type Discovery**: `ls types/` shows all available event types  
- **📋 Specific Requirements**: Each type defines exactly what fields are mandatory
- **🔧 Maintainability**: New types don't require editing existing schemas
- **👨‍💻 Developer Experience**: Clear understanding of each event type's needs
- **📦 Modular Loading**: Parsers can load only needed type schemas

## Available Event Types

### Messaging Class
| Type | Schema File | Description |
|------|-------------|-------------|
| `spam` | `messaging-spam.json` | Unsolicited commercial messages and unwanted email |
| `bulk_messaging` | `messaging-bulk-messaging.json` | Legitimate but unwanted bulk communications |

### Connection Class  
| Type | Schema File | Description |
|------|-------------|-------------|
| `login_attack` | `connection-login-attack.json` | Brute force login attempts and authentication attacks |
| `port_scan` | `connection-port-scan.json` | Network port scanning and reconnaissance activities |
| `ddos` | `connection-ddos.json` | Distributed Denial of Service attacks |
| `ddos_amplification` | `connection-ddos-amplification.json` | DDoS attacks using amplification techniques |
| `auth_failure` | `connection-auth-failure.json` | Authentication failure incidents |

### Vulnerability Class
| Type | Schema File | Description |
|------|-------------|-------------|
| `cve` | `vulnerability-cve.json` | Common Vulnerabilities and Exposures reports |
| `open` | `vulnerability-open.json` | Open services and exposed resources |
| `misconfiguration` | `vulnerability-misconfiguration.json` | Security misconfigurations and hardening issues |

### Reputation Class
| Type | Schema File | Description |
|------|-------------|-------------|
| `blocklist` | `reputation-blocklist.json` | IP/domain blocklist inclusion reports |
| `threat_intelligence` | `reputation-threat-intelligence.json` | Threat intelligence and IOC reports |

### Infrastructure Class
| Type | Schema File | Description |
|------|-------------|-------------|
| `bot` | `infrastructure-bot.json` | Botnet infections and compromised systems |
| `compromised_server` | `infrastructure-compromised-server.json` | Compromised servers and infrastructure |

### Content Class
| Type | Schema File | Description |
|------|-------------|-------------|
| `phishing` | `content-phishing.json` | Phishing websites and credential harvesting |
| `malware` | `content-malware.json` | Malware hosting and distribution |

### Copyright Class
| Type | Schema File | Description |
|------|-------------|-------------|
| `copyright` | `copyright-copyright.json` | Generic copyright infringement and DMCA violations |
| `p2p` | `copyright-p2p.json` | Peer-to-peer copyright infringement (BitTorrent, etc.) |
| `cyberlocker` | `copyright-cyberlocker.json` | File hosting service copyright infringement |
| `ugc_platform` | `copyright-ugc-platform.json` | User-generated content platform infringement |
| `link_site` | `copyright-link-site.json` | Link aggregation site infringement |
| `usenet` | `copyright-usenet.json` | Usenet newsgroup copyright infringement |

## Schema Structure

Each type schema follows this structure:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://xarf.org/schemas/v4/types/{category}-{type}.json",
  "title": "XARF v4 {Category} - {Type} Type Schema",
  "description": "Schema for {specific abuse type description}",
  "allOf": [
    {
      "$ref": "../xarf-core.json"
    },
    {
      "type": "object",
      "properties": {
        "category": {"const": "{category}"},
        "type": {"const": "{type}"},
        // Type-specific fields and constraints
      },
      "required": ["type-specific-required-fields"]
    }
  ],
  "examples": [
    // Complete example report for this type
  ]
}
```

## Usage

### Validate Against Specific Type
```bash
# Validate a spam report
ajv validate -s types/messaging-spam.json -d sample-spam-report.json

# Validate a DDoS report  
ajv validate -s types/connection-ddos.json -d sample-ddos-report.json
```

### Validate Against Master Schema
```bash
# Master schema automatically selects correct type schema
ajv validate -s ../xarf-v4-master.json -d any-xarf-report.json
```

### Parser Implementation
```python
# Load only needed schemas
spam_schema = load_schema("types/messaging-spam.json")  
ddos_schema = load_schema("types/connection-ddos.json")

# Or use master schema for all types
master_schema = load_schema("../xarf-v4-master.json")
```

## Adding New Types

1. Create new schema file: `{category}-{new-type}.json`
2. Add conditional reference in `../xarf-v4-master.json`
3. Update this README with the new type
4. Add test cases in the test suite

## Migration from Class-Based Schemas

The original category-based schemas (`messaging-class.json`, etc.) are preserved for backward compatibility. New implementations should use type-specific schemas for better granularity and maintainability.