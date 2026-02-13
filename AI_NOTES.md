# AI Usage Notes

## What AI Was Used For

### AI Tools Used
- **Primary**: Google Gemini 2.0 (via Cursor/Claude/ChatGPT)
- **Code Generation**: AI-assisted for boilerplate and component scaffolding
- **Documentation**: AI-assisted for initial drafts

### Specific AI Contributions

1. **Backend Architecture**
   - ✅ AI generated initial FastAPI route structure
   - ✅ Manual review: Verified error handling, logging patterns
   - ✅ Manual implementation: Custom RAG pipeline logic, FAISS integration

2. **RAG Pipeline (`services/qa_service.py`)**
   - ✅ AI suggested prompt structure for Gemini
   - ✅ Manual implementation: Context building, similarity scoring normalization
   - ✅ Manual verification: Tested with various query types and edge cases

3. **FAISS Vector Store (`vectorstore/faiss_store.py`)**
   - ✅ AI provided basic FAISS index setup
   - ✅ Manual implementation: Persistence logic, metadata management, deletion with rebuild
   - ✅ Manual testing: Verified vector integrity after add/delete operations

4. **Frontend Components**
   - ✅ AI generated Shadcn UI component imports
   - ✅ Manual design: Custom layouts (Bento Grid), interaction patterns
   - ✅ Manual implementation: Error states, loading skeletons, responsive behavior

5. **Design System**
   - ✅ AI suggested Tailwind classes
   - ✅ Manual creation: Swiss-minimal design guidelines, typography system
   - ✅ Manual refinement: Color palette, spacing, micro-interactions

6. **Text Chunking (`utils/text.py`)**
   - ✅ AI provided basic chunking logic
   - ✅ Manual optimization: Overlap handling, chunk size tuning (tested with 300/500/1000 chars)

7. **MongoDB Integration**
   - ✅ AI suggested Motor async patterns
   - ✅ Manual implementation: Schema design, query optimization, index selection

8. **Status/Health Page**
   - ✅ AI generated health check endpoints
   - ✅ Manual implementation: Real-time status indicators, connection testing logic

### What I Checked/Verified Myself

1. **Embeddings Quality**
   - Tested Gemini embedding consistency
   - Verified 768-dimensional output matches FAISS index dimension
   - Compared retrieval results with different embedding models (settled on gemini-embedding-001)

2. **Chunk Size Optimization**
   - Experimented with 300, 500, 1000 character chunks
   - Measured answer quality with different overlap values (50, 100, 150)
   - Final choice: 500 chars with 100 overlap (best balance of context and granularity)

3. **Error Handling**
   - Manually tested all error paths (invalid files, empty queries, disconnected DB)
   - Added specific error messages for user clarity
   - Verified graceful degradation when services are unavailable

4. **FAISS Persistence**
   - Verified index survives server restarts
   - Tested concurrent read/write scenarios
   - Ensured metadata stays in sync with vector index

5. **CORS Configuration**
   - Tested cross-origin requests from different domains
   - Verified preflight handling for POST requests
   - Configured appropriate headers for production

6. **UI Responsiveness**
   - Manually tested on mobile (375px), tablet (768px), desktop (1920px)
   - Verified touch interactions on mobile browsers
   - Tested keyboard navigation and accessibility

## LLM Choice and Reasoning

### Primary LLM: Google Gemini 2.0 Flash

**Reasoning:**

1. **Unified Ecosystem**
   - Single API for both embeddings (gemini-embedding-001) and generation (gemini-2.0-flash)
   - Simplified auth and rate limiting management
   - Consistent error handling across both services

2. **Performance**
   - Fast inference (< 2s for typical queries)
   - 768-dim embeddings strike good balance (vs 1536 for OpenAI)
   - Generous free tier perfect for MVP/demo

3. **Quality**
   - Excellent at grounded Q&A (stays close to context)
   - Good at citing sources accurately
   - Handles technical and conversational queries well

4. **Cost**
   - Free tier: 15 RPM, 1500 RPD (sufficient for demo)
   - Production pricing competitive vs OpenAI/Claude

### Alternatives Considered

- **OpenAI GPT-4**: More expensive, separate embedding API
- **Claude 3**: No native embedding model, would need separate service
- **Open-source (Llama)**: Hosting complexity not worth it for MVP

### Embedding Model: `gemini-embedding-001`

- **Dimension**: 768 (vs 1536 for OpenAI)
- **Speed**: ~100ms for 50 chunks
- **Quality**: Strong semantic similarity, works well with FAISS L2 distance
- **Batch support**: 100 texts per call (config: `EMBEDDING_BATCH_SIZE`)

## Development Workflow

1. **Initial Setup**: AI generated project structure, I organized into clean layers
2. **Core Implementation**: Pair programming with AI (AI suggests, I refine/test)
3. **Testing**: Manual end-to-end testing with real documents
4. **Optimization**: Iterative tuning of chunk size, top-k, prompt engineering
5. **Documentation**: AI drafted, I edited for accuracy and completeness

## Confidence Level

- **Backend Logic**: 95% confident (thoroughly tested)
- **RAG Pipeline**: 90% confident (validated with diverse queries)
- **FAISS Integration**: 85% confident (tested add/delete/search, not stress-tested at scale)
- **Frontend UX**: 95% confident (responsive, accessible, error-handled)
- **Production Readiness**: 80% (needs rate limiting, advanced validation, monitoring)

## Key Manual Decisions

1. Chose FAISS over Pinecone/Weaviate for simplicity and local persistence
2. Used MongoDB over PostgreSQL for flexible schema and async support
3. Implemented chunk-level (not sentence-level) splitting for better context preservation
4. Normalized similarity scores using max distance scaling (better UX than raw L2)
5. Limited history to 5 entries (performance vs utility tradeoff)
6. Chose Swiss-minimal design over trendy gradients for professional feel
