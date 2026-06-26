from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

from dotenv import load_dotenv
load_dotenv()

from ai_provider import AIProvider

from rag.pdf_loader import extract_text
from rag.chunker import chunk_text
from rag.vector_store import store_chunks
from rag.retrieval import retrieve_context


app = FastAPI(
    title="AI Study Assistant",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class ChatRequest(BaseModel):
    provider: str
    prompt: str
    api_key: str | None = None


class QuestionRequest(BaseModel):
    question: str


class QuizRequest(BaseModel):
    topic: str = "document"



@app.get("/health")
def health():
    return {
        "status":"AI Study Assistant Running"
    }



@app.post("/chat")
def chat(request: ChatRequest):

    context = retrieve_context(request.prompt)


    prompt = f"""
You are an AI Study Assistant.

Use this context:

{context}


Question:

{request.prompt}


Answer:
"""


    answer = AIProvider.groq(prompt)


    return {
        "response":answer
    }





@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):


    os.makedirs(
        "uploads",
        exist_ok=True
    )


    file_path = f"uploads/{file.filename}"


    with open(file_path,"wb") as buffer:

        buffer.write(
            await file.read()
        )


    pdf_text = extract_text(file_path)


    chunks = chunk_text(pdf_text)


    store_chunks(chunks)


    return {

        "message":"PDF uploaded successfully",

        "chunks":len(chunks)

    }





@app.post("/ask-document")
def ask_document(request: QuestionRequest):


    context = retrieve_context(
        request.question
    )


    prompt = f"""

You are an AI Study Assistant.

Use ONLY this document context.


If answer is not available say:

I could not find that information in the uploaded document.


Context:

{context}


Question:

{request.question}


Answer:

"""


    answer = AIProvider.groq(prompt)


    return {

        "answer":answer

    }





@app.post("/generate-quiz")
def generate_quiz(request: QuizRequest):


    context = retrieve_context(
        request.topic
    )


    prompt = f"""

Create a quiz using ONLY this context.

Generate exactly 5 questions.


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


    quiz = AIProvider.groq(prompt)


    return {

        "quiz":quiz

    }





frontend_path="../frontend"


app.mount(
    "/",
    StaticFiles(
        directory=frontend_path,
        html=True
    ),
    name="frontend"
)