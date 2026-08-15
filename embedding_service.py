from sentence_transformers import SentenceTransformer
from database import SessionLocal
from models import DocumentChunk

model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embedding(text: str):
    return model.encode(text).tolist()


def create_query_embedding(question: str):
    return model.encode(question).tolist()



def search_similar_chunks(question: str,  document_id: int, limit: int = 3):
    db = SessionLocal()

    try:
        question_embedding = create_query_embedding(question)

        chunks = (
            db.query(DocumentChunk)
            .filter(DocumentChunk.document_id == document_id)
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
        "What backend technologies are required?",
        document_id=4
    )

    print("Number of results:", len(results))

    for chunk in results:
        print("\nChunk ID:", chunk.id)
        print(chunk.text[:200])