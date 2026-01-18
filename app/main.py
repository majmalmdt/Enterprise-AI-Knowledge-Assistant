from fastapi import FastAPI
from app.api.routes import documents, chat, section
from app.database import init_db
from fastapi.middleware.cors import CORSMiddleware
from app.vector_store.chroma_client import chroma_client
app = FastAPI(title="AI Knowledge Assistant")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change "*" to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router, prefix="/documents", tags=["Documents"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(section.router, prefix="/sections", tags=["Sections"])

@app.on_event("startup")
async def on_startup():
    await init_db()    