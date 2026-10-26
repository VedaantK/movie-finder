"""Describe-the-vibe Netflix finder: an interactive menu over the ChromaDB collection.

Run after load_data.py:  uv run app.py
"""

import textwrap
import uuid

import chromadb
import numpy as np

DB_PATH = "db"
N_RESULTS = 5

client = chromadb.PersistentClient(path=DB_PATH)
titles = client.get_or_create_collection("titles")
# Saved picks live in their own collection so they persist across runs too
watchlist = client.get_or_create_collection("watchlist")


def show_results(ids, metadatas, documents):
    print()
    for i, (meta, doc) in enumerate(zip(metadatas, documents), start=1):
        print(f"{i}. {meta['title']} ({meta['type']}, {meta['year']}) - {meta['genres']}")
        print(textwrap.fill(doc, width=80, initial_indent="   ", subsequent_indent="   "))
    print()


def results_menu(ids, metadatas, documents):
    """Show results and let the user act on them until they go back."""
    while True:
        show_results(ids, metadatas, documents)
        choice = input("[number] more like this, [w number] add to watchlist, [Enter] back: ").strip().lower()
        if not choice:
            return
        save = choice.startswith("w")
        num = choice.lstrip("w").strip()
        if not num.isdigit() or not 1 <= int(num) <= len(ids):
            print("Not a valid choice.")
            continue
        picked = int(num) - 1
        if save:
            add_to_watchlist(ids[picked])
        else:
            print(f"\nMore like {metadatas[picked]['title']}:")
            ids, metadatas, documents = more_like_this(ids[picked])


def ask_type_filter():
    choice = input("Movies, TV shows, or both? [m/t/Enter for both]: ").strip().lower()
    if choice == "m":
        return {"type": "Movie"}
    if choice == "t":
        return {"type": "TV Show"}
    return None


def search():
    query = input("\nDescribe what you're in the mood for: ").strip()
    if not query:
        return
    result = titles.query(query_texts=[query], n_results=N_RESULTS, where=ask_type_filter())
    results_menu(result["ids"][0], result["metadatas"][0], result["documents"][0])


def query_by_embedding(embedding, exclude_ids):
    """Nearest titles to an embedding, skipping the ones in exclude_ids."""
    result = titles.query(query_embeddings=[embedding], n_results=N_RESULTS + len(exclude_ids))
    rows = [
        (id_, meta, doc)
        for id_, meta, doc in zip(result["ids"][0], result["metadatas"][0], result["documents"][0])
        if id_ not in exclude_ids
    ][:N_RESULTS]
    ids, metadatas, documents = zip(*rows)
    return list(ids), list(metadatas), list(documents)


def more_like_this(title_id):
    embedding = titles.get(ids=[title_id], include=["embeddings"])["embeddings"][0]
    return query_by_embedding(embedding, exclude_ids={title_id})


def add_title():
    print("\nAdd a title (it becomes searchable immediately).")
    title = input("Title: ").strip()
    description = input("Description: ").strip()
    if not title or not description:
        print("Title and description are required.")
        return
    kind = "TV Show" if input("Movie or TV show? [m/t]: ").strip().lower() == "t" else "Movie"
    year = input("Release year: ").strip()
    genres = input("Genres (comma separated): ").strip()
    titles.upsert(
        ids=[f"user-{uuid.uuid4().hex[:8]}"],
        documents=[description],
        metadatas=[{
            "title": title,
            "type": kind,
            "genres": genres,
            "rating": "",
            "year": int(year) if year.isdigit() else 0,
        }],
    )
    print(f"Added '{title}'. Collection now has {titles.count()} titles.")


def add_to_watchlist(title_id):
    # Copy the stored embedding so the watchlist doesn't re-embed anything
    item = titles.get(ids=[title_id], include=["embeddings", "metadatas", "documents"])
    watchlist.upsert(
        ids=[title_id],
        embeddings=item["embeddings"],
        metadatas=item["metadatas"],
        documents=item["documents"],
    )
    print(f"Saved '{item['metadatas'][0]['title']}' to your watchlist.")


def show_watchlist():
    items = watchlist.get(include=["metadatas", "documents"])
    if not items["ids"]:
        print("\nYour watchlist is empty. Save titles from search results with 'w <number>'.")
        return
    print("\nYour watchlist:")
    show_results(items["ids"], items["metadatas"], items["documents"])
    remove = input("[number] remove, [Enter] back: ").strip()
    if remove.isdigit() and 1 <= int(remove) <= len(items["ids"]):
        watchlist.delete(ids=[items["ids"][int(remove) - 1]])
        print("Removed.")


def surprise_me():
    """Recommend titles closest to the average 'taste' of everything on the watchlist."""
    items = watchlist.get(include=["embeddings", "metadatas"])
    if not items["ids"]:
        print("\nAdd a few titles to your watchlist first.")
        return
    taste = np.mean(items["embeddings"], axis=0)
    names = ", ".join(meta["title"] for meta in items["metadatas"])
    print(f"\nBecause your watchlist has: {names}")
    results_menu(*query_by_embedding(taste.tolist(), exclude_ids=set(items["ids"])))


MENU = {
    "1": ("Search by vibe", search),
    "2": ("Add a title", add_title),
    "3": ("View watchlist", show_watchlist),
    "4": ("Surprise me (based on watchlist)", surprise_me),
}


def main():
    print(f"Netflix vibe finder - {titles.count()} titles loaded.")
    if titles.count() == 0:
        print("The database is empty. Run 'uv run load_data.py' first.")
        return
    while True:
        print()
        for key, (label, _) in MENU.items():
            print(f"{key}. {label}")
        print("q. Quit")
        choice = input("> ").strip().lower()
        if choice == "q":
            break
        if choice in MENU:
            MENU[choice][1]()
        else:
            print("Pick a number from the menu.")


if __name__ == "__main__":
    main()
