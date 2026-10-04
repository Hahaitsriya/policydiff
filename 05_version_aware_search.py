from pathlib import Path
import json

from sentence_transformers import SentenceTransformer, util

CHUNKS_FILE = Path("data/processed/reddit_privacy_chunks.json")

chunks = json.loads(CHUNKS_FILE.read_text(encoding="utf-8"))
model = SentenceTransformer("all-MiniLM-L6-v2")

question = "How did Reddit's privacy policy change regarding advertising?"


def search_version(version, top_k=2):
    version_chunks = [
        chunk for chunk in chunks
        if chunk["version"] == version
    ]

    texts = [chunk["text"] for chunk in version_chunks]

    question_embedding = model.encode(question, convert_to_tensor=True)
    text_embeddings = model.encode(texts, convert_to_tensor=True)

    scores = util.cos_sim(question_embedding, text_embeddings)[0]

    results = []

    for index, chunk in enumerate(version_chunks):
        results.append(
            {
                "score": float(scores[index]),
                "chunk_id": chunk["chunk_id"],
                "source": chunk["source"],
                "text": chunk["text"],
            }
        )

    results.sort(key=lambda item: item["score"], reverse=True)
    return results[:top_k]


old_results = search_version("old")
new_results = search_version("new")

print(f"\nQuestion: {question}\n")

print("BEST EVIDENCE FROM THE OLD POLICY\n")
for result in old_results:
    print(f"Score: {result['score']:.3f} | Chunk: {result['chunk_id']}")
    print(result["text"][:600])
    print("\n" + "-" * 70 + "\n")

print("BEST EVIDENCE FROM THE NEW POLICY\n")
for result in new_results:
    print(f"Score: {result['score']:.3f} | Chunk: {result['chunk_id']}")
    print(result["text"][:600])
    print("\n" + "-" * 70 + "\n")