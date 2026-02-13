# Prompts Used During Development

This document tracks the major prompts I used with AI tools during the development of this application.

## Initial Setup

### Prompt 1: Project Structure
```
Create a full-stack project structure for a RAG-based Q&A application using:
- Backend: Python FastAPI with layered architecture
- Frontend: React with Shadcn UI
- Vector Store: FAISS
- Database: MongoDB
- LLM: Google Gemini

Include folders for routes, services, models, and utils.
```

### Prompt 2: Backend Architecture
```
Design a FastAPI backend with clean separation of concerns:
- routes/ for API endpoints
- services/ for business logic (document processing, embeddings, Q&A)
- models/ for Pydantic schemas
- vectorstore/ for FAISS management
- Include proper error handling, logging, and CORS setup
```

## Backend Development

### Prompt 3: Document Upload Service
```
Create a document upload service that:
1. Accepts .txt files via FastAPI
2. Validates UTF-8 encoding
3. Chunks text into 500-char segments with 100-char overlap
4. Generates embeddings using Google Gemini
5. Stores vectors in FAISS
6. Saves metadata to MongoDB
Include error handling for invalid files and encoding issues.
```

### Prompt 4: RAG Pipeline
```
Implement a RAG pipeline for question answering:
1. Embed user question with Gemini
2. Search FAISS for top-5 similar chunks
3. Build a grounded prompt with retrieved context
4. Generate answer with Gemini
5. Return answer with source citations (document name, chunk index, similarity score)
6. Store Q&A in MongoDB history
```

### Prompt 5: FAISS Vector Store
```
Create a FAISS vector store manager that:
- Maintains an in-memory IndexFlatL2 index
- Persists to disk (faiss_index.bin + metadata.json)
- Supports add, search, and delete by document ID
- Handles index rebuilding after deletions
- Loads from disk on startup
```

### Prompt 6: Health Check Endpoint
```
Create a status/health endpoint that checks:
- Backend API status
- MongoDB connection
- Gemini API availability (with model info)
- FAISS vector count
Return structured JSON with status, message, and optional model field.
```

## Frontend Development

### Prompt 7: React Router Setup
```
Set up React Router with these pages:
- HomePage: Dashboard showing docs and recent Q&A
- UploadPage: Drag-and-drop for .txt files
- AskPage: Question input with answer and sources display
- StatusPage: Health monitoring grid
Include a Layout component with navigation.
```

### Prompt 8: Upload Page UI
```
Create an upload page with:
- Large drag-and-drop zone (h-64) with dashed border
- File validation (client-side, .txt only)
- Upload progress indicator
- Document list with delete buttons
- Empty state with call-to-action
Use Shadcn UI components and Tailwind CSS.
```

### Prompt 9: Ask Page with Sources
```
Design an Ask page that:
- Shows large input field with submit button
- Displays loading state while processing
- Shows answer in a card
- Lists sources with document name, chunk preview, and similarity percentage
- Includes Q&A history sidebar (last 5)
- Handles empty results gracefully
```

### Prompt 10: Status Page Design
```
Create a status monitoring page with:
- 4 cards: Backend, Database, LLM, Vector Store
- Color-coded status indicators (green/yellow/red)
- Glowing dot animation for active services
- Model info for LLM card
- Vector count for FAISS
- Responsive grid layout
```

## Styling and UX

### Prompt 11: Design System
```
Create a Swiss-minimal design system with:
- Fonts: JetBrains Mono (headings) + Inter (body)
- High-contrast color palette
- Borders instead of shadows
- Micro-interactions (hover lift, active scale)
- Asymmetric Bento Grid layout
- Tailwind utility classes for consistency
```

### Prompt 12: Loading States
```
Add loading states for:
- Document upload (spinner + progress)
- Q&A processing (skeleton with message)
- Document list fetch (skeleton cards)
- Status checks (pulsing dots)
Use consistent animation patterns across all pages.
```

## Integration and Testing

### Prompt 13: Error Handling
```
Add comprehensive error handling:
- Invalid file types (show user-friendly message)
- Empty questions (disable submit)
- Network errors (retry option)
- Empty document list (call-to-action)
- Disconnected services (graceful degradation on status page)
```

### Prompt 14: Environment Configuration
```
Create environment variable management:
- Backend .env with GEMINI_API_KEY, MONGODB_URI, CORS_ORIGINS
- Frontend .env with REACT_APP_BACKEND_URL
- .env.example templates for both
- Config.py for centralized backend settings
```

### Prompt 15: Deployment Prep
```
Prepare for deployment:
- Review code for hardcoded secrets
- Create comprehensive .gitignore
- Add README with setup instructions
- Document architecture and tech stack
- Create AI_NOTES.md explaining LLM choices
```

## Optimization

### Prompt 16: Chunk Size Tuning
```
Help me analyze optimal chunk size for RAG:
- Test with 300, 500, 1000 character chunks
- Measure retrieval relevance
- Consider context window vs granularity
- Recommend overlap percentage
```

### Prompt 17: Prompt Engineering
```
Improve the RAG prompt to:
- Emphasize staying grounded in context
- Handle "I don't know" cases gracefully
- Be concise but complete
- Cite sources naturally
Test with edge cases like ambiguous questions and missing context.
```

## Additional Prompts

### Prompt 18: MongoDB Schema
```
Design MongoDB schemas for:
- documents collection (id, filename, file_size, chunk_count, uploaded_at)
- qa_history collection (id, question, answer, sources[], timestamp)
Use Motor for async operations.
```

### Prompt 19: Tailwind Configuration
```
Set up Tailwind with:
- Custom fonts (JetBrains Mono, Inter)
- Shadcn UI theme variables
- Custom utility classes for Swiss design
- Responsive breakpoints
```

### Prompt 20: Testing Strategy
```
Outline a testing strategy for:
- Backend: pytest for routes and services
- Frontend: manual testing of user flows
- Integration: end-to-end upload → ask → verify sources
- Edge cases: empty inputs, disconnected services, large files
```

---

## Key Manual Interventions

After each prompt, I:
1. **Reviewed** the generated code for bugs and inconsistencies
2. **Tested** with real data and edge cases
3. **Refactored** for better structure and readability
4. **Optimized** performance bottlenecks (batching, async)
5. **Validated** against requirements and best practices

## What I Didn't Use AI For

- Architecture decisions (layered backend, RAG pipeline flow)
- Chunk size and overlap tuning (empirical testing)
- Design system choices (Swiss-minimal aesthetic)
- FAISS distance normalization formula
- MongoDB schema design
- Deployment strategy
- Final code review and refactoring
