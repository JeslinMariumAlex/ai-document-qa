from fastapi import FastAPI
# UploadFile and File are used to handle file uploads in FastAPI.
from fastapi import UploadFile, File
# pydantic is used to define and validate the request body that our API recieves.
from pydantic import BaseModel
# pypdf is a library for reading and manipulating PDF files in Python.
from pypdf import PdfReader

app = FastAPI()


@app.get("/")
def home():
    return {"message": "AI Document Q&A API is Running"}



# create the model for the request body
class QuestionRequest(BaseModel):
    question: str


@app.post("/ask")
def ask_question(request: QuestionRequest):
    return {
        "message": "Question received",
        "question": request.question
        }


@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):

    reader = PdfReader(file.file)

    text = ""
    
    for page in reader.pages:
        text += page.extract_text() or ""

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "text": text
    }