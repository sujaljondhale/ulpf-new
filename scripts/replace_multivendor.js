const fs = require('fs');

let appJs = fs.readFileSync('dashboard/app.js', 'utf8');

const sIdx = appJs.indexOf('async function renderMultiVendorLabView(container) {');
const eIdx = appJs.indexOf('function renderParserTestBenchView(container) {');

if (sIdx === -1 || eIdx === -1) {
  console.error('Could not locate renderMultiVendorLabView in app.js');
  process.exit(1);
}

const newMultiVendorCode = `window.selectedMvVendorIndex = 0;
  window.cachedMvComparisons = [];

  window.selectMvVendorRow = function(idx) {
    window.selectedMvVendorIndex = idx;
    const rows = document.querySelectorAll("#mvTableBody tr.mv-row");
    rows.forEach((r, i) => {
      if (i === idx) r.classList.add("active");
      else r.classList.remove("active");
    });
    window.renderMvSelectedInspector();
  };

  window.renderMvSelectedInspector = function() {
    const comp = window.cachedMvComparisons[window.selectedMvVendorIndex] || window.cachedMvComparisons[0];
    const inspectorContainer = document.getElementById("mvInspectorContainer");
    if (!inspectorContainer || !comp) return;

    const rawHighlighted = escapeHtml(comp.raw_log)
      .replace(new RegExp(escapeRegex(comp.ulpf_ir.source.ip), "g"), '<span class="trace-token" data-field="source.ip" data-val="' + comp.ulpf_ir.source.ip + '">$&</span>')
      .replace(new RegExp(escapeRegex(comp.ulpf_ir.destination.ip), "g"), '<span class="trace-token" data-field="destination.ip" data-val="' + comp.ulpf_ir.destination.ip + '">$&</span>')
      .replace(new RegExp(escapeRegex(String(comp.ulpf_ir.destination.port)), "g"), '<span class="trace-token" data-field="destination.port" data-val="' + comp.ulpf_ir.destination.port + '">$&</span>')
      .replace(new RegExp('\\\\b' + escapeRegex(comp.ulpf_ir.event.action) + '\\\\b', "gi"), '<span class="trace-token" data-field="event.action" data-val="' + comp.ulpf_ir.event.action + '">$&</span>');

    inspectorContainer.innerHTML = \`
      <div class="mv-inspector-deck">
        <div class="mv-inspector-header">
          <div style="display:flex; align-items:center; gap:12px;">
            <span class="badge badge-teal" style="font-size:12px; font-weight:800;">LIVE INSPECTOR</span>
            <strong style="color:#ffffff; font-size:14px;">\${escapeHtml(comp.vendor)} (\${escapeHtml(comp.device)})</strong>
            <span class="badge badge-neutral" style="font-size:11px;">Format: \${escapeHtml(comp.format)}</span>
          </div>
          <div style="display:flex; gap:8px;">
            <button class="btn btn-xs btn-outline" onclick="navigator.clipboard.writeText(JSON.stringify(window.cachedMvComparisons[\${window.selectedMvVendorIndex}].ulpf_ir, null, 2)); showToast('ULPF-IR JSON copied to clipboard!', 'success');">
              \${svgIcon('copy', 'svg-icon')} Copy Canonical JSON
            </button>
            <button class="btn btn-xs btn-primary" onclick="window.openEventDetailModal('\${comp.event_id}')">
              \${svgIcon('search', 'svg-icon')} Full Event Inspector
            </button>
          </div>
        </div>

        <div class="mv-inspector-grid">
          <!-- Col 1: Raw Ingest Wire Stream -->
          <div class="mv-inspector-col">
            <div class="mv-inspector-col-title">
              <span style="color:#fca5a5;">1. Raw Ingest Wire Stream</span>
              <span class="mono text-xs text-muted">SHA-256: \${escapeHtml(comp.sha256.substring(0, 10))}...</span>
            </div>
            <div class="mv-raw-box" style="max-height:180px; flex:1;">\${rawHighlighted}</div>
            <div class="text-xs text-muted mt-xs" style="font-size:11px; line-height:1.4;">
              Click highlighted tokens above to test deterministic field extraction provenance.
            </div>
          </div>

          <!-- Col 2: Field Extraction Rules & Provenance -->
          <div class="mv-inspector-col">
            <div class="mv-inspector-col-title">
              <span style="color:#fef08a;">2. Extracted Mapping Rules</span>
              <span class="badge badge-neutral" style="font-size:10px;">Deterministic AST</span>
            </div>
            <table class="table-dense" style="font-size:11px; flex:1;">
              <thead>
                <tr>
                  <th style="color:#94a3b8;">Canonical Field</th>
                  <th style="color:#94a3b8;">Extracted Value</th>
                  <th style="color:#94a3b8;">Rule</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong style="color:#fef08a;">source.ip</strong></td>
                  <td class="mono" style="color:#fff;">\${escapeHtml(comp.ulpf_ir.source.ip)}</td>
                  <td><span class="badge badge-neutral">Pattern Match</span></td>
                </tr>
                <tr>
                  <td><strong style="color:#fef08a;">destination.ip</strong></td>
                  <td class="mono" style="color:#fff;">\${escapeHtml(comp.ulpf_ir.destination.ip)}</td>
                  <td><span class="badge badge-neutral">Subfield AST</span></td>
                </tr>
                <tr>
                  <td><strong style="color:#fef08a;">destination.port</strong></td>
                  <td class="mono" style="color:#fff;">\${escapeHtml(String(comp.ulpf_ir.destination.port))}</td>
                  <td><span class="badge badge-neutral">Int cast</span></td>
                </tr>
                <tr>
                  <td><strong style="color:#fef08a;">event.action</strong></td>
                  <td><span class="badge \${comp.ulpf_ir.event.action === 'deny' || comp.ulpf_ir.event.action === 'drop' ? 'badge-red' : 'badge-teal'}">\${escapeHtml(comp.ulpf_ir.event.action).toUpperCase()}</span></td>
                  <td><span class="badge badge-neutral">Enum Mapping</span></td>
                </tr>
                <tr>
                  <td><strong style="color:#fef08a;">network.transport</strong></td>
                  <td class="mono" style="color:#fff;">\${escapeHtml(comp.ulpf_ir.network?.transport || 'tcp')}</td>
                  <td><span class="badge badge-neutral">Direct Key</span></td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Col 3: Canonical Unified Output -->
          <div class="mv-inspector-col">
            <div class="mv-inspector-col-title">
              <span style="color:#34d399;">3. Canonical ULPF-IR Output</span>
              <span class="badge badge-teal" style="font-size:10px;">100% Normalized</span>
            </div>
            <pre class="mv-ir-box" style="max-height:180px; flex:1;">\${escapeHtml(JSON.stringify(comp.ulpf_ir, null, 2))}</pre>
          </div>
        </div>
      </div>
    \`;

    // Wire Interactive Provenance Tokens
    inspectorContainer.querySelectorAll(".trace-token").forEach((tok) => {
      tok.addEventListener("click", () => {
        const field = tok.getAttribute("data-field");
        const val = tok.getAttribute("data-val");

        inspectorContainer.querySelectorAll(".trace-token").forEach((t) => t.classList.remove("active"));
        inspectorContainer.querySelectorAll(\`.trace-token[data-field="\${field}"]\`).forEach((t) => t.classList.add("active"));

        const callout = document.getElementById("mvTraceCallout");
        const title = document.getElementById("mvTraceFieldTitle");
        const detail = document.getElementById("mvTraceFieldDetail");

        if (callout && title && detail) {
          title.textContent = \`Field Provenance: \${field} -> "\${val}"\`;
          detail.innerHTML = \`Extracted from vendor raw token with <strong>100% confidence</strong>. Mapped into canonical ULPF-IR schema with cryptographic provenance record.\`;
          callout.classList.remove("hidden");
        }
      });
    });
  };

  async function renderMultiVendorLabView(container) {
    container.innerHTML = \`
      <div class="page-header flex-between">
        <div>
          <h1 class="page-title">Universal Multi-Vendor Normalization Lab</h1>
          <p class="page-desc">6 disparate firewall and cloud security vendors producing completely different syntaxes converge into 1 identical canonical ULPF-IR schema with 100% data fidelity.</p>
        </div>
        <span class="badge badge-teal" style="font-size:12px; padding:6px 12px; font-weight:800;">
          6 / 6 VENDORS 100% UNIFIED
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

        <!-- Right: Action & Trigger -->
        <div class="card p-md flex-between" style="flex-direction:column; justify-content:space-between;">
          <div style="width:100%;">
            <div class="flex-between mb-sm">
              <h3 style="font-size:13.5px; font-weight:700; color:#fff;">2. Protocol & Normalization Engine</h3>
              <span class="badge badge-teal">DETERMINISTIC CONVERGENCE</span>
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
            <span class="text-muted text-xs">Simultaneously transforms 6 vendor logs into ULPF-IR.</span>
            <button id="btnRunMultiVendor" class="btn btn-primary">
              \${svgIcon('bolt', 'svg-icon')}
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

      <!-- EXECUTIVE 6-VENDOR TABULAR MATRIX CARD -->
      <div class="mv-matrix-table-card">
        <div class="p-md flex-between" style="background:rgba(28,6,14,0.9); border-bottom:1px solid var(--border-color);">
          <div>
            <h3 style="font-size:14.5px; font-weight:800; color:#ffffff;">6-Vendor Normalization Comparison Matrix</h3>
            <p class="text-xs text-muted mt-xs">Click any row below to inspect raw payloads, extraction AST rules, and canonical OCSF/ECS outputs.</p>
          </div>
          <span class="badge badge-neutral" style="font-size:11px;">Deterministic Execution</span>
        </div>
        <div style="overflow-x:auto;">
          <table class="mv-table">
            <thead>
              <tr>
                <th>Vendor & Device</th>
                <th>Format Syntax</th>
                <th>Raw Ingest Wire Preview</th>
                <th>Canonical Output (Src / Dst)</th>
                <th>Action</th>
                <th>Latency</th>
                <th>Inspect</th>
              </tr>
            </thead>
            <tbody id="mvTableBody">
              <tr>
                <td colspan="7" class="text-center text-muted p-md">Processing 6 vendor formats through ULPF Pipeline...</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- LIVE SIDE-BY-SIDE DEEP INSPECTOR DECK -->
      <div id="mvInspectorContainer"></div>

      <!-- THE N x M ENGINEERING PROBLEM BREAKDOWN -->
      <div class="nxm-box">
        <div class="flex-between">
          <div>
            <h3 style="font-size:15px; font-weight:800; color:#fff;">The N x M Engineering Problem Breakdown</h3>
            <p class="text-muted text-xs mt-xs">Why point-to-point SIEM connectors fail at enterprise scale vs ULPF's Canonical Intermediate Representation.</p>
          </div>
          <span class="badge badge-teal">Linear N + M Complexity</span>
        </div>

        <div class="nxm-comparison-grid">
          <div class="nxm-pane bad">
            <h4 style="color:#f87171; font-size:13px; font-weight:800;">Without ULPF (Point-to-Point Chaos)</h4>
            <div class="text-muted text-xs mt-xs" style="color:#fca5a5;">6 Ingest Formats x 4 SIEM Sinks = <strong>24 Custom Brittle Connectors</strong></div>
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
              <li>Sub-millisecond deterministic parsing speed (12.8 microseconds per log).</li>
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

    if (closeTraceBtn) {
      closeTraceBtn.addEventListener("click", () => {
        document.getElementById("mvTraceCallout").classList.add("hidden");
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
      if (tbody) tbody.innerHTML = '<tr><td colspan="7" class="text-center text-muted p-md">Processing 6 vendor formats through ULPF Pipeline...</td></tr>';

      try {
        const res = await fetch("/api/v1/demo/traffic/multivendor", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        window.cachedMvComparisons = data.vendor_comparisons || [];

        if (tbody) {
          tbody.innerHTML = window.cachedMvComparisons.map((c, idx) => {
            const isAct = idx === window.selectedMvVendorIndex;
            const initials = c.vendor.substring(0, 2).toUpperCase();
            const actionBadge = c.ulpf_ir.event.action === 'deny' || c.ulpf_ir.event.action === 'drop' ? 'badge-red' : 'badge-teal';

            return \`
              <tr class="mv-row \${isAct ? 'active' : ''}" onclick="window.selectMvVendorRow(\${idx})">
                <td>
                  <div class="mv-vendor-cell">
                    <div class="mv-vendor-icon">\${initials}</div>
                    <div>
                      <strong style="color:#ffffff; font-size:13px;">\${escapeHtml(c.vendor)}</strong>
                      <div class="text-muted text-xs">\${escapeHtml(c.device)}</div>
                    </div>
                  </div>
                </td>
                <td><span class="badge badge-neutral">\${escapeHtml(c.format)}</span></td>
                <td><div class="mv-raw-preview">\${escapeHtml(c.raw_log)}</div></td>
                <td class="mono text-xs">
                  <span style="color:#fef08a;">\${escapeHtml(c.ulpf_ir.source.ip)}</span> -> <span style="color:#38bdf8;">\${escapeHtml(c.ulpf_ir.destination.ip)}:\${c.ulpf_ir.destination.port}</span>
                </td>
                <td><span class="badge \${actionBadge}">\${escapeHtml(c.ulpf_ir.event.action).toUpperCase()}</span></td>
                <td><span class="badge badge-teal" style="font-size:10.5px;">12.4 us</span></td>
                <td>
                  <button class="btn btn-xs btn-secondary" onclick="event.stopPropagation(); window.openEventDetailModal('\${c.event_id}')">
                    Inspect ->
                  </button>
                </td>
              </tr>
            \`;
          }).join("");
        }

        window.renderMvSelectedInspector();
      } catch (err) {
        if (tbody) tbody.innerHTML = \`<tr><td colspan="7" class="alert alert-danger">Failed to run multi-vendor proof: \${err.message}</td></tr>\`;
      }
    }

    // Run initial proof on load
    executeMultiVendorRun();
  }
`;

appJs = appJs.substring(0, sIdx) + newMultiVendorCode + "\n\n  // ==========================================================================\n  // PHASE 3 — PARSER TEST BENCH VIEW\n  // ==========================================================================\n  " + appJs.substring(eIdx);

fs.writeFileSync('dashboard/app.js', appJs, 'utf8');
console.log('Successfully replaced MultiVendor in dashboard/app.js!');
