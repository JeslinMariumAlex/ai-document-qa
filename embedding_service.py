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



def create_query_embedding(question: str):
    return model.encode(question).tolist()



def search_similar_chunks(question: str, limit: int = 3):
    db = SessionLocal()

    try:
        question_embedding = create_query_embedding(question)

        chunks = (
            db.query(DocumentChunk)
            .order_by(
                DocumentChunk.embedding.cosine_distance(question_embedding)
            )
            .limit(limit)
            .all()
        )

        return chunks

    finally:
        db.close()
        

if __name__ == "__main__":
    results = search_similar_chunks(
        "What backend technologies are required?"
    )

    print("Number of results:", len(results))

    for chunk in results:
        print("\nChunk ID:", chunk.id)
        print(chunk.text[:200])