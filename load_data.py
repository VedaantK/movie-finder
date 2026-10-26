"""Load the Netflix titles CSV into a persistent ChromaDB collection.

Run once:  uv run load_data.py
Re-running is safe: upsert() replaces rows with the same ID instead of duplicating them.
"""

from pathlib import Path

import chromadb
import pandas as pd

CSV_PATH = Path("data/netflix_titles.csv")
DB_PATH = "db"
COLLECTION = "titles"
BATCH_SIZE = 1000  # Chroma rejects very large single upserts


def main():
    if not CSV_PATH.exists():
        raise SystemExit(f"Missing {CSV_PATH}. Download it from Kaggle (see README).")

    df = pd.read_csv(CSV_PATH)
    df = df.dropna(subset=["description"])
    # Chroma metadata can't hold None/NaN, so fill blanks
    df = df.fillna({"title": "", "type": "", "listed_in": "", "rating": "", "release_year": 0})

    client = chromadb.PersistentClient(path=DB_PATH)
    collection = client.get_or_create_collection(COLLECTION)

    for start in range(0, len(df), BATCH_SIZE):
        batch = df.iloc[start:start + BATCH_SIZE]
        collection.upsert(
            ids=batch["show_id"].tolist(),
            # Only the description is embedded; the rest is metadata for display and filtering
            documents=batch["description"].tolist(),
            metadatas=[
                {
                    "title": row.title,
                    "type": row.type,
                    "genres": row.listed_in,
                    "rating": row.rating,
                    "year": int(row.release_year),
                }
                for row in batch.itertuples()
            ],
        )
        print(f"Loaded {min(start + BATCH_SIZE, len(df))}/{len(df)}")

    print(f"Done. Collection '{COLLECTION}' now has {collection.count()} titles.")


if __name__ == "__main__":
    main()
