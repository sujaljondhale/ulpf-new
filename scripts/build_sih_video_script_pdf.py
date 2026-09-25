import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

os.makedirs("docs", exist_ok=True)
PDF_PATH = "docs/SIH_2026_Video_Demo_and_Explanation_Playbook.pdf"

class ScriptNumberedCanvas(canvas.Canvas):
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
        
        # Header accent banner
        self.setStrokeColor(colors.HexColor('#00D084'))
        self.setLineWidth(1.5)
        self.line(40, h - 35, w - 40, h - 35)
        
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor('#1E293B'))
        self.drawString(40, h - 28, "SMART INDIA HACKATHON 2026  |  PS-26156: ULPF  |  TEAM: MEGABYTES (CMRU025)")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor('#64748B'))
        self.drawRightString(w - 40, h - 28, "OFFICIAL VIDEO DEMO & TECHNICAL EXPLANATION PLAYBOOK")
        
        # Footer
        self.setStrokeColor(colors.HexColor('#E2E8F0'))
        self.setLineWidth(1)
        self.line(40, 40, w - 40, 40)
        
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor('#64748B'))
        self.drawString(40, 26, "Universal Log Pre-processing Framework — Blockchain & Cybersecurity Category")
        self.drawRightString(w - 40, 26, f"Page {self._pageNumber} of {page_count}")
        
        self.restoreState()


def build_video_script_pdf():
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
        spaceBefore=8,
        spaceAfter=3
    )

    h2_style = ParagraphStyle(
        'H2Style',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12.5,
        textColor=colors.HexColor('#0284C7'),
        spaceBefore=6,
        spaceAfter=2
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

    scene_title = ParagraphStyle(
        'SceneTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#00D084')
    )

    scene_body = ParagraphStyle(
        'SceneBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.5,
        textColor=colors.HexColor('#F8FAFC')
    )

    story = []

    # =========================================================================
    # PAGE 1: PRE-FLIGHT CHECKLIST & SCENES 1, 2, 3
    # =========================================================================
    story.append(Paragraph("SIH 2026 VIDEO DEMONSTRATION & EXPLANATION PLAYBOOK", doc_title))
    story.append(Paragraph("MINUTE-BY-MINUTE SCREENPLAY, VERBATIM SPOKEN SCRIPT & JURY DEFENSE", doc_subtitle))
    story.append(Spacer(1, 4))

    meta_table_data = [
        [
            Paragraph("<b>Problem Statement ID:</b> 26156", body),
            Paragraph("<b>Theme:</b> Blockchain & Cybersecurity", body),
            Paragraph("<b>Target Video Duration:</b> 3:30 – 3:45 Minutes", body)
        ],
        [
            Paragraph("<b>Team ID:</b> CMRU025", body),
            Paragraph("<b>Team Name:</b> MEGABYTES", body),
            Paragraph("<b>Institution:</b> CMR University, Bengaluru", body)
        ]
    ]
    meta_table = Table(meta_table_data, colWidths=[175, 175, 186])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 4))

    # Pre-recording setup table
    setup_data = [
        [Paragraph("<b>Pre-Recording Setup</b>", body_bold), Paragraph("<b>Target URL / Command</b>", body_bold), Paragraph("<b>Preparation & Action Checklist</b>", body_bold)],
        [Paragraph("Tab 1: Testing Hub", body), Paragraph("<code>http://localhost:8000/testing/</code>", body), Paragraph("Ready on Socket Radar Scope and Stress Cannon controls.", body)],
        [Paragraph("Tab 2: SOC Dashboard", body), Paragraph("<code>http://localhost:8000/dashboard/</code>", body), Paragraph("Ready on Merkle Integrity Vault and AI Onboarding queue.", body)],
        [Paragraph("Tab 3: Terminal Console", body), Paragraph("PowerShell in <code>ulpf-new</code> root", body), Paragraph("Ready to run <code>python scripts/run_benchmarks.py</code> & <code>docker compose ps</code>.", body)],
    ]
    setup_table = Table(setup_data, colWidths=[110, 160, 266])
    setup_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#FFFFFF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(setup_table)
    story.append(Spacer(1, 5))

    story.append(Paragraph("1. Minute-by-Minute Screenplay & Spoken Script", h1_style))

    scenes_p1 = [
        ("SCENE 1 (0:00 – 0:35) | Problem Context & The Core Differentiator",
         "Open Tab 2: Main SOC Dashboard (http://localhost:8000/dashboard/). Hover over Top KPI Cards (Analyzed Events, Live EPS, Threat Incidents) and show the real-time event stream.",
         "Respected Judges, welcome to the demonstration of ULPF — the Universal Log Pre-processing Framework, developed by Team MEGABYTES for Smart India Hackathon Problem Statement 26156 under the Blockchain and Cybersecurity theme.\n\nIn modern enterprise and defense SOCs, security teams face an exponential N x M integration crisis where hundreds of firewall and cloud formats flood expensive SIEMs. This creates huge ingestion licensing taxes, lossy transformations that destroy legal chain-of-custody, and weeks of manual parser coding.\n\nULPF is not another SIEM — it is the vendor-independent, air-gapped preprocessing and cryptographic interoperability layer between heterogeneous log sources and downstream analytics."),
        ("SCENE 2 (0:35 – 1:15) | Multi-Socket Wire Ingress & Live Socket Radar",
         "Switch to Tab 1: Testing Simulator Hub (/testing/). Scroll to Live Network Port Radar (SOCKET RADAR SCOPE). Click button: [DISPATCH ACTIVE SOCKET PROBES]. Show green sweep, blips with ripple pings, and latency badges updating to 0.45 ms RTT.",
         "Here on our Testing Simulator Hub, you are seeing our Live Network Port Radar. ULPF operates at the wire layer using non-blocking asynchronous sockets on pure Syslog UDP :5140, Syslog TCP :5141, and REST Ingestion on :8000, with zero client-side agent overhead.\n\nWhen I trigger an active socket probe across all 6 subsystems, you can see real-time datagram handshakes with sub-millisecond response times—averaging just 0.45 milliseconds—proving our drop-in readiness for high-speed network edge devices."),
        ("SCENE 3 (1:15 – 1:55) | 184k EPS Stress Cannon & 8-Threat Red-Team Arsenal",
         "Still on Testing Hub. Scroll to Stress Cannon. Click 'SYN FLOOD DoS' from 8-threat grid. Click [DISPATCH 1,000 PACKET BURST]. Show immediate transmission receipts and wiretap console feed updating.",
         "Next, our High-Velocity Stress Cannon and Red-Team Cyber Threat Arsenal tests system resilience across 8 active attack scenarios—including SYN Floods, SQL Injection chains, DNS Tunneling, and Ransomware canaries.\n\nWhen we fire a 1,000-datagram burst directly over UDP socket 5140, ULPF sustains an empirical throughput of over 184,400 packets per second with a memory footprint of just 42 Megabytes RSS. Our C-Fast compiler deterministically normalizes multi-vendor formats into canonical ULPF-IR.")
    ]

    for title, action, narration in scenes_p1:
        narr_formatted = "<br/>".join([f"<i>&ldquo;{line}&rdquo;</i>" for line in narration.split("\n\n")])
        s_data = [
            [Paragraph(f"<b>{title}</b>", scene_title)],
            [Paragraph(f"<b>[ACTION ON SCREEN]:</b> {action}<br/><br/><b>[WHAT TO SAY WORD-FOR-WORD]:</b><br/>{narr_formatted}", scene_body)]
        ]
        s_t = Table(s_data, colWidths=[536])
        s_t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
            ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#1E293B')),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#334155')),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 5),
            ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(s_t)
        story.append(Spacer(1, 3))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: SCENES 4, 5, 6 & DOCKER/REDPANDA PRO-CLIPS
    # =========================================================================
    story.append(Paragraph("1. Minute-by-Minute Screenplay & Spoken Script (Continued)", h1_style))

    scenes_p2 = [
        ("SCENE 4 (1:55 – 2:35) | Cryptographic SHA-256 Merkle Ledger (Blockchain Theme)",
         "Switch to Tab 2: Main Dashboard -> Navigate to Merkle Integrity Vault / Forensic Studio. Show 125 Logs/Block visualizer with root hash verification. Click [SIMULATE LOG TAMPER]. Show red alert flashing.",
         "This brings us to our core link to the Blockchain & Cybersecurity theme: our Cryptographic SHA-256 Merkle Ledger Vault.\n\nUnlike conventional SIEMs that perform lossy normalization, ULPF preserves 100% of the raw byte stream and batches events into 125-log cryptographic blocks. A SHA-256 Merkle root is calculated for every block. If an adversary gains root privileges on the server and alters even a single byte of a historical log, the Merkle tree recalculation immediately fails, alerting the SOC of evidence tampering.\n\nThis guarantees complete non-repudiation and court-admissible digital chain-of-custody under Section 65B of the Indian Evidence Act."),
        ("SCENE 5 (2:35 – 3:15) | Sovereign Air-Gapped AI Parser Onboarding Engine",
         "In Main Dashboard -> Navigate to AI Onboarding / Unknown Logs Queue. Select unparsed SCADA/Modbus log format. Click [SYNTHESIZE AI PARSER]. Show generated Pydantic schema and regex tokens, click [APPROVE TO PRODUCTION].",
         "What happens when a network device emits a completely unknown, proprietary, or zero-day log format?\n\nInstead of breaking the pipeline or requiring weeks of manual regex coding, ULPF routes the log to our Sovereign AI Onboarding Engine. Powered by a local, air-gapped Large Language Model running on Ollama, the AI analyzes the syntax, synthesizes a deterministic parser, validates it against test samples, and presents it to the administrator for single-click deployment.\n\nBecause the LLM runs 100% locally on-premise, zero sensitive telemetry or defense logs ever leave the air-gapped network."),
        ("SCENE 6 (3:15 – 3:45) | Analytics Studio, Docker / Redpanda Power-Clip & Conclusion",
         "Switch to Analytics Studio (show live EPS chart & severity breakdown). Switch to Terminal window: run 'docker compose ps' and 'python scripts/run_benchmarks.py' showing 100% OPERATIONAL [OK].",
         "Finally, our Analytics Studio exports standardized telemetry into OCSF v1.1.0, Elastic ECS, and OpenSearch, while enabling rapid CERT-In 6-Hour incident reporting compliance.\n\nThe entire ULPF ecosystem—including core workers, Redpanda streaming brokers, MinIO immutable vaults, and OpenSearch nodes—runs with a single 'docker compose up' command. As demonstrated by our live benchmark suite executing here, all subsystem benchmarks are 100% operational.\n\nULPF delivers sovereign, high-throughput cyber defense for India's strategic networks. Thank you!")
    ]

    for title, action, narration in scenes_p2:
        narr_formatted = "<br/>".join([f"<i>&ldquo;{line}&rdquo;</i>" for line in narration.split("\n\n")])
        s_data = [
            [Paragraph(f"<b>{title}</b>", scene_title)],
            [Paragraph(f"<b>[ACTION ON SCREEN]:</b> {action}<br/><br/><b>[WHAT TO SAY WORD-FOR-WORD]:</b><br/>{narr_formatted}", scene_body)]
        ]
        s_t = Table(s_data, colWidths=[536])
        s_t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
            ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#1E293B')),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#334155')),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 5),
            ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(s_t)
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 4))

    # Docker / Redpanda pro-tip box
    docker_tip_data = [
        [Paragraph("<b>💡 5-SECOND PRO-TIP: HOW TO SHOW DOCKER, REDPANDA & MINIO IN THE VIDEO</b>", body_bold)],
        [Paragraph(
            "• <b>Terminal Clip (3 seconds):</b> Run <code>docker compose ps</code> showing all microservices healthy (api, redpanda, minio, opensearch).<br/>"
            "• <b>Dashboard Indicator (2 seconds):</b> In Dashboard Overview, point to the green badges: <code>Redpanda: Connected (:9092)</code>, <code>MinIO: Mounted (ulpf-raw)</code>, <code>OpenSearch: Indexing (:9200)</code>.<br/>"
            "• <b>Judges' Impression:</b> Demonstrating containerization in 5 seconds proves enterprise readiness without wasting valuable pitch time on boring setup screens.",
            callout_green
        )]
    ]
    t_dtip = Table(docker_tip_data, colWidths=[536])
    t_dtip.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#ECFDF5')),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#F0FDF4')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#10B981')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_dtip)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: DEEP-DIVE TECHNICAL EXPLANATION FOR JUDGES & JURY Q&A
    # =========================================================================
    story.append(Paragraph("2. Deep-Dive Technical Explanations for Judges", h1_style))
    story.append(Paragraph(
        "Use these structured technical explanations when explaining architectural decisions or defending during the live evaluation:",
        body
    ))
    story.append(Spacer(1, 3))

    tech_explanations = [
        ("1. Why Wire Sockets (UDP 5140 / TCP 5141) Instead of Agent Forwarders (Logstash / Fluentbit)?",
         "Commercial SIEM forwarders (Logstash, Fluentbit, Splunk Universal Forwarder) require installing heavyweight software on every host, consuming 200MB+ RAM and requiring kernel permissions. Firewalls, switches, and OT/SCADA devices do not allow agent installation. ULPF acts as a non-blocking Syslog proxy listening on native UDP 5140 and TCP 5141, allowing any network appliance to stream logs instantly with zero client agent overhead."),
        ("2. How Does the SHA-256 Merkle Tree Ledger Batching Algorithm Work?",
         "Logs are queued in an asynchronous ring buffer. When 125 logs accumulate (or after a 5-second interval), each raw log's SHA-256 hash forms a leaf node. The leaves are recursively paired and hashed to compute the root hash. The root hash is cryptographically signed and stored with block metadata. If any attacker edits a past log in storage, recalculating the Merkle tree yields a mismatched root, proving evidence tampering."),
        ("3. How Does the Air-Gapped Sovereign AI Onboarding Engine Guarantee Safety?",
         "Unknown logs fall through to the Dead-Letter Queue (DLQ). A local LLM (Qwen 2.5 7B quantized via Ollama) extracts syntax tokens and writes a Python Pydantic V2 parser schema. Before deployment, the parser runs against 20 synthetic test samples in an isolated sandbox. Only upon passing 100% validation and receiving human SOC admin approval is it compiled into the active parser registry. No data ever leaves the local network."),
        ("4. How Does Field-Level Byte Provenance Satisfy Section 65B of the Indian Evidence Act?",
         "Section 65B requires proof that electronic records were produced by an unbroken, uncorrupted computer process. ULPF stores the unmodified raw byte payload alongside the canonical JSON. For every extracted field (e.g. source IP), ULPF stores exact character byte offsets: <code>{'src_ip': '198.51.100.23', 'offset': [45, 59]}</code>, proving exact mathematical lineage between raw evidence and normalized alert.")
    ]

    for title, exp in tech_explanations:
        t_exp_data = [
            [Paragraph(f"<b>{title}</b>", h2_style)],
            [Paragraph(exp, body)]
        ]
        t_exp_t = Table(t_exp_data, colWidths=[536])
        t_exp_t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
            ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#FFFFFF')),
            ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#CBD5E1')),
            ('TOPPADDING', (0,0), (-1,-1), 2.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
            ('LEFTPADDING', (0,0), (-1,-1), 5),
            ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(t_exp_t)
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 4))
    story.append(Paragraph("3. Grand Finale Jury Defense & Q&A Strategy", h1_style))

    jury_qa = [
        ("Q1: How is your solution directly tied to Blockchain?",
         "Answer: 'We utilize the core cryptographic foundation of Blockchain — the SHA-256 Merkle Tree Ledger. Logs are batched into 125-event blocks. Any historical modification causes an immediate Merkle root mismatch, ensuring non-repudiation and court admissibility under Section 65B IE Act.'"),
        ("Q2: How do you achieve 184k EPS with only 42 MB memory footprint?",
         "Answer: 'We use non-blocking asynchronous kernel sockets (socket.SOCK_DGRAM) paired with compiled C-Fast regex tokenizers. Ingestion bypasses heavy object allocation until batch normalization, keeping memory footprint at 42.14 MB RSS on a single CPU core.'"),
        ("Q3: How does ULPF help with CERT-In 6-Hour reporting mandates?",
         "Answer: 'Under CERT-In guidelines, organizations must report cyber incidents within 6 hours. When an incident occurs, investigating disparate raw logs takes days. ULPF's sub-millisecond canonical normalization and unified OCSF indexing allows SOC analysts to query unified cross-vendor incident timelines in seconds.'")
    ]

    for q, a in jury_qa:
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
        story.append(Spacer(1, 2))

    doc.build(story, canvasmaker=ScriptNumberedCanvas)
    print(f"Master Video Playbook PDF Generated: {PDF_PATH}")

if __name__ == '__main__':
    build_video_script_pdf()
