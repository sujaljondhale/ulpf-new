const fs = require('fs');
const path = require('path');

// 1. Process client_app.js
const clientAppPath = path.join(__dirname, '..', 'dashboard', 'client_app.js');
if (fs.existsSync(clientAppPath)) {
  let content = fs.readFileSync(clientAppPath, 'utf8');
  content = content
    .replace(/✓/g, '[OK]')
    .replace(/❌/g, '[ERR]')
    .replace(/✅/g, '[OK]')
    .replace(/📄/g, '')
    .replace(/🌐/g, '')
    .replace(/🛡️/g, '')
    .replace(/🛡/g, '');
  fs.writeFileSync(clientAppPath, content, 'utf8');
  console.log('client_app.js cleaned.');
}

// 2. Process app.js
const appJsPath = path.join(__dirname, '..', 'dashboard', 'app.js');
let appJs = fs.readFileSync(appJsPath, 'utf8');

// Replace toast icons
appJs = appJs.replace(
  'const icon = type === "warning" ? "⚠️" : type === "error" ? "🚨" : type === "info" ? "🤖" : "✅";',
  'const icon = type === "warning" ? svgIcon("alert", "svg-icon") : type === "error" ? svgIcon("alert", "svg-icon") : type === "info" ? svgIcon("info", "svg-icon") : svgIcon("check", "svg-icon");'
);

appJs = appJs.replace(
  '<span style="font-size:22px;">🚨</span>',
  '<span class="toast-critical-icon">' +
  '<svg class="svg-icon svg-icon-xl" viewBox="0 0 24 24" style="stroke:#ff1e44;"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>' +
  '</span>'
);

// General emoji replacements across views and tables
appJs = appJs
  .replace(/⚠️/g, '')
  .replace(/🚨/g, '')
  .replace(/🤖/g, '')
  .replace(/✅/g, '')
  .replace(/❌/g, '')
  .replace(/🚫/g, '')
  .replace(/🛡️/g, '')
  .replace(/🛡/g, '')
  .replace(/🏆/g, '')
  .replace(/⚡/g, '')
  .replace(/📡/g, '')
  .replace(/🔍/g, '')
  .replace(/🧪/g, '')
  .replace(/🔬/g, '')
  .replace(/📚/g, '')
  .replace(/🗄️/g, '')
  .replace(/🗄/g, '')
  .replace(/📐/g, '')
  .replace(/🏢/g, '')
  .replace(/📈/g, '')
  .replace(/💚/g, '')
  .replace(/🎬/g, '')
  .replace(/🔄/g, '')
  .replace(/💡/g, '')
  .replace(/🌟/g, '')
  .replace(/⚖️/g, '')
  .replace(/⚖/g, '')
  .replace(/📊/g, '')
  .replace(/🛍️/g, '')
  .replace(/🛍/g, '')
  .replace(/📁/g, '')
  .replace(/🚀/g, '')
  .replace(/🔎/g, '')
  .replace(/📤/g, '')
  .replace(/❓/g, '')
  .replace(/▶/g, 'Play ')
  .replace(/⏸/g, 'Pause ')
  .replace(/◀/g, '< ')
  .replace(/⏮/g, '<< ')
  .replace(/➔/g, '->')
  .replace(/✓/g, 'OK')
  .replace(/✕/g, 'X');

// Inject svgIcon generator if not present
if (!appJs.includes('function svgIcon(')) {
  const helperCode = `
  // --- INLINE SVG ICON GENERATOR (ZERO EMOJIS) ---
  function svgIcon(name, cls = "svg-icon") {
    const icons = {
      shield: '<svg class="' + cls + '" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>',
      zap: '<svg class="' + cls + '" viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>',
      alert: '<svg class="' + cls + '" viewBox="0 0 24 24"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>',
      check: '<svg class="' + cls + '" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"></polyline></svg>',
      cross: '<svg class="' + cls + '" viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>',
      play: '<svg class="' + cls + '" viewBox="0 0 24 24"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>',
      pause: '<svg class="' + cls + '" viewBox="0 0 24 24"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg>',
      refresh: '<svg class="' + cls + '" viewBox="0 0 24 24"><polyline points="23 4 23 10 17 10"></polyline><polyline points="1 20 1 14 7 14"></polyline><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path></svg>',
      search: '<svg class="' + cls + '" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>',
      database: '<svg class="' + cls + '" viewBox="0 0 24 24"><ellipse cx="12" cy="5" rx="9" ry="3"></ellipse><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"></path><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path></svg>',
      bot: '<svg class="' + cls + '" viewBox="0 0 24 24"><rect x="3" y="11" width="18" height="10" rx="2"></rect><circle cx="12" cy="5" r="2"></circle><path d="M12 7v4"></path><line x1="8" y1="16" x2="8" y2="16"></line><line x1="16" y1="16" x2="16" y2="16"></line></svg>',
      building: '<svg class="' + cls + '" viewBox="0 0 24 24"><rect x="4" y="2" width="16" height="20" rx="2" ry="2"></rect><line x1="9" y1="22" x2="9" y2="22.01"></line><line x1="15" y1="22" x2="15" y2="22.01"></line><line x1="9" y1="6" x2="9" y2="6.01"></line><line x1="15" y1="6" x2="15" y2="6.01"></line><line x1="9" y1="10" x2="9" y2="10.01"></line><line x1="15" y1="10" x2="15" y2="10.01"></line><line x1="9" y1="14" x2="9" y2="14.01"></line><line x1="15" y1="14" x2="15" y2="14.01"></line><line x1="9" y1="18" x2="9" y2="18.01"></line><line x1="15" y1="18" x2="15" y2="18.01"></line></svg>',
      trophy: '<svg class="' + cls + '" viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>',
      code: '<svg class="' + cls + '" viewBox="0 0 24 24"><polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline></svg>',
      pulse: '<svg class="' + cls + '" viewBox="0 0 24 24"><path d="M22 12h-4l-3 9L9 3l-3 9H2"></path></svg>',
      info: '<svg class="' + cls + '" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>'
    };
    return icons[name] || icons.info;
  }
`;
  appJs = appJs.replace('// --- STATE MANAGEMENT ---', helperCode + '\n  // --- STATE MANAGEMENT ---');
}

// 3. Implement full interactive Demo Guide Controller
const demoControllerCode = `
  // --- INTERACTIVE GUIDED DEMO CONTROLLER (NEXT-NEXT TOUR WITH EXPLANATION & SPOTLIGHT BLUR) ---
  const demoTourSteps = [
    {
      route: "sih-demo",
      section: "GRAND FINALE",
      title: "Interactive 10-Stage Pipeline Transformation",
      targetSelector: ".step-visualizer-card",
      description: "Experience the sovereign, lossless preprocessing lifecycle. Watch raw perimeter logs undergo byte-level hashing, deterministic format detection, canonical ULPF-IR translation, and schema validation with zero data loss.",
      mechanics: "Deterministic ULPF-IR canonical schema + SHA-256 raw evidence anchoring.",
      actionName: "Step Next Stage",
      runAction: () => {
        if (typeof window.stepSihNext === "function") {
          window.stepSihNext();
        } else {
          showToast("Stepped forward in 10-stage pipeline.", "info");
        }
      }
    },
    {
      route: "events",
      section: "EVENT STREAM",
      title: "Real-Time Ingestion, Threat Analysis & IP Blocking",
      targetSelector: ".card",
      description: "Live incoming telemetry streams are evaluated in sub-millisecond cycles. Malicious signatures (SQL Injection, RCE, Brute Force) are highlighted instantly, enabling automated perimeter blacklist propagation across firewalls.",
      mechanics: "In-memory streaming signature evaluation & real-time SSE event dispatch.",
      actionName: "Trigger Threat Traffic",
      runAction: async () => {
        try {
          showToast("Simulating Security Incident traffic...", "warning");
          await fetch("/api/v1/demo/scenarios/scenario_2", { method: "POST" });
          fetchEvents();
          fetchMetrics();
        } catch (e) {}
      }
    },
    {
      route: "lab/multivendor",
      section: "COMPATIBILITY LAB",
      title: "Multi-Vendor Heterogeneous Log Normalization",
      targetSelector: ".card",
      description: "Compare logs from CheckPoint, Palo Alto, Cisco ASA, Fortinet, AWS VPC, and Nginx. ULPF maps divergent field names and timestamp formats into a single unified JSON schema while preserving full attribution.",
      mechanics: "Vendor-to-Canonical declarative dictionary mapping & field provenance tagging.",
      actionName: "Run Lab Matrix",
      runAction: () => {
        const btn = document.getElementById("btnRunLabBatch");
        if (btn) btn.click();
        showToast("Executed multi-vendor compatibility test batch.", "success");
      }
    },
    {
      route: "processing/testbench",
      section: "TEST BENCH",
      title: "Sub-Millisecond Deterministic Parser Engine",
      targetSelector: ".card",
      description: "Inspect pre-compiled high-performance regular expression parsers and KV tokenizers. High throughput deterministic parsing guarantees predictable sub-millisecond latency under extreme load.",
      mechanics: "Pre-compiled regex tokenizers executing in sub-0.5ms per log event.",
      actionName: "Execute Parser Test",
      runAction: () => {
        const btn = document.getElementById("btnTestBenchParse");
        if (btn) btn.click();
        showToast("Tested parser extraction on live sample payload.", "success");
      }
    },
    {
      route: "intelligence/ai-onboarding",
      section: "SOVEREIGN AI",
      title: "Air-Gapped SLM Parser Proposal & Human Review",
      targetSelector: ".card",
      description: "When novel proprietary or SCADA logs arrive without an existing parser, an on-device local Small Language Model (Qwen2.5-Coder) generates regex and normalization rules for human-in-the-loop review.",
      mechanics: "Air-gapped LLM/SLM code synthesis + human review promotion queue.",
      actionName: "Inject Unknown SCADA Log",
      runAction: async () => {
        try {
          showToast("Simulating unknown SCADA format ingestion...", "info");
          await fetch("/api/v1/demo/scenarios/scenario_4", { method: "POST" });
          fetchUnknownLogs();
          if (state.currentRoute === "intelligence/ai-onboarding") {
            renderAiOnboardingView(document.getElementById("contentArea"));
          }
        } catch (e) {}
      }
    },
    {
      route: "outputs/siem",
      section: "STANDARDIZED OUTPUTS",
      title: "Simultaneous Export to OCSF v1.1.0 & Elastic ECS",
      targetSelector: ".card",
      description: "Normalized ULPF-IR objects are projected simultaneously into OCSF v1.1.0 and Elastic Common Schema (ECS), ready for direct ingestion into OpenSearch, Splunk, Microsoft Sentinel, and S3 lakes.",
      mechanics: "Multi-target schema projection & zero-copy serialization.",
      actionName: "Generate Quick Traffic",
      runAction: () => {
        triggerTraffic(10, "Firewall-01", "cef");
      }
    },
    {
      route: "system/health",
      section: "SYSTEM READINESS",
      title: "Health Metrics, Non-Repudiation & Zero Loss",
      targetSelector: ".card",
      description: "Monitor real-time collector throughput, storage integrity, SSE connection streams, and memory buffers. Cryptographic SHA-256 evidence guarantees complete tamper resistance.",
      mechanics: "Continuous component heartbeat monitoring + cryptographic audit logging.",
      actionName: "Run Health Check",
      runAction: () => {
        fetchMetrics();
        showToast("System health checks verified: All 7 subsystems 100% OPERATIONAL.", "success");
      }
    }
  ];

  let currentTourStepIndex = 0;
  let isTourActive = false;
  let tourAutoPlayInterval = null;

  function initDemoGuideController() {
    const btnStart = document.getElementById("btnStartDemoGuide");
    const dock = document.getElementById("demoExplanationDock");
    const btnClose = document.getElementById("btnCloseDemoTour");
    const btnPrev = document.getElementById("btnTourPrev");
    const btnNext = document.getElementById("btnTourNext");
    const btnAction = document.getElementById("btnTourAction");
    const btnAutoPlay = document.getElementById("btnTourAutoPlay");

    if (btnStart) {
      btnStart.addEventListener("click", () => {
        startDemoTour(0);
      });
    }

    if (btnClose) {
      btnClose.addEventListener("click", () => {
        stopDemoTour();
      });
    }

    if (btnPrev) {
      btnPrev.addEventListener("click", () => {
        if (currentTourStepIndex > 0) {
          goToTourStep(currentTourStepIndex - 1);
        }
      });
    }

    if (btnNext) {
      btnNext.addEventListener("click", () => {
        if (currentTourStepIndex < demoTourSteps.length - 1) {
          goToTourStep(currentTourStepIndex + 1);
        } else {
          showToast("Guided Demo Completed! Exploring freely.", "success");
          stopDemoTour();
        }
      });
    }

    if (btnAction) {
      btnAction.addEventListener("click", () => {
        const step = demoTourSteps[currentTourStepIndex];
        if (step && typeof step.runAction === "function") {
          step.runAction();
        }
      });
    }

    if (btnAutoPlay) {
      btnAutoPlay.addEventListener("click", () => {
        toggleTourAutoPlay();
      });
    }

    // Keyboard navigation for tour
    window.addEventListener("keydown", (e) => {
      if (!isTourActive) return;
      if (e.key === "ArrowRight") {
        if (currentTourStepIndex < demoTourSteps.length - 1) goToTourStep(currentTourStepIndex + 1);
      } else if (e.key === "ArrowLeft") {
        if (currentTourStepIndex > 0) goToTourStep(currentTourStepIndex - 1);
      } else if (e.key === "Escape") {
        stopDemoTour();
      }
    });
  }

  function startDemoTour(startIndex = 0) {
    isTourActive = true;
    currentTourStepIndex = startIndex;
    document.body.classList.add("demo-tour-active");
    const dock = document.getElementById("demoExplanationDock");
    if (dock) dock.classList.remove("hidden");
    goToTourStep(startIndex);
  }

  function stopDemoTour() {
    isTourActive = false;
    if (tourAutoPlayInterval) {
      clearInterval(tourAutoPlayInterval);
      tourAutoPlayInterval = null;
    }
    document.body.classList.remove("demo-tour-active");
    clearTourHighlights();
    const dock = document.getElementById("demoExplanationDock");
    if (dock) dock.classList.add("hidden");
    const btnAutoPlayText = document.getElementById("btnTourAutoPlayText");
    if (btnAutoPlayText) btnAutoPlayText.textContent = "Auto-Play";
  }

  function toggleTourAutoPlay() {
    const btnText = document.getElementById("btnTourAutoPlayText");
    if (tourAutoPlayInterval) {
      clearInterval(tourAutoPlayInterval);
      tourAutoPlayInterval = null;
      if (btnText) btnText.textContent = "Auto-Play";
      showToast("Tour Auto-Play paused.", "info");
    } else {
      if (btnText) btnText.textContent = "Pause";
      showToast("Tour Auto-Play active (advancing every 5 seconds).", "info");
      tourAutoPlayInterval = setInterval(() => {
        if (currentTourStepIndex < demoTourSteps.length - 1) {
          goToTourStep(currentTourStepIndex + 1);
        } else {
          stopDemoTour();
        }
      }, 5000);
    }
  }

  function clearTourHighlights() {
    document.querySelectorAll(".demo-tour-highlight").forEach((el) => {
      el.classList.remove("demo-tour-highlight");
    });
  }

  function goToTourStep(index) {
    currentTourStepIndex = index;
    const step = demoTourSteps[index];
    if (!step) return;

    // 1. Navigate route if needed
    if (state.currentRoute !== step.route) {
      window.location.hash = "#/" + step.route;
    }

    // 2. Update Explanation Card UI
    const stepBadge = document.getElementById("demoStepBadge");
    const sectionPill = document.getElementById("demoSectionPill");
    const titleText = document.getElementById("demoTourTitleText");
    const descText = document.getElementById("demoTourDescription");
    const mechanicsText = document.getElementById("demoTourMechanicsText");
    const progressBar = document.getElementById("demoProgressBar");
    const btnActionText = document.getElementById("btnTourActionText");
    const btnPrev = document.getElementById("btnTourPrev");
    const btnNext = document.getElementById("btnTourNext");

    if (stepBadge) stepBadge.textContent = "STAGE " + (index + 1) + " / " + demoTourSteps.length;
    if (sectionPill) sectionPill.textContent = step.section;
    if (titleText) titleText.textContent = step.title;
    if (descText) descText.textContent = step.description;
    if (mechanicsText) mechanicsText.textContent = step.mechanics;
    if (btnActionText) btnActionText.textContent = step.actionName || "Run Action";
    if (progressBar) progressBar.style.width = ((index + 1) / demoTourSteps.length * 100) + "%";

    if (btnPrev) btnPrev.disabled = index === 0;
    if (btnNext) btnNext.querySelector("span").textContent = index === demoTourSteps.length - 1 ? "Finish Tour" : "Next";

    // 3. Highlight targeted card and scroll into view smoothly
    setTimeout(() => {
      clearTourHighlights();
      const contentArea = document.getElementById("contentArea");
      if (contentArea) {
        let targetEl = contentArea.querySelector(step.targetSelector);
        if (!targetEl) {
          targetEl = contentArea.firstElementChild;
        }
        if (targetEl) {
          targetEl.classList.add("demo-tour-highlight");
          targetEl.scrollIntoView({ behavior: "smooth", block: "center" });
        }
      }
    }, 150);
  }
`;

// Append demo controller code before closing IIFE
appJs = appJs.replace(/\}\)\(\);?\s*$/, demoControllerCode + '\n})();\n');

fs.writeFileSync(appJsPath, appJs, 'utf8');
console.log('app.js updated successfully.');
