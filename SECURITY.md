# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 4.0.x   | :white_check_mark: |
| < 4.0   | :x:                |

## Reporting a Vulnerability

The XARF project takes security vulnerabilities seriously. We appreciate your efforts to responsibly disclose your findings.

### How to Report

**Please DO NOT report security vulnerabilities through public GitHub issues.**

Instead, please report security vulnerabilities by emailing:

**contact@xarf.org**

### What to Include

Please include the following information in your report:

- Type of vulnerability or security concern
- Affected specification version(s)
- Detailed description of the security issue
- Potential impact on implementations
- Suggested mitigation or fix (if applicable)

### Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Resolution**: Depends on severity and complexity

### Security Update Process

1. **Triage**: We'll confirm the vulnerability and assess severity
2. **Specification Review**: We'll review affected specification sections
3. **Fix Development**: We'll develop and review proposed changes
4. **Community Review**: We'll engage with implementation maintainers
5. **Disclosure**: We'll coordinate disclosure timing with you
6. **Publication**: We'll publish updated specification with security notes

## Security Considerations in XARF Specification

### 1. Evidence Payload Limits

The specification recommends:
- Maximum 5MB per evidence item
- Maximum 15MB total evidence per report
- Implementations should enforce these limits

### 2. Email Address Validation

- All email fields must follow RFC 5322 format
- Implementations should validate email addresses
- Consider DNS MX record checks for untrusted sources

### 3. URL Validation

- All URL fields must be valid HTTP(S) URLs
- Implementations should sanitize URLs before processing
- Be cautious of URL schemes that could trigger code execution

### 4. Timestamp Validation

- All timestamps must use ISO 8601 format with timezone
- Implementations should validate timestamp format
- Consider checking for unreasonable dates (far future/past)

### 5. Size Limits

Implementations should enforce reasonable limits on:
- String field lengths
- Array sizes (e.g., tags, attachments)
- Nested object depth
- Total report size

### 6. Content Type Validation

- Validate `category` and `type` against allowed values
- Reject unknown or invalid combinations
- Follow specification strictly for security-sensitive fields

## Implementation Security Guidelines

### For Parser Developers

1. **Input Validation**: Validate all fields against schema
2. **Size Limits**: Enforce maximum sizes to prevent DoS
3. **Type Safety**: Use strong typing where possible
4. **Error Handling**: Don't expose sensitive information in errors
5. **Sanitization**: Sanitize all user-provided data

### For Report Generators

1. **Data Privacy**: Don't include PII unless necessary
2. **Evidence Selection**: Only include relevant evidence
3. **Size Management**: Compress large evidence items
4. **Timestamp Accuracy**: Use correct timezone information
5. **Field Validation**: Validate before sending

### For Report Processors

1. **Trust Boundaries**: Treat incoming reports as untrusted
2. **Validation**: Validate against specification strictly
3. **Rate Limiting**: Implement rate limits for report processing
4. **Storage**: Secure storage for sensitive report data
5. **Access Control**: Restrict access to report data

## Known Security Considerations

### 1. Personal Information

XARF reports may contain:
- Email addresses
- IP addresses
- Domain names
- Other identifying information

**Recommendation**: Implement appropriate data protection measures compliant with GDPR, CCPA, and other privacy regulations.

### 2. Evidence Attachments

Evidence may include:
- Email headers and bodies
- Malicious payloads
- Network traffic dumps
- Log files

**Recommendation**: Sandbox evidence processing and storage. Never execute or render untrusted evidence without proper isolation.

### 3. Source Authentication

The specification does not mandate cryptographic signatures for reports.

**Recommendation**: Implement additional authentication mechanisms (e.g., DKIM, S/MIME) when transmitting reports via email.

### 4. Transport Security

Reports transmitted over email or HTTP should be protected.

**Recommendation**: Use TLS for all network transmission. Consider end-to-end encryption for sensitive reports.

## Vulnerability Disclosure Policy

We follow a **coordinated disclosure** model:

1. **Private Disclosure**: Report sent to contact@xarf.org
2. **Acknowledgment**: We confirm receipt within 48 hours
3. **Investigation**: We investigate with specification experts
4. **Community Review**: We consult with implementation maintainers
5. **Specification Update**: We publish updated specification
6. **Public Disclosure**: We publish advisory 7 days after publication

## Security Hall of Fame

We recognize security researchers who responsibly disclose vulnerabilities:

<!-- Security researchers will be listed here -->

*No vulnerabilities reported yet.*

## Contact

- **Security Email**: contact@xarf.org
- **PGP Key**: Not yet available
- **GitHub Security Advisories**: https://github.com/xarf/xarf-spec/security/advisories

## Additional Resources

- [XARF Website](https://xarf.org)
- [XARF Specification Repository](https://github.com/xarf/xarf-spec)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)

---

**Last Updated**: 2025-11-30
