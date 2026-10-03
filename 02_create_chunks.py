from pathlib import Path
import json

DATA_FOLDER = Path("data/raw")
OUTPUT_FOLDER = Path("data/processed")

CHUNK_SIZE = 250
OVERLAP = 50


def make_chunks(text, version):
    words = text.split()
    chunks = []
    start = 0
    chunk_number = 1

    while start < len(words):
        end = start + CHUNK_SIZE
        chunk_text = " ".join(words[start:end])

        chunks.append(
            {
                "chunk_id": f"{version}_{chunk_number}",
                "version": version,
                "source": f"reddit_privacy_{version}.md",
                "text": chunk_text,
            }
        )

        start += CHUNK_SIZE - OVERLAP
        chunk_number += 1

    return chunks


old_text = (DATA_FOLDER / "reddit_privacy_old.md").read_text(encoding="utf-8")
new_text = (DATA_FOLDER / "reddit_privacy_new.md").read_text(encoding="utf-8")

old_chunks = make_chunks(old_text, "old")
new_chunks = make_chunks(new_text, "new")

all_chunks = old_chunks + new_chunks

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

output_file = OUTPUT_FOLDER / "reddit_privacy_chunks.json"
output_file.write_text(json.dumps(all_chunks, indent=2), encoding="utf-8")

print(f"Created {len(old_chunks)} chunks from the old policy.")
print(f"Created {len(new_chunks)} chunks from the new policy.")
print(f"Total chunks: {len(all_chunks)}")
print(f"Saved them to: {output_file}")