# XARF v4: Introduction & Overview

## What is XARF v4?

XARF (eXtended Abuse Reporting Format) v4 represents a fundamental evolution from simple abuse reporting to comprehensive abuse intelligence. It transforms XARF from a basic JSON schema into a modern, type-specific abuse reporting platform that bridges the gap between automated tools and threat intelligence systems.

XARF v4 is designed for **real-time operational response** - helping ISPs, hosting providers, and network operators quickly understand and act on abuse reports, rather than serving as a research or analysis format.

## Why XARF v4 Matters

### The Problem
The cybersecurity industry processes millions of abuse reports daily, but current formats are inadequate:

- **v3 XARF** is too simplistic for modern threat landscape
- **Custom formats** create integration overhead for every tool
- **Email-only delivery** limits automation and real-time response
- **Static schemas** can't adapt to new abuse types
- **Manual processing** creates delays that allow abuse to continue

### The Solution
XARF v4 addresses these challenges with:

- **Type-specific architecture** that scales with new abuse types
- **Automation-first design** for immediate machine processing
- **Multi-transport support** (email, API, streaming)
- **Evidence-based reporting** with actionable proof
- **Backwards compatibility** for seamless migration

## Key Improvements Over v3

### Architectural Evolution

| **v3 Approach** | **v4 Approach** | **Benefit** |
|-----------------|-----------------|-------------|
| Simple Types | Type-Specific Architecture (22 types) | Granular categorization |
| Static Schema | Type-Specific Validation | Flexible yet structured |
| Basic Fields | Rich Attribution & Tags | Better context and automation |
| Email-Only | Multi-Transport (email, API, streaming) | Real-time processing |
| Manual Processing | Automation-First Design | Immediate response |

### Real-Time Philosophy

XARF v4 is built around the principle: **One incident = One report**, sent immediately when detected.

- **No bundling** multiple incidents together
- **No daily batching** or delayed reporting  
- **Exception**: Threshold-based reporting (e.g., wait for >5 login attempts before reporting brute force)
- **Goal**: Minimize time between abuse detection and ISP notification

## Core Concepts

### Seven Abuse Classes

XARF v4 organizes all abuse into seven primary classes, each with specific types and evidence requirements:

1. **`messaging`** - Communication abuse (spam, bulk messaging)
   - *Examples*: Email spam, SMS spam, chat abuse
   - *Evidence*: Original messages, headers, content samples

2. **`connection`** - Network attacks (login attacks, DDoS, scans)
   - *Examples*: Brute force attacks, port scans, DDoS traffic
   - *Evidence*: Attack logs, connection attempts, traffic analysis

3. **`infrastructure`** - Service abuse (C2 servers, compromised services)
   - *Examples*: Botnet infections, compromised servers, C2 communications
   - *Evidence*: Traffic analysis, service fingerprints, behavioral indicators

4. **`content`** - Web content abuse (phishing, malware hosting)
   - *Examples*: Phishing sites, malware downloads, fraudulent content
   - *Evidence*: Screenshots, webpage samples, file hashes

5. **`copyright`** - IP infringement (replaces ACNS format)
   - *Examples*: P2P sharing, direct downloads, trademark violations
   - *Evidence*: DMCA notices, torrent metadata, infringing content

6. **`vulnerability`** - Security disclosures (CVEs, misconfigurations)
   - *Examples*: Open services, unpatched systems, security weaknesses
   - *Evidence*: Vulnerability scans, CVE references, proof-of-concept

7. **`reputation`** - Threat intelligence & reputation
   - *Examples*: Blocklist entries, IP reclamation, threat indicators
   - *Evidence*: Intelligence feeds, analysis reports, attribution data

### Evidence-Based Reporting

Every XARF v4 report includes actionable evidence:

- **Structured evidence** with MIME types and descriptions
- **Base64 encoding** for binary content (screenshots, files)
- **Size limits** (5MB per item, 15MB total per report)
- **Hash verification** for evidence integrity
- **Context metadata** (timestamps, source quality indicators)

### Source-Centric Design

XARF v4 focuses on answering: **"What did this IP/domain do wrong?"**

- **Clear attribution** to specific sources (IP addresses, domains)
- **Port information** critical for CGNAT environments
- **Protocol details** for network-based abuse
- **Timeline context** for incident correlation

## Use Cases & Benefits

### For ISPs & Hosting Providers

**What you get:**
- **Standardized intake** format reduces custom parser development
- **Automated processing** enables immediate response workflows
- **Clear evidence** supports customer communication and legal requirements
- **Backwards compatibility** allows gradual migration from v3

**Common integration:**
```
XARF v4 Report → Parser → Ticket System → Automated Response
```

### For Security Researchers & Tools

**What you get:**
- **Rich context** for campaign tracking and attribution
- **Flexible evidence** format supports any content type
- **Tag system** for classification and correlation
- **Multi-language libraries** (Python, JavaScript, Go, PHP, Java, Rust)

**Common use cases:**
- Honeypot and spamtrap reporting
- Malware sandbox integration
- SIEM and log analysis tools
- Threat intelligence platforms

### For Tool Developers

**What you get:**
- **Comprehensive libraries** handle parsing, validation, and conversion
- **Clear specifications** reduce development time
- **Active community** provides support and examples
- **Forward compatibility** protects against future changes

**Integration examples:**
- fail2ban XARF output plugin
- Log analyzer XARF generators  
- Security tool report export
- Custom abuse response systems

## Getting Started

### 1. Understand the Fit

**XARF v4 is ideal for:**
- High-volume automated abuse reporting (1000s/day+)
- Real-time operational response workflows
- Multi-transport delivery requirements
- Complex evidence sharing needs

**Consider alternatives if:**
- You only send a few reports per month manually
- You need advanced threat intelligence correlation
- You require proprietary or classified information sharing

### 2. Evaluate with Samples

Review sample reports for your use case:
- **Spam reports**: `samples/v4/messaging-spam.json`
- **Phishing reports**: `samples/v4/content-phishing.json` 
- **DDoS reports**: `samples/v4/connection-ddos.json`

All samples available in the [Technical Specification](./specification.md#sample-reports).

### 3. Test Integration

**For report receivers (ISPs, hosting providers):**
1. Install parser library: `pip install xarf-parser` or `npm install @xarf/parser`
2. Test with sample v4 reports
3. Validate backwards compatibility with existing v3 reports
4. Begin dual-format processing

**For report senders (security tools, researchers):**
1. Install generator library: `pip install xarf-parser` or `npm install @xarf/parser`
2. Generate test reports for your abuse types
3. Validate output with provided samples
4. Implement delivery mechanisms (email, API, etc.)

### 4. Production Integration

See the [Implementation Guide](./implementation-guide.md) for:
- Complete integration patterns
- Performance optimization guidelines
- Error handling best practices
- Community support resources

## Architecture Overview

### Schema Structure

```json
{
  "xarf_version": "4.0.0",
  "report_id": "uuid-v4",
  "timestamp": "2024-01-01T12:00:00Z",
  "reporter": {
    "org": "Example Security",
    "contact": "abuse@example.com", 
    "type": "automated"
  },
  "source_identifier": "192.0.2.1",
  "class": "messaging",
  "type": "spam",
  "evidence": [...],
  "tags": ["malware:conficker", "campaign:winter2024"]
}
```

**Key design principles:**
- **Required fields**: Only essential information for abuse response
- **Optional enrichment**: Tags, confidence scores, additional context
- **Forward compatibility**: Unknown fields are preserved but ignored
- **Validation**: JSON Schema-based with type-specific rules

### Backwards Compatibility

XARF v4 maintains complete compatibility with v3:

- **Automatic conversion**: v4 parsers process v3 reports transparently
- **Dual generation**: Tools can output both formats during migration
- **Migration tools**: Batch conversion utilities for existing report databases
- **Gradual adoption**: No forced migration timeline

### Version Evolution

```
v4.0.0: Initial release with messaging class
v4.1.0: Add connection class (login attacks, DDoS)
v4.2.0: Add content class (phishing, malware)
v4.3.0: Add infrastructure class (botnets, C2)
v4.4.0: Add copyright class (DMCA replacement)
v4.5.0: Add vulnerability class (security disclosures)
v4.6.0: Add reputation class (threat intelligence)
v5.0.0: Breaking changes (years in future)
```

## Next Steps

### For Technical Implementation

**→ Read the [Technical Specification](./specification.md)**
- Complete JSON schemas for all types
- Field definitions and validation rules
- Evidence format specifications
- Sample reports and test cases
- Implementation requirements for parsers

### For Project Management & Operations

**→ Read the [Implementation Guide](./implementation-guide.md)**  
- Project roadmap and timelines
- Community governance and contribution
- Integration patterns and best practices
- Adoption strategies and support resources
- Infrastructure and development processes

### For Community Involvement

- **GitHub**: https://github.com/xarf/ (specifications, parsers, tools)
- **Issues**: Report bugs, request features, ask questions
- **Discussions**: Architecture decisions, use case feedback
- **Contributing**: Parser development, documentation, samples

---

**XARF v4 transforms abuse reporting from a chore into a competitive advantage.** By providing structured, actionable intelligence in real-time, it enables organizations to respond faster, reduce abuse impact, and build better security operations.

*This document provides the high-level overview. For technical implementation details, see the [Technical Specification](./specification.md). For project management and operational guidance, see the [Implementation Guide](./implementation-guide.md).*