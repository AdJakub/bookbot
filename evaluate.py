import json
import statistics

import reccomender
from reccomender import MIN_RATING, buildProfile, recommend

corpusLocation = "./data/corpus.json"
libraryLocation = "./data/demo_books.json"
benchLocation = "./data/benchmark_mixed_ratings.json"
with open(corpusLocation, "r") as c:
    corpus = json.load(c)

with open(libraryLocation, "r") as l:
    library = json.load(l)

with open(benchLocation, "r") as b:
    bench = json.load(b)

candidateWeights = [0, 0.25, 0.5, 1, 2]


def leaveOneOut(library, corpus):
    ranks = []
    for book in library["books"]:
        if book["Rating"] is None:
            continue
        if book["Rating"] < 10:
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

    return ranks


allRanks = []
rankPerReader = {}
for reader in bench:
    result = leaveOneOut(reader["library"], corpus)
    allRanks.extend(result)
    rankPerReader[reader["name"]] = result
for reader, result in rankPerReader.items():
    print(reader, statistics.mean(result), result)
mean = statistics.mean(allRanks)
median = statistics.median(allRanks)
tenOrLower = 0
twentyfiveOrLower = 0
overHundred = 0
for rank in allRanks:
    if rank <= 10:
        tenOrLower += 1
    if rank <= 25:
        twentyfiveOrLower += 1
    if rank >= 100:
        overHundred += 1
print(mean, median, tenOrLower, twentyfiveOrLower, overHundred, sorted(allRanks)[-15:])


# Demo Library result is [75, 22, 8, 2, 201] 61.6
