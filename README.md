# XARF v4 Specification

The eXtended Abuse Reporting Format (XARF) is a standard for reporting abuse incidents in a structured, machine-readable format. XARF v4 introduces a category-based architecture with seven main abuse categories and enhanced evidence handling.

## 📚 Documentation

- **[Introduction & Overview](docs/introduction.md)** - High-level overview and use cases
- **[Technical Specification](docs/specification.md)** - Complete technical reference
- **[Implementation Guide](docs/implementation-guide.md)** - Deployment and project management
- **[JSON Schemas](schemas/)** - Formal validation schemas for all XARF v4 categories and event types

## 🗂️ Seven Abuse Categories

XARF v4 organizes all abuse reports into seven main categories:

1. **messaging** - Communication abuse (email spam, SMS, chat)
2. **connection** - Network attacks (DDoS, port scans, login attacks)
3. **content** - Malicious web content (phishing, malware sites, defacement)
4. **infrastructure** - Compromised systems (botnets, C2, compromised servers)
5. **copyright** - IP infringement (DMCA, trademark violations)
6. **vulnerability** - Security vulnerabilities (CVE reports, misconfigurations)
7. **reputation** - Threat intelligence (blocklist entries, IOC data)

### Event Types by Category

Each category contains multiple specific event types with dedicated schemas:

| Category | Event Types | Schema Location |
|-------|-------------|-----------------|
| **messaging** | `spam`, `bulk_messaging` | [`schemas/v4/types/messaging-*.json`](schemas/v4/types/) |
| **connection** | `login_attack`, `port_scan`, `ddos`, `infected_host`, `sql_injection`, `vuln_scanning`, `reconnaissance`, `scraping` | [`schemas/v4/types/connection-*.json`](schemas/v4/types/) |
| **vulnerability** | `cve`, `open`, `misconfiguration` | [`schemas/v4/types/vulnerability-*.json`](schemas/v4/types/) |
| **content** | `phishing`, `malware`, `fraud`, `csam`, `csem`, `exposed_data`, `brand_infringement`, `remote_compromise`, `suspicious_registration` | [`schemas/v4/types/content-*.json`](schemas/v4/types/) |
| **infrastructure** | `botnet`, `compromised_server` | [`schemas/v4/types/infrastructure-*.json`](schemas/v4/types/) |
| **reputation** | `blocklist`, `threat_intelligence` | [`schemas/v4/types/reputation-*.json`](schemas/v4/types/) |
| **copyright** | `copyright`, `p2p`, `cyberlocker`, `ugc_platform`, `link_site`, `usenet` | [`schemas/v4/types/copyright-*.json`](schemas/v4/types/) |

## 📄 Sample Reports

Sample reports are organized by version for reference and migration purposes:

```
samples/
├── v4/               # XARF v4 samples - one per schema type (32 total)
│   ├── messaging-spam.json
│   ├── messaging-bulk-messaging.json
│   ├── connection-login-attack.json
│   ├── connection-port-scan.json
│   ├── connection-ddos.json
│   ├── connection-infected-host.json
│   ├── connection-sql-injection.json
│   ├── connection-vuln-scanning.json
│   ├── connection-reconnaissance.json
│   ├── connection-scraping.json
│   ├── content-brand-infringement.json
│   ├── content-fraud.json
│   ├── content-remote-compromise.json
│   ├── content-suspicious-registration.json
│   ├── vulnerability-cve.json
│   ├── vulnerability-open.json
│   ├── vulnerability-misconfiguration.json
│   ├── content-phishing.json
│   ├── content-malware.json
│   ├── content-csam.json
│   ├── content-csem.json
│   ├── content-exposed-data.json
│   ├── infrastructure-botnet.json
│   ├── infrastructure-compromised-server.json
│   ├── reputation-blocklist.json
│   ├── reputation-threat-intelligence.json
│   ├── copyright-copyright.json
│   ├── copyright-p2p.json
│   ├── copyright-cyberlocker.json
│   ├── copyright-ugc-platform.json
│   ├── copyright-link-site.json
│   └── copyright-usenet.json
└── v3/               # XARF v3 samples (legacy format, migration reference)
    ├── spam_v3_sample.json
    ├── ddos_v3_sample.json
    ├── phishing_v3_sample.json
    └── botnet_v3_sample.json
```

## 🚀 Quick Start

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

## 🔧 Parser Libraries

- **Python**: [xarf-python](https://github.com/xarf/xarf-python) (Alpha)
- **JavaScript**: Coming soon
- **Go**: Coming soon

## 🌐 XARF v3 Compatibility

XARF v4 maintains backward compatibility with v3 reports. See our [migration guide](docs/specification.md#xarf-v3-migration) for details.

## 📊 Schema Structure

```json
{
  "xarf_version": "4.0.0",
  "report_id": "uuid-v4",
  "timestamp": "2024-01-01T12:00:00Z",
  "reporter": {
    "org": "Example Security",
    "contact": "abuse@example.com",
    "domain": "example.com",
    "type": "automated|manual|hybrid"
  },
  "sender": {
    "org": "Example Security",
    "contact": "abuse@example.com",
    "domain": "example.com"
  },
  "source_identifier": "192.0.2.1",
  "category": "messaging|connection|content|infrastructure|copyright|vulnerability|reputation",
  "type": "specific_type_per_category",
  "evidence_source": "spamtrap|honeypot|user_report|automated_scan|manual_analysis",
  "evidence": [
    {
      "content_type": "text/plain|image/png|application/pdf|message/rfc822",
      "description": "Human-readable evidence description",
      "payload": "base64_encoded_evidence_data"
    }
  ],
  "tags": ["structured:tagging", "for:classification"],
  "_internal": {
    "source_system": "system_identifier",
    "custom": "organization_specific_metadata"
  }
}
```

## 🤝 Contributing

XARF v4 is an open standard. We welcome contributions from the security community:

- **Issues**: Report bugs or suggest improvements
- **Samples**: Contribute anonymized real-world examples
- **Documentation**: Help improve clarity and completeness
- **Parsers**: Implement XARF support in new languages

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

## 🔗 Links

- **Website**: https://xarf.org
- **GitHub**: https://github.com/xarf
- **Specification**: v4.0.0 (Alpha)