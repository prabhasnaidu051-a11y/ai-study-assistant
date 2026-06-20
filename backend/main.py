from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from typing import Optional

from ai_provider import AIProvider

from rag.pdf_loader import extract_text
from rag.chunker import chunk_text
from rag.vector_store import store_chunks
from rag.retrieval import retrieve_context


app = FastAPI(
    title="AI Study Assistant",
    version="1.0.0"
)

# -----------------------------
# CORS
# -----------------------------
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
    api_key: Optional[str] = None


class QuestionRequest(BaseModel):
    question: str


class QuizRequest(BaseModel):
    topic: str = "document"


# -----------------------------
# Home
# -----------------------------
@app.get("/")
def home():

    return {
        "message": "AI Study Assistant Backend Running"
    }


# -----------------------------
# AI Chat
# -----------------------------
@app.post("/chat")
def chat(request: ChatRequest):

    if request.provider == "Ollama":

        context = retrieve_context(
            request.prompt
        )

        prompt = f"""
You are an AI Study Assistant.

Use only this document context:

{context}

Question:
{request.prompt}

Answer:
"""

        answer = AIProvider.ollama(
            prompt
        )


    elif request.provider == "OpenAI":

        answer = AIProvider.openai(
            request.prompt,
            request.api_key
        )


    else:

        answer = "Unsupported provider"


    return {
        "response": answer
    }

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):

    pdf_text = extract_text(file.file)

    chunks = chunk_text(pdf_text)

    store_chunks(chunks)

    return {
        "message": "PDF uploaded successfully",
        "chunks": len(chunks)
    }

# -----------------------------
# Ask Uploaded Documents
# -----------------------------
@app.post("/ask-document")
def ask_document(
    request: QuestionRequest
):

    context = retrieve_context(
        request.question
    )

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

    answer = AIProvider.ollama(
        prompt
    )

    return {
        "answer": answer
    }


# -----------------------------
# Generate Quiz
# -----------------------------
@app.post("/generate-quiz")
def generate_quiz(
    request: QuizRequest
):

    context = retrieve_context(
        request.topic
    )

    prompt = f"""
You are a quiz generator.

IMPORTANT:
- Use ONLY the text inside Context.
- Use ONLY information from Context.
- Do NOT use any outside knowledge.
- Do NOT add chapter numbers unless they appear in Context.
- Do NOT create examples.
- Do NOT create scenarios.
- Do NOT add explanations.
- Do NOT infer anything.
- Questions must be based only on sentences found in Context.
- Questions must be formed directly from facts in Context.
- Do NOT reword concepts.
- Do NOT replace words (e.g. isolated system → closed system).
- Use the same terminology as Context.
- Every answer must appear exactly in the Context.
- Answers must be copied exactly from Context.
- Answers must be copied word-for-word from the Context.
- Do not shorten answers.
- Do not paraphrase answers.
- Ignore incomplete words.
- Ignore text fragments.
- Ignore labels such as "Length:".
- Use only complete facts and sentences from the Context.
- Create quiz questions ONLY from the Context.
- One question per fact.
- Generate EXACTLY 5 questions.
- If fewer than 5 facts exist, repeat no facts.
- Output Question 1 through Question 5.

Context:
{context}

Create questions directly from the Context.

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

    quiz = AIProvider.ollama(
        prompt
    )

    print("CONTEXT:", context)
    print("QUIZ RESPONSE:", quiz)

    return {
        "quiz": quiz
    }