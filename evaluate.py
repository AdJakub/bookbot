import json
import statistics

from reccomender import MIN_RATING, buildProfile, recommend

corpusLocation = "./data/corpus.json"
libraryLocation = "./data/demo_books.json"
benchLocation = "./data/benchmark_readers.json"
with open(corpusLocation, "r") as c:
    corpus = json.load(c)

with open(libraryLocation, "r") as l:
    library = json.load(l)

with open(benchLocation, "r") as b:
    bench = json.load(b)


def leaveOneOut(library, corpus):
    ranks = []
    for book in library["books"]:
        if book["Rating"] is None:
            continue
        if book["Rating"] < MIN_RATING:
            continue
        leftOut = book["gutenberg_id"]
        smaller = {
            "books": [
                book for book in library["books"] if book["gutenberg_id"] != leftOut
            ]
        }
        results = recommend(smaller, corpus, topN=len(corpus["books"]))
        for i, result in enumerate(results):
            if result["gutenberg_id"] == leftOut:
                ranks.append(i + 1)
                break

    return (ranks, statistics.mean(ranks))


for reader in bench:
    print(reader["name"], leaveOneOut(reader["library"], corpus))

# Demo Library result is [75, 22, 8, 2, 201] 61.6
