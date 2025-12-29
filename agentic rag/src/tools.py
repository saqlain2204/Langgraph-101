import os
import uuid
from langchain_core.tools import tool
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

pc = Pinecone(api_key=PINECONE_API_KEY)
desc = pc.describe_index(name=INDEX_NAME)
host = desc["host"]
index = pc.Index(host=host)

@tool
def hybrid_retriever_tool(query: str, top_k: int = 3) -> str:
    """Hybrid search on Pinecone: returns top answer(s) for a query."""
    dense_query_embedding = pc.inference.embed(
        model="llama-text-embed-v2",
        inputs=[query],
        parameters={"input_type": "query", "truncate": "END"}
    )
    sparse_query_embedding = pc.inference.embed(
        model="pinecone-sparse-english-v0",
        inputs=[query],
        parameters={"input_type": "query", "truncate": "END"}
    )
    d = dense_query_embedding[0]
    s = sparse_query_embedding[0]
    query_response = index.query(
        top_k=top_k,
        vector=d['values'],
        sparse_vector={'indices': s['sparse_indices'], 'values': s['sparse_values']},
        include_values=False,
        include_metadata=True
    )
    if not query_response.matches:
        return "No relevant results found."
    results = []
    for match in query_response.matches:
        results.append({
            "page_content": match.metadata.get("text", ""),
            "metadata": match.metadata
        })
    return "\n".join([doc["page_content"] for doc in results])

if __name__ == "__main__":
    query = "What is reward hacking?"
    print(hybrid_retriever_tool.run(query))