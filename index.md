---
layout: default
title: "XARF v4 - The Modern Standard for Abuse Reporting"
description: "Real-time, evidence-based abuse reporting format for ISPs, security researchers, and network operators"
---

<div class="hero">
  <div class="hero-content">
    <h1 class="hero-title">XARF v4</h1>
    <p class="hero-subtitle">The Modern Standard for Abuse Reporting</p>
    <p class="hero-description">
      Real-time, evidence-based abuse reporting format designed for automated processing and immediate response. 
      Transform your abuse handling from manual chores into competitive advantage.
    </p>
    <div class="hero-actions">
      <a href="{{ '/docs/introduction' | relative_url }}" class="btn btn-primary">Get Started</a>
      <a href="{{ '/tools/validator' | relative_url }}" class="btn btn-secondary">Try Online Validator</a>
    </div>
  </div>
  
  <div class="hero-code">
    <div class="code-preview">
      <div class="code-header">
        <span class="code-title">spam-report.json</span>
        <button class="code-copy" onclick="copyCode(this)">Copy</button>
      </div>
      <pre><code class="language-json">{
  "xarf_version": "4.0.0",
  "class": "messaging",
  "type": "spam",
  "timestamp": "2025-01-11T14:30:00Z",
  "source_identifier": "203.0.113.45",
  "evidence": [{
    "content_type": "message/rfc822",
    "description": "Spam email with headers",
    "payload": "UmVjZWl2ZWQ6IGZyb20...",
    "hash": "a1b2c3d4e5f6..."
  }],
  "tags": ["spam:commercial", "automated"]
}</code></pre>
    </div>
  </div>
</div>

<div class="features">
  <div class="container">
    <h2 class="section-title">Why XARF v4?</h2>
    <div class="features-grid">
      <div class="feature">
        <div class="feature-icon">🚀</div>
        <h3>Real-Time Processing</h3>
        <p>One incident = one report, sent immediately when detected. No batching, no delays.</p>
      </div>
      <div class="feature">
        <div class="feature-icon">🔍</div>
        <h3>Evidence-Based</h3>
        <p>Structured evidence with integrity hashes. Screenshots, logs, and samples included.</p>
      </div>
      <div class="feature">
        <div class="feature-icon">⚡</div>
        <h3>Type-Specific</h3>
        <p>22 specialized schemas across 7 abuse classes. Precise validation for each scenario.</p>
      </div>
      <div class="feature">
        <div class="feature-icon">🤖</div>
        <h3>Automation-First</h3>
        <p>Designed for immediate machine processing. Reduce manual work, accelerate response.</p>
      </div>
      <div class="feature">
        <div class="feature-icon">🔒</div>
        <h3>Source-Centric</h3>
        <p>Focus on abusive sources with IP, port, and protocol details. Perfect for CGNAT environments.</p>
      </div>
      <div class="feature">
        <div class="feature-icon">📊</div>
        <h3>Standards-Based</h3>
        <p>JSON Schema validation, RFC 3339 timestamps, modern web standards throughout.</p>
      </div>
    </div>
  </div>
</div>

<div class="use-cases">
  <div class="container">
    <h2 class="section-title">Perfect For</h2>
    <div class="use-cases-grid">
      <div class="use-case">
        <h3>ISPs & Hosting Providers</h3>
        <p>Standardized intake format reduces custom parser development. Automated processing enables immediate response workflows.</p>
        <ul>
          <li>Automated ticket creation</li>
          <li>Customer notification systems</li>
          <li>Legal compliance documentation</li>
        </ul>
      </div>
      <div class="use-case">
        <h3>Security Researchers</h3>
        <p>Rich context for campaign tracking and attribution. Flexible evidence format supports any content type.</p>
        <ul>
          <li>Honeypot and spamtrap reporting</li>
          <li>Malware sandbox integration</li>
          <li>Threat intelligence platforms</li>
        </ul>
      </div>
      <div class="use-case">
        <h3>Tool Developers</h3>
        <p>Comprehensive libraries handle parsing, validation, and conversion. Clear specifications reduce development time.</p>
        <ul>
          <li>SIEM and log analysis tools</li>
          <li>Security product integrations</li>
          <li>Custom abuse response systems</li>
        </ul>
      </div>
    </div>
  </div>
</div>

<div class="stats">
  <div class="container">
    <div class="stats-grid">
      <div class="stat">
        <div class="stat-number">22</div>
        <div class="stat-label">Abuse Types</div>
      </div>
      <div class="stat">
        <div class="stat-number">7</div>
        <div class="stat-label">Abuse Classes</div>
      </div>
      <div class="stat">
        <div class="stat-number">100%</div>
        <div class="stat-label">v3 Compatible</div>
      </div>
      <div class="stat">
        <div class="stat-number">5MB</div>
        <div class="stat-label">Max Evidence Size</div>
      </div>
    </div>
  </div>
</div>

<div class="getting-started">
  <div class="container">
    <h2 class="section-title">Get Started in Minutes</h2>
    <div class="steps">
      <div class="step">
        <div class="step-number">1</div>
        <div class="step-content">
          <h3>Explore the Format</h3>
          <p>Review our comprehensive documentation and sample reports.</p>
          <a href="{{ '/docs/introduction' | relative_url }}" class="step-link">Read Introduction →</a>
        </div>
      </div>
      <div class="step">
        <div class="step-number">2</div>
        <div class="step-content">
          <h3>Test Online</h3>
          <p>Use our interactive validator to test XARF reports in your browser.</p>
          <a href="{{ '/tools/validator' | relative_url }}" class="step-link">Try Validator →</a>
        </div>
      </div>
      <div class="step">
        <div class="step-number">3</div>
        <div class="step-content">
          <h3>Integrate</h3>
          <p>Download parser libraries and follow our implementation guide.</p>
          <a href="{{ '/docs/implementation-guide' | relative_url }}" class="step-link">Implementation Guide →</a>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
function copyCode(button) {
  const codeBlock = button.closest('.code-preview').querySelector('code');
  const text = codeBlock.textContent;
  
  navigator.clipboard.writeText(text).then(() => {
    const originalText = button.textContent;
    button.textContent = 'Copied!';
    button.classList.add('copied');
    
    setTimeout(() => {
      button.textContent = originalText;
      button.classList.remove('copied');
    }, 2000);
  });
}
</script>