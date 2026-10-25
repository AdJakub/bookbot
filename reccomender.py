import json
from collections import Counter

dataLocation = "./data/books.json"
corpusLocation = "./data/corpus.json"

with open(dataLocation, "r") as j:
    bookList = json.load(j)

with open(corpusLocation, "r") as c:
    corpus = json.load(c)

corpusById = {}
for corpusBook in corpus["books"]:
    corpusById[corpusBook["gutenberg_id"]] = corpusBook

likedSubjects = set()
excludedBooks = set()

for book in bookList["books"]:
    excludedBooks.add(book["gutenberg_id"])
    if book["Rating"] != None:
        if int(book["Rating"]) >= 7:
            gid = book["gutenberg_id"]
            likedSubjects.update(corpusById[gid]["subjects"])

scores = Counter()
recList = []

for corpusBook in corpus["books"]:
    if corpusBook["gutenberg_id"] in excludedBooks:
        continue
    r = likedSubjects.intersection(corpusBook["subjects"])
    scores[corpusBook["gutenberg_id"]] = len(r)

for rec in scores.most_common(5):
    author = corpusById[rec[0]]["Author"]
    title = corpusById[rec[0]]["Title"]
    formatted = {"Author": author, "Title": title, "W1": rec[1]}
    recList.append(formatted)

print(recList)
