#!/usr/bin/env python3
"""
Fix all connection-type schemas to focus on source rather than destination.
Remove destination_ip requirements and add proper connection fields.
"""

import json
import os
from pathlib import Path

# Common connection properties to add to all connection schemas
COMMON_CONNECTION_PROPERTIES = {
    "destination_ip": {
        "type": "string",
        "anyOf": [
            {"format": "ipv4"},
            {"format": "ipv6"}
        ],
        "description": "Target IP address (optional victim context)"
    },
    "destination_port": {
        "type": "integer",
        "minimum": 1,
        "maximum": 65535,
        "description": "Target port number"
    },
    "protocol": {
        "type": "string",
        "enum": ["tcp", "udp", "icmp", "sctp"],
        "description": "Network protocol used in the attack"
    },
    "first_seen": {
        "type": "string",
        "format": "date-time",
        "description": "When attack activity was first observed"
    },
    "last_seen": {
        "type": "string",
        "format": "date-time", 
        "description": "When attack activity was last observed"
    }
}

# Source port requirement for IP-based sources
SOURCE_PORT_REQUIREMENT = {
    "if": {
        "properties": {
            "source_identifier": {
                "anyOf": [
                    {"format": "ipv4"},
                    {"format": "ipv6"}
                ]
            }
        }
    },
    "then": {
        "required": ["source_port"]
    }
}

def fix_connection_schema(schema_path):
    """Fix a connection schema file."""
    print(f"Fixing {schema_path.name}...")
    
    with open(schema_path, 'r') as f:
        schema = json.load(f)
    
    # Find the allOf with properties
    for item in schema["allOf"]:
        if "properties" in item and "class" in item["properties"]:
            # Add common connection properties
            item["properties"].update(COMMON_CONNECTION_PROPERTIES)
            
            # Fix required fields - remove destination_ip, require protocol and first_seen
            item["required"] = ["protocol", "first_seen"]
            
            # Add source_port requirement for IP sources
            item.update(SOURCE_PORT_REQUIREMENT)
            break
    
    # Write back
    with open(schema_path, 'w') as f:
        json.dump(schema, f, indent=2)
    
    print(f"Fixed {schema_path.name}")

def main():
    """Fix all connection schemas."""
    types_dir = Path("/Users/tknecht/Projects/xarf/xarf-spec/schemas/v4/types")
    
    connection_schemas = list(types_dir.glob("connection-*.json"))
    
    for schema_path in connection_schemas:
        # Skip DDos as we already fixed it
        if "ddos.json" in schema_path.name:
            print(f"Skipping {schema_path.name} (already fixed)")
            continue
            
        fix_connection_schema(schema_path)
    
    print(f"Fixed {len(connection_schemas)-1} connection schemas")

if __name__ == "__main__":
    main()