import json
import statistics
from collections import Counter
from operator import itemgetter

dataLocation = "./data/books.json"
corpusLocation = "./data/corpus.json"

W_SUBJECT = 1
W_SHELF = 0.5
W_FK = 0.15
W_TIME = 0.15


def jaccardSimilarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union


with open(dataLocation, "r") as j:
    bookList = json.load(j)

with open(corpusLocation, "r") as c:
    corpus = json.load(c)

corpusById = {}
for corpusBook in corpus["books"]:
    corpusById[corpusBook["gutenberg_id"]] = corpusBook

likedShelves = set()
likedSubjects = set()
readFk = []
readRt = []

excludedBooks = set()

for book in bookList["books"]:
    if book["Rating"] != None:
        if int(book["Rating"]) >= 7:
            gid = book["gutenberg_id"]
            likedShelves.update(corpusById[gid]["bookshelves"])
            readFk.append(corpusById[gid]["Flesch-Kincaid"])
            readRt.append(corpusById[gid]["word_count"] / 260)

fkAverages = statistics.mean(readFk)
rtAverages = statistics.median(readRt)
allFk = []
allRt = []

for corpusBook in corpus["books"]:
    if (
        "Category: Encyclopedias/Dictionaries/Reference"
        not in corpusBook["bookshelves"]
    ):
        allFk.append(corpusBook["Flesch-Kincaid"])
        allRt.append(corpusBook["word_count"] / 260)

fkRange = max(allFk) - min(allFk)
rtRange = max(allRt) - min(allRt)


for book in bookList["books"]:
    excludedBooks.add(book["gutenberg_id"])
    if book["Rating"] != None:
        if int(book["Rating"]) >= 7:
            gid = book["gutenberg_id"]
            likedSubjects.update(corpusById[gid]["subjects"])

subjectScore = {}
shelfScore = {}
scoreTotal = {}
recList = []
fkScore = {}
rtScore = {}

for corpusBook in corpus["books"]:
    if "Category: Encyclopedias/Dictionaries/Reference" in corpusBook["bookshelves"]:
        continue
    if corpusBook["gutenberg_id"] in excludedBooks:
        continue
    fkDistance = abs(corpusBook["Flesch-Kincaid"] - fkAverages)
    fkSim = 1 - fkDistance / fkRange
    rtDistance = abs(corpusBook["word_count"] / 260 - rtAverages)
    rtSim = 1 - rtDistance / rtRange
    subjectSim = jaccardSimilarity(likedSubjects, set(corpusBook["subjects"]))
    shelfSim = jaccardSimilarity(likedShelves, set(corpusBook["bookshelves"]))
    subjectScore[corpusBook["gutenberg_id"]] = subjectSim
    shelfScore[corpusBook["gutenberg_id"]] = shelfSim
    fkScore[corpusBook["gutenberg_id"]] = fkSim
    rtScore[corpusBook["gutenberg_id"]] = rtSim
    scoreTotal[corpusBook["gutenberg_id"]] = (
        W_SUBJECT * subjectSim + W_SHELF * shelfSim + W_FK * fkSim + W_TIME * rtSim
    )


for rec in sorted(scoreTotal.items(), reverse=True, key=itemgetter(1))[:10]:
    author = corpusById[rec[0]]["Author"]
    title = corpusById[rec[0]]["Title"]
    formatted = {
        "Author": author,
        "Title": title,
        "Score": rec[1],
        "FK": fkScore[rec[0]],
        "RT": rtScore[rec[0]],
    }
    recList.append(formatted)


print(recList)
