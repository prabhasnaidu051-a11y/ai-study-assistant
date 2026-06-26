from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from pydantic import BaseModel

from ai_provider import AIProvider

from rag.pdf_loader import extract_text
from rag.chunker import chunk_text
from rag.vector_store import store_chunks
from rag.retrieval import retrieve_context


app = FastAPI(title="AI Study Assistant", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Request Models
# -----------------------------
class ChatRequest(BaseModel):
    provider: str
    prompt: str
    api_key: str | None = None


class QuestionRequest(BaseModel):
    question: str


class QuizRequest(BaseModel):
    topic: str = "document"


# -----------------------------
# Home
# -----------------------------
# Serve Frontend
frontend_path = "../frontend"

app.mount(
    "/static",
    StaticFiles(directory=frontend_path),
    name="static"
)


@app.get("/")
@app.head("/")
def home():
    return FileResponse(
        os.path.join(frontend_path, "index.html")
    )
# -----------------------------
# AI Chat
# -----------------------------
@app.post("/chat")
def chat(request: ChatRequest):
    if request.provider == "Ollama":
        context = retrieve_context(request.prompt)

        prompt = f"""
You are an AI Study Assistant.

Use only this document context:

{context}

Question:
{request.prompt}

Answer:
"""

        answer = AIProvider.ollama(prompt)

    elif request.provider == "OpenAI":
        answer = AIProvider.openai(request.prompt, request.api_key)

    else:
        answer = "Unsupported provider"

    return {"response": answer}


# -----------------------------
# Upload PDF
# -----------------------------
@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if file.filename is None:
        return {"message": "No filename provided"}

    os.makedirs("uploads", exist_ok=True)

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    pdf_text = extract_text(file_path)

    chunks = chunk_text(pdf_text)

    store_chunks(chunks)

    return {"message": "PDF uploaded successfully", "chunks": len(chunks)}


# -----------------------------
# Ask Uploaded Documents
# -----------------------------


@app.post("/ask-document")
def ask_document(request: QuestionRequest):
    context = retrieve_context(request.question)

    prompt = f"""
You are an AI Study Assistant.

Use ONLY the information provided in the context below.

If the answer is not present in the context,
respond exactly with:

I could not find that information in the uploaded document.

Context:
{context}

Question:
{request.question}

Answer:
"""

    answer = AIProvider.ollama(prompt)

    return {"answer": answer}


# -----------------------------
# Generate Quiz
# -----------------------------
@app.post("/generate-quiz")
def generate_quiz(request: QuizRequest):
    context = retrieve_context(request.topic)

    prompt = f"""
You are a quiz generator.

IMPORTANT:
- Use ONLY the text inside Context.
- Use ONLY information from Context.
- Do NOT use outside knowledge.
- Do NOT add explanations.
- Answers must be copied exactly from Context.
- Generate EXACTLY 5 questions.

Context:
{context}

Format:

Question 1:
Answer:

Question 2:
Answer:

Question 3:
Answer:

Question 4:
Answer:

Question 5:
Answer:
"""

    quiz = AIProvider.ollama(prompt)

    print("CONTEXT:", context)
    print("QUIZ RESPONSE:", quiz)

    return {"quiz": quiz}
