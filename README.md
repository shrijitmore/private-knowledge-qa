# Private Knowledge Q&A

A full-stack web application that enables users to upload private documents, ask questions, and receive AI-generated answers grounded in the uploaded content with source citations.

## 🚀 Live Demo

**Live App**: [Your Hosted URL Here]  
**GitHub**: [Your GitHub URL Here]

## ✨ Features

- **Document Upload**: Upload `.txt` files to build your private knowledge base
- **Smart Q&A**: Ask natural language questions about your documents
- **Source Citations**: See which document chunks were used to generate each answer
- **Q&A History**: Track your last 5 questions and answers
- **Health Monitoring**: Real-time status page for backend, database, LLM, and vector store
- **Swiss-Minimal UI**: Clean, professional interface with JetBrains Mono + Inter fonts

## 🏗️ Architecture

### Tech Stack

**Frontend**
- React 19 with React Router
- Shadcn UI + Tailwind CSS
- Axios for API calls

**Backend**
- Python FastAPI (layered architecture)
- Google Gemini 2.0 Flash (text generation)
- Gemini Embedding 001 (768-dim embeddings)
- FAISS vector store (in-memory + disk persistence)
- MongoDB (metadata storage)

### How It Works (RAG Pipeline)

1. **Document Upload**: Text files are chunked (500 chars, 100 overlap) and embedded using Gemini
2. **Indexing**: Embeddings stored in FAISS, metadata in MongoDB
3. **Question**: User query is embedded
4. **Retrieval**: FAISS finds top-5 most similar chunks
5. **Generation**: Gemini generates answer using retrieved context
6. **Response**: Answer returned with source citations

## 🛠️ Local Development

### Prerequisites

- Python 3.9+
- Node.js 16+
- MongoDB instance (local or Atlas)
- Google Gemini API key

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your credentials

# Run server
uvicorn server:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env
# Edit .env with backend URL

# Run dev server
npm start
```

The app will be available at `http://localhost:3000`

## 📋 Environment Variables

### Backend (.env)

```env
GEMINI_API_KEY=your_gemini_api_key_here
MONGODB_URI=your_mongodb_connection_string_here
CORS_ORIGINS=http://localhost:3000,https://your-frontend-url.com
```

### Frontend (.env)

```env
REACT_APP_BACKEND_URL=http://localhost:8000
```

## 🐳 Docker Deployment (Optional)

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access app at http://localhost:3000
```

## 📝 What's Done

✅ Full RAG pipeline with Gemini embeddings and generation  
✅ Document upload, list, and delete operations  
✅ Semantic search with FAISS vector store  
✅ Source citations with similarity scores  
✅ Q&A history tracking (last 5 queries)  
✅ Comprehensive status/health monitoring page  
✅ Swiss-minimal responsive UI  
✅ Error handling and loading states  
✅ Clean layered backend architecture  

## 🔮 What's Not Done (Future Enhancements)

- PDF and DOCX file support (currently .txt only)
- User authentication and multi-user workspaces
- Conversation context for follow-up questions
- Document preview/viewer
- Export Q&A history
- Rate limiting middleware
- Advanced file validation on frontend

## 📁 Project Structure

```
private-knowledge-qa/
├── backend/
│   ├── routes/          # API endpoints
│   ├── services/        # Business logic (RAG, embeddings, documents)
│   ├── models/          # Pydantic schemas
│   ├── vectorstore/     # FAISS management
│   ├── utils/           # Text processing
│   ├── server.py        # FastAPI app
│   ├── config.py        # Configuration
│   └── database.py      # MongoDB client
├── frontend/
│   ├── src/
│   │   ├── pages/       # HomePage, AskPage, UploadPage, StatusPage
│   │   ├── components/  # UI components
│   │   └── App.js       # Router setup
│   └── package.json
├── README.md
├── AI_NOTES.md
├── ABOUTME.md
└── PROMPTS_USED.md
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Run specific test
pytest tests/test_documents.py -v
```

## 📄 License

MIT

## 👤 Author

See [ABOUTME.md](ABOUTME.md) for details.
