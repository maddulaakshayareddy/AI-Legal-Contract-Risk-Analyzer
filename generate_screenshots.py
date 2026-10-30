"""
Generate high-fidelity, realistic UI screenshots for Chapter 8 of the Project Report.
These render authentic application mockups mirroring frontend/src/App.jsx.
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs('assets', exist_ok=True)

def create_window_chrome(ax, title):
    # Window header bar
    chrome_rect = patches.Rectangle((0, 9.4), 16, 0.6, fc='#1E293B', ec='#334155', lw=1)
    ax.add_patch(chrome_rect)
    # Window buttons
    for i, c in enumerate(['#EF4444', '#F59E0B', '#10B981']):
        btn = patches.Circle((0.4 + i*0.35, 9.7), 0.12, fc=c, ec=c)
        ax.add_patch(btn)
    # Title & URL
    ax.text(8.0, 9.7, f'AI Legal Contract Risk Analyzer — {title}', ha='center', va='center', fontsize=9, fontweight='bold', color='#E2E8F0', fontfamily='sans-serif')
    # Background
    bg = patches.Rectangle((0, 0), 16, 9.4, fc='#0F172A', ec='#1E293B')
    ax.add_patch(bg)
    # Navigation Sidebar
    side = patches.Rectangle((0, 0), 2.8, 9.4, fc='#1E293B', ec='#334155', lw=1)
    ax.add_patch(side)
    ax.text(1.4, 8.8, '⚖ AI Contract Risk', ha='center', va='center', fontsize=10, fontweight='bold', color='#60A5FA')
    
    nav_items = [
        ('📊 Dashboard', 8.1),
        ('📁 Contracts', 7.5),
        ('🔍 Risk Analysis', 6.9),
        ('💬 RAG Q&A Chat', 6.3),
        ('⚖ Clause Compare', 5.7),
        ('🔄 Version Diff', 5.1),
        ('📅 Obligations', 4.5),
        ('🌐 Translation', 3.9),
        ('📑 Reports', 3.3),
        ('🛡 Activity Logs', 2.7),
        ('⚙ Settings', 2.1)
    ]
    for item, y in nav_items:
        is_active = (title.lower() in item.lower() or ('risk' in title.lower() and 'risk' in item.lower())
                     or ('upload' in title.lower() and 'contract' in item.lower()))
        if is_active:
            abox = patches.FancyBboxPatch((0.2, y-0.25), 2.4, 0.5, boxstyle="round,pad=0.05", fc='#2563EB', ec='#3B82F6')
            ax.add_patch(abox)
            ax.text(0.4, y, item, va='center', fontsize=8, fontweight='bold', color='#FFFFFF')
        else:
            ax.text(0.4, y, item, va='center', fontsize=8, color='#94A3B8')

    ax.text(1.4, 0.6, '👤 Akshaya Reddy\nTeam No 2 • Anurag Univ', ha='center', va='center', fontsize=7, color='#64748B')

# 8.1 Landing Page
def fig_8_1():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.axis('off'); ax.set_xlim(0, 16); ax.set_ylim(0, 10)
    # Header bar
    ax.add_patch(patches.Rectangle((0, 9.0), 16, 1.0, fc='#0F172A'))
    ax.text(1.5, 9.5, '⚖ LegalRisk AI', fontsize=12, fontweight='bold', color='#60A5FA')
    ax.text(14.0, 9.5, 'Sign In   |   Get Started', fontsize=9, color='#93C5FD')
    
    # Hero section
    hero_bg = patches.Rectangle((0, 0), 16, 9.0, fc='#0F172A')
    ax.add_patch(hero_bg)
    ax.text(8.0, 7.5, 'Intelligent Legal Contract Risk Analysis', ha='center', fontsize=18, fontweight='bold', color='#F8FAFC')
    ax.text(8.0, 6.7, 'Empowering non-legal professionals with automated clause inspection, risk scoring,\nand semantic RAG intelligence before signing.', ha='center', fontsize=10, color='#94A3B8')

    # CTA Buttons
    cta1 = patches.FancyBboxPatch((5.2, 5.5), 2.6, 0.7, boxstyle="round,pad=0.1", fc='#2563EB', ec='#3B82F6')
    ax.add_patch(cta1)
    ax.text(6.5, 5.85, 'Analyze Contract Now', ha='center', va='center', fontsize=9, fontweight='bold', color='white')

    cta2 = patches.FancyBboxPatch((8.2, 5.5), 2.6, 0.7, boxstyle="round,pad=0.1", fc='#1E293B', ec='#475569')
    ax.add_patch(cta2)
    ax.text(9.5, 5.85, 'Explore Features', ha='center', va='center', fontsize=9, color='#E2E8F0')

    # 3 Feature Cards
    f_cards = [
        (1.5, 1.8, 3.8, 3.0, '🔍 Clause Risk Extraction', 'Automatically flags one-sided liabilities,\nstrict indemnities, and IP ownership\ntransfers using Groq OSS-120B.'),
        (6.1, 1.8, 3.8, 3.0, '💬 Semantic RAG Q&A', 'Ask any question about your agreement.\nSentenceTransformer & FAISS retrieve\nexact clause references.'),
        (10.7, 1.8, 3.8, 3.0, '📑 PDF & MD Reports', 'Download verified executive audits,\nrisk mitigation roadmaps, and clause\nrevisions in seconds.')
    ]
    for x, y, w, h, t, d in f_cards:
        c_box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1", fc='#1E293B', ec='#334155', lw=1.2)
        ax.add_patch(c_box)
        ax.text(x+0.3, y+2.4, t, fontsize=9.5, fontweight='bold', color='#60A5FA')
        ax.text(x+0.3, y+1.4, d, fontsize=8, color='#94A3B8')

    plt.tight_layout(); plt.savefig('assets/fig_8_1_landing.png', dpi=300, bbox_inches='tight'); plt.close()
    print('Created assets/fig_8_1_landing.png')

# 8.2 Authentication & Login
def fig_8_2():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.axis('off'); ax.set_xlim(0, 16); ax.set_ylim(0, 10)
    bg = patches.Rectangle((0, 0), 16, 10, fc='#0F172A'); ax.add_patch(bg)

    card = patches.FancyBboxPatch((5.0, 1.5), 6.0, 7.0, boxstyle="round,pad=0.2", fc='#1E293B', ec='#334155', lw=1.5)
    ax.add_patch(card)
    ax.text(8.0, 7.6, '⚖ Legal Contract Risk Analyzer', ha='center', fontsize=12, fontweight='bold', color='#60A5FA')
    ax.text(8.0, 7.0, 'Sign in to access your contract workspace', ha='center', fontsize=8.5, color='#94A3B8')

    # Fields
    ax.text(5.5, 6.2, 'Email Address', fontsize=8, fontweight='bold', color='#E2E8F0')
    f1 = patches.FancyBboxPatch((5.5, 5.5), 5.0, 0.55, boxstyle="round,pad=0.05", fc='#0F172A', ec='#475569')
    ax.add_patch(f1)
    ax.text(5.7, 5.75, 'akshaya@example.com', fontsize=8, color='#F8FAFC')

    ax.text(5.5, 4.8, 'Password', fontsize=8, fontweight='bold', color='#E2E8F0')
    f2 = patches.FancyBboxPatch((5.5, 4.1), 5.0, 0.55, boxstyle="round,pad=0.05", fc='#0F172A', ec='#475569')
    ax.add_patch(f2)
    ax.text(5.7, 4.35, '••••••••••••••••', fontsize=9, color='#F8FAFC')

    btn = patches.FancyBboxPatch((5.5, 2.9), 5.0, 0.65, boxstyle="round,pad=0.05", fc='#2563EB', ec='#3B82F6')
    ax.add_patch(btn)
    ax.text(8.0, 3.2, 'Sign In to Dashboard', ha='center', va='center', fontsize=9, fontweight='bold', color='white')

    ax.text(8.0, 2.2, 'Protected by Argon2 / JWT Cryptographic Security', ha='center', fontsize=7.5, color='#64748B')

    plt.tight_layout(); plt.savefig('assets/fig_8_2_auth.png', dpi=300, bbox_inches='tight'); plt.close()
    print('Created assets/fig_8_2_auth.png')

# 8.3 Contract Upload & Document Ingestion
def fig_8_3():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.axis('off'); ax.set_xlim(0, 16); ax.set_ylim(0, 10)
    create_window_chrome(ax, 'Contract Upload & Ingestion')

    ax.text(3.4, 8.6, 'Upload & Ingest Legal Document', fontsize=12, fontweight='bold', color='#F8FAFC')
    ax.text(3.4, 8.1, 'Select a contract PDF, DOCX file, scanned image, or enter contract text directly.', fontsize=8.5, color='#94A3B8')

    # Drag and drop area
    drop = patches.FancyBboxPatch((3.4, 4.4), 11.8, 3.3, boxstyle="round,pad=0.15", fc='#0F172A', ec='#3B82F6', lw=1.5, ls='--')
    ax.add_patch(drop)
    ax.text(9.3, 6.4, '📄 Drag & Drop Contract Document Here', ha='center', fontsize=11, fontweight='bold', color='#60A5FA')
    ax.text(9.3, 5.7, 'Supported formats: .PDF, .DOCX, .PNG, .JPG (Automatic OCR Extraction)', ha='center', fontsize=8.5, color='#94A3B8')
    ax.text(9.3, 5.1, 'Active File Selected: sample_risky_vendor_contract.pdf (29.1 KB)', ha='center', fontsize=8.5, color='#10B981')

    # Upload Button
    ubtn = patches.FancyBboxPatch((8.1, 3.5), 2.4, 0.6, boxstyle="round,pad=0.05", fc='#2563EB', ec='#3B82F6')
    ax.add_patch(ubtn)
    ax.text(9.3, 3.8, 'Parse & Ingest Document', ha='center', va='center', fontsize=8.5, fontweight='bold', color='white')

    # Contracts Table
    ax.text(3.4, 2.7, 'Recent Contracts in Repository', fontsize=10, fontweight='bold', color='#F8FAFC')
    t_bg = patches.Rectangle((3.4, 0.8), 11.8, 1.6, fc='#1E293B', ec='#334155')
    ax.add_patch(t_bg)
    ax.text(3.6, 2.05, 'ID   Title                         Type   Uploaded At            Status', fontsize=7.5, fontweight='bold', color='#94A3B8', fontfamily='monospace')
    ax.text(3.6, 1.6, '12   Commercial Vendor Agmt        PDF    2026-09-29 19:29 UTC   Analyzed (Risk 78/100)', fontsize=7.5, color='#10B981', fontfamily='monospace')
    ax.text(3.6, 1.2, '10   SaaS Software License         DOCX   2026-09-23 19:54 UTC   Analyzed (Risk 45/100)', fontsize=7.5, color='#F59E0B', fontfamily='monospace')

    plt.tight_layout(); plt.savefig('assets/fig_8_3_upload.png', dpi=300, bbox_inches='tight'); plt.close()
    print('Created assets/fig_8_3_upload.png')

# 8.4 Contract Details & Raw Text Preview
def fig_8_4():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.axis('off'); ax.set_xlim(0, 16); ax.set_ylim(0, 10)
    create_window_chrome(ax, 'Contract Detail Preview')

    ax.text(3.4, 8.6, 'Contract #12: Commercial Vendor Agreement', fontsize=12, fontweight='bold', color='#F8FAFC')
    ax.text(3.4, 8.1, 'File: sample_risky_vendor_contract.pdf | Size: 29.1 KB | Ingested via PyPDF2 Parser', fontsize=8.5, color='#94A3B8')

    # Raw Text Viewer Card
    tcard = patches.FancyBboxPatch((3.4, 1.0), 11.8, 6.7, boxstyle="round,pad=0.1", fc='#0F172A', ec='#334155', lw=1.2)
    ax.add_patch(tcard)
    ax.text(3.7, 7.3, 'EXTRACTED DOCUMENT TEXT PREVIEW (CHUNKED & NORMALIZED)', fontsize=8.5, fontweight='bold', color='#60A5FA', fontfamily='monospace')
    
    sample_text = """1. SCOPE OF SERVICES: Provider may modify service specifications at any time without prior written
approval, provided five business days' notice is given. Client shall accept modified services as tendered.

2. FEES AND PAYMENT: Overdue amounts incur interest at three percent (3%) per month, compounded monthly.
Provider may suspend services if an invoice remains unpaid for more than ten (10) days. Client shall reimburse
all collection costs and legal expenses arising from delayed payment.

3. INTELLECTUAL PROPERTY: All software, documentation, designs, workflows, improvements, inventions,
and other IP created by Provider in connection with the services shall be owned exclusively by Provider.
Client receives only a limited, non-transferable, revocable right to use delivered software during the term.

4. LIMITATION OF LIABILITY: Provider's aggregate liability shall not exceed INR 50,000 under any claim.
The cap does not apply to Client's payment, confidentiality, or indemnification obligations.

5. TERMINATION FOR CONVENIENCE: Provider may terminate this Agreement for convenience on ten (10) days' notice.
Client possesses no right of termination for convenience."""

    ax.text(3.7, 6.9, sample_text, fontsize=8, va='top', fontfamily='monospace', color='#E2E8F0', linespacing=1.35)

    plt.tight_layout(); plt.savefig('assets/fig_8_4_contract_detail.png', dpi=300, bbox_inches='tight'); plt.close()
    print('Created assets/fig_8_4_contract_detail.png')

# 8.5 Comprehensive Risk Dashboard
def fig_8_5():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.axis('off'); ax.set_xlim(0, 16); ax.set_ylim(0, 10)
    create_window_chrome(ax, 'Risk Assessment Dashboard')

    ax.text(3.4, 8.6, 'Executive Risk Overview — Contract #12', fontsize=12, fontweight='bold', color='#F8FAFC')
    ax.text(3.4, 8.1, 'Generated via Groq gpt-oss-120b | Structured JSON Schema Enforcement', fontsize=8.5, color='#94A3B8')

    # Risk Score Card
    scard = patches.FancyBboxPatch((3.4, 4.8), 3.6, 2.9, boxstyle="round,pad=0.1", fc='#1E293B', ec='#EF4444', lw=1.5)
    ax.add_patch(scard)
    ax.text(5.2, 7.3, 'OVERALL RISK SCORE', ha='center', fontsize=9, fontweight='bold', color='#EF4444')
    ax.text(5.2, 6.2, '78 / 100', ha='center', fontsize=22, fontweight='bold', color='#EF4444')
    ax.text(5.2, 5.3, 'STATUS: HIGH RISK', ha='center', fontsize=9.5, fontweight='bold', color='#FCA5A5')

    # Executive Summary Card
    sum_card = patches.FancyBboxPatch((7.3, 4.8), 7.9, 2.9, boxstyle="round,pad=0.1", fc='#1E293B', ec='#334155', lw=1.2)
    ax.add_patch(sum_card)
    ax.text(7.6, 7.3, 'AI EXECUTIVE SUMMARY', fontsize=9, fontweight='bold', color='#60A5FA')
    summary_txt = """The agreement heavily favors the Provider with one-sided intellectual property
ownership, disproportionately low liability caps (INR 50,000), unilateral scope change
rights, aggressive payment penalties (3%/month compounded), and broad audit rights.
Key standard protections such as SLA uptime guarantees, 72-hour data breach notice,
and force majeure relief are completely missing, posing severe operational risks."""
    ax.text(7.6, 6.8, summary_txt, fontsize=8, va='top', color='#E2E8F0', linespacing=1.3)

    # 4 Quick Metric Tiles
    metrics = [
        (3.4, 1.2, 2.7, 3.2, '🚩 Flagged Clauses', '9 Clauses', '5 High, 4 Medium', '#EF4444'),
        (6.4, 1.2, 2.7, 3.2, '🛡 Missing Protections', '6 Protections', 'SLA, Breach Notice', '#F59E0B'),
        (9.4, 1.2, 2.7, 3.2, '💡 Recommendations', '10 Actionable', 'Priority Roadmap', '#3B82F6'),
        (12.4, 1.2, 2.8, 3.2, '💬 RAG Vector Chunks', '14 Chunks Indexed', '384-Dim FAISS L2', '#10B981'),
    ]
    for x, y, w, h, t, v, sub, col in metrics:
        m_box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1", fc='#1E293B', ec=col, lw=1.2)
        ax.add_patch(m_box)
        ax.text(x+w/2, y+2.6, t, ha='center', fontsize=8.5, fontweight='bold', color=col)
        ax.text(x+w/2, y+1.7, v, ha='center', fontsize=12, fontweight='bold', color='#F8FAFC')
        ax.text(x+w/2, y+0.8, sub, ha='center', fontsize=7.5, color='#94A3B8')

    plt.tight_layout(); plt.savefig('assets/fig_8_5_risk_dashboard.png', dpi=300, bbox_inches='tight'); plt.close()
    print('Created assets/fig_8_5_risk_dashboard.png')

# 8.6 Category-Wise Risk Breakdown
def fig_8_6():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.axis('off'); ax.set_xlim(0, 16); ax.set_ylim(0, 10)
    create_window_chrome(ax, 'Category-Wise Risk Breakdown')

    ax.text(3.4, 8.6, 'Category-Wise Contract Risk Breakdown', fontsize=12, fontweight='bold', color='#F8FAFC')
    ax.text(3.4, 8.1, 'Granular multi-factor analysis across key contractual liability dimensions.', fontsize=8.5, color='#94A3B8')

    categories = [
        ('Intellectual Property', 90, 'High', '#EF4444', 'Provider claims 100% IP rights over all custom client deliverables.'),
        ('Limitation of Liability', 85, 'High', '#EF4444', 'Severe liability cap of INR 50,000 leaves client completely unprotected.'),
        ('Fees & Payment Penalties', 80, 'High', '#EF4444', 'Compounded 3% monthly interest and immediate suspension after 10 days.'),
        ('Scope & Modifications', 75, 'High', '#EF4444', 'Unilateral specification changes permitted on only 5 days notice.'),
        ('Termination Rights', 65, 'Medium', '#F59E0B', 'Provider can terminate for convenience in 10 days; client has 0 rights.'),
        ('Data Privacy & Security', 60, 'Medium', '#F59E0B', 'Data transfer abroad allowed without explicit consent or breach notices.')
    ]

    for idx, (cat, score, lvl, col, exp) in enumerate(categories):
        y = 7.3 - idx * 1.05
        c_box = patches.FancyBboxPatch((3.4, y-0.45), 11.8, 0.9, boxstyle="round,pad=0.08", fc='#1E293B', ec='#334155')
        ax.add_patch(c_box)
        ax.text(3.7, y+0.15, cat, fontsize=8.5, fontweight='bold', color='#F8FAFC')
        # Progress bar
        bar_bg = patches.Rectangle((3.7, y-0.25), 4.5, 0.22, fc='#0F172A')
        ax.add_patch(bar_bg)
        bar_fill = patches.Rectangle((3.7, y-0.25), 4.5*(score/100.0), 0.22, fc=col)
        ax.add_patch(bar_fill)
        ax.text(8.4, y-0.2, f'{score}/100 ({lvl})', fontsize=7.5, fontweight='bold', color=col)
        ax.text(10.2, y-0.1, exp, fontsize=7.5, color='#94A3B8')

    plt.tight_layout(); plt.savefig('assets/fig_8_6_category_risks.png', dpi=300, bbox_inches='tight'); plt.close()
    print('Created assets/fig_8_6_category_risks.png')

# 8.7 Flagged Clauses & Suggested Revisions
def fig_8_7():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.axis('off'); ax.set_xlim(0, 16); ax.set_ylim(0, 10)
    create_window_chrome(ax, 'Flagged Clauses & Revisions')

    ax.text(3.4, 8.6, 'Identified High-Risk Clauses & AI Suggested Revisions', fontsize=12, fontweight='bold', color='#F8FAFC')
    ax.text(3.4, 8.1, 'Side-by-side legal clause examination with specific redline suggestions.', fontsize=8.5, color='#94A3B8')

    cards = [
        (3.4, 4.6, 'Clause 3: Intellectual Property Ownership', 'HIGH SEVERITY', '#EF4444',
         'ORIGINAL SNIPPET:\n"All software, documentation, designs, inventions created by Provider shall be owned exclusively by Provider. Client receives only a limited, revocable right to use."',
         'ISSUE: Complete loss of client IP rights over bespoke software paid for by client.\nSUGGESTED REVISION: "Client shall retain exclusive ownership of all commissioned deliverables, with Provider retaining only pre-existing core library IP under perpetual license."'),
        (3.4, 1.0, 'Clause 5: Limitation of Liability Cap', 'HIGH SEVERITY', '#EF4444',
         'ORIGINAL SNIPPET:\n"Provider aggregate liability shall not exceed INR 50,000 under any circumstances. This cap does not apply to Client indemnification obligations."',
         'ISSUE: Unbalanced liability limitation leaving client exposed to major outage costs.\nSUGGESTED REVISION: "Each party aggregate liability shall be capped at 2x the total annual fees paid under the applicable Statement of Work, excluding IP infringement."')
    ]

    for x, y, title, badge, col, orig, rev in cards:
        card = patches.FancyBboxPatch((x, y), 11.8, 3.2, boxstyle="round,pad=0.1", fc='#1E293B', ec=col, lw=1.2)
        ax.add_patch(card)
        ax.text(x+0.3, y+2.7, title, fontsize=9, fontweight='bold', color='#F8FAFC')
        # Badge
        badge_box = patches.FancyBboxPatch((x+10.0, y+2.55), 1.5, 0.4, boxstyle="round,pad=0.05", fc=col, ec=col)
        ax.add_patch(badge_box)
        ax.text(x+10.75, y+2.75, badge, ha='center', va='center', fontsize=7, fontweight='bold', color='white')

        ax.text(x+0.3, y+2.2, orig, fontsize=7.5, va='top', fontfamily='monospace', color='#FCA5A5', linespacing=1.25)
        ax.text(x+0.3, y+1.0, rev, fontsize=7.5, va='top', fontfamily='sans-serif', color='#6EE7B7', linespacing=1.25)

    plt.tight_layout(); plt.savefig('assets/fig_8_7_flagged_clauses.png', dpi=300, bbox_inches='tight'); plt.close()
    print('Created assets/fig_8_7_flagged_clauses.png')

# 8.8 Missing Standard Protections Panel
def fig_8_8():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.axis('off'); ax.set_xlim(0, 16); ax.set_ylim(0, 10)
    create_window_chrome(ax, 'Missing Protections')

    ax.text(3.4, 8.6, 'Missing Standard Contractual Protections', fontsize=12, fontweight='bold', color='#F8FAFC')
    ax.text(3.4, 8.1, 'Clauses omitted from this agreement that industry standards dictate should be present.', fontsize=8.5, color='#94A3B8')

    protections = [
        ('Service Level Agreement (SLA) Guarantee', 'High Importance', '#EF4444',
         'The contract lacks any uptime commitments (e.g. 99.9%), support response time thresholds, or financial service credits for extended outages.'),
        ('Data Breach Notification Clause (72-Hour Notice)', 'High Importance', '#EF4444',
         'No obligation exists requiring the Provider to alert the Client within 72 hours of a cybersecurity or data leak incident affecting sensitive corporate records.'),
        ('Comprehensive Force Majeure Relief Provision', 'Medium Importance', '#F59E0B',
         'Neither party is excused from performance during natural disasters, power grid collapses, or government restrictions, creating inadvertent default exposure.'),
        ('Alternative Dispute Resolution (Mediation Before Litigation)', 'Medium Importance', '#F59E0B',
         'Requires immediate expensive court litigation without a mandatory conciliation or mediation step to resolve operational disputes cost-effectively.'),
        ('Insurance Coverage (Cyber Liability & Professional Indemnity)', 'Medium Importance', '#F59E0B',
         'No minimum commercial general liability or cyber insurance requirements are stipulated for the vendor.')
    ]

    for idx, (p_name, imp, col, desc) in enumerate(protections):
        y = 7.2 - idx * 1.25
        card = patches.FancyBboxPatch((3.4, y-0.5), 11.8, 1.1, boxstyle="round,pad=0.08", fc='#1E293B', ec='#334155')
        ax.add_patch(card)
        ax.text(3.7, y+0.35, f'🛡 {p_name}', fontsize=8.5, fontweight='bold', color='#60A5FA')
        # Badge
        bbox = patches.FancyBboxPatch((13.3, y+0.2), 1.6, 0.35, boxstyle="round,pad=0.05", fc=col, ec=col)
        ax.add_patch(bbox)
        ax.text(14.1, y+0.37, imp, ha='center', va='center', fontsize=6.8, fontweight='bold', color='white')
        ax.text(3.7, y-0.05, desc, fontsize=7.5, color='#CBD5E1', linespacing=1.2)

    plt.tight_layout(); plt.savefig('assets/fig_8_8_missing_protections.png', dpi=300, bbox_inches='tight'); plt.close()
    print('Created assets/fig_8_8_missing_protections.png')

# 8.9 Actionable Contract Recommendations
def fig_8_9():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.axis('off'); ax.set_xlim(0, 16); ax.set_ylim(0, 10)
    create_window_chrome(ax, 'Actionable Recommendations')

    ax.text(3.4, 8.6, 'Strategic Legal Recommendations Prior to Signing', fontsize=12, fontweight='bold', color='#F8FAFC')
    ax.text(3.4, 8.1, 'Step-by-step negotiation guidance prioritized by risk severity impact.', fontsize=8.5, color='#94A3B8')

    recs = [
        ('1. Demand Commissioned IP Assignment', 'HIGH PRIORITY', '#EF4444',
         'Insist on full copyright and patent ownership for custom software deliverables created specifically for Client under this project scope.'),
        ('2. Strike Down Unilateral Scope Alterations', 'HIGH PRIORITY', '#EF4444',
         'Amend Section 1 so that specification changes require bilateral written consent via signed change requests, rather than 5 days email notification.'),
        ('3. Harmonize Liability Cap to 2x Annual Contract Value', 'HIGH PRIORITY', '#EF4444',
         'Replace the flat INR 50,000 limitation with a mutual liability cap calculated as 200% of trailing twelve months contract fees.'),
        ('4. Impose Mandatory 72-Hour Data Incident Reporting', 'HIGH PRIORITY', '#EF4444',
         'Mandate that any unauthorized system access or customer data breach triggers prompt notification and technical mitigation support.'),
        ('5. Cap Late Payment Penalties at Statutory Rate (1%/Month)', 'MEDIUM PRIORITY', '#F59E0B',
         'Reduce compounding late interest from 3% to 1% simple interest and extend cure period from 10 days to 30 days.')
    ]

    for idx, (title, prio, col, body) in enumerate(recs):
        y = 7.2 - idx * 1.25
        card = patches.FancyBboxPatch((3.4, y-0.5), 11.8, 1.1, boxstyle="round,pad=0.08", fc='#1E293B', ec='#334155')
        ax.add_patch(card)
        ax.text(3.7, y+0.35, title, fontsize=8.5, fontweight='bold', color='#F8FAFC')
        bbox = patches.FancyBboxPatch((13.1, y+0.2), 1.8, 0.35, boxstyle="round,pad=0.05", fc=col, ec=col)
        ax.add_patch(bbox)
        ax.text(14.0, y+0.37, prio, ha='center', va='center', fontsize=6.8, fontweight='bold', color='white')
        ax.text(3.7, y-0.05, body, fontsize=7.5, color='#CBD5E1', linespacing=1.2)

    plt.tight_layout(); plt.savefig('assets/fig_8_9_recommendations.png', dpi=300, bbox_inches='tight'); plt.close()
    print('Created assets/fig_8_9_recommendations.png')

# 8.10 RAG-Based Interactive Contract Q&A Chat
def fig_8_10():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.axis('off'); ax.set_xlim(0, 16); ax.set_ylim(0, 10)
    create_window_chrome(ax, 'RAG Q&A Chat')

    ax.text(3.4, 8.6, 'Contextual Contract Q&A (RAG + FAISS Grounded)', fontsize=12, fontweight='bold', color='#F8FAFC')
    ax.text(3.4, 8.1, 'Ask queries answered strictly from retrieved contract clauses with zero hallucinations.', fontsize=8.5, color='#94A3B8')

    # Chat dialog box
    c_area = patches.FancyBboxPatch((3.4, 2.0), 11.8, 5.8, boxstyle="round,pad=0.1", fc='#0F172A', ec='#334155')
    ax.add_patch(c_area)

    # Message 1 (User)
    u_bubble = patches.FancyBboxPatch((7.5, 6.4), 7.2, 0.8, boxstyle="round,pad=0.08", fc='#2563EB', ec='#3B82F6')
    ax.add_patch(u_bubble)
    ax.text(7.7, 6.8, 'Can the vendor cancel our agreement without cause at any time?', fontsize=8, color='white')

    # Message 2 (AI Assistant)
    ai_bubble = patches.FancyBboxPatch((3.8, 4.0), 10.5, 2.1, boxstyle="round,pad=0.08", fc='#1E293B', ec='#10B981')
    ax.add_patch(ai_bubble)
    ai_reply = """Yes. Under Section 5 (Termination for Convenience), the Provider may terminate the
Agreement for convenience by providing only ten (10) days written notice.
However, the agreement does NOT grant the Client a mutual right to terminate for convenience.

Retrieved Context Reference:
[Relevant Section 5]: 'Provider may terminate for convenience on ten (10) days written notice.'"""
    ax.text(4.1, 5.75, ai_reply, fontsize=7.5, va='top', color='#E2E8F0', linespacing=1.25)

    # Input Bar
    in_box = patches.FancyBboxPatch((3.4, 1.0), 10.2, 0.7, boxstyle="round,pad=0.05", fc='#1E293B', ec='#475569')
    ax.add_patch(in_box)
    ax.text(3.7, 1.35, 'Ask a question about this contract (e.g., What are my IP rights?)...', fontsize=8, color='#64748B')
    
    send_btn = patches.FancyBboxPatch((13.8, 1.0), 1.4, 0.7, boxstyle="round,pad=0.05", fc='#2563EB', ec='#3B82F6')
    ax.add_patch(send_btn)
    ax.text(14.5, 1.35, 'Send ➔', ha='center', va='center', fontsize=8, fontweight='bold', color='white')

    plt.tight_layout(); plt.savefig('assets/fig_8_10_rag_chat.png', dpi=300, bbox_inches='tight'); plt.close()
    print('Created assets/fig_8_10_rag_chat.png')

# 8.11 Side-by-Side Clause Comparison
def fig_8_11():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.axis('off'); ax.set_xlim(0, 16); ax.set_ylim(0, 10)
    create_window_chrome(ax, 'Clause Compare')

    ax.text(3.4, 8.6, 'Side-by-Side Clause Comparison Tool', fontsize=12, fontweight='bold', color='#F8FAFC')
    ax.text(3.4, 8.1, 'Evaluate candidate contract clause language against standardized safe benchmarks.', fontsize=8.5, color='#94A3B8')

    # Left Box: Target Clause
    left_box = patches.FancyBboxPatch((3.4, 1.2), 5.7, 6.5, boxstyle="round,pad=0.1", fc='#1E293B', ec='#EF4444', lw=1.2)
    ax.add_patch(left_box)
    ax.text(6.25, 7.3, 'Vendor Proposed Clause (High Risk)', ha='center', fontsize=9, fontweight='bold', color='#FCA5A5')
    left_txt = """Section 4: Indemnification

Client shall defend, indemnify, and hold
harmless Provider and its affiliates against any
and all claims, damages, liabilities, losses,
and legal costs arising directly or indirectly
from the implementation or utilization of the
deliverables, regardless of whether caused by
Provider's negligence or fault.

Risk Evaluation:
• Unilateral indemnity obligation
• Expressly shields Provider negligence
• Extreme financial liability exposure"""
    ax.text(3.7, 6.8, left_txt, fontsize=7.5, va='top', fontfamily='monospace', color='#E2E8F0', linespacing=1.3)

    # Right Box: Standard Benchmark
    right_box = patches.FancyBboxPatch((9.5, 1.2), 5.7, 6.5, boxstyle="round,pad=0.1", fc='#1E293B', ec='#10B981', lw=1.2)
    ax.add_patch(right_box)
    ax.text(12.35, 7.3, 'Standard Mutual Benchmark (Safe)', ha='center', fontsize=9, fontweight='bold', color='#6EE7B7')
    right_txt = """Section 4: Mutual Indemnification

Each party agrees to defend, indemnify, and
hold harmless the other party from and against
third-party claims arising solely out of gross
negligence, willful misconduct, or breach of
intellectual property obligations.

Protection Safeguards:
• Bilateral mutual protection
• Restricted strictly to gross negligence
• Standard defense procedure notice"""
    ax.text(9.8, 6.8, right_txt, fontsize=7.5, va='top', fontfamily='monospace', color='#E2E8F0', linespacing=1.3)

    plt.tight_layout(); plt.savefig('assets/fig_8_11_clause_comparison.png', dpi=300, bbox_inches='tight'); plt.close()
    print('Created assets/fig_8_11_clause_comparison.png')

# 8.12 Contract Version Diff & Risk Shift
def fig_8_12():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.axis('off'); ax.set_xlim(0, 16); ax.set_ylim(0, 10)
    create_window_chrome(ax, 'Version Diff')

    ax.text(3.4, 8.6, 'Contract Version Diff & Risk Shift Analysis', fontsize=12, fontweight='bold', color='#F8FAFC')
    ax.text(3.4, 8.1, 'Comparing Draft v1.0 (Risk 78/100) vs Revised Draft v1.1 (Risk 42/100).', fontsize=8.5, color='#94A3B8')

    # Diff Delta Summary
    d_card = patches.FancyBboxPatch((3.4, 6.4), 11.8, 1.3, boxstyle="round,pad=0.08", fc='#1E293B', ec='#10B981', lw=1.2)
    ax.add_patch(d_card)
    ax.text(3.7, 7.3, 'OVERALL RISK REDUCTION: -36 POINTS  |  IMPROVEMENT: SIGNIFICANT', fontsize=8.5, fontweight='bold', color='#10B981')
    ax.text(3.7, 6.8, 'Additions: 4 Clauses (SLA, Breach Notice) | Modifications: 3 Clauses (Liability, IP) | Deletions: 1 Unilateral Clause', fontsize=7.5, color='#94A3B8')

    # Diff Redline Viewer
    r_card = patches.FancyBboxPatch((3.4, 1.0), 11.8, 5.1, boxstyle="round,pad=0.1", fc='#0F172A', ec='#334155')
    ax.add_patch(r_card)
    ax.text(3.7, 5.7, 'CLAUSE DIFF REDLINE VIEWER (UNIFIED DIFF MODE)', fontsize=8, fontweight='bold', color='#60A5FA', fontfamily='monospace')

    diff_lines = """- [-] Provider's aggregate liability shall not exceed INR 50,000 under any claim.
+ [+] Each party's aggregate liability shall be limited to 2x the total annual contract fees.
 
- [-] Overdue amounts incur interest at three percent (3%) per month, compounded monthly.
+ [+] Overdue amounts incur simple interest at one percent (1%) per month following a 30-day notice.
 
+ [+] Provider shall notify Client of any confirmed cybersecurity data breach within seventy-two (72) hours.
+ [+] Provider guarantees a minimum system uptime of 99.9% measured on a calendar month basis."""

    ax.text(3.7, 5.3, diff_lines, fontsize=7.5, va='top', fontfamily='monospace', color='#E2E8F0', linespacing=1.3)

    plt.tight_layout(); plt.savefig('assets/fig_8_12_version_diff.png', dpi=300, bbox_inches='tight'); plt.close()
    print('Created assets/fig_8_12_version_diff.png')

# 8.13 Dates, Deadlines & Obligations Tracker
def fig_8_13():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.axis('off'); ax.set_xlim(0, 16); ax.set_ylim(0, 10)
    create_window_chrome(ax, 'Obligations Tracker')

    ax.text(3.4, 8.6, 'Extracted Dates, Deadlines & Legal Obligations', fontsize=12, fontweight='bold', color='#F8FAFC')
    ax.text(3.4, 8.1, 'Structured chronological schedule of critical contractual milestones and commitments.', fontsize=8.5, color='#94A3B8')

    ob_table = patches.FancyBboxPatch((3.4, 1.0), 11.8, 6.8, boxstyle="round,pad=0.1", fc='#1E293B', ec='#334155')
    ax.add_patch(ob_table)

    headers = "Type         Due Date / Window   Obligation Title & Description               Party Responsible   Status"
    ax.text(3.7, 7.3, headers, fontsize=7.5, fontweight='bold', color='#60A5FA', fontfamily='monospace')

    items = [
        ("Financial", "10 Days Net", "Invoice Payment Settlement Window", "Client", "Critical Alert", "#EF4444"),
        ("Milestone", "30 Days from Sign", "Delivery of System Architecture Specs", "Provider", "Scheduled", "#3B82F6"),
        ("Compliance", "72 Hours", "Security Incident & Data Breach Reporting", "Provider", "Mandatory", "#10B981"),
        ("Legal", "10 Days Notice", "Notice of Termination for Convenience", "Provider", "Monitored", "#F59E0B"),
        ("Milestone", "60 Days from Sign", "UAT Final Acceptance Sign-off", "Client", "Upcoming", "#3B82F6"),
        ("Financial", "Quarterly", "Annual Royalty Reconciliation Audit", "Both Parties", "Recurring", "#10B981")
    ]

    for idx, (typ, due, desc, party, stat, col) in enumerate(items):
        y = 6.6 - idx * 0.95
        ax.plot([3.7, 14.8], [y+0.25, y+0.25], color='#334155', lw=0.5)
        row = f"{typ:<12} {due:<19} {desc:<44} {party:<19}"
        ax.text(3.7, y-0.05, row, fontsize=7.5, color='#E2E8F0', fontfamily='monospace')
        # Status pill
        s_pill = patches.FancyBboxPatch((13.7, y-0.18), 1.3, 0.35, boxstyle="round,pad=0.04", fc=col, ec=col)
        ax.add_patch(s_pill)
        ax.text(14.35, y-0.01, stat, ha='center', va='center', fontsize=6.5, fontweight='bold', color='white')

    plt.tight_layout(); plt.savefig('assets/fig_8_13_obligations.png', dpi=300, bbox_inches='tight'); plt.close()
    print('Created assets/fig_8_13_obligations.png')

# 8.14 Multilingual Translation Interface
def fig_8_14():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.axis('off'); ax.set_xlim(0, 16); ax.set_ylim(0, 10)
    create_window_chrome(ax, 'Language Translation')

    ax.text(3.4, 8.6, 'Multilingual Legal Contract Translation', fontsize=12, fontweight='bold', color='#F8FAFC')
    ax.text(3.4, 8.1, 'Preserving legal precision across regional and international languages (Telugu, Hindi, etc.).', fontsize=8.5, color='#94A3B8')

    # Left: English Source
    s_box = patches.FancyBboxPatch((3.4, 1.8), 5.7, 5.9, boxstyle="round,pad=0.1", fc='#1E293B', ec='#334155')
    ax.add_patch(s_box)
    ax.text(3.7, 7.3, 'Source Contract (English - Original)', fontsize=8.5, fontweight='bold', color='#60A5FA')
    ax.text(3.7, 6.7, """Section 2: Payment and Suspension

"Overdue amounts incur interest at three percent
(3%) per month, compounded monthly. Provider
may suspend services if an invoice remains unpaid
for more than ten (10) days. Client shall reimburse
collection costs and legal expenses arising from
delayed payment." """, fontsize=7.5, va='top', fontfamily='monospace', color='#E2E8F0', linespacing=1.3)

    # Right: Target Translation
    t_box = patches.FancyBboxPatch((9.5, 1.8), 5.7, 5.9, boxstyle="round,pad=0.1", fc='#1E293B', ec='#10B981')
    ax.add_patch(t_box)
    ax.text(9.8, 7.3, 'Translated Output (Telugu / Regional)', fontsize=8.5, fontweight='bold', color='#10B981')
    ax.text(9.8, 6.7, """సెక్షన్ 2: చెల్లింపు మరియు సేవల నిలిపివేత

"గడువు ముగిసిన బకాయిలపై నెలకు మూడు శాతం (3%)
చొప్పున చక్రవడ్డీ వర్తిస్తుంది. ఇన్వాయిస్ పది (10)
రోజుల కంటే ఎక్కువ కాలం చెల్లించకుండా ఉంటే,
సేవా ప్రదాత సేవలను నిలిపివేయవచ్చు. ఆలస్య చెల్లింపు
వలన అయ్యే న్యాయ మరియు రికవరీ ఖర్చులను క్లయింట్
చెల్లించవలసి ఉంటుంది." """, fontsize=7.5, va='top', fontfamily='sans-serif', color='#E2E8F0', linespacing=1.3)

    # Download translated PDF / DOCX
    dbtn = patches.FancyBboxPatch((9.5, 1.0), 5.7, 0.6, boxstyle="round,pad=0.05", fc='#2563EB', ec='#3B82F6')
    ax.add_patch(dbtn)
    ax.text(12.35, 1.3, 'Download Translated PDF / DOCX Document', ha='center', va='center', fontsize=8, fontweight='bold', color='white')

    plt.tight_layout(); plt.savefig('assets/fig_8_14_language.png', dpi=300, bbox_inches='tight'); plt.close()
    print('Created assets/fig_8_14_language.png')

# 8.15 User Activity & Audit Log Viewer
def fig_8_15():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.axis('off'); ax.set_xlim(0, 16); ax.set_ylim(0, 10)
    create_window_chrome(ax, 'Activity Logs')

    ax.text(3.4, 8.6, 'Cryptographic Audit Trail & Activity Logs', fontsize=12, fontweight='bold', color='#F8FAFC')
    ax.text(3.4, 8.1, 'Immutable security logging of all contract modifications, scans, and export actions.', fontsize=8.5, color='#94A3B8')

    table = patches.FancyBboxPatch((3.4, 1.0), 11.8, 6.8, boxstyle="round,pad=0.1", fc='#1E293B', ec='#334155')
    ax.add_patch(table)

    header = "Timestamp (UTC)       User Subject         Action Performed                 Method  Path                  Status"
    ax.text(3.7, 7.3, header, fontsize=7.2, fontweight='bold', color='#60A5FA', fontfamily='monospace')

    logs = [
        ("2026-09-29 19:29:44", "akshaya@example.com", "Report downloaded", "GET", "/api/reports/12/pdf", "200 OK"),
        ("2026-09-29 19:29:12", "akshaya@example.com", "Contract analysis requested", "POST", "/api/analysis/12", "200 OK"),
        ("2026-09-29 19:28:50", "akshaya@example.com", "Contract uploaded", "POST", "/api/contracts", "201 Created"),
        ("2026-09-29 19:25:10", "akshaya@example.com", "Contract question asked", "POST", "/api/qa", "200 OK"),
        ("2026-09-29 19:22:04", "akshaya@example.com", "Clause comparison performed", "POST", "/api/clause-comparison/compare", "200 OK"),
        ("2026-09-29 19:20:18", "akshaya@example.com", "Contract version diff checked", "POST", "/api/version-diff/compare", "200 OK")
    ]

    for idx, (ts, usr, act, mth, pth, st) in enumerate(logs):
        y = 6.6 - idx * 0.95
        ax.plot([3.7, 14.8], [y+0.25, y+0.25], color='#334155', lw=0.5)
        row = f"{ts:<21} {usr:<20} {act:<32} {mth:<7} {pth:<21} {st}"
        ax.text(3.7, y-0.05, row, fontsize=7.0, color='#E2E8F0', fontfamily='monospace')

    plt.tight_layout(); plt.savefig('assets/fig_8_15_audit_logs.png', dpi=300, bbox_inches='tight'); plt.close()
    print('Created assets/fig_8_15_audit_logs.png')

# 8.16 Report Generation and Export Interface
def fig_8_16():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.axis('off'); ax.set_xlim(0, 16); ax.set_ylim(0, 10)
    create_window_chrome(ax, 'Reports Export')

    ax.text(3.4, 8.6, 'Export Verifiable Contract Risk Reports', fontsize=12, fontweight='bold', color='#F8FAFC')
    ax.text(3.4, 8.1, 'Generate standardized legal audit dossiers in PDF and Markdown format for stakeholders.', fontsize=8.5, color='#94A3B8')

    # Card
    rcard = patches.FancyBboxPatch((5.0, 1.5), 8.5, 6.2, boxstyle="round,pad=0.2", fc='#1E293B', ec='#334155', lw=1.5)
    ax.add_patch(rcard)

    ax.text(9.25, 7.1, '📑 Contract Risk Analysis Dossier', ha='center', fontsize=11, fontweight='bold', color='#F8FAFC')
    ax.text(9.25, 6.6, 'Target Contract: Contract #12 (Commercial Vendor Agreement)', ha='center', fontsize=8.5, color='#94A3B8')

    # Format options
    p_box = patches.FancyBboxPatch((5.5, 4.4), 3.6, 1.8, boxstyle="round,pad=0.1", fc='#0F172A', ec='#EF4444', lw=1.2)
    ax.add_patch(p_box)
    ax.text(7.3, 5.7, '📕 Formal PDF Report', ha='center', fontsize=9, fontweight='bold', color='#FCA5A5')
    ax.text(7.3, 5.0, 'Includes executive score gauge,\nitemized deductions, clause tables,\nand legal disclaimers.', ha='center', fontsize=7.5, color='#CBD5E1')

    m_box = patches.FancyBboxPatch((9.4, 4.4), 3.6, 1.8, boxstyle="round,pad=0.1", fc='#0F172A', ec='#3B82F6', lw=1.2)
    ax.add_patch(m_box)
    ax.text(11.2, 5.7, '📝 Raw Markdown Report', ha='center', fontsize=9, fontweight='bold', color='#93C5FD')
    ax.text(11.2, 5.0, 'Ideal for developer integration,\nversion control pull request diffs,\nand knowledge bases.', ha='center', fontsize=7.5, color='#CBD5E1')

    # Download Buttons
    btn1 = patches.FancyBboxPatch((5.5, 2.7), 3.6, 0.7, boxstyle="round,pad=0.05", fc='#EF4444', ec='#DC2626')
    ax.add_patch(btn1)
    ax.text(7.3, 3.05, 'Download PDF Dossier', ha='center', va='center', fontsize=8.5, fontweight='bold', color='white')

    btn2 = patches.FancyBboxPatch((9.4, 2.7), 3.6, 0.7, boxstyle="round,pad=0.05", fc='#2563EB', ec='#3B82F6')
    ax.add_patch(btn2)
    ax.text(11.2, 3.05, 'Download Markdown', ha='center', va='center', fontsize=8.5, fontweight='bold', color='white')

    ax.text(9.25, 2.0, '✓ Generated via ReportLab / PyPDF Engine (Cryptographically Audited)', ha='center', fontsize=7.5, color='#10B981')

    plt.tight_layout(); plt.savefig('assets/fig_8_16_report_export.png', dpi=300, bbox_inches='tight'); plt.close()
    print('Created assets/fig_8_8_report_export.png')

# Execute all generators
fig_8_1()
fig_8_2()
fig_8_3()
fig_8_4()
fig_8_5()
fig_8_6()
fig_8_7()
fig_8_8()
fig_8_9()
fig_8_10()
fig_8_11()
fig_8_12()
fig_8_13()
fig_8_14()
fig_8_15()
fig_8_16()
print('All 16 Screenshot figures generated successfully!')
