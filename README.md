# smart-cdi-reviewer

**smart-cdi-reviewer** is an open-source LegalTech tool that automatically checks the compliance of permanent employment contracts (CDI) with the Moroccan Labor Law using natural language processing and large language models.

## Overview

The project aims to help HR professionals, legal consultants, auditors, and employers verify that employment contracts (CDI, CDD, or other types) comply with the Moroccan Labor Code. The system automatically extracts and analyzes clauses from submitted contracts, detects potential legal issues, and generates a structured compliance report with AI-driven insights and references to relevant labor law articles.

# Contract Compliance System

## System Architecture

The system consists of three main services that communicate via RabbitMQ and Redis.

### Main Services
1. **Frontend**  
   - User interface for uploading contracts and visualizing reports.

2. **Backend (Spring Boot)**  
   - Handles REST APIs, authentication, and message routing.

3. **AI Service (FastAPI)**  
   - Processes contract text, performs clause analysis, and generates compliance reports using the **Gemini LLM**.

### Supporting Services
- **Redis** – Caching and temporary data storage.  
- **RabbitMQ** – Message broker connecting the backend and AI service.  

---

## Workflow

1. The user uploads a contract (PDF or DOCX) through the frontend.  
2. The backend extracts the text and sends it via RabbitMQ to the AI service.  
3. The AI service:  
   - Splits and indexes the contract.  
   - Retrieves relevant legal clauses.  
   - Calls the **Gemini** model to analyze compliance.  
4. Results are temporarily stored in Redis and sent back to the backend.  
5. The frontend displays the compliance report with insights and suggestions.


## Screenshots

### Contract Upload

![Contract Upload](./images/upload.png)

### Contract Analysis

![Contract Upload](./images/image_cdi_1.png)

### Compliance Report Example

![Compliance Report](<./images/image_2(1).png>)

## Features

- Upload and analyze CDI, CDD, or other employment contracts
- AI-powered clause analysis with Google Gemini
- Automatic detection of non-compliant clauses
- Structured compliance report with issue explanations and suggestions
- Scalable microservice architecture (Docker-based)
- Asynchronous task processing via RabbitMQ
- Result caching via Redis
- Secure backend with Spring Boot and role-based auth

## Technology Stack

- Frontend: Built with React, Vite, TypeScript, and Tailwind CSS, providing a modern, fast, and responsive interface for uploading and reviewing employment contracts.
- Backend (API Gateway): Developed using Spring Boot and Java 17, exposing REST APIs that handle authentication, user management, and communication with the AI service.
- AI Service: Implemented with FastAPI and Python 3.10+, using LangChain and Google Gemini API to analyze contract clauses and assess compliance with Moroccan labor laws.
- Message Broker: RabbitMQ is used to manage asynchronous communication between the main backend and the AI service through background workers.
- Cache / Temporary Store: Redis stores intermediate AI results and enables real-time updates during contract processing.
- Containerization: Entire system runs in Docker and Docker Compose, making it easy to deploy and scale in local or cloud environments.
- Data & Storage: Contract data, extracted clauses, and generated reports are stored as JSON files in a structured directory under legal-data/.
- Environment Management: Configuration and API keys are securely managed using python-dotenv and Spring Boot’s configuration system.
- Testing: Pytest (for AI microservice) and JUnit (for backend) ensure robustness and maintainability through automated tests.
- Version Control & CI/CD: Managed via Git and GitHub Actions (planned) to automate builds, testing, and deployment pipelines.



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
│
├── backend/                 # Spring Boot backend (REST API, authentication, business logic)
├── frontend/                # React + Vite frontend (UI for uploading and viewing reports)
├── ai-service/              # Python AI microservice (LLM contract analysis)
├── legal-data/              # Labor law articles and references for compliance checks
├── docker-compose.yml       # Multi-service setup (backend, frontend, AI, Redis, RabbitMQ)
├── README.md
├── LICENSE
└── .gitignore
```

## Tasks and Roadmap

Roadmap
###  Phase 1 — Core Infrastructure

Setup microservices (frontend, backend, AI, Redis, RabbitMQ)

Implement asynchronous task flow (RabbitMQ → AI → Redis → Backend)

### Phase 2 — AI Contract Analysis

Develop LangChain + Gemini workflow for contract compliance

Build full pipeline (splitter → retriever → generation)

### Phase 3 — Frontend Enhancements

Add interactive compliance report visualization

Support multi-language UI (FR / EN)

### Phase 4 — Security & Deployment

Implement JWT-based authentication

CI/CD setup (GitHub Actions)

Deploy to cloud (Render, GCP, or AWS)
### Frontend UI

Simple upload form and report viewer
Authentication portal

## Collaborators

This project is a collaboration between [Hamza](https://github.com/Hamza-Jr) and [Mouad](https://github.com/devcom33).
