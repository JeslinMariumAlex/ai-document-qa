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
Include all relevant information from the context.
If the question asks for technologies, tools, frameworks, or databases, list all relevant ones explicitly mentioned in the context.
If the context does not contain the answer, say that the information is not available in the provided document.
Do not use outside knowledge.
Do not contradict information stated in your own answer.

Context:
{context}

Question:
{question}

Answer:
"""

    return prompt



if __name__ == "__main__":
    question = "What backend frameworks, API technologies, and databases are mentioned in the document?"

    chunks = search_similar_chunks(question,document_id=4, limit=5)

    prompt = build_prompt(question, chunks)
    answer = generate_answer(prompt)

    print(answer)
