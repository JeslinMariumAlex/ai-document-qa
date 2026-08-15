from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

text = "FastAPI is a Python framework for building APIs."

embedding = model.encode(text)

print("Embedding dimensions:", len(embedding))
print("First 10 values:", embedding[:10])