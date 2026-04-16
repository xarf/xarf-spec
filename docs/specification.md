# XARF v4: Technical Specification

## Table of Contents
1. [Overview](#overview)
2. [Schema Architecture](#schema-architecture)
3. [Core Schema Definition](#core-schema-definition)
4. [Category-Specific Schemas](#category-specific-schemas)
5. [Evidence Specifications](#evidence-specifications)
6. [Backwards Compatibility](#backwards-compatibility)
7. [Sample Reports](#sample-reports)
8. [Internal Metadata Usage](#internal-metadata-usage)

## Overview

This document provides the complete technical specification for XARF v4 schema validation, field definitions, and format requirements. It serves as the authoritative reference for implementing XARF v4 parsers, validators, and generators.

For a high-level introduction to XARF v4, see the [Introduction & Overview](./introduction.md). For guidance on building parsers, validators, and generators against this spec, see the [Implementer's Guide](./implementation-guide.md).

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

- **JSON Schema based** - Formal validation using JSON Schema Draft 2020-12
- **Conditional validation** - Type-specific requirements based on category/type combinations
- **Extensible design** - `additionalProperties: true` at the report level permits unknown fields for forward compatibility
- **Multi-level validation** - Standard and strict modes

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

### Schema Field Classification

To enable both human readability and programmatic detection of field requirements, XARF v4 schemas use two complementary mechanisms:

#### 1. Description Prefixes

All field descriptions are prefixed with their requirement level:

- **`REQUIRED:`** - Field must be present (also in `required` array)
- **`RECOMMENDED:`** - Field should be included when available
- **`OPTIONAL:`** - Field may be included for additional context

Example:
```json
{
  "source_port": {
    "type": "integer",
    "description": "RECOMMENDED: Source port number - critical for identifying sources in CGNAT environments"
  }
}
```

#### 2. The `x-recommended` Extension

For programmatic detection of recommended fields, schemas use the JSON Schema extension property `x-recommended: true`:

```json
{
  "source_port": {
    "type": "integer",
    "minimum": 1,
    "maximum": 65535,
    "x-recommended": true,
    "description": "RECOMMENDED: Source port number - critical for identifying sources in CGNAT environments"
  }
}
```

**Determining Field Requirements Programmatically:**

| Condition | Requirement Level |
|-----------|-------------------|
| Field is in `required` array | **Required** |
| Field has `x-recommended: true` | **Recommended** |
| Neither of the above | **Optional** |

This dual approach ensures that:
- Developers can quickly understand requirements by reading descriptions
- Validators and tools can programmatically determine field requirements
- The schema remains compatible with standard JSON Schema validators

### Base Report Structure

The authoritative base schema is defined in [`xarf-core.json`](../schemas/v4/xarf-core.json). All XARF v4 reports are validated against it.

Every report carries a small set of required identity and routing fields: the schema version, a unique report ID, when the incident occurred, who is reporting it, what the abuse source is, and how the abuse is classified (category + type). Beyond those, the schema defines recommended fields that improve report utility — such as evidence and a confidence score — and optional fields for additional context.

Contact information (reporter and sender) follows a shared structure capturing the organization name, a contact email, and a domain for verification. The distinction between reporter and sender matters when a third-party service files on behalf of a client.

| Field | Required | Type | Notes |
|-------|----------|------|-------|
| `org` | Yes | string | Organization name; max 200 chars |
| `contact` | Yes | email | Contact email address |
| `domain` | Yes | hostname | Organization domain for verification |

Evidence items each carry a MIME type and a base64-encoded payload. Integrity hashes and a human-readable description are recommended; size metadata is optional.

| Field | Requirement | Type | Notes |
|-------|-------------|------|-------|
| `content_type` | Required | string | MIME type of the evidence (e.g. `message/rfc822`, `image/png`) |
| `payload` | Required | string | Base64-encoded evidence data |
| `description` | Recommended | string | Human-readable description; max 500 chars |
| `hash` | Recommended | string | Integrity hash; format: `algorithm:hexvalue` (e.g. `sha256:e3b0c4…`) |
| `size` | Optional | integer | Size in bytes; max 5 MB per item |

The `_internal` object is a free-form container for operational metadata (ticket IDs, analyst assignments, SLA data, etc.) that parsers must strip before transmitting any report.

Each specific `category` + `type` combination has its own schema that extends it with additional required, recommended, and optional fields. The following section describe those per-type schemas which are defined in [`/schemas/v4/types/`](../schemas/v4/types/).

## Category-Specific Schemas

### 1. Messaging Category

**Purpose:** Communication-based abuse including spam and unwanted messaging

**Valid Types:** `spam`, `bulk_messaging`, `phishing`

**Evidence Sources:** `spamtrap`, `user_complaint`, `automated_filter`, `honeypot`

**Category-Specific Fields:**

| Field | Requirement | Applies To | Type | Notes |
|-------|-------------|------------|------|-------|
| `protocol` | Required | both | enum | Values differ slightly per type; `signal` and `chat` only valid for `spam` |
| `smtp_from` | Required | both | email | Required when `protocol=smtp`; `source_port` also required in that case |
| `recipient_count` | Required | `bulk_messaging` | integer | Minimum 100 |
| `subject` | Recommended | both | string | Max 500 characters |
| `unsubscribe_provided` | Recommended | `bulk_messaging` | boolean | Whether the message includes an unsubscribe mechanism |
| `message_id` | Recommended | `spam` | string | Helps with deduplication |
| `smtp_to` | Recommended | `spam` | email | SMTP envelope recipient |
| `sender_name` | Optional | both | string | Display name of the sender |
| `bulk_indicators` | Optional | `bulk_messaging` | object | Structured sub-fields: `high_volume`, `template_based`, `commercial_sender` |
| `opt_in_evidence` | Optional | `bulk_messaging` | boolean | Whether there is evidence of recipient opt-in |
| `language` | Optional | `spam` | string | ISO 639-1 (e.g. `en`, `en-US`) |
| `spam_indicators` | Optional | `spam` | object | Structured sub-fields: `suspicious_links`, `commercial_content`, `bulk_characteristics` |
| `user_agent` | Optional | `spam` | string | From message headers |

**Schema Definitions:**
Examples and formal schema definition: [`messaging-spam.json`](../schemas/v4/types/messaging-spam.json), [`messaging-bulk-messaging.json`](../schemas/v4/types/messaging-bulk-messaging.json)

### 2. Content Category

**Purpose:** Malicious or abusive web content — from phishing and malware to fraud, data exposure, brand abuse, and compromised sites

**Valid Types:** `phishing`, `malware`, `fraud`, `csam`, `csem`, `exposed_data`, `brand_infringement`, `suspicious_registration`, `remote_compromise`

**Evidence Notes:**
- Screenshot strongly recommended for most types; include HTML source alongside it when possible
- For `csam` and `csem`, do not attach visual content — use hash values and reference IDs instead

**Category-Specific Fields:**

| Field | Requirement | Applies To | Type | Notes |
|-------|-------------|------------|------|-------|
| `url` | Required | all | uri | URL of the abusive content |
| `infringement_type` | Required | `brand_infringement` | enum | e.g. `typosquatting`, `lookalike`, `counterfeit` |
| `legitimate_site` | Required | `brand_infringement` | uri | URL of the legitimate brand website |
| `classification` | Required | `csam` | enum | Legal classification: `baseline`, `A1`, `A2`, `B1`, `B2` |
| `detection_method` | Required | `csam`, `csem` | enum | Different valid values per type |
| `exploitation_type` | Required | `csem` | enum | e.g. `grooming`, `sextortion`, `trafficking` |
| `data_types` | Required | `exposed_data` | array | Min 1 item; e.g. `credentials`, `financial`, `personal_information` |
| `exposure_method` | Required | `exposed_data` | enum | e.g. `misconfigured_server`, `git_repository`, `paste_site` |
| `fraud_type` | Required | `fraud` | enum | e.g. `investment`, `romance`, `tech_support`, `advance_fee` |
| `compromise_type` | Required | `remote_compromise` | enum | e.g. `webshell`, `backdoor`, `defacement`, `malicious_redirect` |
| `registration_date` | Required | `suspicious_registration` | datetime | When the domain was registered |
| `suspicious_indicators` | Required | `suspicious_registration` | array | Min 1 item; e.g. `typosquatting`, `brand_keyword`, `fast_flux` |
| `domain` | Recommended | all | string | FQDN of the abusive content |
| `target_brand` | Recommended | all | string | Most relevant for `phishing` and `brand_infringement` |
| `verification_method` | Recommended | all | enum | How content was verified: `manual`, `automated_crawler`, `user_report`, `honeypot`, `threat_intelligence` |
| `verified_at` | Recommended | all | datetime | When content was last confirmed active |
| `infringing_elements` | Recommended | `brand_infringement` | array | e.g. `logo`, `brand_name`, `color_scheme`, `domain_name` |
| `similarity_score` | Recommended | `brand_infringement` | number | 0.0–1.0 visual/textual similarity to legitimate site |
| `content_removed` | Recommended | `csam` | boolean | Whether the content has been removed |
| `hash_values` | Recommended | `csam` | object | Sub-fields: `sha256` (recommended), `photodna` (recommended), `md5`, `sha1` |
| `media_type` | Recommended | `csam` | enum | `image`, `video`, `audio`, `text`, `mixed` |
| `ncmec_report_id` | Recommended | `csam` | string | NCMEC CyberTipline report ID |
| `evidence_type` | Recommended | `csem` | array | e.g. `chat_logs`, `images`, `user_profile` |
| `platform` | Recommended | `csem` | enum | e.g. `social_media`, `messaging_app`, `gaming_platform` |
| `reporting_obligations` | Recommended | `csem` | array | e.g. `NCMEC`, `IWF`, `local_law_enforcement` |
| `victim_age_range` | Recommended | `csem` | enum | `infant`, `toddler`, `prepubescent`, `pubescent`, `unknown` |
| `affected_organization` | Recommended | `exposed_data` | string | Organization whose data was exposed |
| `encryption_status` | Recommended | `exposed_data` | enum | `unencrypted`, `encrypted`, `partially_encrypted`, `hashed`, `unknown` |
| `record_count` | Recommended | `exposed_data` | integer | Number of records exposed |
| `sensitive_fields` | Recommended | `exposed_data` | array | Specific data fields exposed (e.g. `ssn`, `credit_card`) |
| `claimed_entity` | Recommended | `fraud` | string | Organization or person the fraudster claims to represent |
| `payment_methods` | Recommended | `fraud` | array | e.g. `cryptocurrency`, `wire_transfer`, `gift_cards` |
| `distribution_method` | Recommended | `malware` | enum | e.g. `drive_by_download`, `email_attachment`, `exploit_kit` |
| `file_hashes` | Recommended | `malware` | object | Sub-fields: `md5`, `sha1`, `sha256` (recommended), `ssdeep` |
| `malware_family` | Recommended | `malware` | string | e.g. `Emotet`, `TrickBot` |
| `malware_type` | Recommended | `malware` | enum | e.g. `trojan`, `ransomware`, `infostealer`, `rat` |
| `cloned_site` | Recommended | `phishing` | uri | Legitimate site being impersonated |
| `credential_fields` | Recommended | `phishing` | array | Form fields present on the phishing page (e.g. `username`, `password`) |
| `lure_type` | Recommended | `phishing` | enum | e.g. `account_suspension`, `security_alert`, `shipping_notification` |
| `submission_url` | Recommended | `phishing` | uri | Where credentials are submitted |
| `affected_cms` | Recommended | `remote_compromise` | enum | e.g. `wordpress`, `joomla`, `drupal` |
| `compromise_indicators` | Recommended | `remote_compromise` | array | Structured IoCs: each item has `type` and `value` |
| `malicious_activities` | Recommended | `remote_compromise` | array | e.g. `spam_sending`, `hosting_phishing`, `data_exfiltration` |
| `persistence_mechanisms` | Recommended | `remote_compromise` | array | e.g. `cron_job`, `modified_core_files`, `htaccess_modification` |
| `webshell_details` | Recommended | `remote_compromise` | object | Sub-fields: `family`, `capabilities`, `password_protected` |
| `days_since_registration` | Recommended | `suspicious_registration` | integer | |
| `predicted_usage` | Recommended | `suspicious_registration` | array | e.g. `phishing`, `spam`, `botnet_c2` |
| `registrant_details` | Recommended | `suspicious_registration` | object | Sub-fields: `email_domain`, `country`, `privacy_protected`, `bulk_registrations` |
| `risk_score` | Recommended | `suspicious_registration` | number | 0.0–1.0 |
| `targeted_brands` | Recommended | `suspicious_registration` | array | Brands potentially targeted |
| `asn` | Optional | all | integer | Autonomous System Number |
| `attack_vector` | Optional | all | enum | e.g. `phishing`, `malware`, `data_leak`, `remote_compromise` |
| `country_code` | Optional | all | string | ISO 3166-1 alpha-2 |
| `dns_records` | Optional | all | object | Key DNS records (A, AAAA, MX, TXT) |
| `dns_response` | Optional | all | object | DNS query metadata |
| `hosting_provider` | Optional | all | string | e.g. `AWS`, `Cloudflare`, `DigitalOcean` |
| `nameservers` | Optional | all | array | DNS nameservers |
| `registrar` | Optional | all | string | Domain registrar |
| `screenshot_url` | Optional | all | uri | Reference URL to screenshot evidence |
| `ssl_certificate` | Optional | all | object | Sub-fields: `issuer`, `subject`, `valid_from`, `valid_to`, `fingerprint` |
| `whois` | Optional | all | object | Sub-fields: `registrant`, `created_date`, `expiry_date`, `registrar_abuse_contact` |
| `previous_enforcement` | Optional | `brand_infringement` | array | Past actions: each item has `date`, `action`, `result` |
| `products_offered` | Optional | `brand_infringement` | array | Products or services offered on the infringing site |
| `trademark_details` | Optional | `brand_infringement` | object | Sub-fields: `registration_number`, `jurisdiction`, `category` (Nice classes) |
| `account_suspended` | Optional | `csam` | boolean | Whether associated accounts were suspended |
| `perpetrator_indicators` | Optional | `csem` | object | Sub-fields: `account_id`, `ip_addresses`, `pattern_of_behavior` |
| `accessibility` | Optional | `exposed_data` | enum | `public`, `requires_authentication`, `dark_web`, `removed` |
| `data_format` | Optional | `exposed_data` | enum | e.g. `csv`, `sql`, `json` |
| `discovery_source` | Optional | `exposed_data` | enum | e.g. `security_researcher`, `breach_monitoring` |
| `sample_records` | Optional | `exposed_data` | array | Redacted samples for verification; max 5 items |
| `cryptocurrency_addresses` | Optional | `fraud` | array | Each item requires `currency` and `address` |
| `loss_amount` | Optional | `fraud` | object | Sub-fields: `currency` (ISO 4217), `amount` |
| `c2_servers` | Optional | `malware` | array | Each item: `address`, `port`, `protocol` |
| `exploit_cve` | Optional | `malware` | array | CVEs exploited; format: `CVE-YYYY-NNNNN` |
| `file_metadata` | Optional | `malware` | object | Sub-fields: `filename`, `file_size`, `file_type`, `mime_type` |
| `persistence_mechanism` | Optional | `malware` | array | e.g. `registry`, `scheduled_task`, `dll_hijacking` |
| `sandbox_analysis` | Optional | `malware` | object | Sub-fields: `sandbox_name`, `analysis_url`, `verdict`, `score` |
| `targeted_platforms` | Optional | `malware` | array | e.g. `windows`, `linux`, `android` |
| `detection_evasion` | Optional | `phishing` | array | e.g. `geo_blocking`, `captcha`, `user_agent_filtering` |
| `phishing_kit` | Optional | `phishing` | string | Known kit identifier e.g. `16Shop`, `LogoKit` |
| `redirect_chain` | Optional | `phishing` | array | URL redirect sequence leading to phishing page |
| `cleanup_status` | Optional | `remote_compromise` | enum | `not_cleaned`, `partially_cleaned`, `cleaned`, `reinfected`, `unknown` |
| `vulnerability_exploited` | Optional | `remote_compromise` | object | Sub-fields: `cve`, `description`, `component` |
| `activation_behavior` | Optional | `suspicious_registration` | object | Sub-fields: `time_to_activation`, `initial_content` |
| `related_domains` | Optional | `suspicious_registration` | array | Other domains linked by registrant, nameserver, IP, or pattern |
| `ssl_certificate_details` | Optional | `suspicious_registration` | object | Sub-fields: `issued_immediately`, `free_certificate`, `wildcard` |

**Schema Definitions:**
Examples and formal schema definition: [`content-base.json`](../schemas/v4/types/content-base.json), [`content-phishing.json`](../schemas/v4/types/content-phishing.json), [`content-malware.json`](../schemas/v4/types/content-malware.json), [`content-fraud.json`](../schemas/v4/types/content-fraud.json), [`content-csam.json`](../schemas/v4/types/content-csam.json), [`content-csem.json`](../schemas/v4/types/content-csem.json), [`content-exposed-data.json`](../schemas/v4/types/content-exposed-data.json), [`content-brand_infringement.json`](../schemas/v4/types/content-brand_infringement.json), [`content-suspicious_registration.json`](../schemas/v4/types/content-suspicious_registration.json), [`content-remote_compromise.json`](../schemas/v4/types/content-remote_compromise.json)

### 3. Copyright Category

**Purpose:** Intellectual property infringement across file hosting, link sites, P2P networks, Usenet, UGC platforms, and direct web hosting

**Valid Types:** `copyright`, `cyberlocker`, `link_site`, `p2p`, `usenet`, `ugc_platform`

**Category-Specific Fields:**

| Field | Requirement | Applies To | Type | Notes |
|-------|-------------|------------|------|-------|
| `infringing_url` | Required | `copyright`, `cyberlocker`, `link_site`, `ugc_platform` | uri | URL of the infringing content |
| `hosting_service` | Required | `cyberlocker` | string | Name of the file hosting service |
| `site_name` | Required | `link_site` | string | Name of the link aggregation site |
| `p2p_protocol` | Required | `p2p` | enum | `bittorrent`, `edonkey`, `gnutella`, `kademlia`, `other`; `swarm_info` with `info_hash` or `magnet_uri` also required (via anyOf) |
| `platform_name` | Required | `ugc_platform` | string | Name of the UGC platform (e.g. YouTube, TikTok) |
| `newsgroup` | Required | `usenet` | string | Newsgroup name; `message_info.message_id` also required (via anyOf) |
| `rights_holder` | Recommended | all | string | Organization or person holding the copyright |
| `work_title` | Recommended | all | string | Title of the copyrighted work |
| `work_category` | Recommended | all except `copyright` | enum | e.g. `movie`, `tv_show`, `music`, `software`, `ebook`; values vary slightly per type |
| `infringement_type` | Recommended | `copyright`, `ugc_platform` | enum | Different valid values per type |
| `file_info` | Recommended | `cyberlocker` | object | Sub-fields: `filename`, `file_size`, `file_hash`, `upload_date`, `download_count` |
| `uploader_info` | Recommended | `cyberlocker`, `ugc_platform` | object | Sub-fields vary per type |
| `link_info` | Recommended | `link_site` | object | Sub-fields: `page_title`, `posting_date`, `uploader`, `download_count`, `link_count` |
| `linked_content` | Recommended | `link_site` | array | Each item requires `target_url` and `link_type`; max 50 items |
| `site_category` | Recommended | `link_site` | enum | e.g. `torrent_index`, `direct_download_links`, `streaming_links` |
| `swarm_info` | Recommended | `p2p` | object | `info_hash` or `magnet_uri` required; also: `torrent_name`, `file_count`, `total_size` |
| `content_info` | Recommended | `ugc_platform` | object | Sub-fields: `content_id`, `content_title`, `upload_date`, `content_duration`, `view_count` |
| `match_details` | Recommended | `ugc_platform` | object | Sub-fields: `match_confidence`, `match_duration`, `match_percentage`, `reference_id` |
| `message_info` | Recommended | `usenet` | object | `message_id` sub-field required within object |
| `original_url` | Optional | `copyright` | uri | URL of the legitimate/original content |
| `access_method` | Optional | `cyberlocker` | enum | `direct_link`, `password_protected`, `premium_only`, `time_limited`, `captcha_protected` |
| `takedown_info` | Optional | `cyberlocker` | object | Sub-fields: `previous_requests`, `service_response_time`, `automated_removal` |
| `search_terms` | Optional | `link_site` | array | Terms used to find the infringing links; max 10 items |
| `site_ranking` | Optional | `link_site` | object | Sub-fields: `alexa_rank`, `popularity_score` (0.0–10.0) |
| `peer_info` | Optional | `p2p` | object | Sub-fields: `peer_id`, `client_version`, `upload_amount`, `download_amount` |
| `release_date` | Optional | `p2p` | date | Official release date of the work |
| `detection_method` | Optional | `p2p`, `usenet` | enum | Different valid values per type |
| `monetization_info` | Optional | `ugc_platform` | object | Sub-fields: `monetized`, `ad_revenue`, `premium_content` |
| `encoding_info` | Optional | `usenet` | object | Sub-fields: `encoding_format`, `par2_recovery`, `rar_compression` |
| `nzb_info` | Optional | `usenet` | object | Sub-fields: `nzb_name`, `nzb_url`, `indexer_site`, `completion_percentage` |
| `server_info` | Optional | `usenet` | object | Sub-fields: `nntp_server`, `server_group`, `retention_days` |

**Schema Definitions:**
Examples and formal schema definition: [`copyright-copyright.json`](../schemas/v4/types/copyright-copyright.json), [`copyright-cyberlocker.json`](../schemas/v4/types/copyright-cyberlocker.json), [`copyright-link-site.json`](../schemas/v4/types/copyright-link-site.json), [`copyright-p2p.json`](../schemas/v4/types/copyright-p2p.json), [`copyright-usenet.json`](../schemas/v4/types/copyright-usenet.json), [`copyright-ugc-platform.json`](../schemas/v4/types/copyright-ugc-platform.json)

### 4. Connection Category

**Purpose:** Network-level attacks, automated abuse, and unauthorized connection attempts

**Valid Types:** `login_attack`, `port_scan`, `ddos`, `scraping`, `sql_injection`, `vulnerability_scan`, `infected_host`, `reconnaissance`

**Category-Specific Fields:**

| Field | Requirement | Applies To | Type | Notes |
|-------|-------------|------------|------|-------|
| `first_seen` | Required | all | datetime | When activity was first observed |
| `protocol` | Required | all | enum | Valid values vary by type; `icmp` and `sctp` only available for some types |
| `bot_type` | Required | `infected_host` | enum | e.g. `malicious`, `search_engine`, `ai_agent`, `unknown` |
| `probed_resources` | Required | `reconnaissance` | array | Specific paths probed (e.g. `/.env`, `/.git/config`, `/.aws/credentials`) |
| `total_requests` | Required | `scraping` | integer | Minimum 1 |
| `scan_type` | Required | `vulnerability_scan` | enum | e.g. `port_scan`, `web_vuln_scan`, `os_fingerprinting`, `service_enumeration` |
| `destination_ip` | Recommended | all | string | Target IPv4 or IPv6 address; `source_port` also required for `login_attack`, `port_scan`, `ddos` when `source_identifier` is an IP |
| `destination_port` | Recommended | all except `vulnerability_scan` | integer | 1–65535 |
| `attack_vector` | Recommended | `ddos` | string | e.g. `syn_flood`, `udp_flood`, `dns_amplification`, `memcached_amplification` |
| `peak_bps` | Recommended | `ddos` | integer | Peak bits per second |
| `peak_pps` | Recommended | `ddos` | integer | Peak packets per second |
| `behavior_pattern` | Recommended | `infected_host` | enum | e.g. `aggressive_crawling`, `api_abuse`, `vulnerability_probing` |
| `bot_name` | Recommended | `infected_host` | string | Known bot/tool name (e.g. `GPTBot`, `UptimeRobot`) |
| `verification_status` | Recommended | `infected_host` | enum | `verified`, `unverified`, `spoofed`, `unknown` |
| `user_agent` | Recommended | `infected_host`, `scraping` | string | User-Agent string of the bot or scraper |
| `resource_categories` | Recommended | `reconnaissance` | array | e.g. `environment_files`, `credential_files`, `version_control`, `backup_files` |
| `successful_probes` | Recommended | `reconnaissance` | array | Resources that returned success responses (200, 301, 302) |
| `scraping_pattern` | Recommended | `scraping` | enum | e.g. `sequential`, `deep_crawling`, `api_harvesting`, `sitemap_following` |
| `target_content` | Recommended | `scraping` | enum | e.g. `product_data`, `pricing_information`, `user_profiles`, `api_data` |
| `attack_technique` | Recommended | `sql_injection` | enum | e.g. `union_based`, `boolean_blind`, `time_blind`, `stacked_queries` |
| `http_method` | Recommended | `sql_injection` | enum | `GET`, `POST`, `PUT`, `DELETE`, `PATCH`, `HEAD`, `OPTIONS` |
| `injection_point` | Recommended | `sql_injection` | enum | `query_parameter`, `post_body`, `cookie`, `header`, `path`, `json_parameter` |
| `target_url` | Recommended | `sql_injection` | uri | Full URL targeted by the injection attempt |
| `scanner_signature` | Recommended | `vulnerability_scan` | string | Known tool name (e.g. `Nmap`, `Nikto`, `Nessus`, `Burp Scanner`) |
| `targeted_ports` | Recommended | `vulnerability_scan` | array | List of scanned port numbers |
| `last_seen` | Optional | all | datetime | When activity was last observed |
| `amplification_factor` | Optional | `ddos` | number | Amplification factor for reflection/amplification attacks |
| `duration_seconds` | Optional | `ddos` | integer | Attack duration in seconds |
| `mitigation_applied` | Optional | `ddos` | boolean | Whether mitigation was applied during the attack |
| `service_impact` | Optional | `ddos` | enum | `none`, `degraded`, `unavailable` |
| `threshold_exceeded` | Optional | `ddos` | datetime | When the detection threshold was exceeded |
| `accepts_cookies` | Optional | `infected_host` | boolean | |
| `api_endpoints_accessed` | Optional | `infected_host` | array | |
| `follows_crawl_delay` | Optional | `infected_host` | boolean | Whether bot honours crawl-delay directive |
| `javascript_execution` | Optional | `infected_host` | boolean | Whether bot executes JavaScript |
| `request_rate` | Optional | `infected_host`, `scraping` | number | Average requests per second |
| `respects_robots_txt` | Optional | `infected_host`, `scraping` | boolean | |
| `automated_tool` | Optional | `reconnaissance` | boolean | Whether activity appears to be from an automated tool |
| `http_methods` | Optional | `reconnaissance` | array | HTTP methods used during probing |
| `response_codes` | Optional | `reconnaissance` | array | HTTP response codes received |
| `total_probes` | Optional | `reconnaissance` | integer | Total number of probe attempts |
| `user_agent` | Optional | `reconnaissance`, `sql_injection`, `vulnerability_scan` | string | |
| `bot_signature` | Optional | `scraping` | string | Known scraper identity (e.g. `Scrapy`, `AhrefsBot`, `SemrushBot`) |
| `concurrent_connections` | Optional | `scraping` | integer | |
| `data_volume` | Optional | `scraping` | integer | Total bytes transferred |
| `session_duration` | Optional | `scraping` | integer | Duration of scraping session in seconds |
| `unique_urls` | Optional | `scraping` | integer | Number of unique URLs accessed |
| `attempts_count` | Optional | `sql_injection` | integer | Number of injection attempts observed |
| `payload_sample` | Optional | `sql_injection` | string | Sanitized sample of injection payload; max 1000 chars |
| `scan_rate` | Optional | `vulnerability_scan` | number | Requests per second |
| `targeted_services` | Optional | `vulnerability_scan` | array | Services targeted (e.g. `http`, `ssh`, `mysql`, `mongodb`) |
| `total_requests` | Optional | `vulnerability_scan` | integer | |
| `vulnerabilities_probed` | Optional | `vulnerability_scan` | array | Specific CVEs or vulnerability identifiers probed |

**Schema Definitions:**
Examples and formal schema definition: [`connection-login-attack.json`](../schemas/v4/types/connection-login-attack.json), [`connection-port-scan.json`](../schemas/v4/types/connection-port-scan.json), [`connection-ddos.json`](../schemas/v4/types/connection-ddos.json), [`connection-scraping.json`](../schemas/v4/types/connection-scraping.json), [`connection-sql-injection.json`](../schemas/v4/types/connection-sql-injection.json), [`connection-vulnerability-scan.json`](../schemas/v4/types/connection-vulnerability-scan.json), [`connection-infected-host.json`](../schemas/v4/types/connection-infected-host.json), [`connection-reconnaissance.json`](../schemas/v4/types/connection-reconnaissance.json)

### 5. Vulnerability Category

**Purpose:** Exposed services, known CVEs, and security misconfigurations that require remediation

**Valid Types:** `cve`, `misconfiguration`, `open_service`

**Category-Specific Fields:**

| Field | Requirement | Applies To | Type | Notes |
|-------|-------------|------------|------|-------|
| `service` | Required | all | string | Vulnerable service or component name |
| `cve_id` | Required | `cve` | string | CVE identifier; format: `CVE-YYYY-NNNNN` |
| `service_port` | Required | `cve` | integer | Port where vulnerable service is running (1–65535) |
| `cvss_score` | Recommended | `cve` | number | CVSS score 0.0–10.0 |
| `evidence_source` | Recommended | `cve` | enum | `vulnerability_scan`, `researcher_analysis`, `automated_discovery`, `penetration_testing` |
| `exploitability` | Recommended | `cve` | enum | `theoretical`, `poc_available`, `functional`, `weaponized` |
| `patch_available` | Recommended | `cve` | boolean | Whether a patch is available |
| `risk_level` | Recommended | `cve` | enum | `info`, `low`, `medium`, `high`, `critical` |
| `service_version` | Recommended | `cve` | string | Version of the vulnerable service |
| `severity` | Recommended | `cve` | enum | `informational`, `low`, `medium`, `high`, `critical` |
| `cve_ids` | Optional | `cve` | array | Additional CVE identifiers; max 10 items |
| `cvss_vector` | Optional | `cve` | string | CVSS v3 vector string (e.g. `CVSS:3.1/AV:N/...`) |
| `cvss_version` | Optional | `cve` | enum | `2.0`, `3.0`, `3.1` |
| `disclosure_date` | Optional | `cve` | datetime | When CVE was publicly disclosed |
| `impact_assessment` | Optional | `cve` | object | Sub-fields: `confidentiality`, `integrity`, `availability` (each `none`/`low`/`high`) |
| `patch_url` | Optional | `cve` | uri | URL to patch or fix information |
| `patch_version` | Optional | `cve` | string | Version that fixes the vulnerability |
| `remediation_priority` | Optional | `cve` | enum | `low`, `medium`, `high`, `critical`, `emergency` |
| `vendor_advisory` | Optional | `cve` | uri | URL to vendor security advisory |

**Schema Definitions:**
Examples and formal schema definition: [`vulnerability-cve.json`](../schemas/v4/types/vulnerability-cve.json), [`vulnerability-misconfiguration.json`](../schemas/v4/types/vulnerability-misconfiguration.json), [`vulnerability-open-service.json`](../schemas/v4/types/vulnerability-open-service.json)

### 6. Infrastructure Category

**Purpose:** Botnet infections and compromised servers requiring remediation or takedown

**Valid Types:** `botnet`, `compromised_server`

**Category-Specific Fields:**

| Field | Requirement | Applies To | Type | Notes |
|-------|-------------|------------|------|-------|
| `compromise_evidence` | Required | `botnet` | string | Evidence of how the compromise was detected (e.g. `C2 communication observed`) |
| `compromise_method` | Required | `compromised_server` | string | Method used to compromise the server |
| `bot_capabilities` | Recommended | `botnet` | array | Capabilities observed: `ddos`, `spam`, `proxy`, `keylogger`, `file_download`, `remote_shell`, `cryptocurrency_mining`, `data_theft` |
| `c2_protocol` | Recommended | `botnet` | enum | Protocol used for C2 communications: `http`, `https`, `tcp`, `udp`, `dns`, `irc`, `p2p`, `custom` |
| `c2_server` | Recommended | `botnet` | string | Command and control server domain or IP |
| `malware_family` | Recommended | `botnet` | string | Malware family classification (e.g. `mirai`, `emotet`, `zeus`); max 200 chars |

**Schema Definitions:**
Examples and formal schema definition: [`infrastructure-botnet.json`](../schemas/v4/types/infrastructure-botnet.json), [`infrastructure-compromised-server.json`](../schemas/v4/types/infrastructure-compromised-server.json)

### 7. Reputation Category

**Purpose:** IP/domain blocklist inclusion and threat intelligence reports

**Valid Types:** `blocklist`, `threat_intelligence`

**Category-Specific Fields:**

| Field | Requirement | Applies To | Type | Notes |
|-------|-------------|------------|------|-------|
| `threat_type` | Required | all | string | Type of threat for blocklist inclusion or intelligence report |

**Schema Definitions:**
Examples and formal schema definition: [`reputation-blocklist.json`](../schemas/v4/types/reputation-blocklist.json), [`reputation-threat-intelligence.json`](../schemas/v4/types/reputation-threat-intelligence.json)



## Evidence Specifications

### Recommended Content Types

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

### Examples

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
  "xarf_version": "4.2.0",
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
| `Version` | `xarf_version` | Set to "4.x.x", add `legacy_version: "3"` |
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

Complete sample reports for all 32 valid category/type combinations are in [`samples/v4/`](../samples/v4/). Each schema file also contains an inlined example.

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


