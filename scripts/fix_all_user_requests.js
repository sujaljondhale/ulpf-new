const fs = require('fs');
const path = require('path');

const appJsPath = path.join(__dirname, '..', 'dashboard', 'app.js');
let appJs = fs.readFileSync(appJsPath, 'utf8');

// 1. Fix parser_iot_gateway_pipe styling (remove light purple #faf5ff)
appJs = appJs.replace(
  '<tr style="background:#faf5ff;">',
  '<tr>'
);
appJs = appJs.replace(
  '<span class="threat-tag" style="background:#f3e8ff; color:#6b21a8; border-color:#d8b4fe;"> AI-ASSISTED</span>',
  '<span class="badge badge-violet">AI-ASSISTED</span>'
);

// 2. Fix Sovereign Unknown Log Onboarding Workflow Flowchart UI in sih-demo
const oldFlowchartRegex = /<div style="margin-top: 8px; font-family: var\(--font-mono\); font-size: 11px; background: #ffffff;[\s\S]*?DETERMINISTIC PROCESSING\s*<\/div>/;
const newFlowchartHtml = `
            <div class="ai-workflow-rail mt-sm">
              <div class="workflow-chip"><span class="chip-step">1</span> Unknown Log</div>
              <div class="workflow-arrow">→</div>
              <div class="workflow-chip highlight"><span class="chip-step">2</span> Local SLM AI</div>
              <div class="workflow-arrow">→</div>
              <div class="workflow-chip"><span class="chip-step">3</span> Parser Spec</div>
              <div class="workflow-arrow">→</div>
              <div class="workflow-chip"><span class="chip-step">4</span> Human Review</div>
              <div class="workflow-arrow">→</div>
              <div class="workflow-chip approve"><span class="chip-step">5</span> Approve & Promote</div>
              <div class="workflow-arrow">→</div>
              <div class="workflow-chip deterministic"><span class="chip-step">6</span> Deterministic Engine</div>
            </div>
`;
appJs = appJs.replace(oldFlowchartRegex, newFlowchartHtml);

// 3. Fix Before / After Normalization Comparator to NOT reload/redirect page
const oldComparatorHtml = `
      <!-- 5. LIVE BEFORE / AFTER SIDE-BY-SIDE COMPARATOR -->
      <div class="card p-md mb-md" id="comparatorCard">
        <div class="flex-between mb-sm">
          <div>
            <h2 style="font-size: 15px; font-weight: 700;">Live "Before / After" Normalization Comparator</h2>
            <div class="text-muted" style="font-size: 12px;">Inspect raw incoming telemetry versus canonical ULPF-IR representation side-by-side with zero page reload.</div>
          </div>
          <div class="comparator-preset-bar" id="comparatorPresetBar">
            \${sihSamplePresets.map((s, idx) => \`
              <button class="btn btn-sm \${idx === activeSihPresetIndex ? 'btn-primary' : 'btn-secondary'} comp-preset-btn" data-preset-idx="\${idx}" onclick="window.selectSihPreset(\${idx})">
                \${s.vendor.split(' ')[0]}
              </button>
            \`).join('')}
          </div>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 12px;">
          <div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
              <span style="font-size: 12px; font-weight: 700; color: #f87171;">RAW INCOMING LOG (UNTOUCHED EVIDENCE)</span>
              <span class="badge badge-neutral" id="compRawFormatBadge">\${currentSample.format}</span>
            </div>
            <pre class="code-box" id="comparatorRawPre" style="height: 180px; overflow: auto; color: #fca5a5; font-size: 11.5px;">\${escapeHtml(currentSample.raw)}</pre>
          </div>

          <div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
              <span style="font-size: 12px; font-weight: 700; color: #34d399;">NORMALIZED CANONICAL ULPF-IR</span>
              <span class="badge badge-teal">ULPF-IR v1.0 Schema</span>
            </div>
            <pre class="code-box" id="comparatorIrPre" style="height: 180px; overflow: auto; color: #38bdf8; font-size: 11.5px;">\${escapeHtml(JSON.stringify({
              ulpf_version: "1.0",
              event: { category: "network", action: currentSample.action, time: "2026-09-06T14:32:10Z" },
              source: { ip: currentSample.srcIp, port: 54321 },
              destination: { ip: currentSample.dstIp, port: currentSample.dstPort },
              network: { transport: currentSample.proto.toLowerCase(), protocol: "https" },
              device: { vendor: currentSample.vendor, product: currentSample.device },
              raw_sha256: currentSample.sha256
            }, null, 2))}</pre>
          </div>
        </div>
      </div>
`;

appJs = appJs.replace(
  /<!-- 5\. LIVE BEFORE \/ AFTER SIDE-BY-SIDE COMPARATOR -->[\s\S]*?<!-- 6\. EVIDENCE, BENCHMARKS/,
  oldComparatorHtml + '\n\n      <!-- 6. EVIDENCE, BENCHMARKS'
);

// 4. Update window.selectSihPreset to smoothly update UI in-place without page refresh
const newSelectSihPresetCode = `
  window.selectSihPreset = function (idx) {
    activeSihPresetIndex = idx;
    const sample = sihSamplePresets[idx] || sihSamplePresets[0];
    const stage = sihStages[activeSihStageIndex] || sihStages[0];

    // Update preset buttons on comparator card
    document.querySelectorAll(".comp-preset-btn").forEach((btn) => {
      const pIdx = parseInt(btn.getAttribute("data-preset-idx"), 10);
      if (pIdx === idx) {
        btn.className = "btn btn-sm btn-primary comp-preset-btn";
      } else {
        btn.className = "btn btn-sm btn-secondary comp-preset-btn";
      }
    });

    // Update sample selector chips on stepper
    document.querySelectorAll(".sample-chip").forEach((chip, cIdx) => {
      if (cIdx === idx) chip.classList.add("active");
      else chip.classList.remove("active");
    });

    // Update Comparator content in place
    const rawPre = document.getElementById("comparatorRawPre");
    const irPre = document.getElementById("comparatorIrPre");
    const fmtBadge = document.getElementById("compRawFormatBadge");

    if (rawPre) rawPre.textContent = sample.raw;
    if (fmtBadge) fmtBadge.textContent = sample.format;
    if (irPre) {
      irPre.textContent = JSON.stringify({
        ulpf_version: "1.0",
        event: { category: "network", action: sample.action, time: "2026-09-06T14:32:10Z" },
        source: { ip: sample.srcIp, port: 54321 },
        destination: { ip: sample.dstIp, port: sample.dstPort },
        network: { transport: sample.proto.toLowerCase(), protocol: "https" },
        device: { vendor: sample.vendor, product: sample.device },
        raw_sha256: sample.sha256
      }, null, 2);
    }

    // Update Stage Transform Deck if present
    const transform = stage.getTransform(sample);
    const deckPanes = document.querySelectorAll(".stage-transform-deck .deck-pane");
    if (deckPanes.length >= 2) {
      deckPanes[0].querySelector(".deck-pane-title span:first-child").textContent = transform.leftTitle;
      deckPanes[0].querySelector(".deck-data-box").textContent = transform.leftContent;
      deckPanes[1].querySelector(".deck-pane-title span:first-child").textContent = transform.rightTitle;
      deckPanes[1].querySelector(".deck-data-box").textContent = transform.rightContent;
    }
  };
`;

appJs = appJs.replace(
  /window\.selectSihPreset = function \(idx\) \{[\s\S]*?\};/,
  newSelectSihPresetCode
);

// 5. Build Smart Interactive Scenario Exploration Engine (explores relevant website pages + reveals backend architecture)
const upgradedScenarioEngine = `
  // --- MULTI-PAGE SCENARIO EXPLORATION ENGINE WITH BACKEND & DOCKER ARCHITECTURE EXPLANATION ---
  window.runScenarioWithPhases = async function(scenarioId, scenarioName) {
    const existing = document.getElementById("scenarioPhaseModal");
    if (existing) existing.remove();

    // Context details per scenario
    const scenarioConfigs = {
      scenario_1: {
        route: "sih-demo",
        targetSelector: ".step-visualizer-card",
        subtitle: "Normal Enterprise Multi-Vendor Traffic",
        backendSummary: "FastAPI Ingestion Engine + Redis Buffer (Docker Container: ulpf_api)",
        backendDetails: "Ingesting 15 mixed logs (CheckPoint CEF, Fortinet KV, Nginx JSON, Linux Syslog). The Python worker queues packets in memory, computes SHA-256 digests, and validates fields against Pydantic schemas in under 80 microseconds."
      },
      scenario_2: {
        route: "events",
        targetSelector: ".table-responsive",
        subtitle: "Active Security Incident & Instant Blacklist",
        backendSummary: "In-Stream Signature Evaluator + Firewall Block Gate (Docker Container: ulpf_worker)",
        backendDetails: "Detecting SQL Injection and RCE payloads. The backend flags malicious attacker IPs in real-time and broadcasts a security alert over Server-Sent Events (SSE). Clicking Blacklist IP instantly propagates defense rules across all gateways."
      },
      scenario_3: {
        route: "system/health",
        targetSelector: ".grid-3",
        subtitle: "High-Volume Velocity Attack & Cluster Resilience",
        backendSummary: "Full Docker Compose Stack: FastAPI + MinIO S3 + OpenSearch 2.11 Cluster",
        backendDetails: "Stress testing the pipeline at 12,000+ events/sec. Worker processes handle backpressure through bounded in-memory ring buffers and persist immutable raw evidence to local storage and MinIO S3 buckets with zero packet loss."
      },
      scenario_4: {
        route: "intelligence/ai-onboarding",
        targetSelector: ".unknown-logs-container",
        subtitle: "Unknown SCADA Device Ingestion & AI Synthesis",
        backendSummary: "Local Sovereign SLM (Qwen2.5-Coder) + Compiler Engine (Docker: ulpf_ai)",
        backendDetails: "An unparsed SCADA RTU Hex message is quarantined in the review queue. The local air-gapped SLM analyzes the byte stream, extracts fields, and generates a valid declarative YAML parser for 1-click human promotion."
      }
    };

    const cfg = scenarioConfigs[scenarioId] || scenarioConfigs.scenario_1;

    // 1. Navigate to target page if not already there (Scenario 1 stays on sih-demo, others explore live website)
    if (state.currentRoute !== cfg.route) {
      window.location.hash = "#/" + cfg.route;
    }

    const phases = [
      {
        num: 1,
        title: "Phase 1: Multi-Protocol Network Ingestion",
        desc: "Capturing incoming raw packets & computing SHA-256 immutable hashes."
      },
      {
        num: 2,
        title: "Phase 2: Format Detection & Parser Selection",
        desc: "Evaluating syntax to execute optimal sub-millisecond compiled parser."
      },
      {
        num: 3,
        title: "Phase 3: ULPF-IR Normalization & Threat Inspection",
        desc: "Mapping vendor fields to standard schema & inspecting security signatures."
      },
      {
        num: 4,
        title: "Phase 4: Downstream Multi-Target Export & Action",
        desc: "Delivering OCSF/ECS to OpenSearch & enforcing firewall defense rules."
      }
    ];

    const modal = document.createElement("div");
    modal.id = "scenarioPhaseModal";
    modal.className = "scenario-phase-modal";
    modal.innerHTML = \`
      <div class="scenario-phase-header">
        <div>
          <span class="badge badge-amber" style="font-size:10px;">LIVE SCENARIO & BACKEND RUNNER</span>
          <h4 style="font-size:13.5px; font-weight:700; color:#fff; margin-top:2px;">\${scenarioName}</h4>
        </div>
        <button id="btnCloseScenarioModal" class="btn btn-xs btn-danger-outline" style="padding:2px 8px; font-size:10.5px;">✕ Cancel & Close</button>
      </div>
      <div class="scenario-phase-body">
        <!-- Backend Docker Architecture Box -->
        <div class="backend-arch-card mb-sm">
          <div style="font-size:10.5px; font-weight:800; color:#fef08a; text-transform:uppercase; letter-spacing:0.5px;">
            BACKEND INFRASTRUCTURE IN ACTION:
          </div>
          <div style="font-size:12px; font-weight:700; color:#ffffff; margin-top:2px;">
            \${cfg.backendSummary}
          </div>
          <div style="font-size:11px; color:#cbd5e1; margin-top:4px; line-height:1.45;">
            \${cfg.backendDetails}
          </div>
        </div>

        <div id="scenarioPhaseList">
          \${phases.map(p => \`
            <div class="phase-step-item" id="phaseStep_\${p.num}">
              <div class="phase-step-icon">\${p.num}</div>
              <div>
                <strong style="color:#fff; font-size:12px;">\${p.title}</strong>
                <div class="text-muted" style="font-size:11px; margin-top:2px;">\${p.desc}</div>
              </div>
            </div>
          \`).join('')}
        </div>
        <div class="mt-sm flex-between" style="border-top:1px solid var(--border-color); padding-top:10px;">
          <span id="scenarioPhaseStatus" class="text-xs text-muted">Running backend pipeline...</span>
          <div style="display:flex; gap:6px;">
            <button id="btnDismissScenarioModal" class="btn btn-xs btn-primary">Done</button>
          </div>
        </div>
      </div>
    \`;

    document.body.appendChild(modal);

    document.getElementById("btnCloseScenarioModal").onclick = () => modal.remove();
    document.getElementById("btnDismissScenarioModal").onclick = () => modal.remove();

    // Trigger API call
    const p1 = document.getElementById("phaseStep_1");
    if (p1) p1.classList.add("active");

    try {
      const res = await fetch(\`/api/v1/demo/scenarios/\${scenarioId}\`, { method: "POST" });
      const data = await res.json();

      await new Promise(r => setTimeout(r, 600));
      if (p1) { p1.classList.remove("active"); p1.classList.add("completed"); }

      const p2 = document.getElementById("phaseStep_2");
      if (p2) p2.classList.add("active");
      await new Promise(r => setTimeout(r, 600));
      if (p2) { p2.classList.remove("active"); p2.classList.add("completed"); }

      const p3 = document.getElementById("phaseStep_3");
      if (p3) p3.classList.add("active");
      await new Promise(r => setTimeout(r, 600));
      if (p3) { p3.classList.remove("active"); p3.classList.add("completed"); }

      const p4 = document.getElementById("phaseStep_4");
      if (p4) p4.classList.add("active");
      await new Promise(r => setTimeout(r, 500));
      if (p4) { p4.classList.remove("active"); p4.classList.add("completed"); }

      const statusEl = document.getElementById("scenarioPhaseStatus");
      if (statusEl) statusEl.innerHTML = '<span style="color:#34d399; font-weight:700;">OK All 4 Backend Phases Executed!</span>';

      fetchEvents();
      fetchMetrics();
      fetchUnknownLogs();
      if (state.currentRoute === "events") refreshEventsTable();
    } catch (e) {
      showToast("Scenario error: " + e.message, "error");
    }
  };
`;

appJs = appJs.replace(
  /\/\/\s*---\s*SCENARIO PHASE-BY-PHASE EXECUTION RUNNER[\s\S]*?window\.runScenarioWithPhases\s*=\s*async function[\s\S]*?\};\s*\}\)\(\);?\s*$/,
  upgradedScenarioEngine + '\n})();\n'
);

fs.writeFileSync(appJsPath, appJs, 'utf8');
console.log('app.js updated with in-place comparator, new AI flowchart, and multi-page backend scenario explorer.');

// 6. Update style.css with styles for the new AI flowchart and Backend Architecture Card
const styleCssPath2 = path.join(__dirname, '..', 'dashboard', 'style.css');
let styleCss2 = fs.readFileSync(styleCssPath2, 'utf8');

const workflowAndBackendCss = `
/* ==========================================================================
   AI WORKFLOW FLOWCHART & BACKEND ARCHITECTURE CARD
   ========================================================================== */

.ai-workflow-rail {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  padding: 12px;
  background: rgba(16, 4, 8, 0.95);
  border: 1px solid var(--border-color);
  border-radius: 8px;
}

.workflow-chip {
  background: rgba(28, 7, 14, 0.9);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  padding: 6px 10px;
  font-size: 11px;
  font-weight: 700;
  color: var(--text-silver);
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.25s;
}

.workflow-chip .chip-step {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: rgba(229, 9, 46, 0.3);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 9.5px;
}

.workflow-chip.highlight {
  background: rgba(229, 9, 46, 0.25);
  border-color: #fef08a;
  color: #ffffff;
  box-shadow: 0 0 12px rgba(254, 240, 138, 0.35);
}

.workflow-chip.approve {
  background: rgba(16, 185, 129, 0.2);
  border-color: #34d399;
  color: #34d399;
}

.workflow-chip.deterministic {
  background: rgba(99, 102, 241, 0.2);
  border-color: #818cf8;
  color: #c7d2fe;
}

.workflow-arrow {
  color: var(--crimson-ruby);
  font-weight: 800;
  font-size: 13px;
}

.backend-arch-card {
  background: rgba(14, 3, 7, 0.92);
  border: 1px solid var(--border-color);
  border-left: 4px solid #fef08a;
  border-radius: 6px;
  padding: 10px 12px;
}
`;

if (!styleCss2.includes('.ai-workflow-rail {')) {
  styleCss2 += '\n' + workflowAndBackendCss;
  fs.writeFileSync(styleCssPath2, styleCss2, 'utf8');
  console.log('style.css updated with AI workflow rail and backend arch card.');
}
