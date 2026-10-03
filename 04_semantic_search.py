from pathlib import Path
import json

from sentence_transformers import SentenceTransformer, util

CHUNKS_FILE = Path("data/processed/reddit_privacy_chunks.json")

# Load the chunks created in Step 6
chunks = json.loads(CHUNKS_FILE.read_text(encoding="utf-8"))

# This model converts text into meaning-based numerical vectors.
model = SentenceTransformer("all-MiniLM-L6-v2")

question = "How does Reddit use my information for advertising?"

chunk_texts = [chunk["text"] for chunk in chunks]

# Convert the question and every chunk into embeddings.
question_embedding = model.encode(question, convert_to_tensor=True)
chunk_embeddings = model.encode(chunk_texts, convert_to_tensor=True)

# Compare the meaning of the question with the meaning of each chunk.
scores = util.cos_sim(question_embedding, chunk_embeddings)[0]

results = []

for index, chunk in enumerate(chunks):
    results.append(
        {
            "score": float(scores[index]),
            "chunk_id": chunk["chunk_id"],
            "version": chunk["version"],
            "source": chunk["source"],
            "text": chunk["text"],
        }
    )

results.sort(key=lambda item: item["score"], reverse=True)

print(f"\nQuestion: {question}\n")
print("Top 3 semantic matches:\n")

for result in results[:3]:
    print(f"Similarity score: {result['score']:.3f}")
    print(f"Chunk: {result['chunk_id']}")
    print(f"Version: {result['version']}")
    print(f"Source: {result['source']}")
    print(f"Text: {result['text'][:500]}")
    print("\n" + "-" * 70 + "\n")
