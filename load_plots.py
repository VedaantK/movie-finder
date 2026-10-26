"""Load Wikipedia plot summaries (CMU Movie Summary Corpus) into the same ChromaDB collection.

Run after download_data.py:  uv run load_plots.py
Only the TOP_N highest-grossing movies are loaded to keep embedding time reasonable.
"""

import json
import re
from pathlib import Path

import chromadb
import pandas as pd

DATA_DIR = Path("data/cmu/MovieSummaries")
DB_PATH = "db"
COLLECTION = "titles"
TOP_N = 5000
MAX_WORDS = 150  # the default embedding model only reads ~256 word pieces, so keep chunks well under
BATCH_SIZE = 1000


def chunk_plot(text):
    """Split a plot into chunks of whole sentences, each at most ~MAX_WORDS words."""
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    chunks, current = [], []
    for sentence in sentences:
        if current and len(" ".join(current + [sentence]).split()) > MAX_WORDS:
            chunks.append(" ".join(current))
            current = []
        current.append(sentence)
    if current:
        chunks.append(" ".join(current))
    return chunks


def main():
    plots = pd.read_csv(DATA_DIR / "plot_summaries.txt", sep="\t", header=None,
                        names=["wiki_id", "summary"], quoting=3)
    movies = pd.read_csv(DATA_DIR / "movie.metadata.tsv", sep="\t", header=None,
                         names=["wiki_id", "freebase_id", "title", "release_date", "box_office",
                                "runtime", "languages", "countries", "genres"])
    df = movies.merge(plots, on="wiki_id").dropna(subset=["box_office"])
    df = df.sort_values("box_office", ascending=False).head(TOP_N)

    ids, documents, metadatas = [], [], []
    for row in df.itertuples():
        movie_id = f"cmu-{row.wiki_id}"
        year = str(row.release_date)[:4]
        genres = ", ".join(json.loads(row.genres).values())
        for i, chunk in enumerate(chunk_plot(row.summary)):
            ids.append(f"{movie_id}-{i}")
            documents.append(chunk)
            metadatas.append({
                "title": row.title,
                "type": "Movie",
                "genres": genres,
                "rating": "",
                "year": int(year) if year.isdigit() else 0,
                "source": "Wikipedia",
                "movie_id": movie_id,  # groups a movie's chunks so results show each movie once
            })
    print(f"{len(df)} movies split into {len(ids)} chunks.")

    collection = chromadb.PersistentClient(path=DB_PATH).get_or_create_collection(COLLECTION)
    for start in range(0, len(ids), BATCH_SIZE):
        end = start + BATCH_SIZE
        collection.upsert(ids=ids[start:end], documents=documents[start:end], metadatas=metadatas[start:end])
        print(f"Loaded {min(end, len(ids))}/{len(ids)}", flush=True)

    print(f"Done. Collection '{COLLECTION}' now has {collection.count()} items.")


if __name__ == "__main__":
    main()
