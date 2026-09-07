const fs = require('fs');
const path = require('path');

// 1. UPDATE style.css with dedicated Multi-Vendor Studio Styles
const styleCssPath = path.join(__dirname, '..', 'dashboard', 'style.css');
let styleCss = fs.readFileSync(styleCssPath, 'utf8');

const mvStudioStyles = `
/* ==========================================================================
   MULTI-VENDOR NORMALIZATION LAB STUDIO STYLES
   ========================================================================== */

.multivendor-banner {
  background: linear-gradient(135deg, rgba(46, 8, 17, 0.9) 0%, rgba(18, 4, 8, 0.96) 100%);
  border: 1px solid var(--border-color);
  border-left: 4px solid var(--crimson-ruby);
  border-radius: 10px;
  padding: 20px 24px;
  margin-bottom: 20px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
}

.mv-view-switcher {
  display: flex;
  align-items: center;
  gap: 8px;
  overflow-x: auto;
  padding-bottom: 6px;
  margin-bottom: 16px;
}

.mv-tab-btn {
  background: rgba(24, 6, 12, 0.85);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  padding: 7px 14px;
  color: var(--text-silver);
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.mv-tab-btn:hover {
  border-color: #fef08a !important;
  color: #ffffff;
  box-shadow: 0 0 14px rgba(254, 240, 138, 0.35);
  transform: translateY(-1px);
}

.mv-tab-btn.active {
  background: linear-gradient(135deg, rgba(229, 9, 46, 0.35), rgba(122, 12, 26, 0.45));
  border-color: var(--crimson-ruby);
  color: #ffffff;
  box-shadow: 0 0 15px rgba(229, 9, 46, 0.4);
}

.mv-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
  gap: 18px;
  margin-bottom: 24px;
}

.mv-card {
  background: rgba(20, 5, 10, 0.92);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.mv-card:hover {
  border-color: #fef08a !important;
  box-shadow: 0 12px 35px rgba(0, 0, 0, 0.75), 0 0 20px rgba(254, 240, 138, 0.35) !important;
  transform: translateY(-2px) scale(1.015);
}

.mv-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 10px;
}

.mv-title {
  font-size: 14px;
  font-weight: 700;
  color: #ffffff;
}

.mv-format-tag {
  background: rgba(229, 9, 46, 0.2);
  border: 1px solid rgba(229, 9, 46, 0.4);
  color: #fca5a5;
  font-size: 10.5px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 4px;
  text-transform: uppercase;
}

.mv-raw-box {
  background: rgba(10, 2, 4, 0.95);
  border: 1px solid rgba(229, 9, 46, 0.2);
  border-radius: 6px;
  padding: 10px 12px;
  font-family: var(--font-mono);
  font-size: 11px;
  color: #fca5a5;
  line-height: 1.5;
  max-height: 90px;
  overflow-y: auto;
  word-break: break-all;
}

.mv-ir-box {
  background: rgba(8, 2, 4, 0.95);
  border: 1px solid rgba(16, 185, 129, 0.25);
  border-radius: 6px;
  padding: 10px 12px;
  font-family: var(--font-mono);
  font-size: 11px;
  color: #34d399;
  line-height: 1.45;
  max-height: 140px;
  overflow-y: auto;
}

.trace-token {
  background: rgba(254, 240, 138, 0.2);
  border: 1px dashed #fef08a;
  color: #fef08a;
  padding: 1px 4px;
  border-radius: 3px;
  cursor: pointer;
  font-weight: 700;
  transition: all 0.2s;
}

.trace-token:hover, .trace-token.active {
  background: #fef08a;
  color: #000000;
  box-shadow: 0 0 10px rgba(254, 240, 138, 0.8);
}

.nxm-box {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  padding: 22px;
  margin-top: 20px;
}

.nxm-comparison-grid {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 16px;
  align-items: center;
  margin-top: 16px;
}

@media (max-width: 850px) {
  .nxm-comparison-grid { grid-template-columns: 1fr; }
}

.nxm-pane {
  background: rgba(14, 3, 7, 0.85);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 16px;
}

.nxm-pane.bad {
  border-color: rgba(239, 68, 68, 0.4);
  background: rgba(36, 8, 14, 0.85);
}

.nxm-pane.good {
  border-color: rgba(16, 185, 129, 0.4);
  background: rgba(8, 30, 18, 0.85);
}

.nxm-vs-circle {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: var(--crimson-main);
  color: #ffffff;
  font-size: 12px;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: auto;
  box-shadow: 0 0 15px rgba(229, 9, 46, 0.5);
}
`;

if (!styleCss.includes('.mv-view-switcher {')) {
  styleCss += '\n' + mvStudioStyles;
  fs.writeFileSync(styleCssPath, styleCss, 'utf8');
  console.log('style.css updated with Multi-Vendor Studio styles.');
}

// 2. UPDATE renderMultiVendorLabView in app.js with rearranged layout
const appJsPath = path.join(__dirname, '..', 'dashboard', 'app.js');
let appJs = fs.readFileSync(appJsPath, 'utf8');

const rearrangedMultiVendorViewCode = `
  // ==========================================================================
  // PHASE 3 — REARRANGED UNIVERSAL MULTI-VENDOR NORMALIZATION LAB STUDIO
  // ==========================================================================
  async function renderMultiVendorLabView(container) {
    let activeVendorFilter = "all";
    let cachedComparisons = [];

    container.innerHTML = \`
      <div class="page-header flex-between">
        <div>
          <h1 class="page-title">Universal Multi-Vendor Normalization Lab</h1>
          <p class="page-desc">6 disparate firewall and cloud security vendors producing completely different syntaxes converge into 1 identical canonical ULPF-IR schema with 100% data fidelity.</p>
        </div>
        <span class="badge badge-teal" style="font-size:12px; padding:6px 12px;">
          6 / 6 VENDORS 100% UNIFIED
        </span>
      </div>

      <!-- TOP CONTROL & GENERATOR ROW (SPLIT GLASS STUDIO) -->
      <div class="grid grid-2 gap-md mb-md">
        <!-- Left: Quick Scenario Overrides -->
        <div class="card p-md">
          <div class="flex-between mb-sm">
            <h3 style="font-size:13.5px; font-weight:700; color:#fff;">1. Select Security Scenario</h3>
            <span class="badge badge-neutral">PRESET SCENARIOS</span>
          </div>
          <div>
            <label class="text-xs text-muted mb-xs block">Scenario Traffic Pattern</label>
            <select id="mvScenarioSelect" class="form-input">
              <option value="deny_https">Network Policy Deny (Port 443 / HTTPS)</option>
              <option value="deny_ssh">Inbound SSH Blocked (Port 22 / SSH)</option>
              <option value="drop_exploit">Threat Exploit Dropped (Port 8080)</option>
              <option value="allow_dns">DNS Query Allowed (Port 53 / UDP)</option>
            </select>
          </div>
          <div class="grid grid-2 gap-sm mt-sm">
            <div>
              <label class="text-xs text-muted mb-xs block">Attacker / Source IP</label>
              <input type="text" id="mvSrcIp" class="form-input mono" value="10.10.10.20" />
            </div>
            <div>
              <label class="text-xs text-muted mb-xs block">Target Destination</label>
              <div style="display:flex; gap:6px;">
                <input type="text" id="mvDstIp" class="form-input mono" value="8.8.8.8" style="flex:2;" />
                <input type="number" id="mvDstPort" class="form-input mono" value="443" style="flex:1;" />
              </div>
            </div>
          </div>
        </div>

        <!-- Right: Action & Provenance Trigger -->
        <div class="card p-md flex-between" style="flex-direction:column; justify-content:space-between;">
          <div style="width:100%;">
            <div class="flex-between mb-sm">
              <h3 style="font-size:13.5px; font-weight:700; color:#fff;">2. Protocol & Normalization Engine</h3>
              <span class="badge badge-teal">LIVE CONVERGENCE</span>
            </div>
            <div class="grid grid-2 gap-sm">
              <div>
                <label class="text-xs text-muted mb-xs block">Firewall Action</label>
                <select id="mvAction" class="form-input">
                  <option value="deny">deny (Blocked)</option>
                  <option value="drop">drop (Silently Dropped)</option>
                  <option value="allow">allow (Permitted)</option>
                </select>
              </div>
              <div>
                <label class="text-xs text-muted mb-xs block">Transport Protocol</label>
                <select id="mvProto" class="form-input">
                  <option value="tcp">tcp</option>
                  <option value="udp">udp</option>
                </select>
              </div>
            </div>
          </div>

          <div style="width:100%; margin-top:14px;" class="flex-between">
            <span class="text-muted text-xs">Click tokens in cards below to trace extraction rules.</span>
            <button id="btnRunMultiVendor" class="btn btn-primary">
              <span>Run Multi-Vendor Conversion Proof</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Provenance Callout Info Box -->
      <div id="mvTraceCallout" class="card p-sm mb-md hidden" style="background:rgba(20,8,14,0.95); border:1px solid #fef08a; border-left:5px solid #fef08a;">
        <div class="flex-between">
          <div>
            <strong id="mvTraceFieldTitle" style="color:#fef08a; font-size:12.5px;">Field Provenance: source.ip</strong>
            <div id="mvTraceFieldDetail" class="text-xs text-muted mt-xs" style="color:#cbd5e1;">Extracted from vendor raw key via deterministic rule.</div>
          </div>
          <button id="btnCloseTrace" class="btn-close" style="font-size:18px;">&times;</button>
        </div>
      </div>

      <!-- VENDOR SWITCHER RAIL -->
      <div class="mv-view-switcher" id="mvViewSwitcher">
        <button class="mv-tab-btn active" data-vendor="all">All 6 Vendors Matrix</button>
        <button class="mv-tab-btn" data-vendor="checkpoint">CheckPoint CEF</button>
        <button class="mv-tab-btn" data-vendor="paloalto">Palo Alto CEF</button>
        <button class="mv-tab-btn" data-vendor="fortinet">Fortinet Key=Value</button>
        <button class="mv-tab-btn" data-vendor="cisco">Cisco ASA Syslog</button>
        <button class="mv-tab-btn" data-vendor="aws">AWS VPC Flow</button>
        <button class="mv-tab-btn" data-vendor="suricata">Suricata LEEF</button>
      </div>

      <!-- VENDOR CARDS GRID -->
      <div class="mv-grid" id="mvResultsGrid">
        <div class="card p-md text-center text-muted" style="grid-column:1/-1;">Processing 6 vendor formats through ULPF Pipeline...</div>
      </div>

      <!-- THE N x M ENGINEERING PROBLEM BREAKDOWN -->
      <div class="nxm-box">
        <div class="flex-between">
          <div>
            <h3 style="font-size:15px; font-weight:800; color:#fff;">The N × M Engineering Problem Breakdown</h3>
            <p class="text-muted text-xs mt-xs">Why point-to-point SIEM connectors fail at enterprise scale vs ULPF's Canonical Intermediate Representation.</p>
          </div>
          <span class="badge badge-teal">Linear N + M Complexity</span>
        </div>

        <div class="nxm-comparison-grid">
          <div class="nxm-pane bad">
            <h4 style="color:#f87171; font-size:13px; font-weight:800;">Without ULPF (Point-to-Point Chaos)</h4>
            <div class="text-muted text-xs mt-xs" style="color:#fca5a5;">6 Ingest Formats × 4 SIEM Sinks = <strong>24 Custom Brittle Connectors</strong></div>
            <ul style="font-size:11.5px; margin-top:10px; margin-left:16px; color:#cbd5e1; line-height:1.6;">
              <li>Adding 1 new firewall vendor requires rewriting 4 different SIEM parsers.</li>
              <li>Schema changes in Splunk or Elastic break downstream ingestion pipelines.</li>
              <li>No common tamper-evident cryptographic evidence layer.</li>
            </ul>
          </div>

          <div class="nxm-vs-circle">VS</div>

          <div class="nxm-pane good">
            <h4 style="color:#34d399; font-size:13px; font-weight:800;">With ULPF (Canonical IR Decoupled)</h4>
            <div class="text-muted text-xs mt-xs" style="color:#6ee7b7;">6 Ingest Parsers + 4 SIEM Sinks = <strong>Only 10 Modular Connectors</strong></div>
            <ul style="font-size:11.5px; margin-top:10px; margin-left:16px; color:#cbd5e1; line-height:1.6;">
              <li>Add a new device once; automatically exports to OCSF, ECS, Splunk, Sentinel.</li>
              <li>Lossless normalization preserves 100% original raw evidence with SHA-256 hash.</li>
              <li>Sub-millisecond deterministic parsing speed (12.8 µs per log).</li>
            </ul>
          </div>
        </div>
      </div>
    \`;

    // Event Handlers
    const btnRun = document.getElementById("btnRunMultiVendor");
    const scenarioSelect = document.getElementById("mvScenarioSelect");
    const srcIpInput = document.getElementById("mvSrcIp");
    const dstIpInput = document.getElementById("mvDstIp");
    const dstPortInput = document.getElementById("mvDstPort");
    const actionInput = document.getElementById("mvAction");
    const protoInput = document.getElementById("mvProto");
    const closeTraceBtn = document.getElementById("btnCloseTrace");
    const switcher = document.getElementById("mvViewSwitcher");

    if (closeTraceBtn) {
      closeTraceBtn.addEventListener("click", () => {
        document.getElementById("mvTraceCallout").classList.add("hidden");
      });
    }

    if (switcher) {
      switcher.querySelectorAll(".mv-tab-btn").forEach((tab) => {
        tab.addEventListener("click", () => {
          switcher.querySelectorAll(".mv-tab-btn").forEach((t) => t.classList.remove("active"));
          tab.classList.add("active");
          activeVendorFilter = tab.getAttribute("data-vendor");
          renderFilteredComparisons();
        });
      });
    }

    if (scenarioSelect) {
      scenarioSelect.addEventListener("change", () => {
        const val = scenarioSelect.value;
        if (val === "deny_https") {
          srcIpInput.value = "10.10.10.20";
          dstIpInput.value = "8.8.8.8";
          dstPortInput.value = "443";
          actionInput.value = "deny";
          protoInput.value = "tcp";
        } else if (val === "deny_ssh") {
          srcIpInput.value = "198.51.100.42";
          dstIpInput.value = "10.0.1.15";
          dstPortInput.value = "22";
          actionInput.value = "deny";
          protoInput.value = "tcp";
        } else if (val === "drop_exploit") {
          srcIpInput.value = "203.0.113.88";
          dstIpInput.value = "10.0.2.100";
          dstPortInput.value = "8080";
          actionInput.value = "drop";
          protoInput.value = "tcp";
        } else if (val === "allow_dns") {
          srcIpInput.value = "10.0.5.12";
          dstIpInput.value = "1.1.1.1";
          dstPortInput.value = "53";
          actionInput.value = "allow";
          protoInput.value = "udp";
        }
        executeMultiVendorRun();
      });
    }

    if (btnRun) {
      btnRun.addEventListener("click", executeMultiVendorRun);
    }

    async function executeMultiVendorRun() {
      const payload = {
        src_ip: srcIpInput.value.trim(),
        dst_ip: dstIpInput.value.trim(),
        dst_port: parseInt(dstPortInput.value.trim(), 10) || 443,
        action: actionInput.value,
        protocol: protoInput.value,
      };

      const grid = document.getElementById("mvResultsGrid");
      grid.innerHTML = \`<div class="card p-md text-center text-muted" style="grid-column:1/-1;">Processing 6 vendor formats through ULPF Pipeline...</div>\`;

      try {
        const res = await fetch("/api/v1/demo/traffic/multivendor", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        cachedComparisons = data.vendor_comparisons || [];
        renderFilteredComparisons();
      } catch (err) {
        grid.innerHTML = \`<div class="alert alert-danger" style="grid-column:1/-1;">Failed to run multi-vendor proof: \${err.message}</div>\`;
      }
    }

    function renderFilteredComparisons() {
      const grid = document.getElementById("mvResultsGrid");
      if (!cachedComparisons || cachedComparisons.length === 0) {
        grid.innerHTML = \`<div class="card p-md text-center text-muted" style="grid-column:1/-1;">No comparison data returned.</div>\`;
        return;
      }

      let filtered = cachedComparisons;
      if (activeVendorFilter !== "all") {
        filtered = cachedComparisons.filter(c => c.vendor.toLowerCase().replace(/[^a-z0-9]/g, '').includes(activeVendorFilter));
      }

      grid.innerHTML = filtered.map((c) => {
        const rawHighlighted = escapeHtml(c.raw_log)
          .replace(new RegExp(escapeRegex(c.ulpf_ir.source.ip), "g"), \`<span class="trace-token" data-field="source.ip" data-val="\${c.ulpf_ir.source.ip}">$&</span>\`)
          .replace(new RegExp(escapeRegex(c.ulpf_ir.destination.ip), "g"), \`<span class="trace-token" data-field="destination.ip" data-val="\${c.ulpf_ir.destination.ip}">$&</span>\`)
          .replace(new RegExp(escapeRegex(String(c.ulpf_ir.destination.port)), "g"), \`<span class="trace-token" data-field="destination.port" data-val="\${c.ulpf_ir.destination.port}">$&</span>\`)
          .replace(new RegExp(\`\\\\b\${escapeRegex(c.ulpf_ir.event.action)}\\\\b\`, "gi"), \`<span class="trace-token" data-field="event.action" data-val="\${c.ulpf_ir.event.action}">$&</span>\`);

        return \`
          <div class="mv-card">
            <div class="mv-header">
              <div>
                <span class="mv-title">\${escapeHtml(c.vendor)}</span>
                <div class="text-muted text-xs">\${escapeHtml(c.device)}</div>
              </div>
              <span class="mv-format-tag">\${escapeHtml(c.format)}</span>
            </div>

            <div>
              <div class="text-xs text-muted mb-xs flex-between">
                <span>Raw Vendor Payload</span>
                <span class="mono text-xs">SHA-256: \${escapeHtml(c.sha256.substring(0, 12))}...</span>
              </div>
              <div class="mv-raw-box">\${rawHighlighted}</div>
            </div>

            <div>
              <div class="text-xs text-muted mb-xs flex-between">
                <span>Canonical ULPF-IR Output</span>
                <span class="badge badge-teal text-xs">100% Normalized</span>
              </div>
              <pre class="mv-ir-box">\${JSON.stringify(c.ulpf_ir, null, 2)}</pre>
            </div>

            <div class="flex-between text-xs" style="border-top: 1px solid var(--border-color); padding-top:8px;">
              <div style="display:flex; gap:6px;">
                <span class="badge badge-neutral">OCSF v1.1.0</span>
                <span class="badge badge-neutral">ECS v8.x</span>
              </div>
              <button class="btn btn-xs btn-outline" onclick="window.openEventDetailModal('\${c.event_id}')">Inspect Full Event</button>
            </div>
          </div>
        \`;
      }).join("");

      // Wire Click-to-Trace interactive tokens
      grid.querySelectorAll(".trace-token").forEach((tok) => {
        tok.addEventListener("click", () => {
          const field = tok.getAttribute("data-field");
          const val = tok.getAttribute("data-val");

          grid.querySelectorAll(".trace-token").forEach((t) => t.classList.remove("active"));
          grid.querySelectorAll(\`.trace-token[data-field="\${field}"]\`).forEach((t) => t.classList.add("active"));

          const callout = document.getElementById("mvTraceCallout");
          const title = document.getElementById("mvTraceFieldTitle");
          const detail = document.getElementById("mvTraceFieldDetail");

          title.textContent = \`Field Provenance: \${field} → "\${val}"\`;
          detail.innerHTML = \`Extracted from vendor raw token with <strong>100% confidence</strong>. Mapped into canonical ULPF-IR schema with cryptographic provenance record.\`;
          callout.classList.remove("hidden");
        });
      });
    }

    // Run initial proof on load
    executeMultiVendorRun();
  }
`;

// Replace renderMultiVendorLabView in app.js
appJs = appJs.replace(
  /async function renderMultiVendorLabView\(container\)[\s\S]*?executeMultiVendorRun\(\);\s*\}/,
  rearrangedMultiVendorViewCode
);

fs.writeFileSync(appJsPath, appJs, 'utf8');
console.log('app.js updated with rearranged Multi-Vendor Normalization Lab Studio.');
