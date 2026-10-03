from pathlib import Path

DATA_FOLDER = Path("data/raw")

old_file = DATA_FOLDER / "reddit_privacy_old.md"
new_file = DATA_FOLDER / "reddit_privacy_new.md"

old_policy = old_file.read_text(encoding="utf-8")
new_policy = new_file.read_text(encoding="utf-8")

print("Dataset loaded successfully!")
print()
print(f"Old policy: {old_file.name}")
print(f"Characters: {len(old_policy):,}")
print()
print(f"New policy: {new_file.name}")
print(f"Characters: {len(new_policy):,}")
print()
print("First 300 characters of the new policy:")
print(new_policy[:300])