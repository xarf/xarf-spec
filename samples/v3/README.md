# XARF v3 Sample Reports

This directory contains sample XARF v3 reports for reference and migration purposes.

## Purpose

These v3 samples serve several important functions:

1. **Historical Reference** - Document the XARF v3 format structure
2. **Migration Examples** - Show the differences between v3 and v4 formats  
3. **Backward Compatibility** - Test that v4 parsers can handle v3 reports
4. **Implementation Guidance** - Help developers understand format evolution

## XARF v3 vs v4 Key Differences

### Structure Changes
| XARF v3 | XARF v4 | Change |
|---------|---------|--------|
| `Version` | `xarf_version` | Field renamed |
| `ReporterInfo` | `reporter` | Simplified structure |
| `Report.ReportClass` | `class` | Moved to top level |
| `Report.ReportType` | `type` | Moved to top level |
| `Report.Date` | `timestamp` | Moved to top level |
| `Report.Source` | `source_identifier` | Simplified |
| `Report.Attachment` | `evidence` | Renamed and enhanced |
| `Report.AdditionalInfo` | Class-specific fields | Flattened structure |

### New v4 Features
- **Class-based architecture** with 7 specialized abuse classes
- **Enhanced evidence handling** with multiple content types
- **Structured tagging system** for better classification  
- **Reporter type identification** (automated/manual/hybrid)
- **Evidence source tracking** (spamtrap/honeypot/user_report/etc.)
- **Internal metadata support** for processing systems

## Sample Files

- `spam_v3_sample.json` - Email spam report in v3 format
- `ddos_v3_sample.json` - DDoS attack report in v3 format  
- `phishing_v3_sample.json` - Phishing site report in v3 format
- `botnet_v3_sample.json` - Botnet infection report in v3 format

## Migration Path

To migrate from XARF v3 to v4:

1. **Update version field**: `Version: "3.0.0"` → `xarf_version: "4.0.0"`
2. **Restructure reporter info**: Flatten `ReporterInfo` to `reporter` 
3. **Move report fields**: Extract class, type, timestamp to top level
4. **Convert source format**: Map `Source` to `source_identifier`
5. **Update evidence**: Rename `Attachment` to `evidence` with enhanced structure
6. **Add new fields**: Include `evidence_source`, `tags`, etc.
7. **Map to v4 classes**: Choose appropriate abuse class (messaging/connection/content/etc.)

See the [Implementation Guide](../../docs/implementation-guide.md) for detailed migration instructions.

## Compatibility

XARF v4 parsers should maintain backward compatibility with v3 reports through:
- **Automatic field mapping** for renamed fields
- **Default value assignment** for missing v4 fields  
- **Class inference** based on v3 ReportClass/ReportType combinations
- **Evidence conversion** from v3 Attachment format

## Validation

These v3 samples should:
- ✅ Parse successfully in v4-compatible parsers
- ✅ Generate appropriate v4 equivalents when converted
- ✅ Validate against XARF v3 schema requirements
- ✅ Demonstrate common v3 usage patterns