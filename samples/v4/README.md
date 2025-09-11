# XARF v4 Sample Set

This directory contains exactly one representative sample for each of the 22 XARF v4 schema types, providing complete validation coverage with minimal redundancy.

## Coverage

**22 Schema Types → 22 Samples (1:1 mapping)**

### Messaging Class (2 types)
- `messaging-spam.json` → messaging:spam
- `messaging-bulk-messaging.json` → messaging:bulk_messaging

### Connection Class (5 types)  
- `connection-login-attack.json` → connection:login_attack
- `connection-port-scan.json` → connection:port_scan
- `connection-ddos.json` → connection:ddos
- `connection-ddos-amplification.json` → connection:ddos_amplification
- `connection-auth-failure.json` → connection:auth_failure

### Vulnerability Class (3 types)
- `vulnerability-cve.json` → vulnerability:cve
- `vulnerability-open.json` → vulnerability:open
- `vulnerability-misconfiguration.json` → vulnerability:misconfiguration

### Reputation Class (2 types)
- `reputation-blocklist.json` → reputation:blocklist
- `reputation-threat-intelligence.json` → reputation:threat_intelligence

### Infrastructure Class (2 types)
- `infrastructure-bot.json` → infrastructure:bot
- `infrastructure-compromised-server.json` → infrastructure:compromised_server

### Content Class (2 types)
- `content-phishing.json` → content:phishing
- `content-malware.json` → content:malware

### Copyright Class (6 types)
- `copyright-copyright.json` → copyright:copyright
- `copyright-p2p.json` → copyright:p2p
- `copyright-cyberlocker.json` → copyright:cyberlocker
- `copyright-ugc-platform.json` → copyright:ugc_platform
- `copyright-link-site.json` → copyright:link_site
- `copyright-usenet.json` → copyright:usenet

## Usage

These samples are ideal for:
- **Schema validation testing** - Each sample validates against its corresponding schema
- **Integration testing** - Representative data for each abuse type
- **Documentation** - Clear examples of expected data structure
- **CI/CD** - Lightweight test suite with complete coverage

## Generation

This sample set was generated using `scripts/create_minimal_samples.sh`:
- Copied best existing samples for 14 matching types
- Created new samples for 8 missing types
- Ensured all samples match consolidated schema type names
- Validated JSON syntax and structure

## Design Philosophy

This sample set focuses on **schema coverage** and **clarity**:
- One authoritative example per schema type
- No duplicate or legacy samples to avoid confusion
- Clean, well-documented JSON structure
- Perfect for testing, validation, and documentation