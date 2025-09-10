# XARF v4 Schema Deprecation Notice

## Class-Based Schemas → Type-Specific Schemas

**Effective Date**: September 2024  
**Migration Deadline**: XARF v4.1.0 (Target: Q2 2025)

### ⚠️ Deprecated Schemas

The following class-based schemas are **DEPRECATED** and will be removed in XARF v4.1.0:

| Deprecated Schema | Status | Replacement |
|------------------|---------|-------------|
| `messaging-class.json` | ⚠️ Deprecated | Use `types/messaging-spam.json`, `types/messaging-bulk-messaging.json` |
| `connection-class.json` | ⚠️ Deprecated | Use `types/connection-ddos.json`, `types/connection-port-scan.json`, etc. |
| `content-class.json` | ⚠️ Deprecated | Use `types/content-phishing.json`, `types/content-malware.json` |
| `infrastructure-class.json` | ⚠️ Deprecated | Use `types/infrastructure-bot.json`, `types/infrastructure-compromised-server.json` |
| `copyright-class.json` | ⚠️ Deprecated | Use `types/copyright-copyright.json` |
| `vulnerability-class.json` | ⚠️ Deprecated | Use `types/vulnerability-cve.json`, `types/vulnerability-open.json`, etc. |
| `reputation-class.json` | ⚠️ Deprecated | Use `types/reputation-blocklist.json`, `types/reputation-threat-intelligence.json` |
| `xarf-v4-master.json` | ⚠️ Deprecated | Use `xarf-v4-master-types.json` |

### ✅ New Type-Specific Architecture

**Benefits of Type-Specific Schemas:**
- **🔍 Easy Discovery**: `ls types/` shows all available event types
- **📋 Specific Validation**: Each type defines exact requirements
- **🔧 Better Maintainability**: New types don't affect existing schemas  
- **👨‍💻 Developer Experience**: Clear understanding of each event type
- **📦 Modular Loading**: Load only needed schemas

### 🚀 Migration Guide

#### Before (Deprecated)
```bash
# ❌ Don't use class-based validation
ajv validate -s messaging-class.json -d spam-report.json
ajv validate -s xarf-v4-master.json -d any-report.json
```

#### After (Recommended)
```bash
# ✅ Use type-specific validation
ajv validate -s types/messaging-spam.json -d spam-report.json
ajv validate -s xarf-v4-master-types.json -d any-report.json
```

#### Parser Code Migration
```python
# Before
schema = load_schema("messaging-class.json")

# After  
schema = load_schema("types/messaging-spam.json")
# or for dynamic loading
schema = load_schema(f"types/{report_class}-{report_type}.json")
```

### 🗓️ Timeline

| Phase | Date | Action |
|-------|------|--------|
| **Deprecation** | Sep 2024 | Class schemas marked deprecated, type schemas available |
| **Warning Period** | Oct 2024 - Mar 2025 | Validation tools show deprecation warnings |
| **Migration Deadline** | Q2 2025 | XARF v4.1.0 removes deprecated schemas |

### 🔄 Backward Compatibility

**During Deprecation Period:**
- Class-based schemas remain functional
- Both validation approaches work
- Migration warnings in validation tools
- Documentation emphasizes type-specific approach

**After Migration Deadline:**
- Class-based schemas removed
- Type-specific schemas are the only option
- Cleaner, more maintainable codebase

### 📞 Support

Questions about migration?
- **Issues**: [GitHub Issues](https://github.com/xarf/xarf-spec/issues)
- **Discussions**: [GitHub Discussions](https://github.com/xarf/xarf-spec/discussions)
- **Email**: [spec-maintainers@xarf.org](mailto:spec-maintainers@xarf.org)