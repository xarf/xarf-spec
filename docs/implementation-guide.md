# XARF v4 Conformance and Implementer's Guide

This guide is for developers building XARF v4 parsers, validators, and generators. It covers schema architecture, validation modes, field requirement detection, evidence handling, and v3 compatibility. For the authoritative field reference, see [`specification.md`](specification.md). For working examples, see [`../samples/v4/`](../samples/v4/).

---

## Schema Architecture

Every XARF v4 report validates against two schemas in sequence:

1. **[`../schemas/v4/xarf-core.json`](../schemas/v4/xarf-core.json)** — the base schema defining fields common to all reports (`report_id`, `xarf_version`, `timestamp`, `reporter`, `category`, `type`, `source_identifier`, `evidence`, etc.)
2. **The type-specific schema** in [`../schemas/v4/types/`](../schemas/v4/types/) — extends the base using `allOf`:

```json
{
  "allOf": [
    { "$ref": "../xarf-core.json" },
    {
      "properties": { ... },
      "required": [ ... ]
    }
  ]
}
```

### Category and Type Combinations

The `category` and `type` fields together determine which type schema applies. The schema file is always `schemas/v4/types/<category>-<type>.json`.

All 32 valid combinations:

| Category | Types |
|----------|-------|
| `messaging` | `spam`, `bulk_messaging` |
| `connection` | `login_attack`, `port_scan`, `ddos`, `scraping`, `sql_injection`, `vulnerability_scan`, `infected_host`, `reconnaissance` |
| `content` | `phishing`, `malware`, `fraud`, `csam`, `csem`, `exposed_data`, `brand_infringement`, `suspicious_registration`, `remote_compromise` |
| `copyright` | `copyright`, `cyberlocker`, `link_site`, `p2p`, `usenet`, `ugc_platform` |
| `vulnerability` | `cve`, `misconfiguration`, `open_service` |
| `infrastructure` | `botnet`, `compromised_server` |
| `reputation` | `blocklist`, `threat_intelligence` |

Any `category`/`type` combination not in this table must be rejected as invalid, as specified in `xarf-v4-master.json`.

---

## Validation Modes

Implementations should support two validation modes:

| Mode | Required fields | Recommended fields | Use case |
|------|-----------------|--------------------|----------|
| **Standard** (default) | Error if missing | No action | General use |
| **Strict** | Error if missing | Error if missing | High-assurance pipelines |

Unknown fields are permitted in both modes — `xarf-core.json` sets `additionalProperties: true` at the report level.

Example API sketch:

```python
parser = XARFParser(
    mode="standard",  # standard, strict
)
```

v3 report acceptance is a separate feature, not a mode — when enabled, v3 input is auto-converted to v4 and then validated according to whichever mode is active. See [v3 Compatibility](#v3-compatibility).

---

## Detecting Field Requirements Programmatically

Fields carry requirement levels through two mechanisms:

1. A field listed in the schema's `required` array → **Required**
2. A field with `"x-recommended": true` in its property schema → **Recommended**
3. Neither → **Optional**

Field descriptions are also prefixed with `REQUIRED:`, `RECOMMENDED:`, or `OPTIONAL:` for human readability, but implementations must use the machine-readable mechanisms above for enforcement logic.

```python
def get_field_requirement(schema, field_name):
    field_schema = schema.get("properties", {}).get(field_name, {})
    required_fields = schema.get("required", [])
    if field_name in required_fields:
        return "required"
    elif field_schema.get("x-recommended", False):
        return "recommended"
    else:
        return "optional"
```

When merging requirement levels across an `allOf` composition (base schema + type schema), a field is Required if it appears in the `required` array of either constituent schema.

---

## Parser Requirements

### 1. Format Detection

Before validation, determine which version of XARF the input represents:

- **v3**: Top-level `Version` field is present
- **v4**: Top-level `xarf_version` field is present

If neither field is present, or if the input is not valid JSON, reject with a structured error indicating the failure point. Never silently discard or ignore malformed input.

### 2. Schema Validation

Validate in order:

1. Parse JSON. On failure, return a structured error with position and reason.
2. Validate against `xarf-core.json`. Collect all errors before returning — do not stop at the first failure.
3. Extract `category` and `type`. Reject if the combination is not in the valid set of 32.
4. Resolve the type schema path: `schemas/v4/types/<category>-<type>.json`.
5. Validate against the type schema.

Unknown fields are always permitted — the core schema sets `additionalProperties: true`.

### 3. Field Requirement Enforcement

Apply the following per field, after merging requirements from both schemas:

- **Required**: Reject the report if the field is absent.
- **Recommended**: In `strict` mode, reject. In `standard` mode, take no action.
- **Optional**: No action if absent.

### 4. Evidence Processing

For each item in the `evidence` array:

- **Encoding**: Verify the `payload` value is valid standard base64 (RFC 4648). Reject if padding is incorrect or invalid characters are present.
- **Size limits**: Reject if any single item exceeds 5MB decoded. Reject if total decoded size across all items exceeds 15MB.
- **Content type**: Verify `content_type` is a valid MIME type string.
- **Hash verification**: If a `hash` field is present, verify it matches the decoded payload. The format is `algorithm:hexvalue`. Supported algorithms must include at minimum `sha256`, `sha1`, and `md5`.

### 5. Error Handling

Error responses must include:

- The field path where the violation occurred (e.g., `evidence[0].payload`)
- The violation type (schema error, requirement level, size limit, encoding error)
- Whether the violation is an error or a warning
- Enough context for the caller to locate and fix the problem

Structured error responses are strongly preferred over plain text, as they enable programmatic handling by callers.

### 6. `_internal` Field Stripping

The `_internal` field is reserved for internal routing and metadata. It must be removed from any report before transmission or storage. Parsers must strip this field from output regardless of validation mode.

---

## Generator Requirements

### 1. Report Construction

When building a new report:

- Generate a UUID v4 for `report_id`.
- Set `timestamp` in ISO 8601 format with timezone offset (e.g., `2026-03-19T14:00:00Z`).
- Set `xarf_version` to the current spec version string.
- Validate that all required fields for the chosen `category`/`type` combination are present before returning the report.

### 2. Evidence Handling

- Encode all `payload` values using standard base64 (RFC 4648) with no line breaks or whitespace in the encoded string.
- Enforce size limits (5MB per item, 15MB total) with clear errors that identify which item exceeded the limit.
- When the caller requests integrity hashes, compute them over the raw (pre-encoding) bytes and write the result in `algorithm:hexvalue` format.
- Support multiple evidence items in a single report.

### 3. Self-Validation

Before returning any generated report, validate it against both schemas (core + type-specific). Self-validation failures indicate a generator bug and must be surfaced with enough detail to diagnose the cause.

---

## Evidence Handling Reference

### Encoding

All `payload` values must use standard base64 as defined in RFC 4648, Section 4:

- Standard alphabet (`A–Z`, `a–z`, `0–9`, `+`, `/`)
- Padding with `=` is required
- No line breaks, spaces, or other whitespace

### Size Limits

| Scope | Limit |
|-------|-------|
| Single evidence item | 5MB (decoded bytes) |
| Total across all items | 15MB (decoded bytes) |

Limits apply to decoded byte count, not the length of the base64-encoded string.

### Hash Format

```
hash: "<algorithm>:<hexvalue>"
```

Examples:

| Algorithm | Example |
|-----------|---------|
| `sha256` | `sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `sha1` | `sha1:da39a3ee5e6b4b0d3255bfef95601890afd80709` |
| `md5` | `md5:d41d8cd98f00b204e9800998ecf8427e` |

### Recommended Content Types by Category

| Scenario | Recommended `content_type` |
|----------|---------------------------|
| Messaging — full email with headers | `message/rfc822` |
| Content — screenshot | `image/png` |
| Content — page source | `text/html` |
| Connection — log entries | `text/plain` |
| Malware sample | `application/octet-stream` (password-protected zip preferred) |
| CSAM / CSEM | Hash values and reference IDs only — **do not attach visual content** |

---

## Tag Namespace Conventions

Tags use the format `namespace:value`, where both the namespace and value consist of lowercase alphanumeric characters and underscores only.

Standard namespaces:

| Namespace | Purpose | Example |
|-----------|---------|---------|
| `malware:` | Malware family name | `malware:emotet` |
| `campaign:` | Campaign identifier | `campaign:op_nightfall` |
| `cve:` | CVE identifier | `cve:CVE-2021-44228` |
| `botnet:` | Botnet name | `botnet:mirai` |
| `severity:` | Severity level | `severity:high` |
| `confidence:` | Confidence level | `confidence:medium` |
| `tool:` | Tool name | `tool:nmap` |
| `custom:` | Organization-specific values | `custom:internal_case_id` |

Implementations should warn on tags that do not match the `namespace:value` pattern. Unknown namespaces outside the standard set are permitted but should be flagged in strict mode.

---

## v3 Compatibility

### Detection

Check the top-level fields of the parsed JSON:

- `Version` present → v3 format
- `xarf_version` present → v4 format

### Conversion Steps

1. Detect v3 format.
2. Generate a new UUID v4 for `report_id`.
3. Map fields according to the table below.
4. Add `legacy_version: "3"` to the converted report.
5. Convert the `Samples` array to the v4 `evidence` format.
6. Validate the resulting v4 report against both schemas before returning.

### Field Mapping

| v3 Field | v4 Field | Notes |
|----------|----------|-------|
| `Version` | `xarf_version` | Set to current v4 version string; add `legacy_version: "3"` |
| `ReporterInfo.ReporterOrg` | `reporter.org` | Direct |
| `ReporterInfo.ReporterOrgEmail` | `reporter.contact` | Direct |
| `Report.Date` | `timestamp` | Direct |
| `Report.SourceIp` | `source_identifier` | Direct |
| `Report.SourcePort` | `source_port` | Direct |
| `Report.ReportType` | `category` + `type` | Map to the appropriate v4 category/type combination |
| `Report.Samples` | `evidence` | Convert array structure; base64-encode payloads if not already encoded |
| _(absent)_ | `report_id` | Generate new UUID v4 |

v3 `ReportType` values do not map 1:1 to v4 category/type combinations. Implementations must maintain an explicit mapping table. Unmapped `ReportType` values should surface as conversion warnings, not silent failures.

---

## Performance Targets

| Metric | Target |
|--------|--------|
| Typical report parsing (< 1MB) | Sub-millisecond |
| Maximum-size report parsing (15MB) | Sub-second |
| Memory usage | Proportional to evidence size only |
| Thread safety | Stateless parser design required |

Lazy schema loading (load on first use, cache thereafter) is the recommended approach for environments with constrained startup memory. All 32 type schemas need not be loaded eagerly.

---

## Testing Guidance

The [`xarf-parser-tests`](https://github.com/xarf/xarf-parser-tests) repository provides a shared, language-agnostic test suite intended for inclusion in any XARF parser implementation. It contains 49 JSON test samples organized as:

- `samples/valid/` — valid v4 reports and valid v3 reports for conversion testing
- `samples/invalid/` — reports covering schema violations, missing required fields, business rule violations, and malformed data

Machine-readable test definitions with performance targets and compatibility requirements are in `test-definitions/test-cases.json`.

### Minimum Coverage Expected

| Area | Requirement |
|------|-------------|
| Valid category/type combinations | All 32 must parse successfully |
| v3 → v4 conversion | Common types must convert correctly |
| Invalid report rejection | All samples in `samples/invalid/` must be rejected with appropriate errors |
| Evidence edge cases | Max size enforcement, invalid base64, hash mismatch, hash verification success |
| Validation modes | Standard and strict behavior must differ as specified |

Implementations that cannot pass the shared test suite should not claim XARF v4 conformance.

---

## Security Considerations

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
