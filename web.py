"""Browser UI: a movie-screen page with a search bar, backed by the same ChromaDB search as app.py.

Run:  uv run web.py   then open http://localhost:8000
"""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from app import CANDIDATES, titles, top_movies

PORT = 8000
PAGE = Path(__file__).with_name("ui.html").read_bytes()


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/":
            self.send(200, "text/html; charset=utf-8", PAGE)
        elif url.path == "/search":
            query = parse_qs(url.query).get("q", [""])[0].strip()
            results = []
            if query:
                ids, metadatas, documents = top_movies(titles.query(query_texts=[query], n_results=CANDIDATES))
                results = [{**meta, "passage": doc} for meta, doc in zip(metadatas, documents)]
            self.send(200, "application/json", json.dumps(results).encode())
        else:
            self.send(404, "text/plain", b"Not found")

    def send(self, status, content_type, body):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    print(f"Open http://localhost:{PORT}")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
