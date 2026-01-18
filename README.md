# 🧠 Enterprise AI Knowledge Assistant (RAG System)

An event-driven, real-time AI Knowledge Assistant built using FastAPI, Retrieval-Augmented Generation (RAG), ChromaDB, Redis Pub/Sub, and WebSockets. This project demonstrates production-grade AI system design, not just prompt engineering.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![Redis](https://img.shields.io/badge/Redis-7.0+-red.svg)

---

## 🚀 Features

- 📄 **Document ingestion & vectorization** - Upload and process documents into semantic chunks
- 🧠 **Semantic search using ChromaDB** - Vector similarity search for intelligent retrieval
- 🤖 **LLM-powered question answering (RAG)** - Context-aware responses using retrieved knowledge
- 🔄 **Event-driven architecture with Redis** - Decoupled, scalable message routing
- 💬 **Real-time chat via WebSockets** - Bidirectional streaming communication
- 🧩 **Modular, scalable project structure** - Clean architecture for enterprise deployments
- 🛡️ **Hallucination-safe responses** - Returns "I don't know" when context is missing

---

## 🏗️ Architecture Overview

```
Client (Postman / Browser)
        │
        ▼
 WebSocket (FastAPI)
        │
        ▼
 Redis Pub/Sub (event bus)
        │
        ▼
 RAG Service
   ├─ ChromaDB (vector search)
   ├─ Embedding Model
   └─ LLM Service
        │
        ▼
 WebSocket Response (Real-time)
```

---

## 📂 Project Structure

```
app/
├── main.py                      # FastAPI application entry point
├── api/
│   └── routes/
│       ├── chat.py              # WebSocket chat endpoint
│       ├── documents.py         # Document upload/management
│       └── section.py           # Document section CRUD
├── services/
│   ├── rag_service.py           # RAG orchestration logic
│   ├── embedding_service.py     # Text embedding generation
│   ├── llm_service.py           # LLM integration (OpenAI/Azure)
│   └── websocket_manager.py    # WebSocket connection management
├── vector_store/
│   └── chroma_client.py         # ChromaDB client wrapper
├── workers/
│   └── producer.py              # Redis publisher for events
├── db/
│   └── base.py                  # SQLAlchemy base models
├── models/
│   └── section.py               # Document section schema
└── database.py                  # Database connection setup
```

---

## 🔧 Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | FastAPI (async) |
| **Real-time Messaging** | WebSockets |
| **Event Streaming** | Redis Pub/Sub |
| **Vector Database** | ChromaDB |
| **LLM** | OpenAI / Azure OpenAI (pluggable) |
| **Embeddings** | Transformer-based embeddings |
| **Database** | PostgreSQL (SQLAlchemy) |
| **Language** | Python 3.10+ |

---

## 🧠 RAG Pipeline (How it Works)

1. **Documents are uploaded** and parsed
2. **Text is chunked** into semantic units
3. **Chunks are converted** into embeddings
4. **Embeddings are stored** in ChromaDB
5. **User queries are embedded**
6. **Top-K similar chunks** are retrieved
7. **Retrieved context** is sent to the LLM
8. **Final answer** is streamed back via WebSocket

---

## ⚡ Real-Time Chat Flow

1. Client connects via WebSocket
2. Messages are published to Redis
3. RAG service processes messages
4. Responses are published back to Redis
5. WebSocket streams response to client

**This design supports multiple clients and workers.**

---

## 📦 Installation

### Prerequisites

- Python 3.10+
- Redis Server
- PostgreSQL
- OpenAI API Key (or Azure OpenAI)

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/enterprise-rag-system.git
cd enterprise-rag-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration
```

### Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/rag_db

# Redis
REDIS_URL=redis://localhost:6379

# OpenAI
OPENAI_API_KEY=your_api_key_here
MODEL_NAME=gpt-4

# ChromaDB
CHROMA_DB_DIR=./chroma_db

```

---

## 🚀 Running the Application

### 1️⃣ Start Redis

```bash
redis-server
```

### 2️⃣ Start PostgreSQL

```bash
# Using Docker
docker run --name postgres-rag -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres

# Or use your local PostgreSQL installation
```

### 3️⃣ Run Database Migrations

```bash
alembic upgrade head
```

### 4️⃣ Start the Application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

---

## 🧪 Testing (No Manual UI)

### Using Postman

#### 1. Upload a Document

```http
POST http://localhost:8000/api/documents/{section_id}
Content-Type: multipart/form-data

file: [your_document.pdf]
```

#### 2. Connect to WebSocket

```
ws://127.0.0.1:8000/ws/chat/{section_id}
```

Send message:
```json
{
  "message": "What is FastAPI?"
}
```


## 🧪 Debugging & Observability

The system includes detailed logs for:

- ✅ WebSocket connections
- ✅ Redis pub/sub events
- ✅ RAG retrieval results
- ✅ LLM responses


## 📌 Why This Project Matters

This project demonstrates:

- ✅ Real-world AI system design
- ✅ Event-driven architectures
- ✅ Async backend expertise
- ✅ Vector search + LLM integration
- ✅ Production-style safety guardrails

**It is not a toy chatbot, but a scalable AI platform foundation.**

---

## 📄 API Documentation

Once running, access the interactive API docs:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---


## 📜 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 👥 Authors

- **Muhammed Ajmal** - [GitHub](https://github.com/majmalmdt)

---

## 🙏 Acknowledgments

- OpenAI for GPT models
- ChromaDB team for vector database
- FastAPI community
- Redis labs

---


**⭐ If you find this project useful, please consider giving it a star!**