from pathlib import Path
import json

from sentence_transformers import SentenceTransformer, util

CHUNKS_FILE = Path("data/processed/reddit_privacy_chunks.json")
OUTPUT_FILE = Path("data/processed/rag_context.txt")

chunks = json.loads(CHUNKS_FILE.read_text(encoding="utf-8"))
model = SentenceTransformer("all-MiniLM-L6-v2")

question = "How did Reddit's privacy policy change regarding advertising?"


def retrieve(version, top_k=2):
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


def format_evidence(results, version):
    formatted = []

    for result in results:
        formatted.append(
            f"[{version} | {result['source']} | {result['chunk_id']}]\n"
            f"{result['text']}"
        )

    return "\n\n".join(formatted)


old_evidence = format_evidence(retrieve("old"), "OLD POLICY")
new_evidence = format_evidence(retrieve("new"), "NEW POLICY")

rag_context = f"""
You are PolicyDiff, an assistant that compares policy versions.

Rules:
1. Answer only using the evidence below.
2. If the evidence is insufficient, say so.
3. Explain changes clearly.
4. Cite the chunk label that supports every important claim.

Question:
{question}

Evidence from the old policy:
{old_evidence}

Evidence from the new policy:
{new_evidence}
"""

OUTPUT_FILE.write_text(rag_context.strip(), encoding="utf-8")

print("RAG context created successfully.")
print(f"Saved to: {OUTPUT_FILE}")
print("\nPreview:\n")
print(rag_context[:1500])