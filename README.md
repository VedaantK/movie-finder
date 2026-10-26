# Movie Finder

## What it does

This is a movie finder where you quickly describe the plot or something that happened in a movie. Then the system will search through datasets of movies and it will suggest a movie that is simillar to the prompt that was described.

## Data
I used two data sets, they are:

     - Netflix Movies and TV Shows from Kaggle ((kaggle.com/datasets/shivamb/netflix-shows))
          - 8,807 titles with related info
     - CMU Movie Summary Corpus ((cs.cmu.edu/~ark/personas/))
          - Top 5,000 by box office. 

### Chunking
     - The plot descriptions from the Netflix data sets is only a few scentances that have the key information

     - For the CMU data set the model splits each plot into chunks of scentences.  

## How it works
     - Asks for title, description or other basic information about a movie
     - Search uses ChromaDB to return items with closes embeds to the search
     - Also has other features like More Like this, Watchlist and Suprise me which takes movies that you are interesed in and finds one that matches themes from all of them

## Vector database and embedding model
     - ChromaDB 1.5.9 usings its Mini model to process things

## Test queries

Prompt: Federal agent probes a vanished asylum inmate while haunted by hallucinations and flashbacks
Result: Shutter Island

Prompt: Costumed heroesteam up against a purple  space tyrant who wants magic gems to erase 50% of every living thing
Results: Avengers Infinity War


## Getting the data
 uv run download_data.py downloads both datasets into data.

## How to run
1. Install uv.
2. git clone the repo, then cd movie-finder.
3. uv sync
4. uv run download_data.py
5. uv run load_data.py
6. uv run load_plots.py
7. Then either uv run app.py for the terminal menu, or uv run web.py and open http://localhost:8000 for the browser UI.

## AI usage
     - Used Claude Code to help plan out the project, make the UI and also strucute the chunking.

## Citations 
     - Bamman, O'Connor & Smith, Learning Latent Personas of Film Characters, ACL 2013, licensed CC BY-SA 3.0 US