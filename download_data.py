"""Download both datasets into data/.

Run once:  uv run download_data.py
- Netflix titles (Kaggle, via kagglehub)
- CMU Movie Summary Corpus (Wikipedia plot summaries, Bamman et al. 2013)
"""

import shutil
import tarfile
import urllib.request
from pathlib import Path

import kagglehub

CMU_URL = "http://www.cs.cmu.edu/~ark/personas/data/MovieSummaries.tar.gz"

Path("data").mkdir(exist_ok=True)

# Download latest version (cached under ~/.cache/kagglehub)
path = kagglehub.dataset_download("shivamb/netflix-shows")
print("Path to dataset files:", path)
shutil.copy(Path(path) / "netflix_titles.csv", "data/netflix_titles.csv")
print("Copied to data/netflix_titles.csv")

cmu_dir = Path("data/cmu")
if not (cmu_dir / "MovieSummaries").exists():
    cmu_dir.mkdir(exist_ok=True)
    archive = cmu_dir / "MovieSummaries.tar.gz"
    print("Downloading CMU Movie Summary Corpus (46 MB)...")
    urllib.request.urlretrieve(CMU_URL, archive)
    with tarfile.open(archive) as tar:
        tar.extractall(cmu_dir, filter="data")
print("CMU plot summaries are in data/cmu/MovieSummaries")
