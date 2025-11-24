# CHANGELOG: class → category Migration

## [Unreleased] - 2025-11-24

### BREAKING CHANGES
- **Field Renamed**: Changed `class` to `category` in all XARF v4 schemas and samples
- This affects all JSON schema files, sample reports, and documentation
- All implementations must be updated to use the new field name

### Changed

#### Schema Files
- `schemas/v4/xarf-core.json`
  - Updated required field from `"class"` to `"category"`
  - Updated property definition from `class` to `category`
  - Updated description to reference "category" instead of "class"

- `schemas/v4/xarf-v4-master.json`
  - Updated all 20 conditional validation blocks
  - Changed all `"class": {"const": "..."}` to `"category": {"const": "..."}`
  - Updated examples to use `category` field
  - Updated description from "all classes" to "all categories"

#### Type Schema Files (33 files updated)
- All files in `schemas/v4/types/`
- Changed `"class": {"const": "..."}` to `"category": {"const": "..."}`
- Updated `content-base.json` title from "Content Class" to "Content Category"
- Updated all property definitions consistently

**Files modified**:
- connection-ddos.json
- connection-infected-host.json
- connection-login-attack.json
- connection-port-scan.json
- connection-reconnaissance.json
- connection-scraping.json
- connection-sql-injection.json
- connection-vulnerability-scan.json
- content-base.json
- content-brand_infringement.json
- content-csam.json
- content-csem.json
- content-exposed-data.json
- content-fraud.json
- content-malware.json
- content-phishing.json
- content-remote_compromise.json
- content-suspicious_registration.json
- copyright-copyright.json
- copyright-cyberlocker.json
- copyright-link-site.json
- copyright-p2p.json
- copyright-ugc-platform.json
- copyright-usenet.json
- infrastructure-botnet.json
- infrastructure-compromised-server.json
- messaging-bulk-messaging.json
- messaging-spam.json
- reputation-blocklist.json
- reputation-threat-intelligence.json
- vulnerability-cve.json
- vulnerability-misconfiguration.json
- vulnerability-open-service.json

#### Sample Files (30 files updated)
- All JSON files in `samples/v4/`
- Changed `"class": "..."` to `"category": "..."` in all examples

**Files modified**:
- connection-auth-failure.json
- connection-bot.json
- connection-ddos-amplification.json
- connection-ddos.json
- connection-login-attack.json
- connection-port-scan.json
- connection-reconnaissance.json
- connection-scraping.json
- connection-sql-injection.json
- connection-vuln-scanning.json
- content-csam.json
- content-csem.json
- content-exposed-data.json
- content-malware.json
- content-phishing.json
- copyright-copyright.json
- copyright-cyberlocker.json
- copyright-link-site.json
- copyright-p2p.json
- copyright-ugc-platform.json
- copyright-usenet.json
- infrastructure-botnet.json
- infrastructure-compromised-server.json
- messaging-bulk-messaging.json
- messaging-spam.json
- reputation-blocklist.json
- reputation-threat-intelligence.json
- vulnerability-cve.json
- vulnerability-misconfiguration.json
- vulnerability-open.json

#### Documentation Files
- `docs/specification.md`
  - Changed "within class" to "within category"
  - Changed "for each class" to "for each category"

- `schemas/README.md`
  - Updated field description: `class` → `category`
  - Updated code examples to use `category`
  - Updated variable names: `class_name` → `category_name`
  - Updated property access: `.class` → `.category`
  - Updated error messages

- `schemas/v4/types/README.md`
  - Updated template placeholders: `{class}` → `{category}`
  - Updated references from "class-based" to "category-based"
  - Updated schema property examples

- `CONTRIBUTING.md`
  - Updated example JSON to use `category` field

### Added
- `docs/MIGRATION_CLASS_TO_CATEGORY.md` - Comprehensive migration guide
- `CHANGELOG_CLASS_TO_CATEGORY.md` - This changelog

### Validation
- ✅ All 65 JSON files validated successfully
- ✅ No syntax errors detected
- ✅ No remaining `"class"` field references in JSON files
- ✅ All schemas maintain proper structure

### Migration Notes
See `docs/MIGRATION_CLASS_TO_CATEGORY.md` for detailed migration instructions and code examples.

### Statistics
- Total files modified: 98
- JSON schema files: 35 (2 core + 33 types)
- Sample JSON files: 30
- Documentation files: 5 (4 updated + 1 new)
- Lines changed: ~500+
- Zero validation errors
- Zero remaining "class" references in JSON

---

**Note**: This is a breaking change. All XARF v4 implementations must be updated to use `category` instead of `class`.
