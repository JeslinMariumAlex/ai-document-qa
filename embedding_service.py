from sentence_transformers import SentenceTransformer
from database import SessionLocal
from models import DocumentChunk

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_chunks():
    db = SessionLocal()

    try:
        chunks = db.query(DocumentChunk).all()
        return chunks
    finally:
        db.close()


def generate_embeddings():

    db = SessionLocal()

    try:
        chunks = db.query(DocumentChunk).all()

        for chunk in chunks:
            embedding = model.encode(chunk.text).tolist()
            chunk.embedding = embedding

        db.commit()

    finally:
        db.close()
        

if __name__ == "__main__":
    generate_embeddings()

    print("Embeddings generated successfully")        