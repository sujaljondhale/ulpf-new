const fs = require('fs');
const path = require('path');

// ==============================================================================
// 1. UPDATE style.css: Preset chips, Scenarios Phase Player, Cancel Button
// ==============================================================================
const styleCssPath = path.join(__dirname, '..', 'dashboard', 'style.css');
let styleCss = fs.readFileSync(styleCssPath, 'utf8');

const extraCss = `
/* ==========================================================================
   PRESET CHIPS & TEST BENCH BUTTONS (FIXED: NO WHITE BACKGROUNDS)
   ========================================================================== */

.testbench-presets {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 8px;
  margin-bottom: 14px;
}

.preset-chip {
  background: rgba(28, 7, 14, 0.9) !important;
  color: #e2e8f0 !important;
  border: 1px solid var(--border-color) !important;
  border-radius: 6px !important;
  padding: 6px 12px !important;
  font-size: 11.5px !important;
  font-weight: 600 !important;
  font-family: var(--font-sans) !important;
  cursor: pointer !important;
  outline: none !important;
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.4) !important;
}

.preset-chip:hover {
  background: rgba(48, 12, 24, 0.95) !important;
  border-color: #fef08a !important;
  color: #ffffff !important;
  box-shadow: 0 0 16px rgba(254, 240, 138, 0.4), 0 4px 12px rgba(0, 0, 0, 0.6) !important;
  transform: translateY(-2px) scale(1.03) !important;
}

.preset-chip.active {
  background: linear-gradient(135deg, rgba(229, 9, 46, 0.4), rgba(122, 12, 26, 0.5)) !important;
  border-color: var(--crimson-ruby) !important;
  color: #ffffff !important;
  box-shadow: 0 0 14px rgba(229, 9, 46, 0.4) !important;
}

.preset-chip.danger {
  border-color: rgba(239, 68, 68, 0.4) !important;
  color: #fca5a5 !important;
  background: rgba(40, 8, 14, 0.9) !important;
}

.preset-chip.danger:hover {
  border-color: #fef08a !important;
  background: rgba(60, 12, 20, 0.95) !important;
  box-shadow: 0 0 16px rgba(254, 240, 138, 0.45) !important;
}

/* ==========================================================================
   SCENARIO PHASE-BY-PHASE EXECUTION PLAYER (FLOATING MODAL)
   ========================================================================== */

.scenario-phase-modal {
  position: fixed;
  top: 75px;
  right: 24px;
  width: 440px;
  max-width: calc(100vw - 48px);
  background: rgba(20, 5, 10, 0.96);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border: 1px solid var(--border-glow);
  border-radius: 12px;
  box-shadow: 0 25px 70px rgba(0, 0, 0, 0.85), 0 0 35px rgba(229, 9, 46, 0.35);
  z-index: 99995;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  animation: phase-slide 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes phase-slide {
  from { transform: translateX(40px) scale(0.95); opacity: 0; }
  to { transform: translateX(0) scale(1); opacity: 1; }
}

.scenario-phase-header {
  padding: 14px 18px;
  background: linear-gradient(135deg, rgba(60, 12, 22, 0.9) 0%, rgba(24, 6, 12, 0.95) 100%);
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.scenario-phase-body {
  padding: 18px;
}

.phase-step-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 10px;
  border-radius: 6px;
  margin-bottom: 8px;
  background: rgba(28, 7, 14, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: all 0.25s;
}

.phase-step-item.active {
  background: rgba(229, 9, 46, 0.2);
  border-color: #fef08a;
  box-shadow: 0 0 16px rgba(254, 240, 138, 0.35);
  transform: scale(1.02);
}

.phase-step-item.completed {
  border-color: rgba(16, 185, 129, 0.4);
  background: rgba(16, 185, 129, 0.08);
}

.phase-step-icon {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: rgba(40, 10, 18, 0.8);
  border: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 800;
  color: var(--text-silver);
  flex-shrink: 0;
}

.phase-step-item.active .phase-step-icon {
  background: var(--crimson-main);
  color: #ffffff;
  border-color: #fef08a;
  box-shadow: 0 0 10px rgba(254, 240, 138, 0.5);
}

.phase-step-item.completed .phase-step-icon {
  background: #10b981;
  color: #ffffff;
  border-color: #34d399;
}
`;

if (!styleCss.includes('.preset-chip {')) {
  styleCss += '\n' + extraCss;
  fs.writeFileSync(styleCssPath, styleCss, 'utf8');
}

// ==============================================================================
// 2. CLEAN UP ALL REMAINING INLINE WHITE BACKGROUNDS IN app.js
// ==============================================================================
const appJsPath = path.join(__dirname, '..', 'dashboard', 'app.js');
let appJs = fs.readFileSync(appJsPath, 'utf8');

// Replace remaining white/light inline backgrounds in app.js
appJs = appJs
  .replace(/style="background:\s*#fef2f2;[^"]*"/g, 'style="background: rgba(40, 8, 14, 0.85); border: 1px solid rgba(239, 68, 68, 0.4); border-radius: 6px; padding: 14px;"')
  .replace(/style="background:\s*#fffbeb;[^"]*"/g, 'style="background: rgba(40, 16, 8, 0.85); border: 1px solid rgba(245, 158, 11, 0.4); border-radius: 6px; padding: 14px;"')
  .replace(/style="background:\s*#eff6ff;[^"]*"/g, 'style="background: rgba(18, 12, 36, 0.85); border: 1px solid rgba(99, 102, 241, 0.4); border-radius: 6px; padding: 14px;"')
  .replace(/style="background:\s*#ecfdf5;[^"]*"/g, 'style="background: rgba(8, 32, 20, 0.85); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 6px; padding: 14px;"')
  .replace(/style="background:\s*#f8fafc;[^"]*"/g, 'style="background: rgba(22, 6, 12, 0.85); border: 1px solid var(--border-color); border-radius: 6px; padding: 14px;"')
  .replace(/style="background:\s*#ffffff;[^"]*"/g, 'style="background: rgba(28, 7, 14, 0.85); border: 1px solid var(--border-color); border-radius: 6px; padding: 10px;"');

// Add Scenario Phase-by-Phase Interactive Engine in app.js
const scenarioPhaseEngine = `
  // --- SCENARIO PHASE-BY-PHASE EXECUTION RUNNER WITH REAL-TIME EXPLANATIONS ---
  window.runScenarioWithPhases = async function(scenarioId, scenarioName) {
    const existing = document.getElementById("scenarioPhaseModal");
    if (existing) existing.remove();

    const phases = [
      {
        num: 1,
        title: "Phase 1: Multi-Protocol Network Ingestion",
        desc: "Capturing incoming raw network packets and computing immutable SHA-256 cryptographic hashes."
      },
      {
        num: 2,
        title: "Phase 2: Structural Format Detection",
        desc: "Evaluating syntax (CEF, LEEF, Syslog, JSON, KV) to select the optimal compiled deterministic parser."
      },
      {
        num: 3,
        title: "Phase 3: ULPF-IR Normalization & Threat Inspection",
        desc: "Translating proprietary vendor fields into canonical format and scanning for cyber threat signatures."
      },
      {
        num: 4,
        title: "Phase 4: Downstream Multi-Target Export & Defense",
        desc: "Delivering clean OCSF/ECS payloads to OpenSearch and enforcing automated IP blacklist rules."
      }
    ];

    const modal = document.createElement("div");
    modal.id = "scenarioPhaseModal";
    modal.className = "scenario-phase-modal";
    modal.innerHTML = \`
      <div class="scenario-phase-header">
        <div>
          <span class="badge badge-amber" style="font-size:10px;">LIVE SCENARIO RUNNER</span>
          <h4 style="font-size:13.5px; font-weight:700; color:#fff; margin-top:2px;">\${scenarioName}</h4>
        </div>
        <button id="btnCloseScenarioModal" class="btn-close" style="font-size:18px;">&times;</button>
      </div>
      <div class="scenario-phase-body">
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
          <span id="scenarioPhaseStatus" class="text-xs text-muted">Executing Scenario...</span>
          <button id="btnDismissScenarioModal" class="btn btn-xs btn-primary">Done</button>
        </div>
      </div>
    \`;

    document.body.appendChild(modal);

    document.getElementById("btnCloseScenarioModal").onclick = () => modal.remove();
    document.getElementById("btnDismissScenarioModal").onclick = () => modal.remove();

    // Step 1
    const p1 = document.getElementById("phaseStep_1");
    if (p1) p1.classList.add("active");

    try {
      const res = await fetch(\`/api/v1/demo/scenarios/\${scenarioId}\`, { method: "POST" });
      const data = await res.json();

      await new Promise(r => setTimeout(r, 600));
      if (p1) { p1.classList.remove("active"); p1.classList.add("completed"); }

      const p2 = document.getElementById("phaseStep_2");
      if (p2) p2.classList.add("active");
      await new Promise(r => setTimeout(r, 700));
      if (p2) { p2.classList.remove("active"); p2.classList.add("completed"); }

      const p3 = document.getElementById("phaseStep_3");
      if (p3) p3.classList.add("active");
      await new Promise(r => setTimeout(r, 700));
      if (p3) { p3.classList.remove("active"); p3.classList.add("completed"); }

      const p4 = document.getElementById("phaseStep_4");
      if (p4) { p4.classList.add("active"); }
      await new Promise(r => setTimeout(r, 600));
      if (p4) { p4.classList.remove("active"); p4.classList.add("completed"); }

      const statusEl = document.getElementById("scenarioPhaseStatus");
      if (statusEl) statusEl.innerHTML = '<span style="color:#34d399; font-weight:700;">OK All 4 Phases Executed Successfully!</span>';

      fetchEvents();
      fetchMetrics();
      fetchUnknownLogs();
      if (state.currentRoute === "events") refreshEventsTable();
    } catch (e) {
      showToast("Scenario run error: " + e.message, "error");
    }
  };
`;

// Hook dropdown items to the Phase-by-Phase Runner
appJs = appJs.replace(
  /item\.addEventListener\("click", async \(\) => \{[\s\S]*?showToast\(`Scenario executed:[\s\S]*?\}\);/g,
  `item.addEventListener("click", async () => {
    const scenarioId = item.getAttribute("data-scenario");
    const scenarioName = item.querySelector("strong") ? item.querySelector("strong").textContent : "Demo Scenario";
    menuScenario.classList.add("hidden");
    window.runScenarioWithPhases(scenarioId, scenarioName);
  });`
);

// Inject scenarioPhaseEngine before closing IIFE
appJs = appJs.replace(/\}\)\(\);?\s*$/, scenarioPhaseEngine + '\n})();\n');

fs.writeFileSync(appJsPath, appJs, 'utf8');
console.log('app.js updated with phase-by-phase scenario runner and dark theme styles.');

// ==============================================================================
// 3. UPDATE index.html with Cancel Tour Button in Explanation Dock
// ==============================================================================
const indexHtmlPath = path.join(__dirname, '..', 'dashboard', 'index.html');
let indexHtml = fs.readFileSync(indexHtmlPath, 'utf8');

// Ensure Cancel / Exit Tour button is prominently displayed in the explanation header and footer
indexHtml = indexHtml.replace(
  '<button id="btnCloseDemoTour" class="btn-close" title="Exit Guided Demo">&times;</button>',
  '<button id="btnCloseDemoTour" class="btn btn-xs btn-danger-outline" title="Cancel and Exit Guided Demo" style="padding:2px 8px; font-size:10.5px;">✕ Exit Demo</button>'
);

fs.writeFileSync(indexHtmlPath, indexHtml, 'utf8');
console.log('index.html updated with explicit Exit Demo button.');
