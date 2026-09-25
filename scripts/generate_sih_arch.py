import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_architecture_image():
    fig, ax = plt.subplots(figsize=(12, 6.5), dpi=300)
    fig.patch.set_facecolor('#0B0F19')
    ax.set_facecolor('#0B0F19')

    # Main Card
    main_rect = patches.FancyBboxPatch((0.01, 0.01), 0.98, 0.98,
                                        boxstyle="round,pad=0.01,rounding_size=0.02",
                                        facecolor='#030712', edgecolor='#1F2937', linewidth=1.2)
    ax.add_patch(main_rect)

    tiers = [
        {"title": "TIER 1: WIRE INGRESS", "sub": "Raw Sockets & Connectors", "color": "#00D084", "items": ["Syslog UDP (:5140)", "Syslog TCP (:5141)", "REST API (:8000)", "File Replay Hub"], "x": 0.04},
        {"title": "TIER 2: FAST PARSER", "sub": "Deterministic & AI", "color": "#38BDF8", "items": ["C-Fast Compiler", "Syslog, CEF, JSON, KV", "ULPF-IR Canonical Model", "Air-Gapped Sovereign AI"], "x": 0.23},
        {"title": "TIER 3: CRYPTO VAULT", "sub": "Integrity & Threat Triage", "color": "#A78BFA", "items": ["SHA-256 Merkle Ledger", "125 Logs / Block Hash", "Byte-Offset Provenance", "Heuristic Threat Triage"], "x": 0.42},
        {"title": "TIER 4: STORAGE LAYER", "sub": "Persistence & Multi-Store", "color": "#FBBF24", "items": ["SQLite (WAL Mode)", "PostgreSQL Backend", "MinIO Raw Object Vault", "Dead-Letter Queue (DLQ)"], "x": 0.61},
        {"title": "TIER 5: EGRESS SINKS", "sub": "Standardized Outputs", "color": "#F43F5E", "items": ["OCSF v1.1.0 Schemas", "Elastic Common Schema", "OpenSearch & Redpanda", "Forensic Studio & Radar"], "x": 0.80},
    ]

    for t in tiers:
        x = t["x"]
        # Column card
        rect = patches.FancyBboxPatch((x, 0.08), 0.16, 0.84, boxstyle="round,pad=0.015,rounding_size=0.025",
                                      facecolor='#111827', edgecolor='#1F2937', linewidth=1.2)
        ax.add_patch(rect)

        # Header pill
        header_rect = patches.FancyBboxPatch((x + 0.01, 0.82), 0.14, 0.08, boxstyle="round,pad=0.008,rounding_size=0.015",
                                             facecolor=t["color"], edgecolor='none')
        ax.add_patch(header_rect)
        ax.text(x + 0.08, 0.87, t["title"], color='#0B0F19', fontsize=7.5, fontweight='bold', ha='center', va='center')
        ax.text(x + 0.08, 0.84, t["sub"], color='#0B0F19', fontsize=6.2, ha='center', va='center')

        # Items
        y_item = 0.74
        for item in t["items"]:
            item_rect = patches.FancyBboxPatch((x + 0.01, y_item - 0.04), 0.14, 0.09, boxstyle="round,pad=0.008,rounding_size=0.015",
                                               facecolor='#1F2937', edgecolor='#374151', linewidth=0.8)
            ax.add_patch(item_rect)
            ax.text(x + 0.08, y_item + 0.005, item, color='#F3F4F6', fontsize=6.8, fontweight='medium', ha='center', va='center')
            y_item -= 0.13

        # Connecting Arrow (except last)
        if x < 0.80:
            ax.annotate('', xy=(x + 0.178, 0.50), xytext=(x + 0.162, 0.50),
                        arrowprops=dict(arrowstyle="-|>", color='#6B7280', lw=1.5, mutation_scale=12))

    # Top title
    ax.text(0.5, 0.955, "ULPF 5-TIER END-TO-END SYSTEM ARCHITECTURE & DATA FLOW",
            color='#F9FAFB', fontsize=11, fontweight='bold', ha='center', va='center')

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig("docs/sih_assets/sih_architecture_diagram.png", bbox_inches='tight', pad_inches=0.05)
    plt.close()
    print("Generated: docs/sih_assets/sih_architecture_diagram.png")

if __name__ == '__main__':
    generate_architecture_image()
