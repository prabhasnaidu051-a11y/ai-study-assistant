# AI Study Assistant Feature Specification

## Feature Name
AI Document Question Answering

## Description
Users can upload study documents and ask questions. The system retrieves relevant content and generates AI-based answers.

## Requirements

- User can upload PDF files
- System extracts document text
- Vector database stores embeddings
- AI model generates answers
- User can ask questions from documents

## Acceptance Criteria

- PDF upload works successfully
- Questions return relevant answers
- Errors are handled properly

## Implementation Notes

Backend uses FastAPI.
RAG pipeline uses ChromaDB.
AI responses are generated using Ollama.
