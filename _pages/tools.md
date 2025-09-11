---
layout: default
title: "Tools"
description: "Interactive tools for working with XARF v4 - validator, generator, explorer, and more"
permalink: /tools/
---

<div class="tools-index">
    <section class="tools-hero">
        <div class="container">
            <h1 class="tools-hero-title">XARF v4 Tools</h1>
            <p class="tools-hero-description">
                Interactive tools to help you validate, generate, and explore XARF v4 reports. Perfect for testing integrations, learning the format, and debugging issues.
            </p>
        </div>
    </section>

    <section class="section">
        <div class="container">
            <div class="tools-grid">
                <a href="{{ '/tools/validator/' | relative_url }}" class="tool-card">
                    <svg class="tool-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M9 12l2 2 4-4"/>
                        <path d="M21 12c.552 0 1.005-.449.95-.998a10 10 0 0 0-8.953-8.951c-.55-.055-.998.398-.998.95v8a1 1 0 0 0 1 1z"/>
                        <path d="M21 12A9 9 0 1 1 12 3"/>
                    </svg>
                    <h3 class="tool-name">XARF Validator</h3>
                    <p class="tool-description">
                        Validate XARF v4 reports against JSON schemas. Check syntax, structure, and compliance with detailed error reporting.
                    </p>
                    <div class="tool-features">
                        <span class="feature-tag">Real-time validation</span>
                        <span class="feature-tag">Detailed error messages</span>
                        <span class="feature-tag">v3 compatibility check</span>
                    </div>
                </a>

                <a href="{{ '/tools/generator/' | relative_url }}" class="tool-card">
                    <svg class="tool-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/>
                        <circle cx="12" cy="13" r="3"/>
                    </svg>
                    <h3 class="tool-name">Report Generator</h3>
                    <p class="tool-description">
                        Generate sample XARF v4 reports for testing and integration. Choose from all abuse classes and customize fields.
                    </p>
                    <div class="tool-features">
                        <span class="feature-tag">All abuse classes</span>
                        <span class="feature-tag">Customizable fields</span>
                        <span class="feature-tag">Export formats</span>
                    </div>
                </a>

                <a href="{{ '/tools/explorer/' | relative_url }}" class="tool-card">
                    <svg class="tool-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="11" cy="11" r="8"/>
                        <path d="m21 21-4.35-4.35"/>
                    </svg>
                    <h3 class="tool-name">Schema Explorer</h3>
                    <p class="tool-description">
                        Interactive explorer for XARF v4 schemas. Browse all abuse classes, event types, and field definitions with examples.
                    </p>
                    <div class="tool-features">
                        <span class="feature-tag">Interactive browser</span>
                        <span class="feature-tag">Field documentation</span>
                        <span class="feature-tag">Live examples</span>
                    </div>
                </a>

                <a href="{{ '/tools/converter/' | relative_url }}" class="tool-card">
                    <svg class="tool-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
                        <path d="M7.5 4.21l4.5 2.6 4.5-2.6"/>
                        <path d="M7.5 19.79V14.6L3 12"/>
                        <path d="M21 12l-4.5 2.6v5.19"/>
                        <path d="M3.27 6.96L12 12.01l8.73-5.05"/>
                        <path d="M12 22.08V12"/>
                    </svg>
                    <h3 class="tool-name">v3 to v4 Converter</h3>
                    <p class="tool-description">
                        Convert XARF v3 reports to v4 format. Understand the differences and plan your migration strategy.
                    </p>
                    <div class="tool-features">
                        <span class="feature-tag">Automatic conversion</span>
                        <span class="feature-tag">Migration analysis</span>
                        <span class="feature-tag">Compatibility check</span>
                    </div>
                </a>

                <a href="{{ '/tools/formatter/' | relative_url }}" class="tool-card">
                    <svg class="tool-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                        <path d="M14 2v6h6"/>
                        <path d="M16 13H8"/>
                        <path d="M16 17H8"/>
                        <path d="M10 9H8"/>
                    </svg>
                    <h3 class="tool-name">JSON Formatter</h3>
                    <p class="tool-description">
                        Format, minify, and beautify XARF JSON reports. Perfect for debugging and preparing reports for production.
                    </p>
                    <div class="tool-features">
                        <span class="feature-tag">Pretty printing</span>
                        <span class="feature-tag">Minification</span>
                        <span class="feature-tag">Syntax highlighting</span>
                    </div>
                </a>

                <a href="{{ '/tools/diff/' | relative_url }}" class="tool-card">
                    <svg class="tool-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"/>
                        <path d="M9 12h6"/>
                        <path d="M12 9v6"/>
                    </svg>
                    <h3 class="tool-name">Report Diff</h3>
                    <p class="tool-description">
                        Compare two XARF reports side-by-side. Identify differences in structure, fields, and values with visual highlighting.
                    </p>
                    <div class="tool-features">
                        <span class="feature-tag">Side-by-side comparison</span>
                        <span class="feature-tag">Visual highlighting</span>
                        <span class="feature-tag">Field-level diff</span>
                    </div>
                </a>
            </div>
        </div>
    </section>

    <section class="section section-sm">
        <div class="container">
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">CLI Tools</h2>
                    <p class="card-description">
                        Command-line versions of these tools are available for automation and CI/CD integration.
                    </p>
                </div>
                <div class="card-content">
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
                        <div>
                            <h4>Python CLI</h4>
                            <pre><code>pip install xarf-cli
xarf validate report.json
xarf generate --class messaging</code></pre>
                        </div>
                        <div>
                            <h4>Node.js CLI</h4>
                            <pre><code>npm install -g @xarf/cli
xarf-cli validate report.json
xarf-cli generate --class connection</code></pre>
                        </div>
                        <div>
                            <h4>Go CLI</h4>
                            <pre><code>go install github.com/xarf/cli
xarf-cli validate report.json
xarf-cli convert v3-report.json</code></pre>
                        </div>
                    </div>
                </div>
                <div class="card-footer">
                    <a href="{{ '/docs/cli/' | relative_url }}" class="btn btn-outline">
                        View CLI Documentation
                    </a>
                </div>
            </div>
        </div>
    </section>
</div>