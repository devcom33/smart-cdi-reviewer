# smart-cdi-reviewer

**smart-cdi-reviewer** is an open-source LegalTech tool that automatically checks the compliance of permanent employment contracts (CDI) with the Moroccan Labor Law using natural language processing and large language models.

## Overview

The project aims to help HR professionals, legal consultants, and auditors verify that a CDI contract complies with the Moroccan Labor Code. The system extracts clauses from a submitted contract and generates a structured compliance report referencing relevant legal articles.

## Features

- Upload CDI contracts in PDF or DOCX formats
- Automatically extract and analyze contract clauses
- Compare contract content with Moroccan Labor Code
- Generate a compliance report with suggested improvements
- Local LLM integration for private and secure analysis
- Role-based access and secure authentication (JWT)

## Technology Stack

- **LangChain + Ollama** (Local LLMs like Mistral, LLaMA3)
- **Spring Boot** (RESTful backend services)
- **PDF/DOCX Parsing** (Apache POI, PDFBox)
- **Vector Database** (FAISS or Qdrant)
- **Authentication**: JWT, Spring Security
- **Database**: PostgreSQL or MongoDB

## Architecture

1. User uploads a contract
2. Document parser extracts text and clauses
3. Relevant clauses are matched with articles using a vector store
4. LLM evaluates compliance and generates a report
5. The report is returned via API (or frontend interface)

## Getting Started

### Prerequisites

- Java 17+
- Maven
- Docker (for vector DB / Ollama setup)
- Python 3.10+ (for preprocessing or LangChain pipelines if separate)
- Node.js (optional, if using a frontend)

## Project Structure
smart-cdi-reviewer/
├── backend/
│   ├── src/
│   ├── resources/
├── legal-data/               # Moroccan labor law articles and metadata
├── models/                   # LangChain / LLM scripts
├── vector-db/                # Qdrant/FAISS setup
├── docs/                     # Documentation and sample contracts

## Tasks and Roadmap
### Phase 1: Legal & Functional Analysis
Collect Moroccan labor law articles relevant to CDI
Define mandatory and optional contract clauses
Prepare sample contracts (compliant/non-compliant)

### Phase 2: Core Backend
Spring Boot project setup
PDF/DOCX clause extraction module
REST API to upload and process contracts
JWT-based auth and role management

### Phase 3: AI Compliance Engine
Setup and test local LLM (via Ollama)
Create LangChain RAG pipeline
Index legal articles into vector DB
Match clauses to relevant laws
Generate structured compliance report

### Phase 4: Security & Deployment
Dockerize services
CI/CD pipeline (GitHub Actions or GitLab CI)
Deploy to local or cloud environment

### Frontend UI
Simple upload form and report viewer
Authentication portal
