from pathlib import Path
import json
import re

CHUNKS_FILE = Path("data/processed/reddit_privacy_chunks.json")


def tokenize(text):
    return re.findall(r"\b[a-zA-Z]+\b", text.lower())


chunks = json.loads(CHUNKS_FILE.read_text(encoding="utf-8"))

question = "How does Reddit use my information for advertising?"

question_words = set(tokenize(question))
results = []

for chunk in chunks:
    chunk_words = set(tokenize(chunk["text"]))
    score = len(question_words.intersection(chunk_words))

    results.append(
        {
            "score": score,
            "chunk_id": chunk["chunk_id"],
            "version": chunk["version"],
            "source": chunk["source"],
            "text": chunk["text"],
        }
    )

results.sort(key=lambda item: item["score"], reverse=True)

print(f"\nQuestion: {question}\n")
print("Top 3 matching chunks:\n")

for result in results[:3]:
    print(f"Score: {result['score']}")
    print(f"Chunk: {result['chunk_id']}")
    print(f"Version: {result['version']}")
    print(f"Source: {result['source']}")
    print(f"Text: {result['text'][:500]}")
    print("\n" + "-" * 70 + "\n")