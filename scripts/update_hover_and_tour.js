const fs = require('fs');
const path = require('path');

// 1. UPDATE style.css with Cream Hover Glow, Expanded elements, Form Controls, and Fixed Spotlight/Blur
const styleCssPath = path.join(__dirname, '..', 'dashboard', 'style.css');
let styleCss = fs.readFileSync(styleCssPath, 'utf8');

const updatedFormAndHoverStyles = `
/* ==========================================================================
   FORM CONTROLS & DROPDOWN DESIGN SYSTEM (CRIMSON/OBSIDIAN GLASS)
   ========================================================================== */

select, .form-select {
  background: rgba(24, 7, 13, 0.92);
  color: #ffffff;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  padding: 8px 14px;
  font-size: 12.5px;
  font-family: var(--font-sans);
  font-weight: 500;
  outline: none;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  appearance: none;
  -webkit-appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='%23fef3c7' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  padding-right: 34px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

select:hover, .form-select:hover {
  border-color: #fef08a !important;
  box-shadow: 0 0 15px rgba(254, 240, 138, 0.4), 0 4px 12px rgba(0, 0, 0, 0.5) !important;
  transform: translateY(-1px) scale(1.02);
}

select:focus, .form-select:focus {
  border-color: #ff1e44 !important;
  box-shadow: 0 0 18px rgba(229, 9, 46, 0.5) !important;
  background-color: rgba(36, 10, 20, 0.98);
}

input[type="text"], input[type="search"], input[type="number"], input[type="password"], textarea, .form-control {
  background: rgba(22, 6, 12, 0.88);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  padding: 9px 13px;
  color: #ffffff;
  font-family: var(--font-sans);
  font-size: 12.5px;
  outline: none;
  width: 100%;
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.4);
}

input[type="text"]:hover, input[type="search"]:hover, input[type="number"]:hover, textarea:hover, .form-control:hover {
  border-color: #fef08a !important;
  box-shadow: 0 0 14px rgba(254, 240, 138, 0.35) !important;
  transform: scale(1.008);
}

input[type="text"]:focus, input[type="search"]:focus, input[type="number"]:focus, textarea:focus, .form-control:focus {
  border-color: #ff1e44 !important;
  box-shadow: 0 0 18px rgba(229, 9, 46, 0.45) !important;
  background: rgba(36, 9, 18, 0.95);
}

textarea {
  min-height: 90px;
  line-height: 1.5;
  resize: vertical;
}

/* ==========================================================================
   CREAM BORDER HOVER GLOW & SMOOTH EXPANSION (DIFFERENTIATES ALL BLOCKS)
   ========================================================================== */

.card, .metric-card, .scenario-btn-card, .step-visualizer-card, .analogy-pane, .deck-pane, .rail-node, .sample-chip, .readiness-pill, .btn, .nav-item, .table-dense tbody tr, .what-happened-box, .code-box {
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

.card:hover, .step-visualizer-card:hover, .analogy-pane:hover, .deck-pane:hover {
  border-color: #fef08a !important;
  box-shadow: 0 12px 35px rgba(0, 0, 0, 0.75), 0 0 20px rgba(254, 240, 138, 0.35) !important;
  transform: translateY(-2px) scale(1.012) !important;
}

.metric-card:hover, .scenario-btn-card:hover {
  border-color: #fef08a !important;
  box-shadow: 0 14px 40px rgba(0, 0, 0, 0.8), 0 0 22px rgba(254, 240, 138, 0.4) !important;
  transform: translateY(-3px) scale(1.025) !important;
}

.rail-node:hover, .sample-chip:hover, .readiness-pill:hover {
  border-color: #fef08a !important;
  box-shadow: 0 0 15px rgba(254, 240, 138, 0.4) !important;
  transform: translateY(-2px) scale(1.04) !important;
}

.btn:hover {
  transform: translateY(-2px) scale(1.03) !important;
  box-shadow: 0 6px 20px rgba(229, 9, 46, 0.5), 0 0 12px rgba(254, 240, 138, 0.3) !important;
}

.nav-item:hover {
  border-left-color: #fef08a !important;
  transform: translateX(4px) scale(1.01) !important;
  box-shadow: 0 0 12px rgba(254, 240, 138, 0.25) !important;
}

.table-dense tbody tr:hover {
  background: rgba(229, 9, 46, 0.15) !important;
  box-shadow: inset 0 0 0 1px #fef08a, 0 0 14px rgba(254, 240, 138, 0.3) !important;
  transform: scale(1.008) !important;
}

/* ==========================================================================
   ROBUST DEMO TOUR SPOTLIGHT & SELECTIVE BACKGROUND BLUR
   ========================================================================== */

body.demo-tour-active .content-area > *:not(.demo-tour-highlight),
body.demo-tour-active .content-area .card:not(.demo-tour-highlight),
body.demo-tour-active .content-area .step-visualizer-card:not(.demo-tour-highlight),
body.demo-tour-active .content-area .sih-hero-banner:not(.demo-tour-highlight),
body.demo-tour-active .content-area .page-header:not(.demo-tour-highlight),
body.demo-tour-active .sidebar {
  filter: blur(5px) opacity(0.35) !important;
  pointer-events: none !important;
  transform: scale(0.99) !important;
  transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

.demo-tour-highlight {
  position: relative !important;
  z-index: 1005 !important;
  filter: none !important;
  opacity: 1 !important;
  transform: scale(1.015) !important;
  pointer-events: auto !important;
  border-color: #fef08a !important;
  box-shadow: 0 0 0 3px #ff1e44, 0 0 50px rgba(229, 9, 46, 0.85), 0 0 25px rgba(254, 240, 138, 0.5), 0 25px 60px rgba(0, 0, 0, 0.95) !important;
  transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1) !important;
}
`;

// Replace demo tour CSS block with updated styles
styleCss = styleCss.replace(
  /\/\* Background Dimming & Blur effect on non-focused elements[\s\S]*?(\.analogy-grid \{)/,
  updatedFormAndHoverStyles + '\n\n$1'
);

fs.writeFileSync(styleCssPath, styleCss, 'utf8');
console.log('style.css updated with cream hover and improved tour blur.');

// 2. UPDATE app.js with comprehensive 8-stage plain-English tour and resilient element targeting
const appJsPath = path.join(__dirname, '..', 'dashboard', 'app.js');
let appJs = fs.readFileSync(appJsPath, 'utf8');

const updatedTourStepsCode = `
  // --- COMPREHENSIVE 8-STAGE BEGINNER-FRIENDLY GUIDED DEMO TOUR ---
  const demoTourSteps = [
    {
      route: "sih-demo",
      section: "STAGE 1 - CORE PLATFORM",
      title: "Universal Cybersecurity Translator (10-Stage Pipeline)",
      targetSelector: ".step-visualizer-card, .sih-hero-banner, .card",
      description: "Think of this as a Universal Translator for cybersecurity. Organizations have dozens of different firewalls and servers speaking completely different computer languages. ULPF listens to all of them, takes an exact tamper-proof digital fingerprint (SHA-256), and translates every message into one clean, common standard format without losing a single piece of evidence.",
      mechanics: "Byte-level hashing + Universal intermediate representation (ULPF-IR).",
      actionName: "Step Next Stage",
      runAction: () => {
        if (typeof window.stepSihNext === "function") {
          window.stepSihNext();
        } else {
          showToast("Stepping forward in 10-stage pipeline...", "info");
        }
      }
    },
    {
      route: "pipeline",
      section: "STAGE 2 - REAL-TIME FLOW",
      title: "High-Speed Live Ingestion Highway",
      targetSelector: ".pipeline-grid, .card, .content-area",
      description: "Watch security messages flow through our 4-stage processing highway in real-time: Receive -> Identify Format -> Standardize Fields -> Forward to Security Centers. Over 10,000 security logs can pass through every single second with near-zero delay (under 0.1 milliseconds).",
      mechanics: "Asynchronous zero-copy memory queue + lock-free dispatch.",
      actionName: "Inject 10 Live Events",
      runAction: () => {
        triggerTraffic(10, "Firewall-01", "cef");
      }
    },
    {
      route: "events",
      section: "STAGE 3 - THREAT DEFENSE",
      title: "Spotting Attackers & 1-Click Instant Blacklist",
      targetSelector: ".table-responsive, .card",
      description: "When an attacker tries to hack in (using password brute-force or SQL injection attacks), ULPF detects the attack pattern in real-time, highlights it in red, and lets any security guard immediately block the attacker's IP address across all network gateways with a single click.",
      mechanics: "In-stream malicious signature matching + Instant IP Blacklisting API.",
      actionName: "Simulate Cyber Attack",
      runAction: async () => {
        try {
          showToast("Simulating live cyber attack traffic...", "warning");
          await fetch("/api/v1/demo/scenarios/scenario_2", { method: "POST" });
          fetchEvents();
          fetchMetrics();
        } catch (e) {}
      }
    },
    {
      route: "lab/multivendor",
      section: "STAGE 4 - TRANSLATION LAB",
      title: "Multi-Vendor Compatibility Lab (6+ Brands)",
      targetSelector: ".grid-2, .card, .content-area",
      description: "See how logs from CheckPoint, Palo Alto, Cisco ASA, Fortinet, AWS Cloud, and Nginx are translated side-by-side. The original raw vendor log is on the left, and the clean, uniform result is on the right. No matter the brand, everything becomes simple and standardized.",
      mechanics: "Vendor-to-Canonical declarative dictionary mapping with full attribution.",
      actionName: "Run Multi-Vendor Test",
      runAction: () => {
        const btn = document.getElementById("btnRunLabBatch");
        if (btn) btn.click();
        showToast("Ran multi-vendor compatibility translation batch.", "success");
      }
    },
    {
      route: "processing/testbench",
      section: "STAGE 5 - SPEED PARSER",
      title: "Sub-Millisecond Regex & Key-Value Test Bench",
      targetSelector: ".grid-2, .card, .content-area",
      description: "Test how fast the translator dissects messy log text. You can paste any raw computer log into the test box, and ULPF instantly breaks it down into neat, structured fields (like User, IP Address, Port, and Result) in less than 0.5 milliseconds.",
      mechanics: "Pre-compiled high-throughput deterministic tokenizers.",
      actionName: "Test Sample Log",
      runAction: () => {
        const btn = document.getElementById("btnTestBenchParse");
        if (btn) btn.click();
        showToast("Tested parser engine on live sample payload.", "success");
      }
    },
    {
      route: "intelligence/ai-onboarding",
      section: "STAGE 6 - SELF-LEARNING AI",
      title: "Air-Gapped AI Assistant for Brand New Devices",
      targetSelector: ".grid-2, .card, .content-area",
      description: "What happens when your company buys a brand new device with a log format ULPF has never seen before? Our sovereign, 100% on-device AI automatically inspects the mystery log, writes a new translation rule, and presents it to a human for 1-click approval. No internet connection or cloud required.",
      mechanics: "Air-gapped local SLM (Qwen2.5-Coder) code synthesis + human review queue.",
      actionName: "Inject Unknown SCADA Log",
      runAction: async () => {
        try {
          showToast("Injecting unknown SCADA log into AI review queue...", "info");
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
      section: "STAGE 7 - EXPORT HUBS",
      title: "Sending Clean Data to All Security Tools (OCSF & ECS)",
      targetSelector: ".grid-2, .card, .content-area",
      description: "Once logs are standardized, ULPF outputs them in both Open Cybersecurity Schema (OCSF) and Elastic Common Schema (ECS). This means your security team can view the exact same data in OpenSearch, Splunk, Microsoft Sentinel, and cloud lakes without having to convert anything twice.",
      mechanics: "Simultaneous dual-schema projection & zero-copy JSON streaming.",
      actionName: "Generate Quick Traffic",
      runAction: () => {
        triggerTraffic(10, "Firewall-01", "cef");
      }
    },
    {
      route: "system/health",
      section: "STAGE 8 - TAMPER-PROOF AUDIT",
      title: "System Health & 100% Cryptographic Proof",
      targetSelector: ".grid-3, .card, .content-area",
      description: "Confirm that all 7 platform components are running in healthy condition. Every single log event processed is permanently sealed with a SHA-256 cryptographic signature, guaranteeing zero data tampering for courtroom-level legal compliance and forensics.",
      mechanics: "Continuous heartbeat monitoring + SHA-256 non-repudiation guarantee.",
      actionName: "Run Full Health Audit",
      runAction: () => {
        fetchMetrics();
        showToast("System health audit verified: All subsystems 100% Operational.", "success");
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
          showToast("Guided Tour Completed! Feel free to explore all modules.", "success");
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

    // Keyboard navigation
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
      showToast("Tour Auto-Play active (advancing every 6 seconds).", "info");
      tourAutoPlayInterval = setInterval(() => {
        if (currentTourStepIndex < demoTourSteps.length - 1) {
          goToTourStep(currentTourStepIndex + 1);
        } else {
          stopDemoTour();
        }
      }, 6000);
    }
  }

  function clearTourHighlights() {
    document.querySelectorAll(".demo-tour-highlight").forEach((el) => {
      el.classList.remove("demo-tour-highlight");
    });
  }

  function highlightAndScrollTarget(targetSelector) {
    clearTourHighlights();
    const contentArea = document.getElementById("contentArea");
    if (!contentArea) return;

    const selectors = targetSelector.split(",").map(s => s.trim());
    let targetEl = null;

    for (const sel of selectors) {
      targetEl = contentArea.querySelector(sel);
      if (targetEl) break;
    }

    if (!targetEl) {
      targetEl = contentArea.firstElementChild;
    }

    if (targetEl) {
      targetEl.classList.add("demo-tour-highlight");
      targetEl.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  }

  function goToTourStep(index) {
    currentTourStepIndex = index;
    const step = demoTourSteps[index];
    if (!step) return;

    // 1. Navigate route
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

    // 3. Highlight with multiple retries for asynchronous view rendering
    highlightAndScrollTarget(step.targetSelector);
    setTimeout(() => highlightAndScrollTarget(step.targetSelector), 150);
    setTimeout(() => highlightAndScrollTarget(step.targetSelector), 400);
    setTimeout(() => highlightAndScrollTarget(step.targetSelector), 800);
  }
`;

// Replace demo controller section in app.js
appJs = appJs.replace(
  /\/\/\s*---\s*INTERACTIVE GUIDED DEMO CONTROLLER[\s\S]*?\}\)\(\);?\s*$/,
  updatedTourStepsCode + '\n})();\n'
);

fs.writeFileSync(appJsPath, appJs, 'utf8');
console.log('app.js updated with 8-stage plain-English tour and multi-retry target spotlight.');
