---
layout: default
title: "Documentation"
description: "Complete documentation for XARF v4 specification, implementation guides, and API references"
permalink: /docs/
---

<div class="docs-index">
    <section class="docs-hero">
        <div class="container">
            <h1 class="docs-hero-title">Documentation</h1>
            <p class="docs-hero-description">
                Everything you need to understand, implement, and use XARF v4 for modern abuse reporting. From high-level concepts to detailed technical specifications.
            </p>
        </div>
    </section>

    <section class="section">
        <div class="container">
            <div class="docs-sections">
                <div class="docs-section-card">
                    <svg class="section-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>
                        <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
                    </svg>
                    <h3 class="section-title">Getting Started</h3>
                    <p class="section-description">
                        Learn the fundamentals of XARF v4, understand the abuse classification system, and get your first integration running.
                    </p>
                    <div class="section-links">
                        <a href="{{ '/docs/introduction/' | relative_url }}">Introduction & Overview</a>
                        <a href="{{ '/docs/quick-start/' | relative_url }}">Quick Start Guide</a>
                        <a href="{{ '/docs/migration/' | relative_url }}">Migration from v3</a>
                    </div>
                </div>

                <div class="docs-section-card">
                    <svg class="section-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                        <path d="M14 2v6h6"/>
                        <path d="M16 13H8"/>
                        <path d="M16 17H8"/>
                        <path d="M10 9H8"/>
                    </svg>
                    <h3 class="section-title">Technical Specification</h3>
                    <p class="section-description">
                        Complete technical reference including JSON schemas, field definitions, validation rules, and implementation requirements.
                    </p>
                    <div class="section-links">
                        <a href="{{ '/docs/specification/' | relative_url }}">Full Specification</a>
                        <a href="{{ '/docs/schemas/' | relative_url }}">JSON Schemas</a>
                        <a href="{{ '/docs/validation/' | relative_url }}">Validation Rules</a>
                    </div>
                </div>

                <div class="docs-section-card">
                    <svg class="section-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M12 2 2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
                    </svg>
                    <h3 class="section-title">Abuse Classes</h3>
                    <p class="section-description">
                        Detailed documentation for each of the seven abuse classes, including event types, evidence requirements, and examples.
                    </p>
                    <div class="section-links">
                        <a href="{{ '/docs/classes/messaging/' | relative_url }}">Messaging</a>
                        <a href="{{ '/docs/classes/connection/' | relative_url }}">Connection</a>
                        <a href="{{ '/docs/classes/content/' | relative_url }}">Content</a>
                        <a href="{{ '/docs/classes/infrastructure/' | relative_url }}">Infrastructure</a>
                        <a href="{{ '/docs/classes/copyright/' | relative_url }}">Copyright</a>
                        <a href="{{ '/docs/classes/vulnerability/' | relative_url }}">Vulnerability</a>
                        <a href="{{ '/docs/classes/reputation/' | relative_url }}">Reputation</a>
                    </div>
                </div>

                <div class="docs-section-card">
                    <svg class="section-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>
                        <path d="M15 2H9a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V3a1 1 0 0 0-1-1"/>
                    </svg>
                    <h3 class="section-title">Implementation Guide</h3>
                    <p class="section-description">
                        Practical guidance for deploying XARF v4 in production environments, including integration patterns and best practices.
                    </p>
                    <div class="section-links">
                        <a href="{{ '/docs/implementation-guide/' | relative_url }}">Implementation Guide</a>
                        <a href="{{ '/docs/integration-patterns/' | relative_url }}">Integration Patterns</a>
                        <a href="{{ '/docs/best-practices/' | relative_url }}">Best Practices</a>
                    </div>
                </div>

                <div class="docs-section-card">
                    <svg class="section-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M9 12l2 2 4-4"/>
                        <path d="M21 12c.552 0 1.005-.449.95-.998a10 10 0 0 0-8.953-8.951c-.55-.055-.998.398-.998.95v8a1 1 0 0 0 1 1z"/>
                        <path d="M21 12A9 9 0 1 1 12 3"/>
                    </svg>
                    <h3 class="section-title">Parser Libraries</h3>
                    <p class="section-description">
                        Official parser libraries and SDKs for multiple programming languages, with examples and API documentation.
                    </p>
                    <div class="section-links">
                        <a href="{{ '/docs/libraries/python/' | relative_url }}">Python Library</a>
                        <a href="{{ '/docs/libraries/javascript/' | relative_url }}">JavaScript Library</a>
                        <a href="{{ '/docs/libraries/go/' | relative_url }}">Go Library</a>
                        <a href="{{ '/docs/libraries/' | relative_url }}">All Libraries</a>
                    </div>
                </div>

                <div class="docs-section-card">
                    <svg class="section-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                    </svg>
                    <h3 class="section-title">Community & Support</h3>
                    <p class="section-description">
                        Join the XARF community, contribute to the specification, and get support from other implementers.
                    </p>
                    <div class="section-links">
                        <a href="{{ '/community/' | relative_url }}">Community Guidelines</a>
                        <a href="{{ '/contributing/' | relative_url }}">Contributing</a>
                        <a href="https://github.com/xarf/xarf-spec/discussions" target="_blank" rel="noopener">Discussions</a>
                        <a href="https://github.com/xarf/xarf-spec/issues" target="_blank" rel="noopener">Issues</a>
                    </div>
                </div>
            </div>
        </div>
    </section>
</div>