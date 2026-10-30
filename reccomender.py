import json
import math
import statistics
from collections import defaultdict
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
# parked subsubject socring
WEAK_CREDIT = 1.0


def minutes(book):
    return book["word_count"] / READING_SPEED


def isProse(book):
    return REFERENCE_SHELF not in book["bookshelves"]


def closeness(value, typical, valueRange):
    distance = abs(value - typical)
    fraction = distance / valueRange
    result = 1 - fraction
    return max(0, result)


def jaccardSimilarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    if union == 0:
        return 0
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
    likedPaths = defaultdict(set)

    for book in library["books"]:
        excludedBooks.add(book["gutenberg_id"])
        if book["Rating"] != None:
            if int(book["Rating"]) >= MIN_RATING:
                gid = book["gutenberg_id"]
                if gid not in corpusById:
                    continue
                likedShelves.update(corpusById[gid]["bookshelves"])
                readFk.append(corpusById[gid]["Flesch-Kincaid"])
                readRt.append(math.log(minutes(corpusById[gid])))
                for record in corpusById[gid]["subject_records"]:
                    if record["main_subject"]:
                        likedSubjects.add(record["main_subject"])
                        likedPaths[record["main_subject"]].add(
                            "Fiction" in record["sub_subject"]
                        )

    if not readFk:
        return None

    fkAverages = statistics.mean(readFk)
    rtAverages = statistics.median(readRt)
    allFk = []
    allRt = []

    for corpusBook in corpus["books"]:
        if isProse(corpusBook):
            allFk.append(corpusBook["Flesch-Kincaid"])
            allRt.append(math.log(minutes(corpusBook)))

    cutsFk = statistics.quantiles(allFk, n=20)
    fkLow = cutsFk[0]
    fkHigh = cutsFk[-1]
    cutsRt = statistics.quantiles(allRt, n=20)
    rtLow = cutsRt[0]
    rtHigh = cutsRt[-1]
    fkRange = fkHigh - fkLow
    rtRange = rtHigh - rtLow

    profile = {
        "likedSubjects": likedSubjects,
        "likedShelves": likedShelves,
        "likedPaths": likedPaths,
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
    candidateSubjects = set()
    candidatePaths = defaultdict(set)
    for record in book["subject_records"]:
        if record["main_subject"]:
            candidateSubjects.add(record["main_subject"])
            candidatePaths[record["main_subject"]].add(
                "Fiction" in record["sub_subject"]
            )
    sharedPaths = candidatePaths.keys() & profile["likedPaths"].keys()
    creditSum = 0
    for subject in sharedPaths:
        if candidatePaths[subject] & profile["likedPaths"][subject]:
            creditSum += 1.0
        else:
            creditSum += WEAK_CREDIT
    subDenom = len(candidateSubjects.union(profile["likedSubjects"]))
    if subDenom == 0:
        subjectSim = 0
    else:
        subjectSim = creditSum / subDenom

    fkSim = closeness(book["Flesch-Kincaid"], profile["fk"], profile["fkRange"])
    rtSim = closeness(math.log(minutes(book)), profile["rt"], profile["rtRange"])
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
        "gutenberg_id": book["gutenberg_id"],
    }


def recommend(library, corpus, topN=10):
    profile = buildProfile(library, corpus)

    if profile is None:
        return []

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
