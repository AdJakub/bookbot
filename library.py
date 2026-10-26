from stats import countWords
from utils import (
    estimateReadingTime,
    getAuthor,
    getGutenbergId,
    getSentenceCount,
    getSyllableTotal,
    getTitle,
    removeHeader,
)


def analyzeText(headeredText):
    bookText = removeHeader(headeredText)
    wordCount = countWords(bookText)
    sentenceCount = getSentenceCount(bookText)
    syllableCount = getSyllableTotal(bookText)
    author = getAuthor(headeredText)
    title = getTitle(headeredText)
    readingTime = estimateReadingTime(wordCount)
    gutenbergId = getGutenbergId(headeredText)
    fkReadingGrade = (
        0.39 * (wordCount / sentenceCount) + 11.8 * (syllableCount / wordCount) - 15.59
    )

    tempDict = {
        "gutenberg_id": gutenbergId,
        "Title": title,
        "Author": author,
        "word_count": wordCount,
        "sentence_count": sentenceCount,
        "syllable_count": syllableCount,
        "Flesch-Kincaid": fkReadingGrade,
        "Reading time": readingTime,
    }
    return tempDict


def addBook(library, result, path=None):
    if library["books"]:
        newId = library["books"][-1]["id"] + 1
    else:
        newId = 1
    foundBook = None
    for book in library["books"]:
        if book["gutenberg_id"] == result["gutenberg_id"]:
            foundBook = book
            break
    if foundBook != None:
        # if book["Read Count"] > 0:
        foundBook["Read Count"] += 1
        return foundBook
    else:
        tempDict = {
            "gutenberg_id": result["gutenberg_id"],
            "id": newId,
            "Title": result["Title"],
            "Author": result["Author"],
            "Path": path,
            "word_count": result["word_count"],
            "sentence_count": result["sentence_count"],
            "syllable_count": result["syllable_count"],
            "Flesch-Kincaid": result["Flesch-Kincaid"],
            "Read Count": 1,
            "Rating": None,
        }
        library["books"].append(tempDict)
        return tempDict


def setRating(library, gutenbergId, rating):
    for book in library["books"]:
        if gutenbergId == book["gutenberg_id"]:
            book["Rating"] = rating
            return True
    return False
