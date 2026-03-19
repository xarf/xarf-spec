# XARF v4: Introduction & Overview

## What is XARF v4?

XARF (eXtended Abuse Reporting Format) v4 is an open JSON standard for reporting internet abuse incidents. It is designed for **real-time operational response** — helping ISPs, hosting providers, and network operators quickly understand and act on abuse reports, rather than serving as a research or analysis format.

XARF v4 organizes abuse into seven categories (`messaging`, `connection`, `infrastructure`, `content`, `copyright`, `vulnerability`, `reputation`) with 32 specific types across them, each with its own validated schema.

## Why XARF v4 Matters

### The Problem
The cybersecurity industry processes millions of abuse reports daily, but current formats are inadequate:

- **v3 XARF** is too simplistic for the modern threat landscape
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

| **v3 Approach** | **v4 Approach** | **Benefit** |
|-----------------|-----------------|-------------|
| Simple Types | Type-Specific Architecture (32 types) | Granular categorization |
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
- **Tag system** for categorization and correlation
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

## Next Steps

### Authoritative Field & Schema Reference

**→ Read the [Technical Specification](./specification.md)**
- Base report structure and field definitions
- All 32 category/type schemas with required, recommended, and optional fields
- Evidence format, backwards compatibility, and internal metadata

### Building a Parser, Validator, or Generator

**→ Read the [Implementer's Guide](./implementation-guide.md)**
- Schema architecture and validation modes
- Parser and generator conformance requirements
- Evidence handling, tag namespaces, v3 compatibility
- Performance targets and testing guidance

### Community & Contributing

- [GitHub organization](https://github.com/xarf/) — specifications, parsers, tools
- [Issues](https://github.com/xarf/xarf-spec/issues) — bug reports, feature requests, questions
- [Discussions](https://github.com/xarf/xarf-spec/discussions) — architecture decisions, use case feedback
- [Contributing guide](../CONTRIBUTING.md)
