---
title: "Introduction & Overview"
description: "Get started with XARF v4 - the modern standard for abuse reporting"
order: 1
---

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

All samples available in the [Tools section]({{ '/tools/validator' | relative_url }}).

### 3. Test Integration

**For report receivers (ISPs, hosting providers):**
1. Test with our [online validator]({{ '/tools/validator' | relative_url }})
2. Review existing sample reports
3. Begin planning integration workflow

**For report senders (security tools, researchers):**
1. Generate test reports using our validator
2. Validate output with provided samples
3. Plan delivery mechanisms (email, API, etc.)

### 4. Production Integration

See the [Implementation Guide]({{ '/docs/implementation-guide' | relative_url }}) for:
- Complete integration patterns
- Performance optimization guidelines
- Error handling best practices
- Community support resources