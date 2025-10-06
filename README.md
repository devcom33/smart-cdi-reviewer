# smart-cdi-reviewer

**smart-cdi-reviewer** is an open-source LegalTech tool that automatically checks the compliance of permanent employment contracts (CDI) with the Moroccan Labor Law using natural language processing and large language models.

## Overview

The project aims to help HR professionals, legal consultants, auditors, and employers verify that employment contracts (CDI, CDD, or other types) comply with the Moroccan Labor Code. The system automatically extracts and analyzes clauses from submitted contracts, detects potential legal issues, and generates a structured compliance report with AI-driven insights and references to relevant labor law articles.

## System Architecture

- The system is composed of three main services communicating via RabbitMQ and Redis:
1- Frontend – User interface to upload contracts and visualize reports
2- Backend (Spring Boot) – Handles REST APIs, authentication, and message routing
3- AI Service (FastAPI) – Processes contract text, performs clause analysis, and generates compliance reports using Gemini LLM
- Supporting services:
**Redis** – Caching and temporary data store
**RabbitMQ** – Message broker connecting backend and AI service

## Workflow

1-The user uploads a contract (PDF/DOCX) through the frontend.
2-The backend extracts the text and sends it via RabbitMQ to the AI service.
3-The AI service:
  Splits and indexes the contract
  Retrieves relevant legal clauses
  Calls the Gemini model to analyze compliance
4-Results are stored temporarily in Redis and sent back to the backend.
5-The frontend displays the compliance report with insights and suggestions.


## Screenshots

### Contract Upload

![Contract Upload](./images/upload.png)

### Contract Analysis

![Contract Upload](./images/image_cdi_1.png)

### Compliance Report Example

![Compliance Report](<./images/image_2(1).png>)

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



## Getting Started

### Prerequisites

- Java 17+
- Maven
- Docker (for vector DB / Ollama setup)
- Python 3.10+ (for preprocessing or LangChain pipelines if separate)
- Node.js (optional, if using a frontend)

## Project Structure

```
smart-cdi-reviewer/
├── backend/
│   ├── src/
│   ├── resources/
├── legal-data/               # Moroccan labor law articles and metadata
├── models/                   # LangChain / LLM scripts
├── vector-db/                # Qdrant/FAISS setup
├── docs/                     # Documentation and sample contracts
```

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

## Collaborators

This project is a collaboration between [Hamza](https://github.com/Hamza-Jr) and [Mouad](https://github.com/devcom33).
