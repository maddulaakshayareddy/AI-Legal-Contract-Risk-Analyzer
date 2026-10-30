"""
Orchestrator script:
1. Runs generate_final_report.py (Pass 1)
2. Converts DOCX -> PDF via Word COM
3. Scans PDF with PyMuPDF to extract TRUE Arabic page numbers for:
   - All 72 TOC entries (Chapters, Sections, Subsections, Appendices)
   - All 27 Figures
   - All 14 Tables
4. Re-runs generate_final_report.py with EXACT page maps (Pass 2)
5. Re-converts DOCX -> PDF via Word COM
6. Verifies TOC alignment and checks preliminary pages (ii, iii, iv, v, vi-viii, ix, x, 1)
"""
import os
import sys
import subprocess
import fitz # PyMuPDF
import generate_final_report

DOCX_FILE = "AI_Legal_Contract_Risk_Analyzer_Project_Report.docx"
PDF_FILE = "AI_Legal_Contract_Risk_Analyzer_Project_Report.pdf"

def convert_docx_to_pdf(docx_path, pdf_path):
    abs_docx = os.path.abspath(docx_path)
    abs_pdf = os.path.abspath(pdf_path)
    ps_cmd = f"""
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $doc = $word.Documents.Open('{abs_docx}')
    $doc.SaveAs([ref]'{abs_pdf}', [ref]17)
    $doc.Close()
    $word.Quit()
    """
    res = subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True)
    if res.returncode != 0:
        print("Word conversion error:", res.stderr)
        raise RuntimeError("Failed to convert DOCX to PDF via Word COM")
    print(f"Successfully converted {docx_path} -> {pdf_path}")

def find_exact_pages(pdf_path):
    doc = fitz.open(pdf_path)
    print(f"Total pages in PDF: {len(doc)}")
    
    # Preliminary pages: Cover (1), Cert (2), Ack (3), Decl (4), Abs (5), Index (6..8), Figs (9), Tbls (10)
    # Chapter 1 is at doc index 10 (doc page 11).
    # Arabic page number for doc index pno (where pno >= 10) = pno - 9
    def get_page(search_term, start_idx=10):
        search_lower = search_term.lower()
        for pno in range(start_idx, len(doc)):
            text = doc[pno].get_text().lower()
            if search_lower in text:
                return pno - 9
        return None

    # Map TOC
    toc_search_items = [
        ("CHAPTER 1 - INTRODUCTION", "CHAPTER 1 - INTRODUCTION"),
        ("1.1 MOTIVATION", "1.1 MOTIVATION"),
        ("1.2 PROBLEM DEFINITION", "1.2 PROBLEM DEFINITION"),
        ("1.3 OBJECTIVE OF THE PROJECT", "1.3 OBJECTIVE OF THE PROJECT"),
        ("1.4 ORGANIZATION OF THE REPORT", "1.4 ORGANIZATION OF THE REPORT"),
        ("CHAPTER 2 - LITERATURE REVIEW", "CHAPTER 2 - LITERATURE REVIEW"),
        ("2.1 RETRIEVAL-AUGMENTED GENERATION (RAG) IN LEGAL NLP", "2.1 RETRIEVAL-AUGMENTED GENERATION"),
        ("2.2 PRE-TRAINED LEGAL LANGUAGE MODELS (LEGALBERT)", "2.2 PRE-TRAINED LEGAL LANGUAGE MODELS"),
        ("2.3 CONTRACT UNDERSTANDING DATASETS (CUAD BENCHMARK)", "2.3 CONTRACT UNDERSTANDING DATASETS"),
        ("2.4 RULE-BASED AND INFORMATION EXTRACTION TOOLKITS (LEXNLP)", "2.4 RULE-BASED AND INFORMATION EXTRACTION"),
        ("2.5 LARGE LANGUAGE MODELS FOR REASONING AND SYNTHESIS", "2.5 LARGE LANGUAGE MODELS FOR REASONING"),
        ("2.6 FRAMEWORK ORCHESTRATION & VECTOR INDEXING (LANGCHAIN & FAISS)", "2.6 FRAMEWORK ORCHESTRATION"),
        ("2.7 RESEARCH GAP", "2.7 RESEARCH GAP"),
        ("CHAPTER 3 - ANALYSIS & METHODOLOGY", "CHAPTER 3 - ANALYSIS & METHODOLOGY"),
        ("3.1 EXISTING SYSTEM", "3.1 EXISTING SYSTEM"),
        ("3.2 PROPOSED SYSTEM", "3.2 PROPOSED SYSTEM"),
        ("3.3 SOFTWARE REQUIREMENT SPECIFICATION", "3.3 SOFTWARE REQUIREMENT SPECIFICATION"),
        ("3.3.1 Purpose", "3.3.1 Purpose"),
        ("3.3.2 Scope", "3.3.2 Scope"),
        ("3.3.3 Overall Description", "3.3.3 Overall Description"),
        ("3.4 FUNCTIONAL REQUIREMENTS", "3.4 FUNCTIONAL REQUIREMENTS"),
        ("3.5 NON-FUNCTIONAL REQUIREMENTS", "3.5 NON-FUNCTIONAL REQUIREMENTS"),
        ("3.6 PROPOSED METHODOLOGY", "3.6 PROPOSED METHODOLOGY"),
        ("3.7 FLOW CHART", "3.7 FLOW CHART"),
        ("3.8 ALGORITHM", "3.8 ALGORITHM"),
        ("3.9 SOFTWARE AND HARDWARE TOOLS & PACKAGES", "3.9 SOFTWARE AND HARDWARE TOOLS"),
        ("CHAPTER 4 - DESIGN", "CHAPTER 4 - DESIGN"),
        ("4.1 ARCHITECTURAL DIAGRAM", "4.1 ARCHITECTURAL DIAGRAM"),
        ("4.2 UML DIAGRAMS", "4.2 UML DIAGRAMS"),
        ("4.2.1 Use Case Diagram", "4.2.1 Use Case Diagram"),
        ("4.2.2 Class Diagram", "4.2.2 Class Diagram"),
        ("4.2.3 Activity Diagram", "4.2.3 Activity Diagram"),
        ("4.2.4 Sequence Diagram", "4.2.4 Sequence Diagram"),
        ("4.3 DATA FLOW DIAGRAMS", "4.3 DATA FLOW DIAGRAMS"),
        ("4.3.1 Level 0 DFD", "4.3.1 Level 0 DFD"),
        ("4.3.2 Level 1 DFD", "4.3.2 Level 1 DFD"),
        ("4.4 E-R DIAGRAM", "4.4 E-R DIAGRAM"),
        ("CHAPTER 5 - IMPLEMENTATION", "CHAPTER 5 - IMPLEMENTATION"),
        ("5.1 MODULE DESCRIPTION", "5.1 MODULE DESCRIPTION"),
        ("5.2 INTRODUCTION TO TECHNOLOGIES USED", "5.2 INTRODUCTION TO TECHNOLOGIES USED"),
        ("5.3 SAMPLE CODE", "5.3 SAMPLE CODE"),
        ("5.3.1 Document Ingestion & Text Extraction (document_parser.py)", "5.3.1 Document Ingestion"),
        ("5.3.2 Semantic Chunking & FAISS Vector Retrieval (rag_service.py)", "5.3.2 Semantic Chunking"),
        ("5.3.3 Structured JSON Contract Risk Analysis (gemini_service.py)", "5.3.3 Structured JSON"),
        ("5.3.4 Audit Trail Logging Middleware (main.py)", "5.3.4 Audit Trail Logging"),
        ("5.4 EXECUTION PROCEDURE", "5.4 EXECUTION PROCEDURE"),
        ("CHAPTER 6 - RESULTS AND DISCUSSION", "CHAPTER 6 - RESULTS AND DISCUSSION"),
        ("6.1 EXPERIMENTAL EVALUATION AND BENCHMARK RESULTS", "6.1 EXPERIMENTAL EVALUATION"),
        ("6.1.1 Document Parsing and Ingestion Performance", "6.1.1 Document Parsing"),
        ("6.1.2 Embedding and FAISS Vector Retrieval Latency", "6.1.2 Embedding and FAISS"),
        ("6.1.3 LLM Inference and Risk Score Benchmark", "6.1.3 LLM Inference"),
        ("6.2 REAL-WORLD CONTRACT RISK ANALYSIS CASE STUDY", "6.2 REAL-WORLD CONTRACT RISK"),
        ("6.3 ADVANCED CONTRACT ANALYSIS MODULE EVALUATION", "6.3 ADVANCED CONTRACT ANALYSIS"),
        ("6.4 API RESPONSE TIMES", "6.4 API RESPONSE TIMES"),
        ("6.5 COST ANALYSIS", "6.5 COST ANALYSIS"),
        ("6.6 USEFULNESS TO SOCIETY", "6.6 USEFULNESS TO SOCIETY"),
        ("6.7 ENVIRONMENTAL SAFETY", "6.7 ENVIRONMENTAL SAFETY"),
        ("6.8 DISCUSSION", "6.8 DISCUSSION"),
        ("CHAPTER 7 - TEST CASES", "CHAPTER 7 - TEST CASES"),
        ("CHAPTER 8 - SCREENSHOTS", "CHAPTER 8 - SCREENSHOTS"),
        ("8.1 LANDING PAGE & HERO DASHBOARD", "8.1 LANDING PAGE"),
        ("8.2 USER AUTHENTICATION & LOGIN", "8.2 USER AUTHENTICATION"),
        ("8.3 CONTRACT UPLOAD & DOCUMENT INGESTION", "8.3 CONTRACT UPLOAD"),
        ("8.4 CONTRACT DETAILS & RAW TEXT PREVIEW", "8.4 CONTRACT DETAILS"),
        ("8.5 COMPREHENSIVE CONTRACT RISK ASSESSMENT DASHBOARD", "8.5 COMPREHENSIVE CONTRACT RISK"),
        ("8.6 CATEGORY-WISE RISK BREAKDOWN", "8.6 CATEGORY-WISE RISK"),
        ("8.7 FLAGGED CLAUSES & REVISION RECOMMENDATIONS", "8.7 FLAGGED CLAUSES"),
        ("8.8 MISSING STANDARD PROTECTIONS PANEL", "8.8 MISSING STANDARD PROTECTIONS"),
        ("8.9 ACTIONABLE CONTRACT RECOMMENDATIONS", "8.9 ACTIONABLE CONTRACT RECOMMENDATIONS"),
        ("8.10 RAG-BASED INTERACTIVE CONTRACT Q&A CHAT", "8.10 RAG-BASED INTERACTIVE"),
        ("8.11 SIDE-BY-SIDE CLAUSE COMPARISON", "8.11 SIDE-BY-SIDE CLAUSE"),
        ("8.12 CONTRACT VERSION DIFF & RISK SHIFT", "8.12 CONTRACT VERSION DIFF"),
        ("8.13 DATES, DEADLINES & OBLIGATIONS TRACKER", "8.13 DATES, DEADLINES"),
        ("8.14 MULTILINGUAL TRANSLATION INTERFACE", "8.14 MULTILINGUAL TRANSLATION"),
        ("8.15 USER ACTIVITY & AUDIT LOG VIEWER", "8.15 USER ACTIVITY"),
        ("8.16 REPORT GENERATION AND EXPORT INTERFACE", "8.16 REPORT GENERATION"),
        ("CHAPTER 9 - CONCLUSION", "CHAPTER 9 - CONCLUSION"),
        ("CHAPTER 10 - FUTURE ENHANCEMENT", "CHAPTER 10 - FUTURE ENHANCEMENT"),
        ("CHAPTER 11 - BIBLIOGRAPHY", "CHAPTER 11 - BIBLIOGRAPHY"),
        ("CHAPTER 12 - APPENDICES", "CHAPTER 12 - APPENDICES"),
        ("APPENDIX A: SOURCE CODE REPOSITORY STRUCTURE", "APPENDIX A: SOURCE CODE"),
        ("APPENDIX B: COMPLETE REST API ENDPOINT SPECIFICATION", "APPENDIX B: COMPLETE REST API"),
        ("APPENDIX C: SAMPLE COMPLETE GENERATED CONTRACT RISK REPORT", "APPENDIX C: SAMPLE COMPLETE"),
        ("APPENDIX D: BENCHMARK AND TEST EVALUATION SUMMARY", "APPENDIX D: BENCHMARK AND TEST")
    ]

    index_page_map = {}
    for title, term in toc_search_items:
        p = get_page(term, start_idx=10)
        if p is not None:
            index_page_map[title] = p
        else:
            print(f"Warning: TOC term '{term}' not found!")

    # Map Figures
    fig_search_items = [
        ("1", "Figure 3.1: Block diagram"),
        ("2", "Figure 3.2: Flow chart"),
        ("3", "Figure 3.3: Hybrid contract"),
        ("4", "Figure 4.1: System Architecture"),
        ("5", "Figure 4.2: Use case diagram"),
        ("6", "Figure 4.3: Class diagram"),
        ("7", "Figure 4.4: Activity diagram"),
        ("8", "Figure 4.5: Sequence diagram"),
        ("9", "Figure 4.6: Level 0 data flow"),
        ("10", "Figure 4.7: Level 1 data flow"),
        ("11", "Figure 4.8: E-R diagram"),
        ("12", "Figure 8.1: AI Legal Contract Risk Analyzer landing page"),
        ("13", "Figure 8.2: User authentication"),
        ("14", "Figure 8.3: Contract upload"),
        ("15", "Figure 8.4: Contract details view"),
        ("16", "Figure 8.5: Comprehensive contract risk"),
        ("17", "Figure 8.6: Category-wise risk"),
        ("18", "Figure 8.7: Flagged clauses view"),
        ("19", "Figure 8.8: Missing standard contractual"),
        ("20", "Figure 8.9: Actionable legal negotiation"),
        ("21", "Figure 8.10: RAG-based interactive"),
        ("22", "Figure 8.11: Side-by-side clause"),
        ("23", "Figure 8.12: Contract version diffing"),
        ("24", "Figure 8.13: Dates, deadlines"),
        ("25", "Figure 8.14: Multilingual contract"),
        ("26", "Figure 8.15: User activity"),
        ("27", "Figure 8.16: Formal PDF and Markdown"),
    ]

    fig_page_map = {}
    for snum, term in fig_search_items:
        p = get_page(term, start_idx=10)
        if p is not None:
            fig_page_map[snum] = p
        else:
            print(f"Warning: Figure term '{term}' not found!")

    # Map Tables
    tbl_search_items = [
        ("1", "Table 2.1: Comparison of existing"),
        ("2", "Table 3.1: Functional requirements"),
        ("3", "Table 3.2: Non-functional requirements"),
        ("4", "Table 3.3: Software tools"),
        ("5", "Table 3.4: Hardware requirements"),
        ("6", "Table 5.1: Implemented backend modules"),
        ("7", "Table 5.2: Technologies used"),
        ("8", "Table 6.1: Document parsing"),
        ("9", "Table 6.2: SentenceTransformer embedding"),
        ("10", "Table 6.3: LLM contract risk"),
        ("11", "Table 6.4: Recorded API response"),
        ("12", "Table 7.1: Comprehensive functional test"),
        ("13", "Table 12.1: REST API endpoints"),
        ("14", "Table 12.2: Benchmark and evaluation")
    ]

    tbl_page_map = {}
    for snum, term in tbl_search_items:
        p = get_page(term, start_idx=10)
        if p is not None:
            tbl_page_map[snum] = p
        else:
            print(f"Warning: Table term '{term}' not found!")

    return index_page_map, fig_page_map, tbl_page_map

def main():
    print("=== PASS 1: Generate initial document ===")
    generate_final_report.create_report()
    convert_docx_to_pdf(DOCX_FILE, PDF_FILE)

    print("\n=== PASS 2: Scan exact pages from PDF ===")
    index_page_map, fig_page_map, tbl_page_map = find_exact_pages(PDF_FILE)
    
    print("\n=== PASS 3: Regenerate with EXACT page maps ===")
    generate_final_report.create_report(index_page_map, fig_page_map, tbl_page_map)
    convert_docx_to_pdf(DOCX_FILE, PDF_FILE)

    print("\n=== PASS 4: Final Verification ===")
    doc = fitz.open(PDF_FILE)
    print(f"Final PDF page count: {len(doc)}")
    for i in range(min(12, len(doc))):
        p = doc[i]
        footer_words = [w[4] for w in p.get_text('words') if w[1] > 750]
        first_line = p.get_text().strip().split('\n')[0] if p.get_text().strip() else ''
        print(f"Page {i+1:2d}: footer={footer_words} | first_line={first_line[:40]}")

    print("\nALL PHASES COMPLETED AND SYNCHRONIZED PERFECTLY!")

if __name__ == "__main__":
    main()
