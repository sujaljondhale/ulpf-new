import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

os.makedirs("docs", exist_ok=True)
PDF_PATH = "docs/SIH_2026_PS26156_ULPF_Master_Deck.pdf"

# Custom Canvas for High-Tech Presentation Background
class PresentationCanvas(canvas.Canvas):
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
            self.draw_background(page_count)
            super().showPage()
        super().save()

    def draw_background(self, page_count):
        self.saveState()
        w, h = self._pagesize
        
        # Deep dark cyber background
        self.setFillColor(colors.HexColor('#0B0F19'))
        self.rect(0, 0, w, h, fill=True, stroke=False)
        
        # Top banner line (Emerald accent)
        self.setStrokeColor(colors.HexColor('#00D084'))
        self.setLineWidth(2.5)
        self.line(30, h - 22, w - 30, h - 22)
        
        # Header text
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor('#9CA3AF'))
        self.drawString(32, h - 18, "SMART INDIA HACKATHON 2026  |  PROBLEM STATEMENT ID: 26156  |  TEAM: MEGABYTES (CMRU025)")
        
        # Footer text
        self.setStrokeColor(colors.HexColor('#1F2937'))
        self.setLineWidth(1)
        self.line(30, 26, w - 30, 26)
        
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor('#6B7280'))
        self.drawString(32, 14, "Universal Log Pre-processing Framework (ULPF) — Blockchain & Cybersecurity Category")
        self.drawRightString(w - 32, 14, f"Slide {self._pageNumber} of {page_count}")
        
        self.restoreState()


def build_pdf():
    # Landscape Letter format (11 x 8.5 inches)
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=landscape(letter),
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom Cyber Typography Styles
    title_style = ParagraphStyle(
        'CyberTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#F9FAFB')
    )
    
    subtitle_style = ParagraphStyle(
        'CyberSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#00D084')
    )
    
    h2_style = ParagraphStyle(
        'CyberH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#38BDF8')
    )
    
    body_style = ParagraphStyle(
        'CyberBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#E5E7EB')
    )
    
    bold_body = ParagraphStyle(
        'CyberBodyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#F3F4F6')
    )

    callout_style = ParagraphStyle(
        'CyberCallout',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#00D084')
    )

    story = []

    # =========================================================================
    # SLIDE 1: TITLE SLIDE & TEAM CREDENTIALS
    # =========================================================================
    story.append(Paragraph("UNIVERSAL LOG PRE-PROCESSING FRAMEWORK (ULPF)", title_style))
    story.append(Paragraph("SMART INDIA HACKATHON 2026 — HARDWARE / SOFTWARE IDEA SUBMISSION", subtitle_style))
    story.append(Spacer(1, 10))

    meta_table_data = [
        [
            Paragraph("<b>Problem Statement ID:</b> 26156", body_style),
            Paragraph("<b>Theme:</b> Blockchain & Cybersecurity", body_style),
            Paragraph("<b>PS Category:</b> Software / Core Cyber Defense", body_style)
        ],
        [
            Paragraph("<b>Team ID:</b> CMRU025", body_style),
            Paragraph("<b>Team Name:</b> MEGABYTES", body_style),
            Paragraph("<b>Institution:</b> CMR University, Bengaluru", body_style)
        ]
    ]
    meta_table = Table(meta_table_data, colWidths=[240, 240, 240])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#111827')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1F2937')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#1F2937')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 12))

    # Core Value Banner
    core_banner = [
        [Paragraph(
            "<b>CORE VALUE PROPOSITION:</b><br/>"
            "ULPF is not another SIEM — it is the vendor-independent, air-gapped preprocessing and cryptographic "
            "interoperability layer between heterogeneous network log sources and the analytical platforms that consume them.",
            callout_style
        )]
    ]
    banner_table = Table(core_banner, colWidths=[720])
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#064E3B')),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#00D084')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(banner_table)
    story.append(Spacer(1, 12))

    # Team Members Table
    team_data = [
        [Paragraph("<b>Team Member</b>", bold_body), Paragraph("<b>Domain Role</b>", bold_body), Paragraph("<b>Key Subsystem Responsibility</b>", bold_body)],
        [Paragraph("Team Leader", body_style), Paragraph("Lead Architect & Cryptography", body_style), Paragraph("SHA-256 Merkle Ledger Vault & High-Throughput Core Pipeline", body_style)],
        [Paragraph("Member 2", body_style), Paragraph("Systems & Sockets Engineer", body_style), Paragraph("Syslog Wire Ingress (UDP :5140, TCP :5141) & Network Socket Radar", body_style)],
        [Paragraph("Member 3", body_style), Paragraph("Parser & Normalization Specialist", body_style), Paragraph("C-Fast Deterministic Regex Matcher (CEF, Syslog, JSON, KV, CSV)", body_style)],
        [Paragraph("Member 4", body_style), Paragraph("AI & Sovereign Inference", body_style), Paragraph("Local Air-Gapped LLM Parser Synthesis Engine (Ollama / Qwen)", body_style)],
        [Paragraph("Member 5", body_style), Paragraph("Forensic UI & Telemetry", body_style), Paragraph("Real-Time Analytics Studio, SSE Wiretap Stream & Threat Visualizer", body_style)],
        [Paragraph("Member 6", body_style), Paragraph("QA & Security Benchmarking", body_style), Paragraph("Red-Team Cyber Attack Scenarios, Load Generator & Docker Orchestration", body_style)],
    ]
    team_table = Table(team_data, colWidths=[150, 200, 370])
    team_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#0F172A')),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#334155')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#1E293B')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(team_table)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 2: PROPOSED SOLUTION & NOVEL ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("PROPOSED SOLUTION & ARCHITECTURAL NOVELTY", title_style))
    story.append(Paragraph("SOLVING THE N x M LOG INTEGRATION & EVIDENCE INTEGRITY CRISIS", subtitle_style))
    story.append(Spacer(1, 10))

    sol_grid = [
        [
            Paragraph("<b>Detailed Solution Breakdown</b>", h2_style),
            Paragraph("<b>Innovation & Technical Uniqueness</b>", h2_style)
        ],
        [
            Paragraph(
                "• <b>Multi-Protocol Wire Ingress:</b> Non-blocking async kernel sockets for Syslog (UDP :5140, TCP :5141), REST API (:8000), and watched file streams.<br/>"
                "• <b>Byte-Exact Raw Preservation:</b> Retains 100% of the raw string with SHA-256 integrity to ensure legal non-repudiation.<br/>"
                "• <b>C-Fast Deterministic Parsing:</b> High-speed sub-millisecond format compiler converting multi-vendor logs into canonical schemas.<br/>"
                "• <b>ULPF Intermediate Representation:</b> Standardized common event model with source, destination, protocol, action, and unmapped fields.<br/>"
                "• <b>Field-Level Byte Provenance:</b> Direct character slice mapping linking every normalized field back to its raw payload offset.<br/>"
                "• <b>Universal Egress Adapters:</b> Exports to OCSF v1.1.0, Elastic ECS, MinIO, SQLite, OpenSearch, and enterprise SIEMs.",
                body_style
            ),
            Paragraph(
                "• <b>N → 1 → M Architecture:</b> Replaces exponential N×M vendor adapters with 1 universal canonical intermediate representation.<br/>"
                "• <b>Cryptographic Merkle Tree Ledger:</b> Batches 125 logs/block into a verifiable SHA-256 tree root, guaranteeing zero historical tampering.<br/>"
                "• <b>Local Sovereign AI Parser Onboarding:</b> Unparsed or zero-day logs automatically trigger an air-gapped LLM (Qwen/Ollama) to synthesize deterministic parsers.<br/>"
                "• <b>Heuristic Security Triage:</b> Real-time signature and heuristic scoring for SQLi, XSS, Ransomware, DNS Tunneling, and SYN floods.<br/>"
                "• <b>100% Air-Gapped & Container Ready:</b> Runs in high-security enclaves with zero outbound internet or cloud dependencies.",
                body_style
            )
        ]
    ]
    sol_table = Table(sol_grid, colWidths=[355, 355])
    sol_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#111827')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1F2937')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#1F2937')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(sol_table)
    story.append(Spacer(1, 10))

    # Comparative Problem-Solution Alignment Table
    align_data = [
        [Paragraph("<b>Industry Problem</b>", bold_body), Paragraph("<b>Conventional Limitation</b>", bold_body), Paragraph("<b>ULPF Architectural Solution</b>", bold_body)],
        [Paragraph("Fragmented Preprocessing", body_style), Paragraph("Each SIEM requires custom brittle regex collectors", body_style), Paragraph("Unified drop-in Syslog & REST pre-processing proxy layer", body_style)],
        [Paragraph("Forensic Evidence Loss", body_style), Paragraph("Normalization alters raw strings, losing court admissibility", body_style), Paragraph("Byte-exact raw payload + SHA-256 Merkle root verification", body_style)],
        [Paragraph("Slow Zero-Day Onboarding", body_style), Paragraph("Manual parser authoring takes 2-3 weeks per vendor", body_style), Paragraph("Sovereign AI generates valid parsers in seconds with human review", body_style)],
        [Paragraph("Cloud Dependency Risks", body_style), Paragraph("Cloud SIEMs risk sovereign data leaks in defense networks", body_style), Paragraph("Air-gapped deployment on commodity on-premise hardware", body_style)],
    ]
    align_table = Table(align_data, colWidths=[150, 250, 320])
    align_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#0F172A')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#334155')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#1E293B')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(align_table)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 3: TECHNICAL APPROACH & 5-TIER SYSTEM ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("TECHNICAL APPROACH & SYSTEM ARCHITECTURE", title_style))
    story.append(Paragraph("5-TIER END-TO-END PIPELINE FROM WIRE INGRESS TO DOWNSTREAM ANALYTICS", subtitle_style))
    story.append(Spacer(1, 8))

    # Embed Architecture Image
    arch_img_path = "docs/sih_assets/sih_architecture_diagram.png"
    if os.path.exists(arch_img_path):
        story.append(Image(arch_img_path, width=720, height=270))
    story.append(Spacer(1, 8))

    # Tech Stack Summary Grid
    tech_data = [
        [
            Paragraph("<b>Ingress & Sockets:</b> FastAPI · Uvicorn · UDP :5140 · TCP :5141 · REST :8000", body_style),
            Paragraph("<b>Parsing & Normalization:</b> C-Fast Regex Compiler · ULPF-IR · OCSF v1.1.0 · ECS", body_style)
        ],
        [
            Paragraph("<b>Sovereign AI Engine:</b> Local Ollama · Qwen 2.5 LLM · Zero-Cloud Isolation", body_style),
            Paragraph("<b>Storage & Crypto Vault:</b> SHA-256 Merkle Ledger · SQLite (WAL) · MinIO · OpenSearch", body_style)
        ]
    ]
    tech_table = Table(tech_data, colWidths=[355, 355])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#111827')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1F2937')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#1F2937')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(tech_table)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 4: FEASIBILITY, EMPIRICAL BENCHMARKS & RISK MITIGATION
    # =========================================================================
    story.append(Paragraph("FEASIBILITY, VIABILITY & EMPIRICAL BENCHMARKS", title_style))
    story.append(Paragraph("TESTED & VERIFIED MAXIMUM THROUGHPUT PERFORMANCE TELEMETRY", subtitle_style))
    story.append(Spacer(1, 6))

    # Embed Scorecard & Terminal Receipt side-by-side or stacked
    score_img = "docs/sih_assets/sih_benchmark_scorecard.png"
    term_img = "docs/sih_assets/sih_terminal_receipt.png"

    if os.path.exists(score_img) and os.path.exists(term_img):
        img_table = Table([[
            Image(score_img, width=355, height=170),
            Image(term_img, width=355, height=170)
        ]], colWidths=[360, 360])
        img_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(img_table)
        story.append(Spacer(1, 8))

    # Risk vs Mitigation Matrix
    risk_data = [
        [Paragraph("<b>Identified Operational Risk</b>", bold_body), Paragraph("<b>Severity</b>", bold_body), Paragraph("<b>Built-in Architectural Mitigation Strategy</b>", bold_body)],
        [Paragraph("Extreme Traffic Ingestion Spikes", body_style), Paragraph("<font color='#FBBF24'>HIGH</font>", body_style), Paragraph("Bounded ring buffer queue with asynchronous backpressure control and non-blocking socket polling.", body_style)],
        [Paragraph("Zero-Day Mutated Log Format", body_style), Paragraph("<font color='#38BDF8'>MEDIUM</font>", body_style), Paragraph("Dead-Letter Queue (DLQ) isolation + Sovereign AI Parser Generator with human-in-the-loop approval.", body_style)],
        [Paragraph("Historical Log Tampering / Deletion", body_style), Paragraph("<font color='#EF4444'>CRITICAL</font>", body_style), Paragraph("SHA-256 Merkle Ledger batching (125 logs/block) guarantees immediate root hash verification failure.", body_style)],
        [Paragraph("Air-Gapped Network Isolation", body_style), Paragraph("<font color='#34D399'>LOW</font>", body_style), Paragraph("Fully self-contained Python & Docker build with zero outbound cloud dependencies or internet calls.", body_style)],
    ]
    risk_table = Table(risk_data, colWidths=[180, 70, 470])
    risk_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#0F172A')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#334155')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#1E293B')),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(risk_table)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 5: IMPACT, STAKEHOLDERS & NATIONAL SECURITY
    # =========================================================================
    story.append(Paragraph("IMPACT, STAKEHOLDERS & NATIONAL CYBER DEFENSE", title_style))
    story.append(Paragraph("STRENGTHENING INDIA'S CYBER SECURITY & SOVEREIGN DIGITAL INFRASTRUCTURE", subtitle_style))
    story.append(Spacer(1, 10))

    impact_grid = [
        [
            Paragraph("<b>National Security & Defense Sovereignty</b>", h2_style),
            Paragraph("<b>Economic ROI & Operational Efficiency</b>", h2_style)
        ],
        [
            Paragraph(
                "• <b>Air-Gapped Sovereign Defense:</b> Operates entirely within classified defense enclaves (NTRO, Tri-Service Cyber Commands, DRDO) with zero telemetry leaks.<br/>"
                "• <b>CERT-In 6-Hour Reporting Compliance:</b> Rapid normalization and indexed storage enable immediate timeline generation for mandatory incident reporting.<br/>"
                "• <b>Court-Admissible Evidence (Sec 65B IE Act):</b> Raw payload retention, byte provenance, and SHA-256 Merkle root satisfy legal digital evidence integrity.<br/>"
                "• <b>Critical Infrastructure Protection:</b> Unifies multi-vendor telemetry across Power Grids, Railways, Telecom, Smart Cities, and Banking SOCs.",
                body_style
            ),
            Paragraph(
                "• <b>90% Reduction in Parser Development:</b> Replaces weeks of manual regular expression authoring with reusable parser schemas and local AI proposals.<br/>"
                "• <b>Elimination of SIEM Ingestion Tax:</b> Pre-filtering, deduplicating, and normalizing logs at the edge cuts commercial SIEM licensing costs by up to 60%.<br/>"
                "• <b>Ultra-Low Hardware Footprint:</b> 42.14 MB RSS allows deployment as a sidecar proxy on branch routers and commodity edge hardware.<br/>"
                "• <b>Zero Vendor Lock-In:</b> Neutral intermediate representation (ULPF-IR) decouples hardware firewalls from proprietary analytics vendors.",
                body_style
            )
        ]
    ]
    impact_table = Table(impact_grid, colWidths=[355, 355])
    impact_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#111827')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1F2937')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#1F2937')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(impact_table)
    story.append(Spacer(1, 10))

    # Stakeholder Target Sectors
    sectors_data = [
        [Paragraph("<b>Target Sector</b>", bold_body), Paragraph("<b>Key Beneficiaries</b>", bold_body), Paragraph("<b>Operational Benefit & Value Add</b>", bold_body)],
        [Paragraph("Defense & Strategic", body_style), Paragraph("NTRO, Defence Cyber Agency, Tri-Services", body_style), Paragraph("Air-gapped, zero-cloud log normalization with cryptographically verified chain of custody.", body_style)],
        [Paragraph("National Response", body_style), Paragraph("CERT-In, NCIIPC, Sectoral CERTs", body_style), Paragraph("Rapid statutory 6-hour incident correlation across heterogeneous multi-vendor datasets.", body_style)],
        [Paragraph("Critical Infrastructure", body_style), Paragraph("Power Grid (POSOCO), Indian Railways, Telecom", body_style), Paragraph("Standardizes legacy SCADA/Modbus, IoT, and enterprise network telemetry seamlessly.", body_style)],
        [Paragraph("Commercial Enterprise", body_style), Paragraph("Banking SOCs, FinTech, Healthcare, MSSPs", body_style), Paragraph("Cuts SIEM ingestion taxes and scales to 184k+ EPS on commodity server nodes.", body_style)],
    ]
    sectors_table = Table(sectors_data, colWidths=[140, 230, 350])
    sectors_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#0F172A')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#334155')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#1E293B')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(sectors_table)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 6: RESEARCH, STANDARDS & 4-PHASE ROADMAP
    # =========================================================================
    story.append(Paragraph("RESEARCH, STANDARDS & STRATEGIC ROADMAP", title_style))
    story.append(Paragraph("INDUSTRY COMPLIANCE, CITATIONS & POST-HACKATHON DEPLOYMENT PLAN", subtitle_style))
    story.append(Spacer(1, 10))

    final_grid = [
        [
            Paragraph("<b>Research Standards & Citations</b>", h2_style),
            Paragraph("<b>Strategic Development Roadmap</b>", h2_style)
        ],
        [
            Paragraph(
                "• <b>Open Cybersecurity Schema Framework (OCSF v1.1.0):</b> Vendor-agnostic cybersecurity event taxonomy for normalized SIEM/lake egress.<br/>"
                "• <b>IETF RFC 5424 / RFC 3164:</b> Standards-track specifications for structured Syslog protocol formatting, headers, and facility mapping.<br/>"
                "• <b>NIST SP 800-92:</b> Guide to Computer Security Log Management and forensic integrity preservation in enterprise networks.<br/>"
                "• <b>MITRE ATT&CK & CWE Framework:</b> Adversarial tactics and signature scoring for heuristic threat triage.<br/>"
                "• <b>Section 65B Indian Evidence Act:</b> Statutory legal framework for electronic records non-repudiation and electronic chain of custody.",
                body_style
            ),
            Paragraph(
                "• <b>Phase 1: Core Engine (Completed):</b> Multi-socket ingress, C-Fast parser, SHA-256 Merkle ledger, 8-threat arsenal, and live telemetry studio.<br/>"
                "• <b>Phase 2: Kernel Acceleration (Q3 2026):</b> eBPF / XDP kernel-bypass socket layer targeting 500,000+ EPS on single CPU socket.<br/>"
                "• <b>Phase 3: Hardware Trust Anchor (Q4 2026):</b> TPM 2.0 / HSM integration for FIPS 140-3 hardware-backed cryptographic log signing.<br/>"
                "• <b>Phase 4: Sovereign Threat Mesh (2027):</b> Distributed peer-to-peer threat IOC correlation across air-gapped defense enclaves.",
                body_style
            )
        ]
    ]
    final_table = Table(final_grid, colWidths=[355, 355])
    final_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#111827')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1F2937')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#1F2937')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(final_table)
    story.append(Spacer(1, 14))

    # Q&A / Conclusion Banner
    qa_banner = [
        [Paragraph(
            "<b>SMART INDIA HACKATHON 2026 — READY FOR LIVE DEMO & EVALUATION</b><br/>"
            "Thank you! The ULPF system testbed is active, validated, and ready for live socket stress testing & forensic audit.",
            callout_style
        )]
    ]
    qa_table = Table(qa_banner, colWidths=[720])
    qa_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1E293B')),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#00D084')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(qa_table)

    doc.build(story, canvasmaker=PresentationCanvas)
    print(f"Generated Master PDF: {PDF_PATH}")

if __name__ == '__main__':
    build_pdf()
