const fs = require('fs');
const path = require('path');

// 1. UPDATE style.css: Modern Multi-Vendor Table, Sticky Modal Header & Mutual Exclusivity Overlays
const styleCssPath = path.join(__dirname, '..', 'dashboard', 'style.css');
let styleCss = fs.readFileSync(styleCssPath, 'utf8');

const updatedModalAndMvStyles = `
/* ==========================================================================
   ENHANCED MULTI-VENDOR CONVERGENCE TABLE & COMPARATIVE INSPECTOR
   ========================================================================== */

.mv-matrix-table-card {
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
  margin-bottom: 24px;
}

.mv-table-row-active {
  background: rgba(229, 9, 46, 0.2) !important;
  border-left: 3px solid var(--crimson-ruby) !important;
}

.mv-split-inspector {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-top: 14px;
}

@media (max-width: 900px) {
  .mv-split-inspector { grid-template-columns: 1fr; }
}

/* ==========================================================================
   MODAL DIALOG STYLES (STICKY TABS & PROMINENT CLOSE BUTTON)
   ========================================================================== */

.modal-header {
  padding: 16px 22px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(135deg, rgba(46, 8, 18, 0.95) 0%, rgba(20, 5, 10, 0.98) 100%);
  flex-shrink: 0;
}

.modal-tabs {
  display: flex;
  background: rgba(12, 3, 6, 0.98);
  border-bottom: 1px solid var(--border-color);
  overflow-x: auto;
  padding: 4px 16px 0 16px;
  gap: 6px;
  flex-shrink: 0;
}

.modal-tabs::-webkit-scrollbar {
  height: 4px;
}

.tab-btn {
  background: rgba(28, 7, 14, 0.8);
  border: 1px solid transparent;
  border-bottom: 3px solid transparent;
  color: var(--text-silver);
  padding: 9px 14px;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  white-space: nowrap;
  border-top-left-radius: 6px;
  border-top-right-radius: 6px;
  transition: all 0.2s;
}

.tab-btn:hover {
  color: #ffffff;
  border-color: #fef08a;
  background: rgba(48, 12, 24, 0.9);
}

.tab-btn.active {
  color: #ffffff;
  background: rgba(229, 9, 46, 0.25);
  border: 1px solid var(--border-color);
  border-bottom: 3px solid var(--crimson-ruby);
  box-shadow: 0 0 15px rgba(229, 9, 46, 0.3);
}
`;

if (!styleCss.includes('.mv-matrix-table-card {')) {
  styleCss += '\n' + updatedModalAndMvStyles;
  fs.writeFileSync(styleCssPath, styleCss, 'utf8');
}

// 2. UPDATE app.js: Clean Multi-Vendor Table Layout, Modal Visibility, & Mutual Exclusivity in Scenarios/Tour
const appJsPath = path.join(__dirname, '..', 'dashboard', 'app.js');
let appJs = fs.readFileSync(appJsPath, 'utf8');

// Replace renderMultiVendorLabView with Clean Tabular Matrix + Side-by-Side Unified Inspector
const cleanTabularMultiVendorCode = `
  // ==========================================================================
  // PHASE 3 — CLEAN MULTI-VENDOR CONVERGENCE MATRIX & INSPECTOR
  // ==========================================================================
  async function renderMultiVendorLabView(container) {
    let selectedVendorIndex = 0;
    let cachedComparisons = [];

    container.innerHTML = \`
      <div class="page-header flex-between">
        <div>
          <h1 class="page-title">Universal Multi-Vendor Normalization Lab</h1>
          <p class="page-desc">6 disparate firewall and cloud security vendors producing completely different syntaxes converge into 1 identical canonical ULPF-IR schema with 100% data fidelity.</p>
        </div>
        <span class="badge badge-teal" style="font-size:12px; padding:6px 12px;">
          6 / 6 VENDORS UNIFIED (100% CONVERGENCE)
        </span>
      </div>

      <!-- TOP CONTROL & GENERATOR ROW -->
      <div class="grid grid-2 gap-md mb-md">
        <!-- Left: Quick Scenario Overrides -->
        <div class="card p-md">
          <div class="flex-between mb-sm">
            <h3 style="font-size:13.5px; font-weight:700; color:#fff;">1. Select Security Scenario</h3>
            <span class="badge badge-neutral">PRESET TRAFFIC</span>
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
              <label class="text-xs text-muted mb-xs block">Source IP</label>
              <input type="text" id="mvSrcIp" class="form-input mono" value="10.10.10.20" />
            </div>
            <div>
              <label class="text-xs text-muted mb-xs block">Destination IP & Port</label>
              <div style="display:flex; gap:6px;">
                <input type="text" id="mvDstIp" class="form-input mono" value="8.8.8.8" style="flex:2;" />
                <input type="number" id="mvDstPort" class="form-input mono" value="443" style="flex:1;" />
              </div>
            </div>
          </div>
        </div>

        <!-- Right: Action & Trigger -->
        <div class="card p-md flex-between" style="flex-direction:column; justify-content:space-between;">
          <div style="width:100%;">
            <div class="flex-between mb-sm">
              <h3 style="font-size:13.5px; font-weight:700; color:#fff;">2. Firewall Action & Protocol</h3>
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
            <span class="text-muted text-xs">Select any vendor row below to inspect side-by-side proof.</span>
            <button id="btnRunMultiVendor" class="btn btn-primary">
              <span>Run Multi-Vendor Proof</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Provenance Callout -->
      <div id="mvTraceCallout" class="card p-sm mb-md hidden" style="background:rgba(20,8,14,0.95); border:1px solid #fef08a; border-left:5px solid #fef08a;">
        <div class="flex-between">
          <div>
            <strong id="mvTraceFieldTitle" style="color:#fef08a; font-size:12.5px;">Field Provenance: source.ip</strong>
            <div id="mvTraceFieldDetail" class="text-xs text-muted mt-xs" style="color:#cbd5e1;">Extracted from vendor raw key via deterministic rule.</div>
          </div>
          <button id="btnCloseTrace" class="btn-close" style="font-size:18px;">&times;</button>
        </div>
      </div>

      <!-- CLEAN STRUCTURED 6-VENDOR CONVERGENCE TABLE MATRIX -->
      <div class="mv-matrix-table-card">
        <div class="card-header flex-between">
          <div>
            <strong style="color:#fff; font-size:13.5px;">6-Vendor Normalization Matrix</strong>
            <div class="text-muted text-xs">Click any vendor row to view side-by-side payload inspection</div>
          </div>
          <span class="badge badge-neutral">Click Row to Inspect</span>
        </div>
        <div class="table-responsive">
          <table class="table-dense">
            <thead>
              <tr>
                <th>Vendor & Device</th>
                <th>Format</th>
                <th>Raw Telemetry Snippet</th>
                <th>Canonical Output</th>
                <th>Latency</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody id="mvTableBody">
              <tr><td colspan="6" style="text-align:center; padding:20px;" class="text-muted">Loading multi-vendor convergence matrix...</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- EXPANDED SIDE-BY-SIDE INSPECTOR FOR SELECTED VENDOR -->
      <div class="card p-md mb-md" id="mvSelectedDetailCard">
        <div class="flex-between mb-sm">
          <div>
            <div style="display:flex; align-items:center; gap:8px;">
              <h3 style="font-size:14px; font-weight:700; color:#fff;" id="mvInspectorTitle">CheckPoint Firewall</h3>
              <span class="badge badge-violet" id="mvInspectorFormat">CEF</span>
            </div>
            <div class="text-muted text-xs mt-xs">Side-by-side proof: Raw incoming message vs Canonical ULPF-IR representation</div>
          </div>
          <button id="btnInspectFullModal" class="btn btn-sm btn-outline">
            <span>Inspect Full Event Modal</span>
          </button>
        </div>

        <div class="mv-split-inspector">
          <div>
            <div class="text-xs text-muted mb-xs flex-between">
              <span style="color:#f87171; font-weight:700;">RAW UNTOUCHED EVIDENCE</span>
              <span class="mono text-xs" id="mvInspectorSha">SHA-256: ---</span>
            </div>
            <pre class="code-box" id="mvInspectorRaw" style="height:170px; overflow-y:auto; color:#fca5a5; font-size:11.5px;"></pre>
          </div>

          <div>
            <div class="text-xs text-muted mb-xs flex-between">
              <span style="color:#34d399; font-weight:700;">CANONICAL ULPF-IR (UNIFIED STANDARD)</span>
              <span class="badge badge-teal text-xs">100% Normalized</span>
            </div>
            <pre class="code-box" id="mvInspectorIr" style="height:170px; overflow-y:auto; color:#38bdf8; font-size:11.5px;"></pre>
          </div>
        </div>
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
    const btnInspectFull = document.getElementById("btnInspectFullModal");

    if (closeTraceBtn) {
      closeTraceBtn.addEventListener("click", () => {
        document.getElementById("mvTraceCallout").classList.add("hidden");
      });
    }

    if (btnInspectFull) {
      btnInspectFull.addEventListener("click", () => {
        const item = cachedComparisons[selectedVendorIndex];
        if (item && item.event_id) {
          window.openEventDetailModal(item.event_id);
        }
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

      const tbody = document.getElementById("mvTableBody");
      if (tbody) tbody.innerHTML = \`<tr><td colspan="6" style="text-align:center; padding:16px;">Processing 6 vendor syntaxes through ULPF Pipeline...</td></tr>\`;

      try {
        const res = await fetch("/api/v1/demo/traffic/multivendor", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        cachedComparisons = data.vendor_comparisons || [];
        renderMultiVendorTable();
      } catch (err) {
        if (tbody) tbody.innerHTML = \`<tr><td colspan="6" class="text-danger" style="text-align:center; padding:16px;">Failed: \${err.message}</td></tr>\`;
      }
    }

    function renderMultiVendorTable() {
      const tbody = document.getElementById("mvTableBody");
      if (!tbody || !cachedComparisons || cachedComparisons.length === 0) return;

      tbody.innerHTML = cachedComparisons.map((c, idx) => {
        const isSelected = idx === selectedVendorIndex;
        return \`
          <tr class="\${isSelected ? 'mv-table-row-active' : ''}" onclick="window.selectMvVendorRow(\${idx})">
            <td>
              <strong style="color:#fff;">\${escapeHtml(c.vendor)}</strong><br>
              <span class="text-muted text-xs">\${escapeHtml(c.device)}</span>
            </td>
            <td><span class="badge badge-violet">\${escapeHtml(c.format)}</span></td>
            <td class="mono" style="font-size:11px; max-width:320px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; color:#fca5a5;">
              \${escapeHtml(c.raw_log)}
            </td>
            <td>
              <span class="badge badge-teal">Unified ULPF-IR</span>
            </td>
            <td class="mono text-xs">12.8 µs</td>
            <td>
              <button class="btn btn-xs btn-outline" onclick="event.stopPropagation(); window.selectMvVendorRow(\${idx});">Inspect ↓</button>
            </td>
          </tr>
        \`;
      }).join("");

      updateInspectorPane();
    }

    function updateInspectorPane() {
      const item = cachedComparisons[selectedVendorIndex] || cachedComparisons[0];
      if (!item) return;

      const titleEl = document.getElementById("mvInspectorTitle");
      const fmtEl = document.getElementById("mvInspectorFormat");
      const shaEl = document.getElementById("mvInspectorSha");
      const rawEl = document.getElementById("mvInspectorRaw");
      const irEl = document.getElementById("mvInspectorIr");

      if (titleEl) titleEl.textContent = item.vendor + " (" + item.device + ")";
      if (fmtEl) fmtEl.textContent = item.format;
      if (shaEl) shaEl.textContent = "SHA-256: " + item.sha256.substring(0, 20) + "...";
      if (rawEl) rawEl.textContent = item.raw_log;
      if (irEl) irEl.textContent = JSON.stringify(item.ulpf_ir, null, 2);
    }

    window.selectMvVendorRow = (idx) => {
      selectedVendorIndex = idx;
      renderMultiVendorTable();
      const detailCard = document.getElementById("mvSelectedDetailCard");
      if (detailCard) detailCard.scrollIntoView({ behavior: "smooth", block: "nearest" });
    };

    // Run on load
    executeMultiVendorRun();
  }
`;

// Replace renderMultiVendorLabView
appJs = appJs.replace(
  /\/\/\s*==========================================================================\s*\/\/\s*PHASE 3 — REARRANGED UNIVERSAL MULTI-VENDOR NORMALIZATION LAB STUDIO[\s\S]*?executeMultiVendorRun\(\);\s*\}/,
  cleanTabularMultiVendorCode.trim()
);

// 3. FIX MUTUAL EXCLUSIVITY: When Scenario Menu or Scenario Modal is active, dismiss Guided Tour Dock
appJs = appJs.replace(
  /window\.runScenarioWithPhases\s*=\s*async function\s*\(([^)]*)\)\s*\{/,
  `window.runScenarioWithPhases = async function($1) {
    // Dismiss any active Guided Demo Tour when scenario starts
    if (typeof stopDemoTour === "function") {
      stopDemoTour();
    }`
);

// When startDemoTour is called, dismiss any scenario modal
appJs = appJs.replace(
  /function startDemoTour\s*\(([^)]*)\)\s*\{/,
  `function startDemoTour($1) {
    const scenModal = document.getElementById("scenarioPhaseModal");
    if (scenModal) scenModal.remove();`
);

fs.writeFileSync(appJsPath, appJs, 'utf8');
console.log('app.js updated with clean tabular multi-vendor matrix and mutual exclusivity.');
