import fitz

doc = fitz.open('AI_Legal_Contract_Risk_Analyzer_Project_Report.pdf')

def get_arabic_page(search_text):
    for pno in range(11, len(doc)): # Start from page 12 (doc index 11 = Arabic 1)
        text = doc[pno].get_text()
        if search_text.lower() in text.lower():
            return pno - 10 # Arabic page number
    return -1

index_items = [
    ("CHAPTER 1 - INTRODUCTION", "CHAPTER 1 - INTRODUCTION"),
    ("  1.1 MOTIVATION", "1.1 MOTIVATION"),
    ("  1.2 PROBLEM DEFINITION", "1.2 PROBLEM DEFINITION"),
    ("  1.3 OBJECTIVE OF THE PROJECT", "1.3 OBJECTIVE OF THE PROJECT"),
    ("  1.4 ORGANIZATION OF THE REPORT", "1.4 ORGANIZATION OF THE REPORT"),
    ("CHAPTER 2 - LITERATURE REVIEW", "CHAPTER 2 - LITERATURE REVIEW"),
    ("  2.1 RETRIEVAL-AUGMENTED GENERATION (RAG) IN LEGAL NLP", "2.1 RETRIEVAL-AUGMENTED GENERATION"),
    ("  2.2 PRE-TRAINED LEGAL LANGUAGE MODELS (LEGALBERT)", "2.2 PRE-TRAINED LEGAL LANGUAGE MODELS"),
    ("  2.3 CONTRACT UNDERSTANDING DATASETS (CUAD BENCHMARK)", "2.3 CONTRACT UNDERSTANDING DATASETS"),
    ("  2.4 RULE-BASED AND INFORMATION EXTRACTION TOOLKITS (LEXNLP)", "2.4 RULE-BASED AND INFORMATION EXTRACTION"),
    ("  2.5 LARGE LANGUAGE MODELS FOR REASONING AND SYNTHESIS", "2.5 LARGE LANGUAGE MODELS FOR REASONING"),
    ("  2.6 FRAMEWORK ORCHESTRATION & VECTOR INDEXING (LANGCHAIN & FAISS)", "2.6 FRAMEWORK ORCHESTRATION"),
    ("  2.7 RESEARCH GAP", "2.7 RESEARCH GAP"),
    ("CHAPTER 3 - ANALYSIS & METHODOLOGY", "CHAPTER 3 - ANALYSIS & METHODOLOGY"),
    ("  3.1 EXISTING SYSTEM", "3.1 EXISTING SYSTEM"),
    ("  3.2 PROPOSED SYSTEM", "3.2 PROPOSED SYSTEM"),
    ("  3.3 SOFTWARE REQUIREMENT SPECIFICATION", "3.3 SOFTWARE REQUIREMENT SPECIFICATION"),
    ("    3.3.1 Purpose", "3.3.1 Purpose"),
    ("    3.3.2 Scope", "3.3.2 Scope"),
    ("    3.3.3 Overall Description", "3.3.3 Overall Description"),
    ("  3.4 FUNCTIONAL REQUIREMENTS", "3.4 FUNCTIONAL REQUIREMENTS"),
    ("  3.5 NON-FUNCTIONAL REQUIREMENTS", "3.5 NON-FUNCTIONAL REQUIREMENTS"),
    ("  3.6 PROPOSED METHODOLOGY", "3.6 PROPOSED METHODOLOGY"),
    ("  3.7 FLOW CHART", "3.7 FLOW CHART"),
    ("  3.8 ALGORITHM", "3.8 ALGORITHM"),
    ("  3.9 SOFTWARE AND HARDWARE TOOLS & PACKAGES", "3.9 SOFTWARE AND HARDWARE TOOLS"),
    ("CHAPTER 4 - DESIGN", "CHAPTER 4 - DESIGN"),
    ("  4.1 ARCHITECTURAL DIAGRAM", "4.1 ARCHITECTURAL DIAGRAM"),
    ("  4.2 UML DIAGRAMS", "4.2 UML DIAGRAMS"),
    ("    4.2.1 Use Case Diagram", "4.2.1 Use Case Diagram"),
    ("    4.2.2 Class Diagram", "4.2.2 Class Diagram"),
    ("    4.2.3 Activity Diagram", "4.2.3 Activity Diagram"),
    ("    4.2.4 Sequence Diagram", "4.2.4 Sequence Diagram"),
    ("  4.3 DATA FLOW DIAGRAMS", "4.3 DATA FLOW DIAGRAMS"),
    ("    4.3.1 Level 0 DFD", "4.3.1 Level 0 DFD"),
    ("    4.3.2 Level 1 DFD", "4.3.2 Level 1 DFD"),
    ("  4.4 E-R DIAGRAM", "4.4 E-R DIAGRAM"),
    ("CHAPTER 5 - IMPLEMENTATION", "CHAPTER 5 - IMPLEMENTATION"),
    ("  5.1 MODULE DESCRIPTION", "5.1 MODULE DESCRIPTION"),
    ("  5.2 INTRODUCTION TO TECHNOLOGIES USED", "5.2 INTRODUCTION TO TECHNOLOGIES USED"),
    ("  5.3 SAMPLE CODE", "5.3 SAMPLE CODE"),
    ("    5.3.1 Document Ingestion & Text Extraction (document_parser.py)", "5.3.1 Document Ingestion"),
    ("    5.3.2 Semantic Chunking & FAISS Vector Retrieval (rag_service.py)", "5.3.2 Semantic Chunking"),
    ("    5.3.3 Structured JSON Contract Risk Analysis (gemini_service.py)", "5.3.3 Structured JSON"),
    ("    5.3.4 Audit Trail Logging Middleware (main.py)", "5.3.4 Audit Trail Logging"),
    ("    5.4 EXECUTION PROCEDURE", "5.4 EXECUTION PROCEDURE"),
    ("CHAPTER 6 - RESULTS AND DISCUSSION", "CHAPTER 6 - RESULTS AND DISCUSSION"),
    ("  6.1 EXPERIMENTAL EVALUATION AND BENCHMARK RESULTS", "6.1 EXPERIMENTAL EVALUATION"),
    ("    6.1.1 Document Parsing and Ingestion Performance", "6.1.1 Document Parsing"),
    ("    6.1.2 Embedding and FAISS Vector Retrieval Latency", "6.1.2 Embedding and FAISS"),
    ("    6.1.3 LLM Inference and Risk Score Benchmark", "6.1.3 LLM Inference"),
    ("  6.2 REAL-WORLD CONTRACT RISK ANALYSIS CASE STUDY", "6.2 REAL-WORLD CONTRACT RISK"),
    ("  6.3 ADVANCED CONTRACT ANALYSIS MODULE EVALUATION", "6.3 ADVANCED CONTRACT ANALYSIS"),
    ("  6.4 API RESPONSE TIMES", "6.4 API RESPONSE TIMES"),
    ("  6.5 COST ANALYSIS", "6.5 COST ANALYSIS"),
    ("  6.6 USEFULNESS TO SOCIETY", "6.6 USEFULNESS TO SOCIETY"),
    ("  6.7 ENVIRONMENTAL SAFETY", "6.7 ENVIRONMENTAL SAFETY"),
    ("  6.8 DISCUSSION", "6.8 DISCUSSION"),
    ("CHAPTER 7 - TEST CASES", "CHAPTER 7 - TEST CASES"),
    ("CHAPTER 8 - SCREENSHOTS", "CHAPTER 8 - SCREENSHOTS"),
    ("  8.1 LANDING PAGE & HERO DASHBOARD", "8.1 LANDING PAGE"),
    ("  8.2 USER AUTHENTICATION & LOGIN", "8.2 USER AUTHENTICATION"),
    ("  8.3 CONTRACT UPLOAD & DOCUMENT INGESTION", "8.3 CONTRACT UPLOAD"),
    ("  8.4 CONTRACT DETAILS & RAW TEXT PREVIEW", "8.4 CONTRACT DETAILS"),
    ("  8.5 COMPREHENSIVE CONTRACT RISK ASSESSMENT DASHBOARD", "8.5 COMPREHENSIVE CONTRACT RISK"),
    ("  8.6 CATEGORY-WISE RISK BREAKDOWN", "8.6 CATEGORY-WISE RISK"),
    ("  8.7 FLAGGED CLAUSES & REVISION RECOMMENDATIONS", "8.7 FLAGGED CLAUSES"),
    ("  8.8 MISSING STANDARD PROTECTIONS PANEL", "8.8 MISSING STANDARD PROTECTIONS"),
    ("  8.9 ACTIONABLE CONTRACT RECOMMENDATIONS", "8.9 ACTIONABLE CONTRACT RECOMMENDATIONS"),
    ("  8.10 RAG-BASED INTERACTIVE CONTRACT Q&A CHAT", "8.10 RAG-BASED INTERACTIVE"),
    ("  8.11 SIDE-BY-SIDE CLAUSE COMPARISON", "8.11 SIDE-BY-SIDE CLAUSE"),
    ("  8.12 CONTRACT VERSION DIFF & RISK SHIFT", "8.12 CONTRACT VERSION DIFF"),
    ("  8.13 DATES, DEADLINES & OBLIGATIONS TRACKER", "8.13 DATES, DEADLINES"),
    ("  8.14 MULTILINGUAL TRANSLATION INTERFACE", "8.14 MULTILINGUAL TRANSLATION"),
    ("  8.15 USER ACTIVITY & AUDIT LOG VIEWER", "8.15 USER ACTIVITY"),
    ("  8.16 REPORT GENERATION AND EXPORT INTERFACE", "8.16 REPORT GENERATION"),
    ("CHAPTER 9 - CONCLUSION", "CHAPTER 9 - CONCLUSION"),
    ("CHAPTER 10 - FUTURE ENHANCEMENT", "CHAPTER 10 - FUTURE ENHANCEMENT"),
    ("CHAPTER 11 - BIBLIOGRAPHY", "CHAPTER 11 - BIBLIOGRAPHY"),
    ("CHAPTER 12 - APPENDICES", "CHAPTER 12 - APPENDICES"),
    ("  APPENDIX A: SOURCE CODE REPOSITORY STRUCTURE", "APPENDIX A: SOURCE CODE"),
    ("  APPENDIX B: COMPLETE REST API ENDPOINT SPECIFICATION", "APPENDIX B: COMPLETE REST API"),
    ("  APPENDIX C: SAMPLE COMPLETE GENERATED CONTRACT RISK REPORT", "APPENDIX C: SAMPLE COMPLETE"),
    ("  APPENDIX D: BENCHMARK AND TEST EVALUATION SUMMARY", "APPENDIX D: BENCHMARK AND TEST")
]

print("UPDATED_INDEX_DATA = [")
for title, search_term in index_items:
    p = get_arabic_page(search_term)
    print(f'    ("{title}", "{p}"),')
print("]")

fig_items = [
    ("1", "Block diagram of AI Legal Contract Risk Analyzer", "Fig 3.1: Block diagram"),
    ("2", "Flow chart of the contract analysis workflow", "Fig 3.2: Flow chart"),
    ("3", "Hybrid contract risk analysis algorithm", "Fig 3.3: Hybrid contract"),
    ("4", "System Architecture of AI Legal Contract Risk Analyzer", "Fig 4.1: System Architecture"),
    ("5", "Use case diagram of AI Legal Contract Risk Analyzer", "Fig 4.2: Use case diagram"),
    ("6", "Class diagram (core domain entities)", "Fig 4.3: Class diagram"),
    ("7", "Activity diagram of the contract analysis workflow", "Fig 4.4: Activity diagram"),
    ("8", "Sequence diagram of the contract analysis request lifecycle", "Fig 4.5: Sequence diagram"),
    ("9", "Level 0 data flow diagram (context diagram)", "Fig 4.6: Level 0 data flow"),
    ("10", "Level 1 data flow diagram", "Fig 4.7: Level 1 data flow"),
    ("11", "E-R diagram of the AI Legal Contract Risk Analyzer database", "Fig 4.8: E-R diagram"),
    ("12", "AI Legal Contract Risk Analyzer landing page and hero section", "Fig 8.1: AI Legal Contract Risk Analyzer landing page"),
    ("13", "User authentication and JWT login interface", "Fig 8.2: User authentication"),
    ("14", "Contract upload and document ingestion interface", "Fig 8.3: Contract upload"),
    ("15", "Contract details view and raw text preview", "Fig 8.4: Contract details view"),
    ("16", "Comprehensive contract risk assessment dashboard with health score", "Fig 8.5: Comprehensive contract risk"),
    ("17", "Category-wise risk breakdown interface", "Fig 8.6: Category-wise risk"),
    ("18", "Flagged clauses view showing severity ratings and redline revisions", "Fig 8.7: Flagged clauses view"),
    ("19", "Missing standard contractual protections panel", "Fig 8.8: Missing standard contractual"),
    ("20", "Actionable legal negotiation recommendations", "Fig 8.9: Actionable legal negotiation"),
    ("21", "RAG-based interactive contract Q&A chat interface", "Fig 8.10: RAG-based interactive"),
    ("22", "Side-by-side clause comparison tool", "Fig 8.11: Side-by-side clause"),
    ("23", "Contract version diffing and risk shift analysis", "Fig 8.12: Contract version diffing"),
    ("24", "Dates, deadlines, and financial obligations tracker", "Fig 8.13: Dates, deadlines"),
    ("25", "Multilingual contract translation interface", "Fig 8.14: Multilingual contract"),
    ("26", "User activity and cryptographic audit log viewer", "Fig 8.15: User activity"),
    ("27", "Formal PDF and Markdown report export interface", "Fig 8.16: Formal PDF and Markdown"),
]

print("\nUPDATED_FIGURES_DATA = [")
for snum, fname, search_term in fig_items:
    p = get_arabic_page(search_term)
    print(f'    ("{snum}", "{fname}", "{p}"),')
print("]")

tbl_items = [
    ("1", "Comparison of existing contract review approaches", "Table 2.1: Comparison of existing"),
    ("2", "Functional requirements of AI Legal Contract Risk Analyzer", "Table 3.1: Functional requirements"),
    ("3", "Non-functional requirements of the system", "Table 3.2: Non-functional requirements"),
    ("4", "Software tools and packages", "Table 3.3: Software tools"),
    ("5", "Hardware requirements", "Table 3.4: Hardware requirements"),
    ("6", "Implemented backend modules and subsystems", "Table 5.1: Implemented backend modules"),
    ("7", "Technologies used and their specific role in the system", "Table 5.2: Technologies used"),
    ("8", "Document parsing and ingestion benchmark", "Table 6.1: Document parsing"),
    ("9", "SentenceTransformer embedding and FAISS search latency", "Table 6.2: Embedding and FAISS"),
    ("10", "LLM contract risk analysis inference benchmark", "Table 6.3: LLM contract risk"),
    ("11", "Recorded API response times across endpoints", "Table 6.4: Recorded API response"),
    ("12", "Comprehensive functional test cases", "Table 7.1: Comprehensive functional test"),
    ("13", "REST API endpoints specification", "Table 12.1: REST API endpoints"),
    ("14", "Benchmark and evaluation artifacts", "Table 12.2: Benchmark and evaluation")
]

print("\nUPDATED_TABLES_DATA = [")
for snum, tname, search_term in tbl_items:
    p = get_arabic_page(search_term)
    print(f'    ("{snum}", "{tname}", "{p}"),')
print("]")
