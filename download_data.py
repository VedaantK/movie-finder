"""Download the Netflix titles dataset from Kaggle into data/.

Run once:  uv run download_data.py
"""

import shutil
from pathlib import Path

import kagglehub

# Download latest version (cached under ~/.cache/kagglehub)
path = kagglehub.dataset_download("shivamb/netflix-shows")
print("Path to dataset files:", path)

Path("data").mkdir(exist_ok=True)
shutil.copy(Path(path) / "netflix_titles.csv", "data/netflix_titles.csv")
print("Copied to data/netflix_titles.csv")
