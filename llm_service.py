from ollama import chat
from embedding_service import search_similar_chunks


def generate_answer(prompt: str):
    response = chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.message.content



def build_prompt(question: str, chunks):
    context = "\n\n".join(chunk.text for chunk in chunks)

    prompt = f"""
Answer the question using only the provided context.

Context:
{context}

Question:
{question}

Answer:
"""

    return prompt



if __name__ == "__main__":
    question = "What backend technologies are required?"

    chunks = search_similar_chunks(
        question,
        document_id=4
    )

    prompt = build_prompt(question, chunks)
    answer = generate_answer(prompt)

    
    print(answer)
