# UploadFile and File are used to handle file uploads in FastAPI.
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
# pydantic is used to define and validate the request body that our API recieves.
from pydantic import BaseModel, Field
# pypdf is a library for reading and manipulating PDF files in Python.
from pypdf import PdfReader
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
from chunking import chunk_text
from models import Document, DocumentChunk
from embedding_service import search_similar_chunks, create_embedding
from llm_service import build_prompt, generate_answer

app = FastAPI()

# This tells , Look at all the models registered with Base in the models.py file and create the database tables if they don't already exist. 
Base.metadata.create_all(bind=engine)


# This gives an endpoint a database session and makes sure it gets closed afterwards.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "AI Document Q&A API is Running"}



# create the model for the request body
class QuestionRequest(BaseModel):
    document_id: int
    question: str = Field(..., min_length=1)


@app.post("/ask")
def ask_question(request: QuestionRequest, db: Session = Depends(get_db)):

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    document = (db.query(Document).filter(Document.id == request.document_id).first())

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    # gets the relevant chunks.
    chunks = search_similar_chunks(request.question, request.document_id, limit=5)

    # creates the prompt from the question + retrieved context.
    prompt = build_prompt(request.question, chunks)
    # sends that prompt to Llama and gets the answer.
    answer = generate_answer(prompt)

    # returns the actual answer to the API caller.
    return {
        "question": request.question,
        "answer": answer
    }


@app.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):


    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    reader = PdfReader(file.file)

    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    # creates a Python object representing a database row.
    document = Document(
        filename=file.filename,
        content_type=file.content_type,
        text=text
    )
    # saves that row into PostgreSQL.
    db.add(document)
    db.commit()
    # gets the generated id from PostgreSQL.
    db.refresh(document)   

    chunks = chunk_text(document.text)

    for chunk in chunks:
        embedding = create_embedding(chunk)

        document_chunk = DocumentChunk(
            document_id=document.id,
            text=chunk,
            embedding=embedding
        )
        db.add(document_chunk)

    db.commit() 

    return {
        "document_id": document.id,
        "filename": document.filename,
        "content_type": document.content_type
    }