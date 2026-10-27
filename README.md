# AI Legal Contract Risk Analyzer

An AI-powered web application that analyzes legal contracts and identifies potential risks, problematic clauses, missing protections, and recommendations.

## Project Overview

The AI Legal Contract Risk Analyzer allows users to upload PDF/DOCX contracts or enter contract text directly. The system extracts the contract content, stores it in PostgreSQL, retrieves relevant sections using Retrieval-Augmented Generation (RAG), and uses Groq LLM AI to generate a structured contract risk analysis.

The application is designed as an educational and informational tool and is not a substitute for professional legal advice.

## Main Features

- User registration and login
- JWT-based authentication
- PostgreSQL database
- Upload PDF and DOCX contracts
- Contract text extraction
- Create contracts directly from text
- View stored contract details
- Semantic document retrieval using SentenceTransformer
- FAISS-based similarity search
- Contract question-answering
- AI-based contract risk analysis
- Overall risk score
- Overall risk level
- Category-wise risk analysis
- Flagged clauses
- Suggested clause revisions
- Missing standard protections
- Recommendations
- Analysis history
- Markdown report generation
- PDF report generation
- Legal disclaimer

## Technology Stack

### Frontend

- React
- Vite
- JavaScript
- HTML
- CSS

### Backend

- Python
- FastAPI
- SQLAlchemy
- JWT Authentication

### Database

- PostgreSQL

### Artificial Intelligence

- Groq API
- SentenceTransformer
- FAISS
- Retrieval-Augmented Generation (RAG)

### Document Processing

- PyPDF2
- python-docx

### Report Generation

- ReportLab
- Markdown

## System Architecture

```text
                     User
                       |
                       v
              React Frontend
                       |
                       v
                 FastAPI API
                       |
       +---------------+---------------+
       |               |               |
       v               v               v
 PostgreSQL      Document Parser       RAG
       |               |               |
       |               v               v
       |          Contract Text   SentenceTransformer
       |                               |
       |                               v
       |                              FAISS
       |                               |
       +---------------+---------------+
                       |
                       v
                  Groq LLM AI
                       |
                       v
             Contract Risk Analysis
                       |
       +---------------+---------------+
       |               |               |
       v               v               v
  Risk Score     Flagged Clauses   Recommendations
                       |
                       v
                  PDF Report