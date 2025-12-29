import os
from dotenv import load_dotenv
import uuid

load_dotenv()

from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec

import requests
from bs4 import BeautifulSoup

def fetch_and_chunk(url, chunk_size=300):
    """Fetches the content from a URL and chunks it into pieces."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = [p.get_text() for p in soup.find_all("p") if p.get_text(strip=True)]
    text = "\n".join(paragraphs)
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i+chunk_size]
        if chunk.strip():
            chunks.append(chunk)
    return chunks

def get_all_url_chunks(urls, chunk_size=300):
    """Fetches and chunks all URLs, returns list of dicts with 'chunk_text'."""
    all_chunks = []
    for url in urls:
        chunks = fetch_and_chunk(url, chunk_size=chunk_size)
        for chunk in chunks:
            all_chunks.append({"chunk_text": chunk, "source_url": url})
    return all_chunks

URLS = [
    "https://lilianweng.github.io/posts/2024-11-28-reward-hacking/",
    "https://lilianweng.github.io/posts/2024-07-07-hallucination/",
    "https://lilianweng.github.io/posts/2024-04-12-diffusion-video/",
]
data = get_all_url_chunks(URLS)
print(data)

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "hybrid-index"

if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        vector_type="dense",
        dimension=1024,
        metric="dotproduct",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

def get_batched_embeddings(pc, data, model, batch_size=96):
    all_embeds = []
    for i in range(0, len(data), batch_size):
        batch = [d['chunk_text'] for d in data[i:i+batch_size]]
        result = pc.inference.embed(
            model=model,
            inputs=batch,
            parameters={"input_type": "passage", "truncate": "END"}
        )
        all_embeds.extend(result)
    return all_embeds

dense_embeddings = get_batched_embeddings(pc, data, model="llama-text-embed-v2", batch_size=96)
sparse_embeddings = get_batched_embeddings(pc, data, model="pinecone-sparse-english-v0", batch_size=96)

desc = pc.describe_index(name=index_name)
host = desc['host']
index = pc.Index(host=host)

records = []
for d, de, se in zip(data, dense_embeddings, sparse_embeddings):
    records.append({
        "id": str(uuid.uuid4()),
        "values": de['values'],
        "sparse_values": {'indices': se['sparse_indices'], 'values': se['sparse_values']},
        "metadata": {'text': d['chunk_text']}
    })

index.upsert(
    vectors=records,
)