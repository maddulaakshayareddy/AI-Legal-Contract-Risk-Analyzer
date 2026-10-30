"""
Script to generate all UML, Architecture, Flowchart, DFD, ER diagrams
and application UI screen figures for the AI Legal Contract Risk Analyzer project report.
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw, ImageFont

os.makedirs('assets', exist_ok=True)

# Helper function to style plots
def setup_fig(figsize=(10, 6)):
    fig, ax = plt.subplots(figsize=figsize, dpi=300)
    ax.axis('off')
    return fig, ax

# ==========================================================
# 1. Fig 3.1: Block Diagram of AI Legal Contract Risk Analyzer
# ==========================================================
def create_block_diagram():
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 8.5)

    # Title Box
    ax.text(5.5, 8.1, 'AI LEGAL CONTRACT RISK ANALYZER - BLOCK DIAGRAM', ha='center', va='center', 
            fontsize=12, fontweight='bold', fontfamily='serif')

    # Tier 1: Client Layer
    rect1 = patches.FancyBboxPatch((0.5, 6.4), 10, 1.3, boxstyle="round,pad=0.1", fc='#EBF5FB', ec='#2980B9', lw=1.5)
    ax.add_patch(rect1)
    ax.text(5.5, 7.3, 'Client Layer - React Single Page Application (Vite + Tailwind CSS)', ha='center', va='center', fontsize=10, fontweight='bold', color='#1B4F72')
    ax.text(5.5, 6.75, 'Landing Page  |  Authentication  |  Contract Ingestion  |  Risk Dashboard  |  RAG Chat  |\nClause Comparison  |  Version Diff  |  Obligations Tracker  |  Language Translation  |  Reports', 
            ha='center', va='center', fontsize=8.5, color='#2C3E50')

    # Arrow 1
    ax.annotate('', xy=(5.5, 5.7), xytext=(5.5, 6.4), arrowprops=dict(arrowstyle="<->", color='#2C3E50', lw=1.5))
    ax.text(5.6, 6.05, 'REST API (HTTP / JSON) & Form-Data', fontsize=8, color='#555555')

    # Tier 2: Backend Application Layer
    rect2 = patches.FancyBboxPatch((0.5, 3.8), 10, 1.9, boxstyle="round,pad=0.1", fc='#E8F8F5', ec='#16A085', lw=1.5)
    ax.add_patch(rect2)
    ax.text(5.5, 5.4, 'Application Layer - FastAPI Backend (Python 3.11)', ha='center', va='center', fontsize=10, fontweight='bold', color='#0E6251')
    
    # Sub-boxes in Backend
    boxes_backend = [
        (0.8, 4.0, 1.8, 1.0, 'API Routers\n• Auth & JWT\n• Contracts\n• Analysis\n• QA & Reports', '#A3E4D7'),
        (2.8, 4.0, 1.9, 1.0, 'Document Parser\n• PyPDF2\n• python-docx\n• EasyOCR', '#A3E4D7'),
        (4.9, 4.0, 1.9, 1.0, 'Semantic Engine\n• SentenceTransformer\n• FAISS Index\n• Overlap Chunking', '#A3E4D7'),
        (7.0, 4.0, 1.9, 1.0, 'LLM & Analysis\n• Groq Client\n• JSON Schema Enforcer\n• Risk Scorer', '#A3E4D7'),
        (9.1, 4.0, 1.2, 1.0, 'Utilities\n• Audit\n• Diffing\n• ReportLab', '#A3E4D7'),
    ]
    for bx, by, bw, bh, btxt, bcol in boxes_backend:
        b_rect = patches.FancyBboxPatch((bx, by), bw, bh, boxstyle="round,pad=0.05", fc=bcol, ec='#117864', lw=1)
        ax.add_patch(b_rect)
        ax.text(bx + bw/2, by + bh/2, btxt, ha='center', va='center', fontsize=7.5, color='#0B5345')

    # Arrow 2
    ax.annotate('', xy=(3.0, 2.7), xytext=(3.0, 3.8), arrowprops=dict(arrowstyle="<->", color='#2C3E50', lw=1.5))
    ax.annotate('', xy=(8.0, 2.7), xytext=(8.0, 3.8), arrowprops=dict(arrowstyle="<->", color='#2C3E50', lw=1.5))
    ax.text(2.1, 3.2, 'SQLAlchemy ORM', fontsize=8, color='#555555')
    ax.text(8.1, 3.2, 'HTTPS Inference', fontsize=8, color='#555555')

    # Tier 3: Persistence & External Cloud Layer
    # Data Layer Box
    rect3 = patches.FancyBboxPatch((0.5, 0.8), 5.0, 1.9, boxstyle="round,pad=0.1", fc='#FEF9E7', ec='#F39C12', lw=1.5)
    ax.add_patch(rect3)
    ax.text(3.0, 2.4, 'Data & Persistence Layer', ha='center', va='center', fontsize=9.5, fontweight='bold', color='#7D6608')
    ax.text(3.0, 1.5, '• PostgreSQL / SQLite (Users, Contracts, Analyses, Clauses, Recs, QA)\n• FAISS Vector Store Index (Embeddings cache)\n• Local Filesystem (Uploaded contracts & Generated PDF reports)', ha='center', va='center', fontsize=8, color='#7D6608')

    # External AI Services Box
    rect4 = patches.FancyBboxPatch((6.0, 0.8), 4.5, 1.9, boxstyle="round,pad=0.1", fc='#FDEDEC', ec='#E74C3C', lw=1.5)
    ax.add_patch(rect4)
    ax.text(8.25, 2.4, 'External AI Cloud Services', ha='center', va='center', fontsize=9.5, fontweight='bold', color='#78281F')
    ax.text(8.25, 1.5, '• Groq Cloud API (openai/gpt-oss-120b)\n• Google Gemini API (Multimodal / Fallback)\n• Hugging Face Hub (all-MiniLM-L6-v2 weights)\n• ISO/IEC & Legal Security Standards', ha='center', va='center', fontsize=8, color='#78281F')

    plt.tight_layout()
    plt.savefig('assets/fig_3_1_block_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('Created assets/fig_3_1_block_diagram.png')

# ==========================================================
# 2. Fig 3.2: Flow Chart of the Contract Analysis Workflow
# ==========================================================
def create_flow_chart():
    fig, ax = plt.subplots(figsize=(9, 12), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 14)

    steps = [
        (4.5, 13.3, 'Start: User uploads contract (PDF / DOCX / Image / Text)', 'oval', '#D4EFDF', '#229954'),
        (4.5, 12.0, 'Validate JWT Auth Token & User Permissions', 'rect', '#EBF5FB', '#2980B9'),
        (4.5, 10.7, 'Extract Text (PyPDF2 / python-docx / EasyOCR)', 'rect', '#EBF5FB', '#2980B9'),
        (4.5, 9.4, 'Is extracted text valid & non-empty?', 'diamond', '#FCF3CF', '#F39C12'),
        (4.5, 7.8, 'Chunk text (1200 chars, 200 overlap) & generate\nSentenceTransformer embeddings (all-MiniLM-L6-v2)', 'rect', '#E8F8F5', '#16A085'),
        (4.5, 6.3, 'Construct FAISS Vector Index (IndexFlatIP)', 'rect', '#E8F8F5', '#16A085'),
        (4.5, 4.9, 'Dispatch Groq LLM Inference with Structured JSON Schema\n(gpt-oss-120b, temp=0.1, max_tokens=8000)', 'rect', '#F5EEF8', '#8E44AD'),
        (4.5, 3.4, 'Parse & Validate Response (Risk Score, Flagged Clauses,\nMissing Protections, Actionable Recommendations)', 'rect', '#E8F8F5', '#16A085'),
        (4.5, 1.9, 'Persist Analysis to PostgreSQL & Log Audit Trail', 'rect', '#EBF5FB', '#2980B9'),
        (4.5, 0.6, 'Render Interactive Risk Dashboard & Enable Q&A / PDF Export', 'oval', '#D4EFDF', '#229954'),
    ]

    for x, y, text, shape, fc, ec in steps:
        if shape == 'oval':
            p = patches.FancyBboxPatch((x-2.4, y-0.4), 4.8, 0.8, boxstyle="round,pad=0.3", fc=fc, ec=ec, lw=1.5)
            ax.add_patch(p)
            ax.text(x, y, text, ha='center', va='center', fontsize=8.5, fontweight='bold', color='#196F3D')
        elif shape == 'rect':
            p = patches.FancyBboxPatch((x-2.7, y-0.45), 5.4, 0.9, boxstyle="square,pad=0.15", fc=fc, ec=ec, lw=1.2)
            ax.add_patch(p)
            ax.text(x, y, text, ha='center', va='center', fontsize=8.5, color='#1B4F72')
        elif shape == 'diamond':
            # polygon diamond
            pts = [[x, y+0.6], [x+2.2, y], [x, y-0.6], [x-2.2, y]]
            p = patches.Polygon(pts, closed=True, fc=fc, ec=ec, lw=1.2)
            ax.add_patch(p)
            ax.text(x, y, text, ha='center', va='center', fontsize=8.5, fontweight='bold', color='#7D6608')

    # Draw arrows
    arrows = [
        (13.3-0.4, 12.0+0.45, ''),
        (12.0-0.45, 10.7+0.45, ''),
        (10.7-0.45, 9.4+0.6, ''),
        (9.4-0.6, 7.8+0.45, 'Yes'),
        (7.8-0.45, 6.3+0.45, ''),
        (6.3-0.45, 4.9+0.45, ''),
        (4.9-0.45, 3.4+0.45, ''),
        (3.4-0.45, 1.9+0.45, ''),
        (1.9-0.45, 0.6+0.4, ''),
    ]
    for y1, y2, lbl in arrows:
        ax.annotate('', xy=(4.5, y2), xytext=(4.5, y1), arrowprops=dict(arrowstyle="->", color='#2C3E50', lw=1.5))
        if lbl:
            ax.text(4.7, (y1+y2)/2, lbl, fontsize=8, fontweight='bold', color='#196F3D')

    # Error branch for No
    ax.annotate('', xy=(7.8, 9.4), xytext=(4.5+2.2, 9.4), arrowprops=dict(arrowstyle="-", color='#C0392B', lw=1.5))
    ax.annotate('', xy=(7.8, 10.7), xytext=(7.8, 9.4), arrowprops=dict(arrowstyle="-", color='#C0392B', lw=1.5))
    err_box = patches.FancyBboxPatch((6.8, 10.7), 2.0, 0.8, boxstyle="square,pad=0.1", fc='#FDEDEC', ec='#C0392B', lw=1.2)
    ax.add_patch(err_box)
    ax.text(7.8, 11.1, 'Return Error 400:\nNo readable text', ha='center', va='center', fontsize=8, color='#78281F')
    ax.text(6.85, 9.6, 'No', fontsize=8, fontweight='bold', color='#C0392B')

    plt.tight_layout()
    plt.savefig('assets/fig_3_2_flow_chart.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('Created assets/fig_3_2_flow_chart.png')

# ==========================================================
# 3. Fig 3.3: Algorithm Box
# ==========================================================
def create_algorithm_box():
    fig, ax = plt.subplots(figsize=(9.5, 6.5), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    # Frame
    p = patches.FancyBboxPatch((0.4, 0.4), 9.2, 9.2, boxstyle="square,pad=0.1", fc='#FAFAFA', ec='#2C3E50', lw=1.5)
    ax.add_patch(p)

    title = "ALGORITHM: Hybrid Legal Contract Risk Analysis and Semantic RAG Pipeline"
    ax.text(0.7, 9.1, title, fontsize=10.5, fontweight='bold', fontfamily='serif', color='#1A5276')
    ax.axhline(8.9, 0.05, 0.95, color='#BDC3C7', lw=1)

    algo_text = """Input: Contract document D (PDF / DOCX / Scanned Image / Plaintext), User Query Q (optional)
Output: Structured Contract Analysis A, Overall Risk Score S (0-100), Flagged Clauses C,
        Recommendations R, Retrieved Q&A Answer Ans

1. INGEST & PARSE:
   Extract raw text T from D via PyPDF2 / python-docx or OCR image parser (EasyOCR).
   If length(T) < 50 characters, RAISE ValueError("Unreadable document format").

2. SEMANTIC CHUNKING:
   Split T into overlapping segments chunks = split_into_chunks(T, chunk_size=1200, overlap=200).

3. VECTOR EMBEDDING & INDEXING:
   For each chunk c_i in chunks:
       e_i = SentenceTransformer("all-MiniLM-L6-v2").encode(c_i, normalize=True)
   Construct FAISS L2/Inner-Product index: index = faiss.IndexFlatIP(dimension=384); index.add(E).

4. LLM RISK REASONING & SCHEMA ENFORCEMENT:
   Construct system prompt with legal boundaries and ANALYSIS_SCHEMA constraints.
   Invoke Groq LLM API (model: openai/gpt-oss-120b, temperature: 0.1, max_tokens: 8000).
   Obtain structured JSON containing overall_risk_score, overall_risk_level, summary,
   category_risks[], flagged_clauses[], missing_standard_protections[], recommendations[].

5. SEMANTIC RAG RETRIEVAL (Upon User Inquiry Q):
   q_emb = SentenceTransformer.encode(Q, normalize=True).
   Retrieve top-k chunks: indices, scores = index.search(q_emb, k=5).
   Assemble context = join(chunks[indices]).
   Invoke LLM Q&A generator strictly conditioned on context. Return synthesized answer Ans.

6. PERSISTENCE & AUDIT:
   Store contract metadata, analysis record, individual clauses, recommendations in PostgreSQL.
   Record user action, timestamp, and HTTP status in audit_logs table. Return full analysis to client."""

    ax.text(0.7, 8.5, algo_text, fontsize=8.5, fontfamily='monospace', va='top', linespacing=1.35, color='#2C3E50')

    plt.tight_layout()
    plt.savefig('assets/fig_3_3_algorithm.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('Created assets/fig_3_3_algorithm.png')

# ==========================================================
# 4. Fig 4.2: Use Case Diagram
# ==========================================================
def create_use_case_diagram():
    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    # System boundary box
    sys_box = patches.FancyBboxPatch((2.2, 0.4), 5.6, 9.2, boxstyle="round,pad=0.1", fc='#FDFEFE', ec='#2C3E50', lw=1.5)
    ax.add_patch(sys_box)
    ax.text(5.0, 9.3, 'AI Legal Contract Risk Analyzer System', ha='center', va='center', fontsize=11, fontweight='bold', fontfamily='serif', color='#1B4F72')

    # Actor 1: User (Left)
    ax.plot([0.8, 0.8], [5.0, 5.5], color='#2C3E50', lw=2) # body
    ax.plot([0.5, 1.1], [5.3, 5.3], color='#2C3E50', lw=2) # arms
    ax.plot([0.8, 0.5], [5.0, 4.4], color='#2C3E50', lw=2) # left leg
    ax.plot([0.8, 1.1], [5.0, 4.4], color='#2C3E50', lw=2) # right leg
    head1 = patches.Circle((0.8, 5.75), 0.25, fc='#D6EAF8', ec='#2C3E50', lw=1.5)
    ax.add_patch(head1)
    ax.text(0.8, 4.0, 'User / Legal\nReviewer', ha='center', va='center', fontsize=9, fontweight='bold', color='#1B4F72')

    # Actor 2: Groq / Gemini LLM API (Right)
    ax.plot([9.2, 9.2], [5.0, 5.5], color='#2C3E50', lw=2)
    ax.plot([8.9, 9.5], [5.3, 5.3], color='#2C3E50', lw=2)
    ax.plot([9.2, 8.9], [5.0, 4.4], color='#2C3E50', lw=2)
    ax.plot([9.2, 9.5], [5.0, 4.4], color='#2C3E50', lw=2)
    head2 = patches.Circle((9.2, 5.75), 0.25, fc='#FADBD8', ec='#2C3E50', lw=1.5)
    ax.add_patch(head2)
    ax.text(9.2, 4.0, 'Groq LLM /\nGemini API', ha='center', va='center', fontsize=9, fontweight='bold', color='#78281F')

    use_cases = [
        ('Register / Login (JWT Auth)', 8.6, True, False),
        ('Upload Contract (PDF / DOCX / OCR)', 7.8, True, False),
        ('Run AI Contract Risk Analysis', 7.0, True, True),
        ('View Risk Score & Category Breakdown', 6.2, True, False),
        ('Inspect Flagged Clauses & Revisions', 5.4, True, False),
        ('Review Missing Standard Protections', 4.6, True, False),
        ('Ask Contract Questions (Semantic RAG)', 3.8, True, True),
        ('Compare Clauses Side-by-Side', 3.0, True, False),
        ('Compare Contract Versions (Diff & Risk)', 2.2, True, False),
        ('Extract Dates & Financial Obligations', 1.4, True, True),
        ('Export PDF & Markdown Risk Reports', 0.7, True, False),
    ]

    for uc_text, y_pos, conn_user, conn_llm in use_cases:
        uc_ellipse = patches.FancyBboxPatch((2.6, y_pos-0.25), 4.8, 0.5, boxstyle="round,pad=0.2", fc='#EBF5FB', ec='#3498DB', lw=1.2)
        ax.add_patch(uc_ellipse)
        ax.text(5.0, y_pos, uc_text, ha='center', va='center', fontsize=8, color='#1B4F72')

        if conn_user:
            ax.plot([1.1, 2.6], [5.2, y_pos], color='#7F8C8D', lw=1, ls='-')
        if conn_llm:
            ax.plot([7.4, 8.9], [y_pos, 5.2], color='#E74C3C', lw=1, ls='--')

    plt.tight_layout()
    plt.savefig('assets/fig_4_2_use_case.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('Created assets/fig_4_2_use_case.png')

# ==========================================================
# 5. Fig 4.3: Class Diagram (Core Domain Entities)
# ==========================================================
def create_class_diagram():
    fig, ax = plt.subplots(figsize=(10.5, 7.5), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 8.5)

    ax.text(5.5, 8.2, 'CLASS DIAGRAM (CORE DOMAIN ENTITIES)', ha='center', va='center', fontsize=11, fontweight='bold', fontfamily='serif')

    def draw_class(x, y, w, h, name, attrs, methods):
        # Outer box
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0", fc='#FDFEFE', ec='#2C3E50', lw=1.2)
        ax.add_patch(rect)
        # Header
        h_rect = patches.Rectangle((x, y + h - 0.5), w, 0.5, fc='#2980B9', ec='#2C3E50', lw=1.2)
        ax.add_patch(h_rect)
        ax.text(x + w/2, y + h - 0.25, name, ha='center', va='center', fontsize=8.5, fontweight='bold', color='white')
        # Attributes
        ax.text(x + 0.1, y + h - 0.65, '\n'.join(attrs), fontsize=7.2, va='top', fontfamily='monospace', color='#2C3E50')
        # Divider line
        div_y = y + h - 0.5 - (len(attrs)*0.22 + 0.15)
        ax.axhline(div_y, x/11, (x+w)/11, color='#BDC3C7', lw=0.8)
        # Methods
        ax.text(x + 0.1, div_y - 0.1, '\n'.join(methods), fontsize=7.2, va='top', fontfamily='monospace', color='#2C3E50')

    # 1. User
    draw_class(0.6, 4.6, 2.8, 3.2, 'User', 
               ['+ id: Integer (PK)', '+ full_name: String', '+ email: String (UK)', '+ hashed_password: str', '+ created_at: DateTime'],
               ['+ verify_password()', '+ generate_jwt_token()', '+ reset_password()'])

    # 2. Contract
    draw_class(4.1, 4.6, 2.9, 3.2, 'Contract',
               ['+ id: Integer (PK)', '+ user_id: Integer (FK)', '+ title: String', '+ file_name: String', '+ file_type: String', '+ raw_text: Text', '+ created_at: DateTime'],
               ['+ extract_text()', '+ generate_chunks()', '+ create_embeddings()'])

    # 3. Analysis
    draw_class(7.6, 4.6, 2.8, 3.2, 'Analysis',
               ['+ id: Integer (PK)', '+ contract_id: Int (FK)', '+ overall_risk_score: Int', '+ overall_risk_level: Str', '+ summary: Text', '+ categories_json: Text'],
               ['+ run_analysis()', '+ calculate_score()', '+ export_report()'])

    # 4. Clause
    draw_class(0.6, 0.6, 2.8, 3.3, 'Clause',
               ['+ id: Integer (PK)', '+ contract_id: Int (FK)', '+ analysis_id: Int (FK)', '+ category: String', '+ original_snippet: Text', '+ issue_summary: Text', '+ severity: String', '+ suggested_revision: Text'],
               ['+ get_snippet()', '+ format_diff()'])

    # 5. Recommendation
    draw_class(4.1, 0.6, 2.9, 3.3, 'Recommendation',
               ['+ id: Integer (PK)', '+ contract_id: Int (FK)', '+ analysis_id: Int (FK)', '+ type: String', '+ title: String', '+ description: Text', '+ importance: String'],
               ['+ filter_by_type()', '+ prioritize()'])

    # 6. Question (QA)
    draw_class(7.6, 0.6, 2.8, 3.3, 'Question',
               ['+ id: Integer (PK)', '+ contract_id: Int (FK)', '+ user_id: Integer (FK)', '+ question_text: Text', '+ answer_text: Text', '+ retrieved_snippets: Text', '+ created_at: DateTime'],
               ['+ retrieve_context()', '+ answer_query()'])

    # Connectors
    # User -> Contract (1 to N)
    ax.annotate('', xy=(4.1, 6.2), xytext=(3.4, 6.2), arrowprops=dict(arrowstyle="->", color='#2C3E50', lw=1.2))
    ax.text(3.5, 6.35, '1..*', fontsize=7.5, fontweight='bold')
    ax.text(3.4, 5.95, '1', fontsize=7.5, fontweight='bold')

    # Contract -> Analysis (1 to N)
    ax.annotate('', xy=(7.6, 6.2), xytext=(7.0, 6.2), arrowprops=dict(arrowstyle="->", color='#2C3E50', lw=1.2))
    ax.text(7.1, 6.35, '1..*', fontsize=7.5, fontweight='bold')
    ax.text(7.0, 5.95, '1', fontsize=7.5, fontweight='bold')

    # Analysis -> Clause (1 to N)
    ax.annotate('', xy=(2.0, 3.9), xytext=(7.6, 4.8), arrowprops=dict(arrowstyle="->", color='#2C3E50', lw=1.2))
    # Analysis -> Recommendation (1 to N)
    ax.annotate('', xy=(5.5, 3.9), xytext=(8.0, 4.6), arrowprops=dict(arrowstyle="->", color='#2C3E50', lw=1.2))
    # Contract -> Question (1 to N)
    ax.annotate('', xy=(9.0, 3.9), xytext=(5.5, 4.6), arrowprops=dict(arrowstyle="->", color='#2C3E50', lw=1.2))

    plt.tight_layout()
    plt.savefig('assets/fig_4_3_class_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('Created assets/fig_4_3_class_diagram.png')

# ==========================================================
# 6. Fig 4.4: Activity Diagram
# ==========================================================
def create_activity_diagram():
    fig, ax = plt.subplots(figsize=(8.5, 11), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 8.5)
    ax.set_ylim(0, 13)

    ax.text(4.25, 12.6, 'ACTIVITY DIAGRAM OF CONTRACT RISK ANALYSIS WORKFLOW', ha='center', va='center', fontsize=10.5, fontweight='bold', fontfamily='serif')

    # Initial node
    init = patches.Circle((4.25, 12.0), 0.2, fc='#2C3E50', ec='#2C3E50')
    ax.add_patch(init)

    activities = [
        (4.25, 11.0, 'User logs into system & validates JWT credentials'),
        (4.25, 10.0, 'User uploads contract file (PDF/DOCX/Image) or enters text'),
        (4.25, 9.0, 'Backend parses document and extracts text content'),
        (4.25, 8.0, 'SentenceTransformer chunks text & builds FAISS vector index'),
        (4.25, 7.0, 'Trigger Groq LLM API with contract text & JSON schema constraints'),
        (4.25, 5.8, 'Parallel Extraction:\n• Compute Category Risk Scores & Composite Score\n• Extract Flagged Clauses with Severity & Suggested Revisions\n• Identify Missing Standard Protections & Legal Recommendations'),
        (4.25, 4.4, 'Persist Analysis, Clauses, and Recommendations to Database'),
        (4.25, 3.4, 'Log user activity in Audit Trail'),
        (4.25, 2.2, 'Interactive Exploration:\nUser views Risk Dashboard, queries RAG Q&A,\ncompares clauses/versions, or exports PDF report'),
    ]

    for x, y, txt in activities:
        box = patches.FancyBboxPatch((x-2.7, y-0.35), 5.4, 0.7 if '\n' not in txt else 1.0, boxstyle="round,pad=0.15", fc='#EBF5FB', ec='#2980B9', lw=1.2)
        ax.add_patch(box)
        ax.text(x, y, txt, ha='center', va='center', fontsize=8, color='#1B4F72')

    # Final node
    fin_out = patches.Circle((4.25, 0.9), 0.25, fc='white', ec='#2C3E50', lw=1.5)
    fin_in = patches.Circle((4.25, 0.9), 0.15, fc='#2C3E50', ec='#2C3E50')
    ax.add_patch(fin_out)
    ax.add_patch(fin_in)

    # Connections
    conns = [
        (12.0-0.2, 11.0+0.35),
        (11.0-0.35, 10.0+0.35),
        (10.0-0.35, 9.0+0.35),
        (9.0-0.35, 8.0+0.35),
        (8.0-0.35, 7.0+0.35),
        (7.0-0.35, 5.8+0.5),
        (5.8-0.5, 4.4+0.35),
        (4.4-0.35, 3.4+0.35),
        (3.4-0.35, 2.2+0.5),
        (2.2-0.5, 0.9+0.25),
    ]
    for y1, y2 in conns:
        ax.annotate('', xy=(4.25, y2), xytext=(4.25, y1), arrowprops=dict(arrowstyle="->", color='#2C3E50', lw=1.3))

    plt.tight_layout()
    plt.savefig('assets/fig_4_4_activity_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('Created assets/fig_4_4_activity_diagram.png')

# ==========================================================
# 7. Fig 4.5: Sequence Diagram
# ==========================================================
def create_sequence_diagram():
    fig, ax = plt.subplots(figsize=(10.5, 8.5), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 9.5)

    ax.text(5.25, 9.1, 'SEQUENCE DIAGRAM OF CONTRACT ANALYSIS REQUEST LIFECYCLE', ha='center', va='center', fontsize=11, fontweight='bold', fontfamily='serif')

    lifelines = [
        (1.0, 'User / Client'),
        (2.8, 'FastAPI Router'),
        (4.6, 'DocumentParser'),
        (6.4, 'RAG / FAISS'),
        (8.2, 'Groq LLM API'),
        (9.8, 'Database (PG)'),
    ]

    for lx, lname in lifelines:
        box = patches.FancyBboxPatch((lx-0.7, 8.3), 1.4, 0.5, boxstyle="square,pad=0.1", fc='#EBF5FB', ec='#2980B9', lw=1.2)
        ax.add_patch(box)
        ax.text(lx, 8.55, lname, ha='center', va='center', fontsize=7.5, fontweight='bold', color='#1B4F72')
        ax.plot([lx, lx], [0.8, 8.3], color='#BDC3C7', lw=1, ls='--')

    messages = [
        (1.0, 2.8, 7.8, 'POST /api/contracts (upload PDF)', '->', '#2C3E50'),
        (2.8, 4.6, 7.3, 'extract_text(pdf_path)', '->', '#2980B9'),
        (4.6, 2.8, 6.8, 'raw_text returned', '-->', '#27AE60'),
        (2.8, 9.8, 6.3, 'INSERT into contracts', '->', '#8E44AD'),
        (9.8, 2.8, 5.8, 'contract_id returned', '-->', '#27AE60'),
        (1.0, 2.8, 5.3, 'POST /api/analysis/{id}', '->', '#2C3E50'),
        (2.8, 6.4, 4.8, 'build_faiss_index(chunks)', '->', '#16A085'),
        (6.4, 2.8, 4.3, 'IndexFlatIP ready', '-->', '#27AE60'),
        (2.8, 8.2, 3.8, 'chat.completions(prompt, JSON schema)', '->', '#E74C3C'),
        (8.2, 2.8, 3.1, 'Structured Analysis JSON', '-->', '#27AE60'),
        (2.8, 9.8, 2.5, 'INSERT analyses, clauses, recommendations', '->', '#8E44AD'),
        (9.8, 2.8, 2.0, 'Transaction committed', '-->', '#27AE60'),
        (2.8, 9.8, 1.5, 'AuditLog: "Contract analysis requested"', '->', '#8E44AD'),
        (2.8, 1.0, 1.0, '200 OK: Full Structured Risk Assessment', '-->', '#2980B9'),
    ]

    for x1, x2, y, msg, arrow, col in messages:
        ls = '--' if '-->' in arrow else '-'
        ax.annotate('', xy=(x2, y), xytext=(x1, y), arrowprops=dict(arrowstyle="->", color=col, lw=1.2, ls=ls))
        mid_x = (x1 + x2) / 2
        ax.text(mid_x, y + 0.12, msg, ha='center', va='bottom', fontsize=7.2, color=col)

    plt.tight_layout()
    plt.savefig('assets/fig_4_5_sequence_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('Created assets/fig_4_5_sequence_diagram.png')

# ==========================================================
# 8. Fig 4.6: Level 0 DFD (Context Diagram)
# ==========================================================
def create_level_0_dfd():
    fig, ax = plt.subplots(figsize=(9.5, 6.5), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)

    ax.text(5.0, 7.6, 'DATA FLOW DIAGRAM - LEVEL 0 (CONTEXT DIAGRAM)', ha='center', va='center', fontsize=11, fontweight='bold', fontfamily='serif')

    # External Entity: User (Left)
    u_box = patches.FancyBboxPatch((0.6, 3.2), 2.0, 1.6, boxstyle="square,pad=0.1", fc='#EBF5FB', ec='#2980B9', lw=1.5)
    ax.add_patch(u_box)
    ax.text(1.6, 4.0, 'User / Legal\nReviewer\n[External Entity]', ha='center', va='center', fontsize=9, fontweight='bold', color='#1B4F72')

    # Central Process: 0.0 AI Legal Contract Risk Analyzer
    proc_circle = patches.Circle((5.0, 4.0), 1.5, fc='#E8F8F5', ec='#16A085', lw=2)
    ax.add_patch(proc_circle)
    ax.text(5.0, 4.3, '0.0', ha='center', va='center', fontsize=12, fontweight='bold', color='#0E6251')
    ax.text(5.0, 3.8, 'AI Legal Contract\nRisk Analyzer\nSystem', ha='center', va='center', fontsize=9.5, fontweight='bold', color='#0E6251')

    # External Entity: Groq / Gemini Cloud (Right)
    g_box = patches.FancyBboxPatch((7.4, 3.2), 2.0, 1.6, boxstyle="square,pad=0.1", fc='#FDEDEC', ec='#E74C3C', lw=1.5)
    ax.add_patch(g_box)
    ax.text(8.4, 4.0, 'Groq LLM /\nGemini API\n[External Entity]', ha='center', va='center', fontsize=9, fontweight='bold', color='#78281F')

    # Data flows User <-> Process
    # User -> System: Contract PDF/DOCX, Queries, Credentials
    ax.annotate('', xy=(3.5, 4.4), xytext=(2.6, 4.4), arrowprops=dict(arrowstyle="->", color='#2C3E50', lw=1.3))
    ax.text(3.05, 4.6, 'Contract files, Q&A queries,\nlogin credentials', ha='center', va='bottom', fontsize=7.5, color='#2C3E50')

    # System -> User: Risk reports, summaries, flagged clauses, Q&A answers
    ax.annotate('', xy=(2.6, 3.6), xytext=(3.5, 3.6), arrowprops=dict(arrowstyle="->", color='#2C3E50', lw=1.3))
    ax.text(3.05, 3.25, 'Risk scores, flagged clauses,\nPDF reports, answers', ha='center', va='top', fontsize=7.5, color='#2C3E50')

    # Data flows System <-> Groq/Gemini
    # System -> Groq: Contract prompts, RAG context, JSON schemas
    ax.annotate('', xy=(7.4, 4.4), xytext=(6.5, 4.4), arrowprops=dict(arrowstyle="->", color='#C0392B', lw=1.3))
    ax.text(6.95, 4.6, 'Prompt, contract chunks,\nJSON schema', ha='center', va='bottom', fontsize=7.5, color='#C0392B')

    # Groq -> System: Inferred analysis JSON, synthesized Q&A
    ax.annotate('', xy=(6.5, 3.6), xytext=(7.4, 3.6), arrowprops=dict(arrowstyle="->", color='#27AE60', lw=1.3))
    ax.text(6.95, 3.25, 'Structured analysis JSON,\nsynthesized answers', ha='center', va='top', fontsize=7.5, color='#27AE60')

    plt.tight_layout()
    plt.savefig('assets/fig_4_6_level_0_dfd.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('Created assets/fig_4_6_level_0_dfd.png')

# ==========================================================
# 9. Fig 4.7: Level 1 DFD
# ==========================================================
def create_level_1_dfd():
    fig, ax = plt.subplots(figsize=(10.5, 8.5), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 9.5)

    ax.text(5.5, 9.1, 'DATA FLOW DIAGRAM - LEVEL 1', ha='center', va='center', fontsize=11, fontweight='bold', fontfamily='serif')

    def draw_proc(x, y, num, name):
        p = patches.Circle((x, y), 0.8, fc='#E8F8F5', ec='#16A085', lw=1.5)
        ax.add_patch(p)
        ax.text(x, y+0.25, num, ha='center', va='center', fontsize=9, fontweight='bold', color='#0E6251')
        ax.text(x, y-0.15, name, ha='center', va='center', fontsize=7, fontweight='bold', color='#0E6251')

    def draw_store(x, y, w, h, name):
        ax.plot([x, x+w], [y+h, y+h], color='#7D6608', lw=1.5)
        ax.plot([x, x+w], [y, y], color='#7D6608', lw=1.5)
        ax.fill_between([x, x+w], y, y+h, color='#FEF9E7', alpha=0.9)
        ax.text(x+w/2, y+h/2, name, ha='center', va='center', fontsize=7.5, fontweight='bold', color='#7D6608')

    # Processes
    draw_proc(2.0, 7.5, '1.0', 'User Auth &\nSession Mgmt')
    draw_proc(5.5, 7.5, '2.0', 'Document\nIngestion & Text\nExtraction')
    draw_proc(9.0, 7.5, '3.0', 'Semantic\nChunking &\nFAISS Indexing')
    draw_proc(3.0, 4.0, '4.0', 'Groq LLM Risk\nAnalysis & Schema\nInference')
    draw_proc(8.0, 4.0, '5.0', 'RAG Contextual\nQ&A Q-Answering')
    draw_proc(5.5, 1.5, '6.0', 'Report Engine\n& Audit Trail\nGeneration')

    # Data Stores
    draw_store(0.6, 5.6, 2.0, 0.6, 'D1: Users')
    draw_store(4.5, 5.6, 2.2, 0.6, 'D2: Contracts')
    draw_store(8.2, 5.6, 2.4, 0.6, 'D3: Vector Store (FAISS)')
    draw_store(1.5, 2.5, 2.4, 0.6, 'D4: Analyses & Clauses')
    draw_store(7.5, 2.5, 2.4, 0.6, 'D5: Q&A Questions')
    draw_store(4.5, 0.2, 2.2, 0.5, 'D6: Audit Logs')

    # Arrows
    # 1.0 <-> D1
    ax.annotate('', xy=(1.6, 6.2), xytext=(2.0, 6.7), arrowprops=dict(arrowstyle="->", color='#2C3E50', lw=1))
    # 2.0 -> D2
    ax.annotate('', xy=(5.5, 6.2), xytext=(5.5, 6.7), arrowprops=dict(arrowstyle="->", color='#2C3E50', lw=1))
    # 2.0 -> 3.0
    ax.annotate('', xy=(8.2, 7.5), xytext=(6.3, 7.5), arrowprops=dict(arrowstyle="->", color='#2C3E50', lw=1))
    # 3.0 -> D3
    ax.annotate('', xy=(9.0, 6.2), xytext=(9.0, 6.7), arrowprops=dict(arrowstyle="->", color='#2C3E50', lw=1))
    # D2 -> 4.0
    ax.annotate('', xy=(3.4, 4.7), xytext=(4.7, 5.6), arrowprops=dict(arrowstyle="->", color='#2C3E50', lw=1))
    # 4.0 -> D4
    ax.annotate('', xy=(2.7, 3.1), xytext=(3.0, 3.2), arrowprops=dict(arrowstyle="->", color='#2C3E50', lw=1))
    # D3 -> 5.0
    ax.annotate('', xy=(8.3, 4.8), xytext=(9.0, 5.6), arrowprops=dict(arrowstyle="->", color='#2C3E50', lw=1))
    # 5.0 -> D5
    ax.annotate('', xy=(8.5, 3.1), xytext=(8.2, 3.2), arrowprops=dict(arrowstyle="->", color='#2C3E50', lw=1))
    # D4 -> 6.0
    ax.annotate('', xy=(4.8, 1.8), xytext=(3.5, 2.5), arrowprops=dict(arrowstyle="->", color='#2C3E50', lw=1))
    # 6.0 -> D6
    ax.annotate('', xy=(5.5, 0.7), xytext=(5.5, 0.9), arrowprops=dict(arrowstyle="->", color='#2C3E50', lw=1))

    plt.tight_layout()
    plt.savefig('assets/fig_4_7_level_1_dfd.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('Created assets/fig_4_7_level_1_dfd.png')

# Run all generator functions
create_block_diagram()
create_flow_chart()
create_algorithm_box()
create_use_case_diagram()
create_class_diagram()
create_activity_diagram()
create_sequence_diagram()
create_level_0_dfd()
create_level_1_dfd()
print("All UML & Flow diagrams generated successfully!")
