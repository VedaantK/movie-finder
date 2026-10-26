# Prompt Log

## AI tools used
- **Claude Code** (Claude Opus 5.5, in the terminal): planning, writing code, testing, git/GitHub setup, and README guidance.

## Development process
1. Picked a project idea (a semantic movie finder) after rejecting a more complex first suggestion.
2. Built the data loader, then tested it on a 3-row sample before loading the real data.
3. Downloaded the Netflix dataset with kagglehub and loaded 8,807 titles into a persistent ChromaDB collection.
4. Found test queries by trial and error, checking each one for shared words with the matching description. One query failed and is noted in the README.
5. Built the terminal menu (search, add, more like this, watchlist, surprise me) and tested it on a copy of the database, including a restart to check persistence.
6. Created the GitHub repo and added the project to my portfolio site.
7. Added the CMU Movie Summary Corpus (top 5,000 movies by box office), split plots into sentence chunks, and merged them into the same search.
8. Built a browser UI styled like a movie theater, then fixed the layout so the screen fills the frame.
9. Wrote the README myself, using a template of section prompts and feedback on my drafts.

## Prompts (verbatim, in order)

**1.** Can you make me a Movie Finder using vector data bases that meets the crieteria for this assignment. https://www.cs.cmu.edu/~113/hw6.html

**2.** yes start with the loading script

> Set up the project with uv (Python 3.12, ChromaDB 1.5.9, pandas), wrote `load_data.py` (persistent client, batched `upsert`, description embedded, other fields as metadata), and tested it on a 3-row sample.

**3.** (Pasted the kagglehub download snippet from Kaggle:)
```python
import kagglehub

# Download latest version
path = kagglehub.dataset_download("shivamb/netflix-shows")

print("Path to dataset files:", path)
```

> Turned it into `download_data.py`, downloaded the data, loaded all 8,807 titles, and searched for test queries with no shared words. Found two that work and one that failed.

**4.** yes build the menu

> Wrote `app.py`: search by vibe with a movie/TV filter, add a title, more like this, a watchlist collection, and "surprise me" (average of watchlist embeddings). Tested it with scripted input on a copy of the database, including a restart.

**5.** set up the git repo

> Committed the code (dataset and database excluded by `.gitignore`). I chose **Public** visibility, then it created github.com/VedaantK/movie-finder and pushed.

**6.** Can you add it to my webiste at vedaantk.github.io

> Added a "MOVIE FINDER" project card to my portfolio with a link to the repo, checked it in a browser, and pushed.

**7.** Does a UI not need to be created?

> Answered that a CLI is enough for full credit and a web UI is optional.

**8.** Can you pull data from here too https://www.cs.cmu.edu/~ark/personas/

> Downloaded the CMU Movie Summary Corpus and measured it: 42,306 plots, median ~190 words, ~109,000 chunks if fully loaded. I chose **the top ~5,000 movies by box office** (to keep loading time reasonable) and **merging them into one search**. Wrote `load_plots.py` (sentence chunks of at most ~150 words, `movie_id` metadata) and updated `app.py` to show each movie once. Result: 23,584 chunks, 32,391 items total.

**9.** Can you generate a simple UI with a nice movie screen like framing and a searchbar in the middle. thats all.

> Wrote `web.py` (a small server using Python's standard library) and `ui.html` (curtains, marquee, screen with a centered search bar). Checked it in a browser.

**10.** Can you make sure the framing is all good with no blank area and then also add it to the normal github pag

> Changed the layout so the screen fills the space between the curtains and seats, checked desktop and phone widths, and pushed the code to GitHub.

**11.** Is that not a part of the requirements of the page I gave you

> Answered that the portfolio entry only needs a repo link and description; a hosted demo is optional.

**12.** Ill spend it on the readme, can you just keep it blank for now with prompts of what I should write about and also open a visual studio project where I can see the project

> Created a README template with prompts under each required section, installed VS Code, and opened the project.

**13.** Can you check if my other two answers are correct and then for the following questions can you give me suggestions on how to answer it. Can you also give me the link to the website again

> Reviewed my first two README sections (correct but thin, plus formatting and typos) and gave suggestions for the remaining sections. Also re-ran the test queries on the full data: Harry Potter now ranks first for the second query but shares the word "academy".

**14.** Check again now

**15.** Can you check everything, and then also make a prompt log with everything

> Reviewed the full README and wrote this prompt log.
