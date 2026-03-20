# XARF JSON Schema Definitions

This directory contains the authoritative JSON Schema definitions for XARF (eXtended Abuse Reporting Format) v4 and legacy v3 formats. These schemas serve as the single source of truth for what constitutes a valid XARF report.

## 📋 Schema Architecture

### XARF v4 Type-Specific Architecture

XARF v4 uses a **type-specific architecture** with 32 dedicated schemas across 7 abuse categories:

| Category | Type-Specific Schemas | Purpose |
|----------|----------------------|---------|
| **messaging** (2) | `messaging-spam`, `messaging-bulk-messaging` | Communication abuse |
| **connection** (8) | `connection-login-attack`, `connection-port-scan`, `connection-ddos`, `connection-infected-host`, `connection-reconnaissance`, `connection-scraping`, `connection-sql-injection`, `connection-vulnerability-scan` | Network attacks |
| **vulnerability** (3) | `vulnerability-cve`, `vulnerability-open-service`, `vulnerability-misconfiguration` | Security vulnerabilities |
| **content** (9) | `content-phishing`, `content-malware`, `content-csam`, `content-csem`, `content-exposed-data`, `content-brand-infringement`, `content-fraud`, `content-remote-compromise`, `content-suspicious-registration` | Malicious web content |
| **infrastructure** (2) | `infrastructure-botnet`, `infrastructure-compromised-server` | Compromised systems |
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

## 📄 Sample Reports

The [`samples/v4/`](../samples/v4/) directory contains one validated sample for each of the 32 schema types.

## 🤝 Contributing

To contribute to XARF schema development:

1. **Test against samples**: Ensure schema changes validate existing samples
2. **Maintain compatibility**: Avoid breaking changes to core fields
3. **Update documentation**: Include field descriptions and examples
4. **Validate thoroughly**: Use `python3 scripts/validate-schemas.py` before submitting
5. **Follow conventions**: Match existing schema patterns and naming

## 📄 License

These schemas are part of the XARF specification and are available under the [MIT License](../LICENSE) for maximum compatibility with both open source and commercial implementations.

