import json
import statistics
from operator import itemgetter

dataLocation = "./data/books.json"
corpusLocation = "./data/corpus.json"

READING_SPEED = 260
REFERENCE_SHELF = "Category: Encyclopedias/Dictionaries/Reference"
MIN_RATING = 7


W_SUBJECT = 1
W_SHELF = 0.5
W_FK = 0.15
W_TIME = 0.15


def minutes(book):
    return book["word_count"] / READING_SPEED


def isProse(book):
    return REFERENCE_SHELF not in book["bookshelves"]


def closeness(value, typical, valueRange):
    distance = abs(value - typical)
    fraction = distance / valueRange
    return 1 - fraction


def jaccardSimilarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union


def buildProfile(library, corpus):
    corpusById = {}
    for corpusBook in corpus["books"]:
        corpusById[corpusBook["gutenberg_id"]] = corpusBook

    likedShelves = set()
    likedSubjects = set()
    readFk = []
    readRt = []
    excludedBooks = set()

    for book in library["books"]:
        excludedBooks.add(book["gutenberg_id"])
        if book["Rating"] != None:
            if int(book["Rating"]) >= MIN_RATING:
                gid = book["gutenberg_id"]
                likedShelves.update(corpusById[gid]["bookshelves"])
                readFk.append(corpusById[gid]["Flesch-Kincaid"])
                readRt.append(minutes(corpusById[gid]))
                likedSubjects.update(corpusById[gid]["subjects"])

    fkAverages = statistics.mean(readFk)
    rtAverages = statistics.median(readRt)
    allFk = []
    allRt = []

    for corpusBook in corpus["books"]:
        if isProse(corpusBook):
            allFk.append(corpusBook["Flesch-Kincaid"])
            allRt.append(minutes(corpusBook))

    fkRange = max(allFk) - min(allFk)
    rtRange = max(allRt) - min(allRt)

    profile = {
        "likedSubjects": likedSubjects,
        "likedShelves": likedShelves,
        "fk": fkAverages,
        "rt": rtAverages,
        "fkRange": fkRange,
        "rtRange": rtRange,
        "readIds": excludedBooks,
    }
    return profile


# for corpusBook in corpus["books"]:

#    if isProse(corpusBook):
#    continue
# if corpusBook["gutenberg_id"] in excludedBooks:
#    continue


def scoreBook(book, profile):
    fkSim = closeness(book["Flesch-Kincaid"], profile["fk"], profile["fkRange"])
    rtSim = closeness(minutes(book), profile["rt"], profile["rtRange"])
    subjectSim = jaccardSimilarity(profile["likedSubjects"], set(book["subjects"]))
    shelfSim = jaccardSimilarity(profile["likedShelves"], set(book["bookshelves"]))
    total = W_SUBJECT * subjectSim + W_SHELF * shelfSim + W_FK * fkSim + W_TIME * rtSim
    return {
        "Author": book["Author"],
        "Title": book["Title"],
        "Score": total,
        "FK": fkSim,
        "RT": rtSim,
        "Subject": subjectSim,
        "Shelf": shelfSim,
    }


def recommend(library, corpus, topN=10):
    profile = buildProfile(library, corpus)

    results = []
    for corpusBook in corpus["books"]:
        if not isProse(corpusBook):
            continue
        if corpusBook["gutenberg_id"] in profile["readIds"]:
            continue
        results.append(scoreBook(corpusBook, profile))
    results.sort(key=itemgetter("Score"), reverse=True)
    top = results[:topN]

    return top


if __name__ == "__main__":
    with open(dataLocation, "r") as j:
        bookList = json.load(j)

    with open(corpusLocation, "r") as c:
        corpus = json.load(c)

    for rec in recommend(bookList, corpus):
        print(f"{rec['Score']:.3f} {rec['Title']} by {rec['Author']}")
