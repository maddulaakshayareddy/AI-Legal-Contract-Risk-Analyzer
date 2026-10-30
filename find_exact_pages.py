import fitz

doc = fitz.open('AI_Legal_Contract_Risk_Analyzer_Project_Report.pdf')

# Doc Page 12 is Arabic Page 1.
# So Arabic Page = pno - 10 (since pno is 0-indexed: pno=11 -> page 1).

headings = [
    'CHAPTER 1 - INTRODUCTION',
    '1.1 MOTIVATION',
    '1.2 PROBLEM DEFINITION',
    '1.3 OBJECTIVE OF THE PROJECT',
    '1.4 ORGANIZATION OF THE REPORT',
    'CHAPTER 2 - LITERATURE REVIEW',
    '2.1 RETRIEVAL-AUGMENTED GENERATION',
    '2.2 PRE-TRAINED LEGAL LANGUAGE MODELS',
    '2.3 CONTRACT UNDERSTANDING DATASETS',
    '2.4 RULE-BASED AND INFORMATION EXTRACTION',
    '2.5 LARGE LANGUAGE MODELS FOR REASONING',
    '2.6 FRAMEWORK ORCHESTRATION',
    '2.7 RESEARCH GAP',
    'CHAPTER 3 - ANALYSIS & METHODOLOGY',
    '3.1 EXISTING SYSTEM',
    '3.2 PROPOSED SYSTEM',
    '3.3 SOFTWARE REQUIREMENT SPECIFICATION',
    '3.3.1 Purpose',
    '3.3.2 Scope',
    '3.3.3 Overall Description',
    '3.4 FUNCTIONAL REQUIREMENTS',
    '3.5 NON-FUNCTIONAL REQUIREMENTS',
    '3.6 PROPOSED METHODOLOGY',
    '3.7 FLOW CHART',
    '3.8 ALGORITHM',
    '3.9 SOFTWARE AND HARDWARE TOOLS',
    'CHAPTER 4 - DESIGN',
    '4.1 ARCHITECTURAL DIAGRAM',
    '4.2 UML DIAGRAMS',
    '4.2.1 Use Case Diagram',
    '4.2.2 Class Diagram',
    '4.2.3 Activity Diagram',
    '4.2.4 Sequence Diagram',
    '4.3 DATA FLOW DIAGRAMS',
    '4.3.1 Level 0 DFD',
    '4.3.2 Level 1 DFD',
    '4.4 E-R DIAGRAM',
    'CHAPTER 5 - IMPLEMENTATION',
    '5.1 MODULE DESCRIPTION',
    '5.2 INTRODUCTION TO TECHNOLOGIES USED',
    '5.3 SAMPLE CODE',
    '5.3.1 Document Ingestion',
    '5.3.2 Semantic Chunking',
    '5.3.3 Structured JSON Contract Risk Analysis',
    '5.3.4 Audit Trail Logging Middleware',
    '5.3.5 Automated PDF Report Generation',
    '5.4 EXECUTION PROCEDURE',
    'CHAPTER 6 - RESULTS AND DISCUSSION',
    '6.1 EXPERIMENTAL EVALUATION',
    '6.1.1 Document Parsing',
    '6.1.2 Embedding and FAISS Vector Retrieval',
    '6.1.3 LLM Inference and Risk Score Benchmark',
    '6.2 REAL-WORLD CONTRACT RISK ANALYSIS CASE STUDY',
    '6.3 ADVANCED CONTRACT ANALYSIS MODULE EVALUATION',
    '6.4 MULTI-LINGUAL CONTRACT TRANSLATION OUTCOMES',
    '6.5 API RESPONSE TIMES',
    '6.6 COST ANALYSIS',
    '6.7 USEFULNESS TO SOCIETY',
    '6.8 ENVIRONMENTAL SAFETY',
    '6.9 DISCUSSION',
    'CHAPTER 7 - TEST CASES',
    'CHAPTER 8 - SCREENSHOTS',
    '8.1 LANDING PAGE',
    '8.2 USER AUTHENTICATION',
    '8.3 CONTRACT UPLOAD',
    '8.4 CONTRACT DETAILS',
    '8.5 COMPREHENSIVE CONTRACT RISK ASSESSMENT',
    '8.6 CATEGORY-WISE RISK BREAKDOWN',
    '8.7 FLAGGED CLAUSES',
    '8.8 MISSING STANDARD PROTECTIONS PANEL',
    '8.9 ACTIONABLE CONTRACT RECOMMENDATIONS',
    '8.10 RAG-BASED INTERACTIVE CONTRACT Q&A CHAT',
    '8.11 SIDE-BY-SIDE CLAUSE COMPARISON',
    '8.12 CONTRACT VERSION DIFF',
    '8.13 DATES, DEADLINES',
    '8.14 MULTILINGUAL TRANSLATION',
    '8.15 USER ACTIVITY & AUDIT LOG VIEWER',
    '8.16 REPORT GENERATION AND EXPORT',
    'CHAPTER 9 - CONCLUSION',
    'CHAPTER 10 - FUTURE ENHANCEMENT',
    'CHAPTER 11 - BIBLIOGRAPHY',
    'CHAPTER 12 - APPENDICES',
    'APPENDIX A: SOURCE CODE REPOSITORY STRUCTURE',
    'APPENDIX B: COMPLETE REST API ENDPOINT SPECIFICATION',
    'APPENDIX C: SAMPLE COMPLETE GENERATED CONTRACT RISK REPORT',
    'APPENDIX D: BENCHMARK AND TEST EVALUATION SUMMARY'
]

print("--- TRUE HEADING PAGE NUMBERS (MAIN BODY) ---")
for h in headings:
    found = False
    for pno in range(11, len(doc)): # Start from page 12 (pno 11)
        text = doc[pno].get_text()
        if h.lower() in text.lower():
            arabic_page = pno - 10
            print(f"'{h}': {arabic_page},")
            found = True
            break
    if not found:
        print(f"'{h}': NOT FOUND,")

print("\n--- FIGURE CAPTIONS (MAIN BODY) ---")
for f_idx in range(1, 28):
    for pno in range(11, len(doc)):
        text = doc[pno].get_text()
        if f"Fig {f_idx}." in text or f"Fig {f_idx}:" in text or f"Figure {f_idx}" in text:
            arabic_page = pno - 10
            print(f"Fig {f_idx}: {arabic_page},")
            break

print("\n--- TABLE CAPTIONS (MAIN BODY) ---")
for t_idx in range(1, 14):
    for pno in range(11, len(doc)):
        text = doc[pno].get_text()
        if f"Table {t_idx}." in text or f"Table {t_idx}:" in text:
            arabic_page = pno - 10
            print(f"Table {t_idx}: {arabic_page},")
            break
