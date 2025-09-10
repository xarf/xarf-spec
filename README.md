# XARF v4 Specification

The eXtended Abuse Reporting Format (XARF) is a standard for reporting abuse incidents in a structured, machine-readable format. XARF v4 introduces a class-based architecture with seven main abuse categories and enhanced evidence handling.

## 📚 Documentation

- **[Introduction & Overview](docs/introduction.md)** - High-level overview and use cases
- **[Technical Specification](docs/specification.md)** - Complete technical reference
- **[Implementation Guide](docs/implementation-guide.md)** - Deployment and project management
- **[JSON Schemas](schemas/)** - Formal validation schemas for all XARF v4 classes and event types

## 🗂️ Seven Abuse Classes

XARF v4 organizes all abuse reports into seven main classes:

1. **messaging** - Communication abuse (email spam, SMS, chat)
2. **connection** - Network attacks (DDoS, port scans, login attacks)
3. **content** - Malicious web content (phishing, malware sites, defacement)
4. **infrastructure** - Compromised systems (botnets, C2, compromised servers)
5. **copyright** - IP infringement (DMCA, trademark violations)
6. **vulnerability** - Security vulnerabilities (CVE reports, misconfigurations)
7. **reputation** - Threat intelligence (blocklist entries, IOC data)

### Event Types by Class

Each class contains multiple specific event types with dedicated schemas:

| Class | Event Types | Schema Location |
|-------|-------------|-----------------|
| **messaging** | `spam`, `bulk_messaging` | [`schemas/v4/types/messaging-*.json`](schemas/v4/types/) |
| **connection** | `ddos`, `port_scan`, `login_attack`, `auth_failure`, `ddos_amplification` | [`schemas/v4/types/connection-*.json`](schemas/v4/types/) |
| **vulnerability** | `cve`, `open`, `misconfiguration` | [`schemas/v4/types/vulnerability-*.json`](schemas/v4/types/) |
| **content** | `phishing`, `malware` | [`schemas/v4/types/content-*.json`](schemas/v4/types/) |
| **infrastructure** | `bot`, `compromised_server` | [`schemas/v4/types/infrastructure-*.json`](schemas/v4/types/) |
| **reputation** | `blocklist`, `threat_intelligence` | [`schemas/v4/types/reputation-*.json`](schemas/v4/types/) |
| **copyright** | `copyright` | [`schemas/v4/types/copyright-*.json`](schemas/v4/types/) |

## 📄 Sample Reports

Sample reports are organized by version for reference and migration purposes:

```
samples/
├── v4/               # XARF v4 samples (current specification)
│   ├── messaging/    # Email spam, phishing, social engineering
│   ├── connection/   # DDoS, port scans, login attacks
│   ├── content/      # Phishing sites, malware distribution, defacement
│   ├── infrastructure/ # Compromised servers, botnets, CVE exploitation
│   ├── copyright/    # DMCA violations, trademark infringement
│   ├── vulnerability/ # CVE reports, open services, misconfigurations
│   └── reputation/   # Blocklist entries, threat intelligence
└── v3/               # XARF v3 samples (legacy format, migration reference)
    ├── spam_v3_sample.json
    ├── ddos_v3_sample.json
    ├── phishing_v3_sample.json
    └── botnet_v3_sample.json
```

## 🚀 Quick Start

```bash
# View a sample report
cat samples/v4/messaging/spam_spamtrap_phishing_sample.json

# Validate against type-specific schema (recommended)
ajv validate -s schemas/v4/types/messaging-spam.json -d samples/v4/messaging/spam_sample.json

# Or validate against master schema (validates all types)
ajv validate -s schemas/v4/xarf-v4-master-types.json -d samples/v4/messaging/spam_sample.json
```

## 🔧 Parser Libraries

- **Python**: [xarf-parser-python](https://github.com/xarf/xarf-parser-python) (Alpha)
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
    "type": "automated|manual|hybrid"
  },
  "source_identifier": "192.0.2.1",
  "class": "messaging|connection|content|infrastructure|copyright|vulnerability|reputation",
  "type": "specific_type_per_class",
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