# Private Knowledge Q&A - PRD

## Problem Statement
Build a full-stack web application called "Private Knowledge Q&A (Mini Workspace)". Users upload text documents, ask questions, and get answers grounded in those documents with source references.

## Architecture
- **Frontend**: React + Shadcn UI + Tailwind CSS + React Router
- **Backend**: FastAPI (Python) with layered architecture (routes/services/models/vectorstore)
- **LLM**: Google Gemini 2.0 Flash (text generation) + Gemini Embedding 001 (embeddings)
- **Vector Store**: FAISS (in-memory + disk persistence)
- **Metadata DB**: MongoDB

## User Personas
- Knowledge workers querying private documents
- Developers seeking quick answers from technical docs
- Teams building internal knowledge bases

## Core Requirements
- Upload .txt files with text chunking and embedding generation
- Semantic search via FAISS vector store
- RAG pipeline: question → embedding → similarity search → context + LLM → answer with sources
- Document management (upload, list, delete)
- System health monitoring (backend, DB, LLM, vectorstore)
- Q&A history (last 5)

## What's Been Implemented (Feb 13, 2026)
- Full backend with FastAPI layered architecture
- Google Gemini integration (embeddings + chat)
- FAISS vector store with persistence
- MongoDB metadata storage
- 4 frontend pages: Home, Upload, Ask, Status
- Swiss-minimal UI with JetBrains Mono + Inter fonts
- All CRUD operations working
- Health monitoring dashboard
- Q&A history tracking

## Prioritized Backlog
### P0 (Complete)
- [x] Document upload with chunking
- [x] Embedding generation
- [x] Similarity search
- [x] RAG pipeline with Gemini
- [x] Source references in answers
- [x] Status page

### P1
- [ ] Support for .pdf and .docx files
- [ ] Authentication / multi-user support
- [ ] Rate limiting middleware

### P2
- [ ] Conversation context (follow-up questions)
- [ ] Document preview/viewer
- [ ] Export Q&A history
- [ ] File size/type validation on frontend before upload
