---
layout: default
title: "Sample Reports"
description: "Real-world XARF v4 sample reports for all abuse classes and event types"
permalink: /samples/
---

<div class="samples-index">
    <section class="hero section-sm">
        <div class="container">
            <div class="hero-content">
                <h1 class="hero-title">Sample Reports</h1>
                <p class="hero-description">
                    Explore real-world XARF v4 sample reports covering all seven abuse classes and 22 event types. Perfect for understanding the format, testing integrations, and learning best practices.
                </p>
            </div>
        </div>
    </section>

    <section class="section">
        <div class="container">
            <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
                <!-- Messaging Class -->
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Messaging</h3>
                        <p class="card-description">Communication abuse including email spam and bulk messaging</p>
                    </div>
                    <div class="card-content">
                        <div class="sample-links">
                            <a href="{{ '/samples/v4/messaging-spam.json' | relative_url }}" class="sample-link">
                                <strong>spam</strong> - Email spam report
                            </a>
                            <a href="{{ '/samples/v4/messaging-bulk-messaging.json' | relative_url }}" class="sample-link">
                                <strong>bulk_messaging</strong> - Bulk messaging abuse
                            </a>
                        </div>
                    </div>
                </div>

                <!-- Connection Class -->
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Connection</h3>
                        <p class="card-description">Network attacks including DDoS, port scans, and login attacks</p>
                    </div>
                    <div class="card-content">
                        <div class="sample-links">
                            <a href="{{ '/samples/v4/connection-login-attack.json' | relative_url }}" class="sample-link">
                                <strong>login_attack</strong> - Brute force attempt
                            </a>
                            <a href="{{ '/samples/v4/connection-port-scan.json' | relative_url }}" class="sample-link">
                                <strong>port_scan</strong> - Network reconnaissance
                            </a>
                            <a href="{{ '/samples/v4/connection-ddos.json' | relative_url }}" class="sample-link">
                                <strong>ddos</strong> - DDoS attack
                            </a>
                            <a href="{{ '/samples/v4/connection-ddos-amplification.json' | relative_url }}" class="sample-link">
                                <strong>ddos_amplification</strong> - Amplification attack
                            </a>
                            <a href="{{ '/samples/v4/connection-auth-failure.json' | relative_url }}" class="sample-link">
                                <strong>auth_failure</strong> - Authentication failures
                            </a>
                        </div>
                    </div>
                </div>

                <!-- Content Class -->
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Content</h3>
                        <p class="card-description">Malicious web content including phishing and malware hosting</p>
                    </div>
                    <div class="card-content">
                        <div class="sample-links">
                            <a href="{{ '/samples/v4/content-phishing.json' | relative_url }}" class="sample-link">
                                <strong>phishing</strong> - Phishing website
                            </a>
                            <a href="{{ '/samples/v4/content-malware.json' | relative_url }}" class="sample-link">
                                <strong>malware</strong> - Malware hosting
                            </a>
                        </div>
                    </div>
                </div>

                <!-- Infrastructure Class -->
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Infrastructure</h3>
                        <p class="card-description">Compromised systems including botnets and C2 servers</p>
                    </div>
                    <div class="card-content">
                        <div class="sample-links">
                            <a href="{{ '/samples/v4/infrastructure-bot.json' | relative_url }}" class="sample-link">
                                <strong>bot</strong> - Botnet infection
                            </a>
                            <a href="{{ '/samples/v4/infrastructure-compromised-server.json' | relative_url }}" class="sample-link">
                                <strong>compromised_server</strong> - Server compromise
                            </a>
                        </div>
                    </div>
                </div>

                <!-- Copyright Class -->
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Copyright</h3>
                        <p class="card-description">IP infringement including P2P sharing and DMCA violations</p>
                    </div>
                    <div class="card-content">
                        <div class="sample-links">
                            <a href="{{ '/samples/v4/copyright-copyright.json' | relative_url }}" class="sample-link">
                                <strong>copyright</strong> - DMCA takedown
                            </a>
                            <a href="{{ '/samples/v4/copyright-p2p.json' | relative_url }}" class="sample-link">
                                <strong>p2p</strong> - P2P file sharing
                            </a>
                            <a href="{{ '/samples/v4/copyright-cyberlocker.json' | relative_url }}" class="sample-link">
                                <strong>cyberlocker</strong> - File hosting abuse
                            </a>
                            <a href="{{ '/samples/v4/copyright-ugc-platform.json' | relative_url }}" class="sample-link">
                                <strong>ugc_platform</strong> - User-generated content
                            </a>
                            <a href="{{ '/samples/v4/copyright-link-site.json' | relative_url }}" class="sample-link">
                                <strong>link_site</strong> - Link directory abuse
                            </a>
                            <a href="{{ '/samples/v4/copyright-usenet.json' | relative_url }}" class="sample-link">
                                <strong>usenet</strong> - Usenet posting
                            </a>
                        </div>
                    </div>
                </div>

                <!-- Vulnerability Class -->
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Vulnerability</h3>
                        <p class="card-description">Security vulnerabilities and system misconfigurations</p>
                    </div>
                    <div class="card-content">
                        <div class="sample-links">
                            <a href="{{ '/samples/v4/vulnerability-cve.json' | relative_url }}" class="sample-link">
                                <strong>cve</strong> - CVE vulnerability
                            </a>
                            <a href="{{ '/samples/v4/vulnerability-open.json' | relative_url }}" class="sample-link">
                                <strong>open</strong> - Open service
                            </a>
                            <a href="{{ '/samples/v4/vulnerability-misconfiguration.json' | relative_url }}" class="sample-link">
                                <strong>misconfiguration</strong> - System misconfiguration
                            </a>
                        </div>
                    </div>
                </div>

                <!-- Reputation Class -->
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Reputation</h3>
                        <p class="card-description">Threat intelligence and reputation data</p>
                    </div>
                    <div class="card-content">
                        <div class="sample-links">
                            <a href="{{ '/samples/v4/reputation-blocklist.json' | relative_url }}" class="sample-link">
                                <strong>blocklist</strong> - Blocklist entry
                            </a>
                            <a href="{{ '/samples/v4/reputation-threat-intelligence.json' | relative_url }}" class="sample-link">
                                <strong>threat_intelligence</strong> - Threat intel report
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section class="section section-sm">
        <div class="container">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Using the Samples</h3>
                    </div>
                    <div class="card-content">
                        <p class="mb-4">These samples demonstrate real-world usage patterns and best practices:</p>
                        <ul class="space-y-2">
                            <li>• <strong>Integration testing</strong> - Test your parsers and validators</li>
                            <li>• <strong>Format learning</strong> - Understand field requirements and structure</li>
                            <li>• <strong>Evidence examples</strong> - See how to include actionable proof</li>
                            <li>• <strong>Validation reference</strong> - Verify your own report generation</li>
                        </ul>
                    </div>
                    <div class="card-footer">
                        <a href="{{ '/tools/validator/' | relative_url }}" class="btn btn-primary">
                            Test with Validator
                        </a>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">XARF v3 Legacy Samples</h3>
                    </div>
                    <div class="card-content">
                        <p class="mb-4">For migration reference, we also provide XARF v3 samples:</p>
                        <div class="sample-links">
                            <a href="{{ '/samples/v3/spam_v3_sample.json' | relative_url }}" class="sample-link">
                                Legacy spam report (v3)
                            </a>
                            <a href="{{ '/samples/v3/ddos_v3_sample.json' | relative_url }}" class="sample-link">
                                Legacy DDoS report (v3)
                            </a>
                            <a href="{{ '/samples/v3/phishing_v3_sample.json' | relative_url }}" class="sample-link">
                                Legacy phishing report (v3)
                            </a>
                            <a href="{{ '/samples/v3/botnet_v3_sample.json' | relative_url }}" class="sample-link">
                                Legacy botnet report (v3)
                            </a>
                        </div>
                    </div>
                    <div class="card-footer">
                        <a href="{{ '/tools/converter/' | relative_url }}" class="btn btn-outline">
                            Convert v3 to v4
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </section>
</div>

<style>
.samples-index .hero {
    background: linear-gradient(135deg, var(--color-background) 0%, var(--color-background-alt) 100%);
}

.sample-links {
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
}

.sample-link {
    display: block;
    padding: var(--space-3);
    background: var(--color-background-alt);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    text-decoration: none;
    color: var(--color-text);
    transition: var(--transition-colors);
    font-size: var(--font-size-sm);
}

.sample-link:hover {
    border-color: var(--color-primary);
    background: var(--color-background);
    text-decoration: none;
}

.sample-link strong {
    color: var(--color-primary);
    font-family: var(--font-family-mono);
}
</style>