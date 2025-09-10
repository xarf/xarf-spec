#!/usr/bin/env python3
"""
Generate individual type schemas from class schemas.
Extracts type enums from class schemas and creates separate files for each type.
"""

import json
import os
from pathlib import Path

# Type definitions from the class schemas
TYPE_DEFINITIONS = {
    "messaging": {
        "spam": {
            "description": "Unsolicited commercial messages and unwanted email",
            "required_fields": ["protocol"],
            "conditional_required": {
                "if_protocol_smtp": ["smtp_from"]
            },
            "specific_fields": ["smtp_from", "smtp_to", "subject", "sender_name", "spam_indicators"]
        },
        "bulk_messaging": {
            "description": "Legitimate but unwanted bulk communications",
            "required_fields": ["protocol", "recipient_count"],
            "conditional_required": {
                "if_protocol_smtp": ["smtp_from"]
            },
            "specific_fields": ["recipient_count", "unsubscribe_provided", "opt_in_evidence", "bulk_indicators"]
        }
    },
    "connection": {
        "login_attack": {
            "description": "Brute force login attempts and authentication attacks",
            "required_fields": ["destination_ip", "protocol"],
            "specific_fields": ["username", "password_attempts", "login_service", "auth_method"]
        },
        "port_scan": {
            "description": "Network port scanning and reconnaissance activities", 
            "required_fields": ["destination_ip", "protocol"],
            "specific_fields": ["scanned_ports", "scan_type", "scan_rate", "unique_targets"]
        },
        "ddos": {
            "description": "Distributed Denial of Service attacks",
            "required_fields": ["destination_ip", "protocol"],
            "specific_fields": ["attack_vector", "peak_pps", "peak_bps", "duration_seconds", "amplification_factor"]
        },
        "ddos_amplification": {
            "description": "DDoS attacks using amplification techniques",
            "required_fields": ["destination_ip", "protocol"],
            "specific_fields": ["amplification_factor", "reflector_service", "peak_pps", "peak_bps"]
        },
        "auth_failure": {
            "description": "Authentication failure incidents",
            "required_fields": ["destination_ip", "protocol"],
            "specific_fields": ["failed_attempts", "login_service", "username"]
        }
    },
    "vulnerability": {
        "cve": {
            "description": "Common Vulnerabilities and Exposures reports",
            "required_fields": ["service", "cve_id"],
            "specific_fields": ["cve_ids", "cvss_score", "cvss_vector", "patch_available", "patch_version"]
        },
        "open": {
            "description": "Open services and exposed resources",
            "required_fields": ["service"],
            "specific_fields": ["service_banner", "access_level", "security_risk"]
        },
        "misconfiguration": {
            "description": "Security misconfigurations and hardening issues",
            "required_fields": ["service"],
            "specific_fields": ["config_issue", "recommended_setting", "risk_level"]
        }
    },
    "reputation": {
        "blocklist": {
            "description": "IP/domain blocklist inclusion reports",
            "required_fields": ["threat_type"],
            "specific_fields": ["blocklist_information", "reputation_score", "confidence_score"]
        },
        "threat_intelligence": {
            "description": "Threat intelligence and IOC reports",
            "required_fields": ["threat_type"],
            "specific_fields": ["threat_categories", "activity_indicators", "sources"]
        }
    },
    "infrastructure": {
        "bot": {
            "description": "Botnet infections and compromised systems",
            "required_fields": ["malware_family"],
            "specific_fields": ["c2_server", "c2_protocol", "bot_capabilities"]
        },
        "compromised_server": {
            "description": "Compromised servers and infrastructure",
            "required_fields": ["compromise_method"],
            "specific_fields": ["data_accessed", "persistent_access", "lateral_movement"]
        }
    },
    "content": {
        "phishing": {
            "description": "Phishing websites and credential harvesting",
            "required_fields": ["url"],
            "specific_fields": ["target_brand", "target_category", "phishing_kit"]
        },
        "malware": {
            "description": "Malware hosting and distribution",
            "required_fields": ["url"],
            "specific_fields": ["malware_family", "file_hash", "payload_type"]
        }
    },
    "copyright": {
        "copyright": {
            "description": "Copyright infringement and DMCA violations",
            "required_fields": ["work_title", "rights_holder"],
            "specific_fields": ["infringing_url", "original_url", "infringement_type"]
        }
    }
}

def create_type_schema(class_name, type_name, type_info):
    """Create a type-specific schema file."""
    
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": f"https://xarf.org/schemas/v4/types/{class_name}-{type_name.replace('_', '-')}.json",
        "title": f"XARF v4 {class_name.title()} - {type_name.replace('_', ' ').title()} Type Schema",
        "description": f"Schema for {type_info['description']}",
        "allOf": [
            {
                "$ref": "../xarf-core.json"
            },
            {
                "type": "object",
                "properties": {
                    "class": {
                        "const": class_name
                    },
                    "type": {
                        "const": type_name
                    }
                },
                "required": type_info.get("required_fields", [])
            }
        ]
    }
    
    return schema

def main():
    """Generate all type schemas."""
    
    # Create types directory
    types_dir = Path("/Users/tknecht/Projects/xarf/xarf-spec/schemas/v4/types")
    types_dir.mkdir(exist_ok=True)
    
    generated_count = 0
    
    for class_name, types in TYPE_DEFINITIONS.items():
        for type_name, type_info in types.items():
            filename = f"{class_name}-{type_name.replace('_', '-')}.json"
            filepath = types_dir / filename
            
            # Skip if already exists (like the ones we created manually)
            if filepath.exists():
                print(f"Skipping {filename} (already exists)")
                continue
                
            schema = create_type_schema(class_name, type_name, type_info)
            
            with open(filepath, 'w') as f:
                json.dump(schema, f, indent=2)
            
            print(f"Created {filename}")
            generated_count += 1
    
    print(f"\nGenerated {generated_count} new type schemas")
    
    # List all type schemas
    type_files = sorted(types_dir.glob("*.json"))
    print(f"\nTotal type schemas: {len(type_files)}")
    for file in type_files:
        print(f"  - {file.name}")

if __name__ == "__main__":
    main()