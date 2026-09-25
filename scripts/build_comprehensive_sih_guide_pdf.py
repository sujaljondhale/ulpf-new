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
        
        # Header banner
        self.setStrokeColor(colors.HexColor('#00D084'))
        self.setLineWidth(1.5)
        self.line(40, h - 35, w - 40, h - 35)
        
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor('#1E293B'))
        self.drawString(40, h - 28, "SMART INDIA HACKATHON 2026  |  PS-26156: ULPF  |  TEAM: MEGABYTES (CMRU025)")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor('#64748B'))
        self.drawRightString(w - 40, h - 28, "MASTER PPT RESTRUCTURING & BENCHMARK REPORT")
        
        # Footer
        self.setStrokeColor(colors.HexColor('#E2E8F0'))
        self.setLineWidth(1)
        self.line(40, 40, w - 40, 40)
        
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor('#64748B'))
        self.drawString(40, 26, "Universal Log Pre-processing Framework — Blockchain & Cybersecurity Category")
        self.drawRightString(w - 40, 26, f"Page {self._pageNumber} of {page_count}")
        
        self.restoreState()


def build_comprehensive_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=48,
        bottomMargin=48
    )

    styles = getSampleStyleSheet()
    
    doc_title = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0F172A')
    )
    
    doc_subtitle = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#059669')
    )
    
    h1_style = ParagraphStyle(
        'H1Style',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=10,
        spaceAfter=4
    )

    h2_style = ParagraphStyle(
        'H2Style',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#0284C7'),
        spaceBefore=6,
        spaceAfter=3
    )
    
    body = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#334155')
    )
    
    body_bold = ParagraphStyle(
        'BodyDarkBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#0F172A')
    )

    callout_green = ParagraphStyle(
        'CalloutGreen',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#065F46')
    )

    critique_red = ParagraphStyle(
        'CritiqueRed',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#991B1B')
    )

    fix_green = ParagraphStyle(
        'FixGreen',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#065F46')
    )

    slide_box_title = ParagraphStyle(
        'SlideBoxTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#FFFFFF')
    )

    slide_box_body = ParagraphStyle(
        'SlideBoxBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#F8FAFC')
    )

    story = []

    # =========================================================================
    # PAGE 1: TITLE & AUDIT SUMMARY
    # =========================================================================
    story.append(Paragraph("SMART INDIA HACKATHON 2026 — MASTER PPT BLUEPRINT & AUDIT", doc_title))
    story.append(Paragraph("PROBLEM STATEMENT ID: 26156 | UNIVERSAL LOG PRE-PROCESSING FRAMEWORK (ULPF)", doc_subtitle))
    story.append(Spacer(1, 6))

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
    meta_table = Table(meta_table_data, colWidths=[175, 175, 180])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 6))

    banner_data = [
        [Paragraph(
            "<b>EXECUTIVE JURY NOTICE & COMPLIANCE SUMMARY:</b><br/>"
            "This master document contains the <b>complete line-by-line audit</b>, <b>all exact text changes</b>, "
            "<b>verbatim slide content</b>, <b>high-contrast terminal screenshots of the live max benchmark</b>, and "
            "<b>forensic validation receipts</b> required to restructure the presentation deck into an award-winning submission.",
            callout_green
        )]
    ]
    banner_table = Table(banner_data, colWidths=[530])
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ECFDF5')),
        ('BOX', (0,0), (-1,-1), 1.2, colors.HexColor('#059669')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(banner_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("1. Slide-by-Slide Audit & Exact Required Changes", h1_style))
    story.append(Paragraph(
        "Pages 3 and 5 in the submitted deck were identical duplicates of pages 2 and 4. "
        "Below is the exact audit and line-by-line fix for all 6 core slides:",
        body
    ))
    story.append(Spacer(1, 4))

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
    t_s123 = Table(s123_audit, colWidths=[105, 205, 220])
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
    # PAGE 2: AUDIT PART 2 + LIVE TERMINAL BENCHMARK SCREENSHOT
    # =========================================================================
    story.append(Paragraph("Slide-by-Slide Audit (Slides 4, 5, 6)", h1_style))
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
    t_s456 = Table(s456_audit, colWidths=[105, 205, 220])
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
    story.append(Spacer(1, 8))

    story.append(Paragraph("2. Live Maximum Benchmark Terminal Execution Screenshot", h1_style))
    story.append(Paragraph(
        "Below is the exact execution screenshot and verified telemetry captured during the live stress run "
        "across all 6 sockets, 8 red-team attack scenarios, 1,000-datagram bursts, and SHA-256 Merkle vaulting:",
        body
    ))
    story.append(Spacer(1, 4))

    term_img_path = "docs/sih_assets/sih_terminal_receipt.png"
    if os.path.exists(term_img_path):
        story.append(Image(term_img_path, width=530, height=255))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: KPI SCORECARD & 5-TIER SYSTEM ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("3. Empirical KPI Scorecard & 5-Tier System Architecture", h1_style))
    score_img_path = "docs/sih_assets/sih_benchmark_scorecard.png"
    if os.path.exists(score_img_path):
        story.append(Image(score_img_path, width=530, height=230))
        story.append(Spacer(1, 6))

    arch_img_path = "docs/sih_assets/sih_architecture_diagram.png"
    if os.path.exists(arch_img_path):
        story.append(Image(arch_img_path, width=530, height=270))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: EXACT SLIDE-BY-SLIDE CONTENT (READY TO COPY-PASTE INTO PPT)
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
        box_t = Table(box_data, colWidths=[530])
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

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Master Complete PDF Generated: {PDF_PATH}")

if __name__ == '__main__':
    build_comprehensive_pdf()
