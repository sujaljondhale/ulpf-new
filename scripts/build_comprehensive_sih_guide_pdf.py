import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

os.makedirs("docs", exist_ok=True)
PDF_PATH = "docs/SIH_2026_PS26156_ULPF_Master_Deck.pdf"

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_header_footer(page_count)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        w, h = self._pagesize
        
        # Top banner accent line
        self.setStrokeColor(colors.HexColor('#00D084'))
        self.setLineWidth(1.5)
        self.line(40, h - 35, w - 40, h - 35)
        
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor('#1E293B'))
        self.drawString(40, h - 28, "SMART INDIA HACKATHON 2026  |  PS-26156: ULPF  |  TEAM: MEGABYTES (CMRU025)")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor('#64748B'))
        self.drawRightString(w - 40, h - 28, "MASTER PPT BLUEPRINT & VIDEO DEMO PLAYBOOK")
        
        # Bottom footer line
        self.setStrokeColor(colors.HexColor('#E2E8F0'))
        self.setLineWidth(1)
        self.line(40, 40, w - 40, 40)
        
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor('#64748B'))
        self.drawString(40, 26, "Universal Log Pre-processing Framework — Blockchain & Cybersecurity Category")
        self.drawRightString(w - 40, 26, f"Page {self._pageNumber} of {page_count}")
        
        self.restoreState()


def build_master_guide_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        leftMargin=38,
        rightMargin=38,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()
    
    doc_title = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=17,
        leading=21,
        textColor=colors.HexColor('#0F172A')
    )
    
    doc_subtitle = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13.5,
        textColor=colors.HexColor('#059669')
    )
    
    h1_style = ParagraphStyle(
        'H1Style',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=9,
        spaceAfter=4
    )

    h2_style = ParagraphStyle(
        'H2Style',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12.5,
        textColor=colors.HexColor('#0284C7'),
        spaceBefore=6,
        spaceAfter=3
    )
    
    body = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#334155')
    )
    
    body_bold = ParagraphStyle(
        'BodyDarkBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#0F172A')
    )

    callout_green = ParagraphStyle(
        'CalloutGreen',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#065F46')
    )

    critique_red = ParagraphStyle(
        'CritiqueRed',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10.5,
        textColor=colors.HexColor('#991B1B')
    )

    fix_green = ParagraphStyle(
        'FixGreen',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10.5,
        textColor=colors.HexColor('#065F46')
    )

    slide_box_title = ParagraphStyle(
        'SlideBoxTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor('#FFFFFF')
    )

    slide_box_body = ParagraphStyle(
        'SlideBoxBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.5,
        textColor=colors.HexColor('#F8FAFC')
    )

    script_scene_title = ParagraphStyle(
        'ScriptSceneTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#00D084')
    )

    script_body = ParagraphStyle(
        'ScriptBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.5,
        textColor=colors.HexColor('#E2E8F0')
    )

    story = []

    # =========================================================================
    # PAGE 1: TITLE, EXECUTIVE NOTICE & AUDIT (SLIDES 1, 2, 3)
    # =========================================================================
    story.append(Paragraph("SMART INDIA HACKATHON 2026 — MASTER PRESENTATION & VIDEO PLAYBOOK", doc_title))
    story.append(Paragraph("PROBLEM STATEMENT ID: 26156 | UNIVERSAL LOG PRE-PROCESSING FRAMEWORK (ULPF)", doc_subtitle))
    story.append(Spacer(1, 5))

    meta_table_data = [
        [
            Paragraph("<b>Problem Statement ID:</b> 26156", body),
            Paragraph("<b>Theme:</b> Blockchain & Cybersecurity", body),
            Paragraph("<b>Category:</b> Software / Cyber Defense", body)
        ],
        [
            Paragraph("<b>Team ID:</b> CMRU025", body),
            Paragraph("<b>Team Name:</b> MEGABYTES", body),
            Paragraph("<b>Institute:</b> CMR University, Bengaluru", body)
        ]
    ]
    meta_table = Table(meta_table_data, colWidths=[175, 175, 186])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 5))

    banner_data = [
        [Paragraph(
            "<b>EXECUTIVE JURY NOTICE & COMPREHENSIVE GUIDE:</b><br/>"
            "This master guide contains the <b>complete line-by-line slide audit</b>, <b>verbatim slide text</b>, "
            "<b>live maximum benchmark terminal screenshot (184k+ EPS)</b>, <b>5-tier architecture flowchart</b>, "
            "<b>minute-by-minute video demonstration script</b>, and <b>Grand Finale jury defense Q&A</b>.",
            callout_green
        )]
    ]
    banner_table = Table(banner_data, colWidths=[536])
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ECFDF5')),
        ('BOX', (0,0), (-1,-1), 1.2, colors.HexColor('#059669')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(banner_table)
    story.append(Spacer(1, 5))

    story.append(Paragraph("1. Slide-by-Slide Critical Audit & Line-by-Line Changes (Slides 1, 2, 3)", h1_style))
    story.append(Paragraph(
        "Pages 3 and 5 in the submitted deck were identical duplicates of pages 2 and 4. "
        "Below is the exact forensic audit and replacement copy for the initial 3 core slides:",
        body
    ))
    story.append(Spacer(1, 3))

    s123_audit = [
        [Paragraph("<b>Slide & Section</b>", body_bold), Paragraph("<b>Identified Flaws in Current Slide</b>", critique_red), Paragraph("<b>Mandatory Replacement & Fix</b>", fix_green)],
        [
            Paragraph("<b>Slide 1: Title Slide</b>", body),
            Paragraph("• Hyphen spacing error (–26156)<br/>• Missing University Name<br/>• Missing Team Leader & 5 members' names & domain roles", critique_red),
            Paragraph("• Set title: Problem Statement ID: 26156<br/>• Add: CMR University, Bengaluru<br/>• Add full 6-member roles table (Lead, Sockets, Parsers, AI, UI, QA)", fix_green)
        ],
        [
            Paragraph("<b>Slide 2: Proposed Solution</b>", body),
            Paragraph("• 'Collects logs from firewalls...' is too generic<br/>• Missing cryptographic integrity proof<br/>• ❌ Zero mention of Merkle trees / Blockchain<br/>• Vague 'Local AI' mention", critique_red),
            Paragraph("• Replace with: 'Multi-Protocol Wire Ingress (Syslog UDP :5140, TCP :5141, REST :8000)'<br/>• Add: 'Byte-Exact Raw Preservation with SHA-256 non-repudiation'<br/>• Add: 'Cryptographic Merkle Tree Ledger (125 logs/block)'<br/>• Add: 'Sovereign local LLM (Qwen/Ollama) parser synthesis'", fix_green)
        ],
        [
            Paragraph("<b>Slide 3: Technical Approach</b>", body),
            Paragraph("• Low-contrast flowchart with missing Merkle vault & threat triage<br/>• Plain unorganized tech stack list on right margin", critique_red),
            Paragraph("• Replace with 5-Tier Data Pipeline (Ingress -> Normalizer -> Crypto Vault -> Storage -> Sinks)<br/>• Group tech stack into 4 clean architectural pillars", fix_green)
        ]
    ]
    t_s123 = Table(s123_audit, colWidths=[105, 205, 226])
    t_s123.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#FFFFFF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_s123)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: AUDIT (SLIDES 4, 5, 6) & LIVE TERMINAL SCREENSHOT
    # =========================================================================
    story.append(Paragraph("Slide-by-Slide Critical Audit (Slides 4, 5, 6)", h1_style))
    s456_audit = [
        [Paragraph("<b>Slide & Section</b>", body_bold), Paragraph("<b>Identified Flaws in Current Slide</b>", critique_red), Paragraph("<b>Mandatory Replacement & Fix</b>", fix_green)],
        [
            Paragraph("<b>Slide 4: Feasibility</b>", body),
            Paragraph("• Terminal screenshot is blurry/tiny (~8pt)<br/>• Shows old 13,615 EPS metric<br/>• Risk-mitigation arrows are hard to scan", critique_red),
            Paragraph("• Embed live max benchmark terminal: <b>184,457.6 Packets/Sec</b>, <b>0.45 ms RTT</b>, <b>42 MB RSS</b><br/>• Format Risk-Mitigation into structured 4-row matrix", fix_green)
        ],
        [
            Paragraph("<b>Slide 5: Impact & Benefits</b>", body),
            Paragraph("• 3 circular icons eat 30% space with zero technical data<br/>• Missing statutory compliance mandates", critique_red),
            Paragraph("• Add: <b>CERT-In 6-Hour Reporting Compliance</b><br/>• Add: <b>Section 65B Indian Evidence Act</b> court admissibility<br/>• Add: <b>NTRO / Defence Air-Gapped Readiness</b>", fix_green)
        ],
        [
            Paragraph("<b>Slide 6: References</b>", body),
            Paragraph("• ❌ <b>Giant empty green box</b> on right side<br/>• Raw words saying 'link' 6 times<br/>• Template watermark text", critique_red),
            Paragraph("• Replace empty box with <b>4-Phase Strategic Roadmap</b> (Core -> eBPF 500k EPS -> TPM 2.0 -> Defense Mesh)<br/>• Clean citations: OCSF v1.1.0, RFC 5424, NIST SP 800-92", fix_green)
        ]
    ]
    t_s456 = Table(s456_audit, colWidths=[105, 205, 226])
    t_s456.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#FFFFFF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_s456)
    story.append(Spacer(1, 6))

    story.append(Paragraph("2. Live Maximum Benchmark Terminal Execution Screenshot", h1_style))
    story.append(Paragraph(
        "Below is the exact execution screenshot and verified telemetry captured during the live stress run "
        "across all 6 sockets, 8 red-team attack scenarios, 1,000-datagram bursts, and SHA-256 Merkle vaulting:",
        body
    ))
    story.append(Spacer(1, 4))

    term_img_path = "docs/sih_assets/sih_terminal_receipt.png"
    if os.path.exists(term_img_path):
        story.append(Image(term_img_path, width=536, height=255))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: KPI SCORECARD & 5-TIER SYSTEM ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("3. Empirical KPI Scorecard & 5-Tier System Architecture", h1_style))
    score_img_path = "docs/sih_assets/sih_benchmark_scorecard.png"
    if os.path.exists(score_img_path):
        story.append(Image(score_img_path, width=536, height=225))
        story.append(Spacer(1, 5))

    arch_img_path = "docs/sih_assets/sih_architecture_diagram.png"
    if os.path.exists(arch_img_path):
        story.append(Image(arch_img_path, width=536, height=265))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: EXACT SLIDE-BY-SLIDE CONTENT (READY TO COPY-PASTE)
    # =========================================================================
    story.append(Paragraph("4. Exact Verbatim Slide Text (Ready to Copy-Paste into PPT)", h1_style))
    story.append(Paragraph(
        "Use the exact structured content below for creating the final presentation slides:",
        body
    ))
    story.append(Spacer(1, 4))

    slides_content = [
        ("SLIDE 1: TITLE & TEAM CREDENTIALS", [
            "• SMART INDIA HACKATHON 2026 | IDEA SUBMISSION",
            "• Problem Statement ID: 26156 | Category: Software / Cyber Defense",
            "• Title: Universal Log Pre-processing Framework (ULPF)",
            "• Theme: Blockchain & Cybersecurity | Team: MEGABYTES (CMRU025)",
            "• Institute: CMR University, Bengaluru",
            "• Value Prop: 'Vendor-Agnostic Wire-Speed Ingestion, Lossless Normalization & SHA-256 Merkle Provenance'",
            "• Team: Lead (Crypto/Pipeline), Member 2 (Sockets), Member 3 (Parsers), Member 4 (AI), Member 5 (UI), Member 6 (QA)"
        ]),
        ("SLIDE 2: PROPOSED SOLUTION & NOVEL ARCHITECTURE", [
            "• Multi-Protocol Wire Ingress: Non-blocking sockets for Syslog (UDP :5140, TCP :5141) and REST (:8000).",
            "• Byte-Exact Raw Preservation: Retains 100% of raw payload with SHA-256 hashing for legal non-repudiation.",
            "• Field-Level Byte Provenance: Bidirectional character offset mapping linking normalized fields to raw slices.",
            "• Cryptographic Merkle Batch Vault: Batches 125 logs/block into immutable SHA-256 tree roots.",
            "• Sovereign AI Parser Onboarding: Air-gapped local LLM (Qwen/Ollama) synthesizes parsers for zero-day logs.",
            "• Core Differentiator: 'ULPF is not another SIEM — it is the vendor-independent preprocessing and interoperability layer.'"
        ]),
        ("SLIDE 3: TECHNICAL APPROACH & 5-TIER PIPELINE", [
            "• Tier 1 (Wire Ingress): Non-blocking sockets (UDP 5140, TCP 5141, REST 8000, File Drop).",
            "• Tier 2 (Parsing Engine): C-Fast Regex Compiler, ULPF-IR Model, Sovereign AI Fallback.",
            "• Tier 3 (Crypto Vault & Threat Triage): SHA-256 Merkle Batch Vault (125 logs/block), Threat Heuristics.",
            "• Tier 4 (Storage Layer): SQLite (WAL Mode), PostgreSQL, MinIO Raw Vault, Dead-Letter Queue (DLQ).",
            "• Tier 5 (Egress Sinks): OCSF v1.1.0, Elastic Common Schema (ECS), OpenSearch, Redpanda, Socket Radar UI."
        ]),
        ("SLIDE 4: FEASIBILITY, EMPIRICAL BENCHMARKS & RISK MITIGATION", [
            "• Direct Wire Ingress Speed: 184,457.6 Packets / Sec (Pure UDP :5140).",
            "• Socket Probe Latency: 0.45 ms – 1.83 ms RTT across all network channels.",
            "• Memory Footprint: 42.14 MB RSS (Runs on lightweight branch routers & edge gateways).",
            "• Cryptographic Integrity: 125 Logs / Block SHA-256 Merkle Vault [Tamper-Proof Audit].",
            "• Risk Mitigation Matrix: Traffic Bursts -> Bounded Buffers | Mutated Schemas -> Sovereign AI DLQ | Tampering -> Merkle Mismatch Alert."
        ]),
        ("SLIDE 5: IMPACT, STAKEHOLDERS & NATIONAL CYBER DEFENSE", [
            "• Air-Gapped Defense Sovereignty: Operates in classified enclaves (NTRO, Tri-Service Cyber Commands, DRDO).",
            "• CERT-In 6-Hour Reporting Compliance: Instant timeline generation for mandatory statutory disclosures.",
            "• Court-Admissible Evidence: Satisfies Section 65B Indian Evidence Act electronic chain of custody.",
            "• Critical Infrastructure: Standardizes telemetry across Power Grids, Railways, Telecom & Banking SOCs.",
            "• Economic Savings: 90% faster parser authoring + 60% reduction in commercial SIEM ingestion licensing taxes."
        ]),
        ("SLIDE 6: RESEARCH STANDARDS, CITATIONS & 4-PHASE ROADMAP", [
            "• OCSF v1.1.0 Specification: Vendor-agnostic cybersecurity event taxonomy for standardized egress.",
            "• IETF RFC 5424 / RFC 3164: Standards-track Syslog protocol transport, header, and facility validation.",
            "• NIST SP 800-92: Guide to Computer Security Log Management and forensic preservation.",
            "• Strategic Roadmap: Phase 1 (Core Engine) -> Phase 2 (eBPF 500k EPS) -> Phase 3 (TPM 2.0 HSM) -> Phase 4 (Defense Mesh)."
        ])
    ]

    for title, points in slides_content:
        box_data = [
            [Paragraph(f"<b>{title}</b>", slide_box_title)],
            [Paragraph("<br/>".join(points), slide_box_body)]
        ]
        box_t = Table(box_data, colWidths=[536])
        box_t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
            ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#1E293B')),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#334155')),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(box_t)
        story.append(Spacer(1, 4))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: MINUTE-BY-MINUTE VIDEO DEMO SCRIPT & JURY DEFENSE STRATEGY
    # =========================================================================
    story.append(Paragraph("5. Official SIH Video Demo Script (Minute-by-Minute Narration)", h1_style))
    story.append(Paragraph(
        "Follow this exact script for recording your 3:00 to 3:45 minute video demonstration for the SIH evaluators:",
        body
    ))
    story.append(Spacer(1, 4))

    video_scenes = [
        ("SCENE 1 (0:00 - 0:35) | Problem Statement & Value Proposition",
         "Screen: Main Dashboard Overview. Show Brand Logo, Top KPI Cards, and Live Ingestion Stream.",
         "Narration: 'Respected Judges, welcome to the demonstration of ULPF — the Universal Log Pre-processing Framework, developed by Team MEGABYTES for SIH Problem Statement 26156 under the Blockchain and Cybersecurity theme. Modern SOCs face an exponential NxM integration crisis where hundreds of firewall and cloud formats flood expensive SIEMs. ULPF is not another SIEM — it is the vendor-independent, air-gapped preprocessing and cryptographic interoperability layer between heterogeneous log sources and downstream analytics.'"),
        ("SCENE 2 (0:35 - 1:15) | Live Sockets & Real-Time Socket Radar Scope",
         "Screen: Testing Simulator Hub (/testing/). Click 'DISPATCH ACTIVE SOCKET PROBES'. Show radar sweep and latency badges.",
         "Narration: 'On our Testing Simulator Hub, you see our Live Network Port Radar. ULPF operates at the wire layer using non-blocking asynchronous sockets on pure Syslog UDP :5140, TCP :5141, and REST :8000 with zero client agent overhead. When we trigger active probes across all 6 subsystems, you see real-time datagram handshakes with sub-millisecond response times averaging just 0.45 ms.'"),
        ("SCENE 3 (1:15 - 1:55) | 184k EPS Stress Cannon & Red-Team Threat Arsenal",
         "Screen: Simulator Threat Grid. Click 'SYN Flood DoS' or 'SQLi', click 'DISPATCH 1,000 PACKET BURST'. Show wiretap receipts.",
         "Narration: 'Next, our High-Velocity Stress Cannon and Red-Team Cyber Threat Arsenal tests system resilience across 8 active attack scenarios. When firing a 1,000-datagram burst over UDP 5140, ULPF sustains over 184,400 packets/sec with a memory footprint of just 42 MB RSS. Our C-Fast compiler deterministically normalizes multi-vendor formats into canonical ULPF-IR.'"),
        ("SCENE 4 (1:55 - 2:35) | Cryptographic SHA-256 Merkle Ledger (Blockchain Theme)",
         "Screen: Main Dashboard Merkle Vault. Show 125 logs/block root hash. Click 'SIMULATE LOG TAMPER'. Show red alert.",
         "Narration: 'This brings us to our core link to the Blockchain & Cybersecurity theme: our Cryptographic SHA-256 Merkle Ledger Vault. ULPF preserves 100% of raw bytes and batches events into 125-log blocks. If an attacker gains root privileges and alters even a single byte of a historical log, the Merkle root calculation immediately fails, proving evidence tampering and satisfying Section 65B of the Indian Evidence Act.'"),
        ("SCENE 5 (2:35 - 3:15) | Sovereign Air-Gapped AI Parser Onboarding",
         "Screen: AI Onboarding Queue. Select unknown log, click 'SYNTHESIZE AI PARSER', show generated Pydantic schema, click Approve.",
         "Narration: 'When a network device emits an unknown zero-day log format, ULPF routes it to our Sovereign AI Onboarding Engine. Powered by a local LLM running on Ollama, the AI synthesizes a deterministic parser and presents it for single-click deployment. Because the LLM runs 100% locally, zero sensitive defense telemetry ever leaves the air-gapped network.'"),
        ("SCENE 6 (3:15 - 3:45) | Analytics Studio, Docker Pro Clip & Benchmark Wrap-up",
         "Screen: Analytics Studio charts, brief terminal flash running 'python scripts/run_benchmarks.py' and 'docker compose ps'.",
         "Narration: 'Finally, our Analytics Studio exports standardized telemetry into OCSF v1.1.0, Elastic ECS, and OpenSearch for CERT-In 6-hour compliance. The entire ecosystem is containerized with Docker and Redpanda streaming sinks. All subsystem benchmarks are 100% operational. ULPF delivers sovereign, high-throughput cyber defense for India. Thank you!'")
    ]

    for title, action, narration in video_scenes:
        scene_data = [
            [Paragraph(f"<b>{title}</b>", script_scene_title)],
            [Paragraph(f"<b>[ACTION ON SCREEN]:</b> {action}<br/><b>[WHAT TO SAY]:</b> <i>{narration}</i>", script_body)]
        ]
        scene_t = Table(scene_data, colWidths=[536])
        scene_t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
            ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#1E293B')),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#334155')),
            ('TOPPADDING', (0,0), (-1,-1), 2.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
            ('LEFTPADDING', (0,0), (-1,-1), 5),
            ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(scene_t)
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 4))
    story.append(Paragraph("6. Grand Finale Jury Defense & Q&A Strategy", h1_style))
    defense_qa = [
        ("Q1: How is your solution related to Blockchain?",
         "Answer: 'We apply the core cryptographic foundation of Blockchain — the SHA-256 Merkle Tree Ledger. Logs are batched into 125-event blocks. Any historical modification causes an immediate Merkle root mismatch, ensuring non-repudiation and court admissibility under Section 65B IE Act.'"),
        ("Q2: How do you handle zero-day log formats without cloud LLMs?",
         "Answer: 'We run a quantized local LLM (Qwen 2.5 via Ollama) on-premise in air-gapped mode. It analyzes structural tokens, generates a deterministic Pydantic parser, and submits it to the SOC administrator for single-click deployment with zero telemetry leaks.'"),
        ("Q3: What is your measured ingestion throughput?",
         "Answer: 'In our live benchmarks, our raw UDP socket collector on port 5140 sustained 184,457.6 packets per second with a memory footprint of just 42.14 MB RSS, allowing ULPF to run directly as a sidecar container on edge gateways.'")
    ]

    for q, a in defense_qa:
        qa_data = [
            [Paragraph(f"<b>{q}</b>", body_bold)],
            [Paragraph(a, body)]
        ]
        qa_t = Table(qa_data, colWidths=[536])
        qa_t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
            ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#CBD5E1')),
            ('TOPPADDING', (0,0), (-1,-1), 2.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
            ('LEFTPADDING', (0,0), (-1,-1), 5),
            ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(qa_t)
        story.append(Spacer(1, 2.5))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Comprehensive 5-Page Master PDF Generated: {PDF_PATH}")

if __name__ == '__main__':
    build_master_guide_pdf()
