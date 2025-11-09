# XARF v4: Technical Specification

## Table of Contents
1. [Overview](#overview)
2. [Schema Architecture](#schema-architecture)
3. [Core Schema Definition](#core-schema-definition)
4. [Category-Specific Schemas](#category-specific-schemas)
5. [Field Definitions Reference](#field-definitions-reference)
6. [Validation Rules](#validation-rules)
7. [Evidence Specifications](#evidence-specifications)
8. [Backwards Compatibility](#backwards-compatibility)
9. [Sample Reports](#sample-reports)
10. [Implementation Requirements](#implementation-requirements)

## Overview

This document provides the complete technical specification for XARF v4 schema validation, field definitions, and format requirements. It serves as the authoritative reference for implementing XARF v4 parsers, validators, and generators.

For a high-level introduction to XARF v4, see the [Introduction & Overview](./introduction.md). For implementation guidance and project management, see the [Implementation Guide](./implementation-guide.md).

### Design Principles

**Core Philosophy:**
1. **Source-Centric**: Focus on "what did this IP do wrong" rather than "what attack occurred"
2. **Evidence-Based**: Every report must include actionable evidence
3. **Real-Time First**: Optimized for fast operational response, not research/analysis
4. **Automation-Friendly**: JSON first, email is just transport
5. **Backwards Compatible**: v3 reports should work transparently
6. **Extensible**: Add new types without breaking existing parsers

**Real-Time Reporting Philosophy:**
- **One incident = One report** (immediately when detected)
- **No bundling** multiple incidents together
- **No daily batching** or delayed reporting
- **Exception**: Threshold-based reporting (e.g., wait for >5 login attempts before reporting brute force)
- **Goal**: Minimize time between abuse detection and ISP notification

### Validation Approach

- **JSON Schema based** - Formal validation using JSON Schema Draft 7
- **Conditional validation** - Type-specific requirements based on category/type combinations  
- **Extensible design** - Forward compatibility with unknown fields
- **Multi-level validation** - Strict, permissive, and legacy modes

## Schema Architecture

### Category-Based Design

XARF v4 organizes abuse reports into seven primary categories, each with specific types and validation rules:

| Category | Purpose | Required Fields | Evidence Focus |
|----------|---------|----------------|----------------|
| `messaging` | Communication abuse | `protocol`, `smtp_from`, `subject` | Original messages, headers |
| `connection` | Network attacks | `destination_ip`, `protocol` | Attack logs, connection data |
| `infrastructure` | Compromised systems | None beyond base | Traffic analysis, indicators |
| `content` | Malicious web content | `url` | Screenshots, webpage samples |
| `copyright` | IP infringement | `work_title`, `rights_holder` | DMCA notices, content samples |
| `vulnerability` | Security disclosures | `service` | Vulnerability scans, CVE data |
| `reputation` | Threat intelligence | `threat_type` | Intelligence feeds, analysis |

### Operational Context

Different abuse categories target different infrastructure layers and require distinct response procedures:

**Infrastructure Layer Targeting:**
- **Client-side abuse** (`infrastructure.bot`) → End-user ISP remediation and quarantine
- **Server-side abuse** (`infrastructure.compromised_server`) → Hosting provider hardening and patching
- **Content-side abuse** (`content.phishing`, `content.fraud`) → Content takedown by hosting provider

**ISP Action Categories:**
1. **Immediate blocking** → Login attacks, active DDoS traffic
2. **Content takedown** → Phishing sites, copyright infringement, spamvertised content
3. **Client remediation** → Bot infections, compromised end-user systems
4. **Infrastructure hardening** → Vulnerable services, compromised servers, CVE patching

## Core Schema Definition

### Attribute Categorization

XARF v4 uses a three-tier system for attribute categorization to provide clear implementation guidance:

1. **Required Attributes**: Must be present for valid XARF reports
2. **Recommended Attributes**: Should be included when available to improve report utility
3. **Optional Attributes**: May be included for additional context or specific use cases

This categorization helps implementers prioritize which fields to support while maintaining interoperability.

### Base Report Structure

All XARF v4 reports share this common structure:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": [
    "xarf_version",
    "report_id",
    "timestamp",
    "reporter",
    "source_identifier",
    "category",
    "type"
  ],
  "properties": {
    "xarf_version": {
      "type": "string",
      "pattern": "^4\\.[0-9]+\\.[0-9]+$",
      "description": "XARF schema version (semantic versioning)"
    },
    "report_id": {
      "type": "string",
      "format": "uuid",
      "description": "Unique report identifier (UUID v4)"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "When the abuse occurred (ISO 8601)"
    },
    "reporter": {
      "$ref": "#/definitions/reporter"
    },
    "source_identifier": {
      "type": "string",
      "description": "IP address, domain, or identifier of abuse source"
    },
    "source_port": {
      "type": "integer",
      "minimum": 1,
      "maximum": 65535,
      "description": "Source port (critical for CGNAT networks)"
    },
    "category": {
      "type": "string",
      "enum": ["messaging", "content", "copyright", "connection", "vulnerability", "infrastructure", "reputation"]
    },
    "type": {
      "type": "string",
      "description": "Specific abuse type within class"
    },
    "evidence_source": {
      "type": "string",
      "description": "Quality/reliability indicator for evidence"
    },
    "evidence": {
      "type": "array",
      "items": { "$ref": "#/definitions/evidence_item" }
    },
    "tags": {
      "type": "array",
      "items": {
        "type": "string",
        "pattern": "^[a-z0-9_]+:[a-z0-9_]+$"
      },
      "description": "Namespaced tags for categorization"
    },
    "_internal": {
      "$ref": "#/definitions/internal_metadata",
      "description": "Internal metadata for operational use - NOT transmitted"
    }
  }
}
```

### Common Definitions

```json
{
  "definitions": {
    "reporter": {
      "type": "object",
      "required": ["org", "contact", "type"],
      "properties": {
        "org": {
          "type": "string",
          "description": "Reporting organization name"
        },
        "contact": {
          "type": "string",
          "format": "email",
          "description": "Contact email for follow-up"
        },
        "type": {
          "type": "string",
          "enum": ["automated", "manual", "unknown"],
          "description": "How this report was generated"
        },
        "reporter_reference_id": {
          "type": "string",
          "description": "Reporter's internal ticket/case ID for correlation and follow-up"
        }
      }
    },
    "evidence_item": {
      "type": "object",
      "required": ["content_type", "payload"],
      "properties": {
        "content_type": {
          "type": "string",
          "description": "MIME type of evidence"
        },
        "description": {
          "type": "string",
          "description": "Human-readable evidence description"
        },
        "payload": {
          "type": "string",
          "description": "Base64-encoded evidence data"
        },
        "hash": {
          "type": "string",
          "pattern": "^(md5|sha1|sha256|sha512):[a-fA-F0-9]+$",
          "description": "Primary hash of evidence for integrity (deprecated - use hashes array)"
        },
        "hashes": {
          "type": "array",
          "items": {
            "type": "string",
            "pattern": "^(md5|sha1|sha256|sha512):[a-fA-F0-9]+$"
          },
          "description": "Array of file hashes using multiple algorithms (e.g., ['md5:abc123', 'sha256:def456'])"
        },
        "size": {
          "type": "integer",
          "minimum": 0,
          "description": "Size of evidence in bytes"
        }
      }
    },
    "internal_metadata": {
      "type": "object",
      "description": "Internal operational metadata - NEVER transmitted, for local use only",
      "additionalProperties": true
    }
  }
}
```

## Category-Specific Schemas

### 1. Messaging Category

**Purpose:** Communication-based abuse including spam and unwanted messaging

**Valid Types:** `spam`, `bulk_messaging`

**Evidence Sources:** `spamtrap`, `user_complaint`, `automated_filter`, `honeypot`

**Class-Specific Fields:**

| Field | Category | Type | Description | Condition |
|-------|----------|------|-------------|-----------|
| `protocol` | **Required** | enum | Communication protocol used | Always |
| `smtp_from` | **Required** | email | SMTP envelope sender | When protocol=smtp |
| `subject` | **Required** | string | Message subject line | When protocol=smtp |
| `message_id` | **Recommended** | string | Message identifier | Helps deduplication |
| `recipient` | **Recommended** | email | Target recipient | Improves tracking |
| `headers` | **Optional** | object | Additional headers | Advanced analysis |
| `body_hash` | **Optional** | string | Message body hash | Duplicate detection |

**Schema Definition:**
```json
{
  "properties": {
    "protocol": {
      "type": "string",
      "enum": ["smtp", "sms", "whatsapp", "telegram", "signal", "chat", "social_media"],
      "description": "Communication protocol used"
    },
    "smtp_from": {
      "type": "string",
      "format": "email",
      "description": "SMTP envelope sender"
    },
    "subject": {
      "type": "string",
      "description": "Message subject line"
    },
    "message_id": {
      "type": "string",
      "description": "Message identifier for tracking"
    },
    "recipient": {
      "type": "string",
      "format": "email",
      "description": "Target recipient address"
    }
  },
  "required": ["protocol"],
  "if": {
    "properties": { "protocol": { "const": "smtp" } }
  },
  "then": {
    "required": ["smtp_from", "subject"]
  }
}
```

**Example:**
```json
{
  "xarf_version": "4.0.0",
  "report_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2024-01-01T12:00:00Z",
  "reporter": {
    "org": "Example Security",
    "contact": "abuse@example.com",
    "type": "automated",
    "reporter_reference_id": "TICKET-2024-001"
  },
  "source_identifier": "192.0.2.1",
  "source_port": 25,
  "category": "messaging",
  "type": "spam",
  "protocol": "smtp",
  "smtp_from": "spam@example.com",
  "subject": "Buy now!",
  "evidence_source": "spamtrap",
  "evidence": [
    {
      "content_type": "message/rfc822",
      "description": "Original spam email",
      "payload": "base64-encoded-email-content"
    }
  ],
  "tags": ["malware:conficker", "campaign:winter2024"],
  "confidence": 0.95
}
```

### 2. Content Category

**Purpose:** Malicious web content including phishing, malware, fraud, exploitation, and harmful content

**Valid Types:** `phishing`, `malware`, `fraud`, `spamvertised`, `csam`, `defacement`, `illegal_advertisement`, `web_hack`, `exploit`, `violence`, `harassment`, `doxing`, `ncii`, `fake_shop`, `hate_speech`, `terrorism`, `self_harm`, `identity_theft`, `pharma_fraud`, `illicit_goods`, `online_predation`, `carding`, `gambling_scam`, `threat_to_life`, `disinformation`

**Evidence Sources:** `crawler`, `user_report`, `automated_scan`, `spam_analysis`

**Evidence Recommendations:**
- **Screenshot strongly recommended** for most content types (except `csam` and `ncii` where screenshots may not be appropriate)
- PNG format preferred for web content screenshots
- Include both screenshot and HTML source when possible

**Class-Specific Fields:**

| Field | Category | Type | Description | Use Case |
|-------|----------|------|-------------|----------|
| `url` | **Required** | uri | URL of malicious content | Always |
| `target_brand` | **Recommended** | string | Brand being impersonated | Phishing, fake shops |
| `file_hash` | **Recommended** | string | Hash of malicious file | Malware detection |
| `malware_family` | **Recommended** | string | Malware family name | When type=malware |
| `file_size` | **Optional** | integer | Size of file in bytes | File tracking |
| `redirect_chain` | **Optional** | array | URL redirect sequence | Advanced tracking |
| `hosting_provider` | **Optional** | string | Hosting service identifier | Takedown routing |
| `victim_count` | **Optional** | integer | Number of known victims | CSAM, NCII cases |
| `takedown_urgency` | **Optional** | string | Urgency level (critical/high/medium/low) | CSAM, NCII, terrorism |
| `target_demographic` | **Optional** | string | Targeted group/community | Hate speech, harassment |
| `extremist_group` | **Optional** | string | Associated extremist organization | Terrorism content |
| `payment_methods` | **Optional** | array | Accepted payment types | Fake shops, fraud |
| `substance_type` | **Optional** | string | Type of controlled substance | Illicit goods |
| `card_bin` | **Optional** | string | Bank identification number | Carding markets |
| `stolen_credentials_count` | **Optional** | integer | Number of compromised credentials | Identity theft |
| `pharmaceutical_type` | **Optional** | string | Type of unregulated medicine | Pharma fraud |
| `victim_age_range` | **Optional** | string | Age range of victims | Online predation, CSAM |
| `threat_level` | **Optional** | string | Assessed threat severity | Threat to life, violence |
| `disinformation_campaign` | **Optional** | string | Campaign identifier | Disinformation |
| `coordination_indicators` | **Optional** | array | Evidence of coordinated activity | Disinformation |
| `geolocation` | **Optional** | string | Geographic location where content was accessible or accessed from (ISO country code or lat/long) | Market-specific phishing, geo-restricted content |
| `device` | **Optional** | string | Device type used to access content (mobile, desktop, tablet) | Device-specific phishing/malware |
| `user_agent` | **Optional** | string | User-Agent string used when accessing content | Browser/client fingerprinting |
| `referrer` | **Optional** | string | HTTP Referrer header value | Track content access patterns |
```

### 3. Copyright Category

**Purpose:** Intellectual property infringement including DMCA and trademark violations

**Valid Types:** `copyright`, `trademark`

**Evidence Sources:** `automated_scan`, `rights_holder_report`, `crawler`

**Class-Specific Fields:**

| Field | Category | Type | Description | Context |
|-------|----------|------|-------------|---------|
| `work_title` | **Required** | string | Title of copyrighted work | Always |
| `rights_holder` | **Required** | string | Copyright/trademark holder | Always |
| `infringing_url` | **Recommended** | uri | URL of infringing content | Web-based infringement |
| `work_identifier` | **Recommended** | string | External ID (IMDB, ISBN) | Helps identification |
| `torrent_hash` | **Recommended** | string | BitTorrent info hash | P2P sharing cases |
| `file_list` | **Optional** | array | List of infringing files | Detailed evidence |
| `swarm_size` | **Optional** | integer | Peers in torrent swarm | P2P metrics |
| `tracker_urls` | **Optional** | array | BitTorrent tracker URLs | P2P infrastructure |
```

### 4. Connection Category

**Purpose:** Network-level attacks and unauthorized connection attempts

**Valid Types:** `login_attack`, `port_scan`, `ddos`, `ddos_amplification`, `auth_failure`, `ip_spoof`

**Evidence Sources:** `honeypot`, `firewall_logs`, `ids_detection`, `flow_analysis`

**Class-Specific Fields:**

| Field | Category | Type | Description | Context |
|-------|----------|------|-------------|---------|
| `destination_ip` | **Required** | ip | Target IP address | Always |
| `protocol` | **Required** | enum | Network protocol (tcp/udp/icmp) | Always |
| `destination_port` | **Recommended** | integer | Target port number | TCP/UDP attacks |
| `attempt_count` | **Recommended** | integer | Number of attempts | Brute force detection |
| `service` | **Recommended** | string | Target service (ssh, rdp) | Service-specific |
| `username` | **Optional** | string | Attempted username | Login attacks |
| `threshold_exceeded` | **Optional** | string |
      "format": "date-time",
      "description": "When threshold was exceeded"
    },
    "attack_vector": {
      "type": "string",
      "description": "Specific attack method used"
    },
    "packet_count": {
      "type": "integer",
      "minimum": 0,
      "description": "Number of packets sent"
    },
    "byte_count": {
      "type": "integer", 
      "minimum": 0,
      "description": "Number of bytes transferred"
    }
  },
  "required": ["destination_ip", "protocol"]
}
```

### 5. Vulnerability Category

**Purpose:** Security vulnerabilities and misconfigurations requiring patching

**Valid Types:** `open`, `cve`, `outdated_dnssec`, `ssl_freak`, `ssl_poodle`, `malicious_activity`

**Evidence Sources:** `vulnerability_scan`, `researcher_analysis`, `automated_discovery`

**Class-Specific Fields:**

| Field | Category | Type | Description | Context |
|-------|----------|------|-------------|---------|
| `service` | **Required** | string | Vulnerable service name | Always |
| `service_version` | **Recommended** | string | Service version | Patch identification |
| `cve_id` | **Recommended** | string | CVE identifier | When applicable |
| `cvss_score` | **Recommended** | number | CVSS score (0-10) | Risk assessment |
| `service_port` | **Optional** | integer | Service port | Service location |
| `exploit_available` | **Optional** | boolean | Public exploit exists | Urgency indicator |
| `patch_available` | **Optional** | boolean | Patch is available | Remediation info |
    "cvss_vector": {
      "type": "string",
      "pattern": "^CVSS:3\\.[01]/.*",
      "description": "CVSS vector string"
    },
    "risk_level": {
      "type": "string",
      "enum": ["low", "medium", "high", "critical"],
      "description": "Risk assessment level"
    },
    "patch_available": {
      "type": "boolean",
      "description": "Whether patch is available"
    }
  },
  "required": ["service"]
}
```

### 6. Infrastructure Category

**Purpose:** Compromised systems and malware infections

**Valid Types:** `bot`, `compromised_server`, `compromised_website`, `compromised_account`, `compromised_microsoft_exchange`, `cve`

**Evidence Sources:** `researcher_analysis`, `automated_discovery`, `traffic_analysis`

**Class-Specific Fields:**

| Field | Category | Type | Description | Context |
|-------|----------|------|-------------|---------|
| `malware_family` | **Recommended** | string | Malware family name | Bot/malware cases |
| `c2_server` | **Recommended** | string | Command & control server | Bot infections |
| `first_seen` | **Recommended** | datetime | First observation | Tracking duration |
| `last_seen` | **Recommended** | datetime | Last observation | Current activity |
| `infection_vector` | **Optional** | string | How system was compromised | Root cause |
| `bot_id` | **Optional** | string | Bot identifier | Bot tracking |
| `compromised_service` | **Optional** | string | Affected service | Service-specific |
```

### 7. Reputation Category

**Purpose:** Threat intelligence and reputation-based blocking

**Valid Types:** `blocklist`, `ip_reclamation`, `trap`

**Evidence Sources:** `threat_intelligence`, `automated_analysis`, `researcher_analysis`

**Class-Specific Fields:**

| Field | Category | Type | Description | Context |
|-------|----------|------|-------------|---------|
| `threat_type` | **Required** | string | Category of threat | Always |
| `confidence_score` | **Recommended** | number | Confidence (0-100) | Trust level |
| `first_reported` | **Recommended** | datetime | First threat report | Historical context |
| `sources` | **Recommended** | array | Information sources | Attribution |
| `asn` | **Optional** | integer | Autonomous System Number | Network context |
| `geographic_location` | **Optional** | string | ISO country code | Geo-location |
| `threat_indicators` | **Optional** | array | Specific IoCs | Detailed evidence |
```

## Field Definitions Reference

### Field Categories

#### Required Fields
These fields MUST be present in all valid XARF v4 reports:

| Field | Type | Format | Description |
|-------|------|--------|-------------|
| `xarf_version` | string | `^4\.[0-9]+\.[0-9]+$` | XARF schema version |
| `report_id` | string | UUID v4 | Unique report identifier |
| `timestamp` | string | ISO 8601 | When abuse occurred |
| `source_identifier` | string | IP/domain | Abuse source identifier |
| `category` | string | enum | Primary abuse category |
| `type` | string | varies | Specific abuse type |
| `reporter` | object | - | Reporting organization info |

#### Recommended Fields
These fields SHOULD be included when the information is available:

| Field | Type | Format | Description | Rationale |
|-------|------|--------|-------------|-----------|
| `source_port` | integer | 1-65535 | Source port | Critical for CGNAT environments |
| `evidence` | array | - | Structured evidence items | Enables automated validation |
| `confidence` | number | 0.0-1.0 | Confidence score | Helps prioritize response |
| `evidence_source` | string | varies | Evidence quality indicator | Improves trust assessment |

#### Optional Fields
These fields MAY be included for additional context:

| Field | Type | Format | Description | Use Case |
|-------|------|--------|-------------|----------|
| `tags` | array | `namespace:value` | Categorization tags | Advanced filtering/routing |
| `custom_fields` | object | - | Organization-specific data | Internal workflows |
| `references` | array | URL | Related resources | Additional context |
| `severity` | string | enum | Impact assessment | Priority handling |

### Reporter Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `org` | string | Yes | Organization name |
| `contact` | string | Yes | Email for follow-up |
| `type` | string | Yes | `automated`, `manual`, `unknown` |
| `reporter_reference_id` | string | No | Reporter's internal ticket/case ID for correlation |

### Evidence Item Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `content_type` | string | Yes | MIME type |
| `payload` | string | Yes | Base64-encoded data |
| `description` | string | No | Human-readable description |
| `hash` | string | No | Single integrity hash (deprecated - use hashes) |
| `hashes` | array | No | Array of hashes with multiple algorithms (e.g., `["md5:abc123", "sha256:def456"]`) |
| `size` | integer | No | Size in bytes |

## Validation Rules

### Core Validation Requirements

1. **Required Field Validation**
   - All base required fields must be present
   - Category-specific required fields must be present based on category value
   - Field types must match schema definitions

2. **Format Validation**
   - `report_id`: Valid UUID v4 format
   - `timestamp`: ISO 8601 date-time format with timezone
   - Email addresses: RFC 5322 compliant
   - URLs: RFC 3986 compliant
   - IP addresses: Valid IPv4 or IPv6 format

3. **Conditional Validation**
   - Evidence items must have valid MIME types
   - Tags must follow `namespace:value` pattern using lowercase alphanumeric and underscore
   - Hash values must match specified algorithm format (`algorithm:hexvalue`)
   - Category-specific required fields validated based on category value

4. **Size Constraints**
   - Individual evidence items: ≤ 5MB
   - Total evidence per report: ≤ 15MB
   - String fields: reasonable length limits (typically 1000 characters)
   - Array fields: reasonable item limits (typically 100 items)

### Validation Levels

**Strict Mode:**
- Fail on any unknown fields
- Require all **Required** and **Recommended** fields
- Enforce strict format validation
- Reject reports missing recommended fields

**Standard Mode (Default):**
- Require all **Required** fields
- Warn when **Recommended** fields are missing
- Allow **Optional** fields
- Validate known fields, warn on unknown fields

**Permissive Mode:**
- Require only **Required** fields
- No warnings for missing **Recommended** fields
- Allow unknown fields for forward compatibility
- Suitable for gradual adoption

**Legacy Mode:**
- Accept v3 format reports
- Convert to v4 structure automatically
- Generate warnings for deprecated patterns
- Map v3 fields to appropriate v4 categories

### Tag Namespace Validation

**Standard Namespaces:**
- `malware:family_name` - Malware family classification
- `campaign:identifier` - Campaign tracking
- `cve:CVE-YYYY-NNNN` - CVE references
- `botnet:name` - Botnet identification
- `severity:level` - Severity classification
- `confidence:level` - Confidence assessment
- `tool:name` - Reporting tool identification
- `custom:value` - Organization-specific tags

## Evidence Specifications

### Supported Content Types

**Text Evidence:**
- `text/plain` - Log entries, configuration files, command output
- `text/csv` - Structured data exports
- `application/json` - JSON-formatted data

**Message Evidence:**
- `message/rfc822` - Complete email messages with headers
- `text/email` - Email fragments or processed content

**Image Evidence:**
- `image/png` - Screenshots (preferred for web content)
- `image/jpeg` - Photos, screenshots
- `image/gif` - Animated content or screenshots

**Document Evidence:**
- `application/pdf` - Reports, documentation
- `text/html` - Webpage snapshots

**Binary Evidence:**
- `application/octet-stream` - Malware samples, unknown binaries
- `application/zip` - Archive files (must be password protected)

### Encoding Requirements

**Base64 Encoding:**
- All evidence payloads must be valid base64 encoded
- No line breaks or whitespace in encoding
- Proper padding required
- Use standard base64 alphabet (RFC 4648)

**Size Management:**
- Compress large text evidence before encoding
- Use screenshots instead of full webpage HTML when possible
- Truncate log files to relevant portions
- Consider external reference for very large evidence

### Evidence Best Practices

**For Messaging Class:**
```json
{
  "evidence": [
    {
      "content_type": "message/rfc822",
      "description": "Original spam email with full headers",
      "payload": "base64-encoded-email"
    }
  ]
}
```

**For Content Class:**
```json
{
  "evidence": [
    {
      "content_type": "image/png", 
      "description": "Screenshot of phishing page",
      "payload": "base64-encoded-screenshot",
      "hash": "sha256:abcd1234..."
    },
    {
      "content_type": "text/html",
      "description": "HTML source of phishing page", 
      "payload": "base64-encoded-html"
    }
  ]
}
```

**For Connection Class:**
```json
{
  "evidence": [
    {
      "content_type": "text/plain",
      "description": "Failed authentication log entries",
      "payload": "base64-encoded-logs"
    }
  ]
}
```

## Backwards Compatibility

### Automatic v3 to v4 Conversion

XARF v4 parsers must support automatic conversion of v3 reports. The conversion process:

1. **Detect Format**: Check for `Version` field (v3) vs `xarf_version` field (v4)
2. **Generate UUID**: Create new UUID v4 for `report_id`
3. **Map Fields**: Convert v3 structure to v4 structure
4. **Add Metadata**: Include `legacy_version: "3"` field
5. **Convert Evidence**: Map `Samples` array to `evidence` format

**Conversion Example:**

```json
// v3 Input
{
  "Version": "3",
  "ReporterInfo": {
    "ReporterOrg": "Example Security",
    "ReporterOrgEmail": "abuse@example.com"
  },
  "Report": {
    "ReportClass": "Activity", 
    "ReportType": "Spam",
    "SourceIp": "192.0.2.1",
    "SourcePort": 25,
    "Date": "2024-01-01T12:00:00Z",
    "SmtpMailFromAddress": "spam@example.com",
    "Samples": [{"ContentType": "message/rfc822", "Payload": "..."}]
  }
}

// v4 Output (auto-converted)
{
  "xarf_version": "4.0.0",
  "report_id": "generated-uuid-v4-here",
  "legacy_version": "3",
  "timestamp": "2024-01-01T12:00:00Z",
  "reporter": {
    "org": "Example Security",
    "contact": "abuse@example.com",
    "type": "unknown"
  },
  "source_identifier": "192.0.2.1",
  "source_port": 25,
  "category": "messaging",
  "type": "spam", 
  "evidence_source": "unknown",
  "protocol": "smtp",
  "smtp_from": "spam@example.com",
  "evidence": [{"content_type": "message/rfc822", "payload": "..."}],
  "tags": []
}
```

### Field Mapping Rules

| v3 Field | v4 Field | Conversion Notes |
|----------|----------|------------------|
| `Version` | `xarf_version` | Set to "4.0.0", add `legacy_version: "3"` |
| `ReporterInfo.ReporterOrg` | `reporter.org` | Direct mapping |
| `ReporterInfo.ReporterOrgEmail` | `reporter.contact` | Direct mapping |
| N/A | `reporter.type` | Set to "unknown" for v3 |
| N/A | `report_id` | Generate new UUID v4 |
| `Report.Date` | `timestamp` | Direct mapping |
| `Report.SourceIp` | `source_identifier` | Direct mapping |
| `Report.SourcePort` | `source_port` | Direct mapping |
| `Report.ReportType` | `category` + `type` | Map to appropriate category/type |
| `Report.Samples` | `evidence` | Convert array structure |

### Migration Strategies

**Dual-Format Processing:**
```
1. Receive report (email/API/stream)
2. Detect format (v3 or v4)
3. If v3: convert to v4 automatically
4. Process with v4 logic
5. Store both original and converted versions
```

**Gradual Migration:**
```
Phase 1: Accept both v3 and v4, process as v4 internally
Phase 2: Generate v4 reports, maintain v3 compatibility
Phase 3: Deprecate v3 support with advance notice
Phase 4: v4-only processing
```

## Sample Reports

Complete sample reports demonstrating proper format for each class:

### Messaging Category -Spam Report
```json
{
  "xarf_version": "4.0.0",
  "report_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2024-01-15T14:30:25Z",
  "reporter": {
    "org": "SpamCop",
    "contact": "reports@spamcop.net",
    "type": "automated",
    "reporter_reference_id": "SC-2024-789012"
  },
  "source_identifier": "192.0.2.123",
  "source_port": 25,
  "category": "messaging",
  "type": "spam",
  "protocol": "smtp",
  "smtp_from": "fake@example.com",
  "subject": "Urgent: Verify Your Account",
  "evidence_source": "spamtrap",
  "evidence": [
    {
      "content_type": "message/rfc822",
      "description": "Complete spam email with headers",
      "payload": "UmVjZWl2ZWQ6IGZyb20gW3NwYW1tZXIuZXhhbXBsZS5jb21dCkZyb206IGZha2VAZXhhbXBsZS5jb20KVG86IHRyYXBAc3BhbWNvcC5uZXQKU3ViamVjdDogVXJnZW50OiBWZXJpZnkgWW91ciBBY2NvdW50CgpDbGljayBoZXJlIHRvIHZlcmlmeSB5b3VyIGFjY291bnQ6IGh0dHA6Ly9ldmlsLmV4YW1wbGUuY29tL3BoaXNoaW5n",
      "hash": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    }
  ],
  "tags": ["campaign:fake_bank_2024", "severity:medium"],
  "confidence": 0.92
}
```

### Content Category -Phishing Report
```json
{
  "xarf_version": "4.0.0",
  "report_id": "123e4567-e89b-12d3-a456-426614174000",
  "timestamp": "2024-01-15T16:45:10Z",
  "reporter": {
    "org": "PhishTank",
    "contact": "admin@phishtank.com",
    "type": "automated",
    "reporter_reference_id": "PT-2024-456789"
  },
  "source_identifier": "203.0.113.45",
  "category": "content",
  "type": "phishing",
  "url": "http://fake-bank.example.com/login.php",
  "target_brand": "Example Bank",
  "geolocation": "US",
  "device": "mobile",
  "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15",
  "referrer": "https://search.example.com/q=bank+login",
  "evidence_source": "crawler",
  "evidence": [
    {
      "content_type": "image/png",
      "description": "Screenshot of phishing page",
      "payload": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==",
      "hash": "sha256:a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3"
    },
    {
      "content_type": "text/html",
      "description": "HTML source of phishing page",
      "payload": "PGh0bWw+PGhlYWQ+PHRpdGxlPkV4YW1wbGUgQmFuayBMb2dpbjwvdGl0bGU+PC9oZWFkPjxib2R5PjxoMT5TZWN1cmUgTG9naW48L2gxPjxmb3JtPjxpbnB1dCB0eXBlPSJ0ZXh0IiBwbGFjZWhvbGRlcj0iVXNlcm5hbWUiPjxpbnB1dCB0eXBlPSJwYXNzd29yZCIgcGxhY2Vob2xkZXI9IlBhc3N3b3JkIj48YnV0dG9uPkxvZ2luPC9idXR0b24+PC9mb3JtPjwvYm9keT48L2h0bWw+"
    }
  ],
  "tags": ["phishing:banking", "target:example_bank"],
  "confidence": 0.98
}
```

### Connection Category -DDoS Report
```json
{
  "xarf_version": "4.0.0",
  "report_id": "987fcdeb-51a2-43d1-9f12-345678901234",
  "timestamp": "2024-01-15T10:20:30Z",
  "reporter": {
    "org": "DDoS Protection Service",
    "contact": "security@ddosprotect.com",
    "type": "automated",
    "reporter_reference_id": "DDOS-INC-20240115-0001"
  },
  "source_identifier": "198.51.100.75",
  "category": "connection",
  "type": "ddos",
  "destination_ip": "203.0.113.100",
  "destination_port": 80,
  "protocol": "tcp",
  "packet_count": 15000,
  "byte_count": 2250000,
  "evidence_source": "flow_analysis",
  "evidence": [
    {
      "content_type": "text/plain",
      "description": "Network flow analysis showing attack pattern",
      "payload": "VGltZXN0YW1wLCBTcmNJUCwgRHN0SUAsIFNyY1BvcnQsIERzdFBvcnQsIFByb3RvY29sLCBQYWNrZXRzLCBCeXRlcwoyMDI0LTAxLTE1VDEwOjIwOjMwWiwgMTk4LjUxLjEwMC43NSwgMjAzLjAuMTEzLjEwMCwgMTIzNCwgODAsIFRDUCwgMTUwMDAsIDIyNTAwMDA="
    }
  ],
  "tags": ["attack:volumetric", "severity:high"],
  "confidence": 0.95
}
```

### Infrastructure Category -Bot Report
```json
{
  "xarf_version": "4.0.0",
  "report_id": "456789ab-cdef-1234-5678-90abcdef1234",
  "timestamp": "2024-01-15T08:15:45Z",
  "reporter": {
    "org": "Botnet Research Group",
    "contact": "research@botnetwatch.org",
    "type": "automated",
    "reporter_reference_id": "BRG-BOT-2024-00234"
  },
  "source_identifier": "192.0.2.200",
  "category": "infrastructure",
  "type": "bot",
  "malware_family": "conficker",
  "c2_server": "evil-c2.example.com",
  "first_seen": "2024-01-10T12:30:00Z",
  "last_seen": "2024-01-15T08:00:00Z",
  "evidence_source": "traffic_analysis",
  "evidence": [
    {
      "content_type": "text/plain",
      "description": "C2 communication logs showing bot activity",
      "payload": "MjAyNC0wMS0xNVQwODowMDowMFogQ29ubmVjdGlvbiB0byBldmlsLWMyLmV4YW1wbGUuY29tOjg0NDMKMjAyNC0wMS0xNVQwODowMToxNVogQm90IElEOiBib3QtMTIzNDU2CjIwMjQtMDEtMTVUMDg6MDE6MzBaIENvbW1hbmQgcmVjZWl2ZWQ6IFVQREFURV9DT05GSUcKMjAyNC0wMS0xNVQwODowMjo0NVogQ29tbWFuZCBleGVjdXRlZCBzdWNjZXNzZnVsbHk="
    }
  ],
  "tags": ["botnet:conficker", "infection:active"],
  "confidence": 0.88
}
```

### Content Category - Malware Distribution Report
```json
{
  "xarf_version": "4.0.0",
  "report_id": "fedcba98-7654-3210-fedc-ba9876543210",
  "timestamp": "2024-01-16T13:45:20Z",
  "reporter": {
    "org": "Malware Analysis Lab",
    "contact": "samples@malware-lab.org",
    "type": "automated",
    "reporter_reference_id": "MAL-2024-9876"
  },
  "source_identifier": "198.51.100.200",
  "category": "content",
  "type": "malware",
  "url": "http://malicious-download.example.com/trojan.exe",
  "malware_family": "emotet",
  "file_hash": "sha256:5d41402abc4b2a76b9719d911017c592",
  "file_size": 245760,
  "evidence_source": "automated_scan",
  "evidence": [
    {
      "content_type": "application/octet-stream",
      "description": "Malware sample (password: infected)",
      "payload": "UEsDBBQACQAIAA... [truncated base64] ...==",
      "hashes": [
        "md5:5d41402abc4b2a76b9719d911017c592",
        "sha1:2fd4e1c67a2d28fced849ee1bb76e7391b93eb12",
        "sha256:d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592",
        "sha512:08f90c1a417155361a5e6b87c99a7c2c4d1f03f4d2b9f5a0c1a2e7f3b4d6a8c9e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0"
      ],
      "size": 245760
    }
  ],
  "tags": ["malware:emotet", "severity:high"],
  "confidence": 0.96
}
```

### Content Category - Fake Shop Report
```json
{
  "xarf_version": "4.0.0",
  "report_id": "def12345-6789-abcd-ef01-234567890abc",
  "timestamp": "2024-01-16T11:20:15Z",
  "reporter": {
    "org": "Consumer Protection Agency",
    "contact": "fraud@consumer-protect.org",
    "type": "manual",
    "reporter_reference_id": "CPA-FAKE-2024-0891"
  },
  "source_identifier": "198.51.100.88",
  "category": "content",
  "type": "fake_shop",
  "url": "http://fake-deals-store.example.com",
  "target_brand": "Major Retailer Brand",
  "payment_methods": ["cryptocurrency", "wire_transfer"],
  "evidence_source": "user_report",
  "evidence": [
    {
      "content_type": "image/png",
      "description": "Screenshot of fake e-commerce storefront",
      "payload": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
      "hash": "sha256:b5bb9d8014a0f9b1d61e21e796d78dccdf1352f23cd32812f4850b878ae4944c"
    }
  ],
  "tags": ["fraud:ecommerce", "severity:high"],
  "confidence": 0.87
}
```

### Content Category - Hate Speech Report
```json
{
  "xarf_version": "4.0.0",
  "report_id": "abc98765-4321-dcba-9876-543210fedcba",
  "timestamp": "2024-01-16T14:55:30Z",
  "reporter": {
    "org": "Online Safety Monitor",
    "contact": "reports@safety-monitor.org",
    "type": "automated",
    "reporter_reference_id": "OSM-HS-2024-3456"
  },
  "source_identifier": "203.0.113.92",
  "category": "content",
  "type": "hate_speech",
  "url": "http://extremist-forum.example.com/thread/12345",
  "target_demographic": "religious minority",
  "takedown_urgency": "high",
  "evidence_source": "automated_scan",
  "evidence": [
    {
      "content_type": "image/png",
      "description": "Screenshot of hateful content",
      "payload": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
      "hash": "sha256:c6b6c6b6c6b6c6b6c6b6c6b6c6b6c6b6c6b6c6b6c6b6c6b6c6b6c6b6c6b6c6b6"
    }
  ],
  "tags": ["content:extremism", "severity:critical"],
  "confidence": 0.91
}
```

### Content Category - Carding Market Report
```json
{
  "xarf_version": "4.0.0",
  "report_id": "789fedcb-a456-7890-1234-567890abcdef",
  "timestamp": "2024-01-16T09:12:45Z",
  "reporter": {
    "org": "Financial Crime Investigation Unit",
    "contact": "cybercrimes@fciu.org",
    "type": "manual",
    "reporter_reference_id": "FCIU-CARD-2024-1122"
  },
  "source_identifier": "198.51.100.135",
  "category": "content",
  "type": "carding",
  "url": "http://dark-market-cards.onion.example.com",
  "card_bin": "411111",
  "stolen_credentials_count": 2500,
  "evidence_source": "researcher_analysis",
  "evidence": [
    {
      "content_type": "image/png",
      "description": "Screenshot of carding marketplace",
      "payload": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==",
      "hash": "sha256:d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5d5"
    }
  ],
  "tags": ["fraud:financial", "severity:critical"],
  "confidence": 0.95
}
```

### Content Category - Disinformation Campaign Report
```json
{
  "xarf_version": "4.0.0",
  "report_id": "321fedcb-9876-5432-10fe-dcba98765432",
  "timestamp": "2024-01-16T16:30:00Z",
  "reporter": {
    "org": "Digital Integrity Alliance",
    "contact": "disinfo@digital-integrity.org",
    "type": "manual",
    "reporter_reference_id": "DIA-DISINFO-2024-7890"
  },
  "source_identifier": "203.0.113.201",
  "category": "content",
  "type": "disinformation",
  "url": "http://fake-news-network.example.com",
  "disinformation_campaign": "election_2024_wave",
  "coordination_indicators": ["identical_posting_times", "shared_imagery", "coordinated_hashtags"],
  "evidence_source": "researcher_analysis",
  "evidence": [
    {
      "content_type": "application/json",
      "description": "Analysis of coordinated posting patterns",
      "payload": "eyJwb3N0X3BhdHRlcm5zIjogWyJ1c2VyMTIzIiwgInVzZXI0NTYiXSwgInRpbWVzdGFtcHMiOiBbIjIwMjQtMDEtMTZUMTY6MDA6MDBaIiwgIjIwMjQtMDEtMTZUMTY6MDA6MDVaIl19",
      "hash": "sha256:e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1"
    }
  ],
  "tags": ["disinfo:election", "coordination:detected"],
  "confidence": 0.83
}
```

## Internal Metadata Usage

### Overview

The `_internal` field provides a completely flexible container for operational metadata that is **NEVER transmitted** between systems. Organizations have complete freedom to define any internal structure needed for their specific operational workflows, integrations, and business processes.

### Key Principles

1. **Never Transmitted**: The `_internal` field must be stripped from all transmitted reports
2. **Complete Freedom**: Organizations define any structure they need for internal operations
3. **No Standards Required**: No predefined fields - use whatever makes sense for your workflow
4. **Operational Focus**: Design internal fields to support your specific processes and integrations

### Use Cases by Organization Type

**Example 1 - Security Research Organization:**
```json
{
  "_internal": {
    "threat_id": "THR-2024-001234", 
    "honeypot_source": "trap_bank_001",
    "campaign_cluster": "fake_bank_wave_2024",
    "ml_confidence": 0.94,
    "analyst_reviewed": false,
    "feed_destinations": ["partner_a", "partner_b"]
  }
}
```

**Example 2 - ISP Abuse Department:**
```json
{
  "_internal": {
    "ticket": "ABUSE-5678",
    "customer": "cust_premium_12345",
    "assigned_analyst": "john.doe",
    "sla_hours": 4,
    "auto_actions": ["temp_block", "customer_email"],
    "billing_impact": true,
    "escalation_path": "tier2_team"
  }
}
```

**Example 3 - Minimalist Approach:**
```json
{
  "_internal": {
    "id": "internal_12345",
    "processed": "2024-01-15T14:30:25Z"
  }
}
```

### Common Usage Patterns

Organizations typically use internal metadata for:

- **Workflow tracking**: Status, assignments, deadlines, escalations
- **Integration data**: Ticket IDs, case references, external system links  
- **Quality metrics**: Confidence scores, validation flags, review requirements
- **Business data**: Customer info, billing, SLA tracking, priority levels
- **Technical metadata**: Processing times, system versions, batch IDs
- **Analysis data**: Campaign correlation, threat intelligence, ML scores

### Implementation Guidelines

1. **Transmission Stripping**: Parsers MUST remove `_internal` before transmission
2. **Local Storage**: Internal fields can be stored alongside transmitted fields
3. **API Responses**: Internal fields should only appear in internal APIs
4. **Logging**: Internal fields are valuable for operational logging
5. **Custom Fields**: Use `custom` object for organization-specific needs

### Security Considerations

- Internal fields may contain sensitive operational data
- Never log internal fields to external systems
- Customer data in internal fields must follow privacy regulations
- Access controls should apply to internal metadata viewing

## Implementation Requirements

### Parser Requirements

XARF v4 parsers MUST implement:

1. **Format Detection**
   - Detect v3 vs v4 format automatically
   - Handle malformed JSON gracefully
   - Provide clear error messages for invalid input

2. **Schema Validation**
   - Validate against complete JSON schema
   - Support all 22 types and their specific requirements
   - Implement conditional validation based on category/type
   - Handle unknown fields according to validation mode

3. **Backwards Compatibility**
   - Convert v3 reports to v4 format automatically
   - Preserve original v3 data when possible
   - Generate appropriate default values for missing v4 fields
   - Add `legacy_version` metadata for tracking

4. **Evidence Processing**
   - Validate base64 encoding
   - Enforce size limits (5MB per item, 15MB total)
   - Verify content-type headers
   - Support hash verification when provided

5. **Error Handling**
   - Provide detailed validation error messages
   - Include field path information for errors
   - Support multiple validation modes (strict/permissive/legacy)
   - Return structured error responses

### Generator Requirements

XARF v4 generators MUST implement:

1. **Report Construction**
   - Generate valid UUID v4 for report_id
   - Set appropriate timestamp in ISO 8601 format
   - Validate all required fields for chosen category/type
   - Support all evidence content types

2. **Evidence Handling**
   - Proper base64 encoding of all payloads
   - Generate integrity hashes when requested
   - Enforce size limits with clear error messages
   - Support multiple evidence items per report

3. **Validation**
   - Self-validate generated reports
   - Ensure compliance with category-specific schemas
   - Check tag format and namespace compliance
   - Verify all required fields are present

### Performance Requirements

**Parsing Performance:**
- Sub-millisecond parsing for typical reports (< 1MB)
- Sub-second parsing for maximum size reports (15MB)
- Memory usage proportional to evidence size only
- Support for streaming large evidence payloads

**Memory Usage:**
- Minimal memory overhead beyond evidence payload size
- Efficient base64 decoding without intermediate copies
- Configurable memory limits for protection
- Garbage collection friendly object structures

**Scalability:**
- Thread-safe parsing operations
- Support for concurrent processing
- Stateless parser design for easy scaling
- Minimal startup overhead for CLI tools

---

This technical specification provides the complete reference for XARF v4 implementation. For project management and operational guidance, see the [Implementation Guide](./implementation-guide.md). For a high-level overview, see the [Introduction & Overview](./introduction.md).