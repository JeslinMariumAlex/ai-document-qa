# UploadFile and File are used to handle file uploads in FastAPI.
from fastapi import FastAPI, UploadFile, File, Depends
# pydantic is used to define and validate the request body that our API recieves.
from pydantic import BaseModel
# pypdf is a library for reading and manipulating PDF files in Python.
from pypdf import PdfReader
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
from models import Document

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
    question: str


@app.post("/ask")
def ask_question(
    request: QuestionRequest,
    db: Session = Depends(get_db)
):
    document = db.query(Document).filter(Document.id == request.document_id).first()

    if not document:
        return {"message": "Document not found"}
    
    return {
        "document_id": document.id,
        "question": request.question,
        "document_text": document.text
        }


@app.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

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

    return {
        "document_id": document.id,
        "filename": document.filename,
        "content_type": document.content_type
    }