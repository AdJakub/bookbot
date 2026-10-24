import json
import os
import sys
from pathlib import Path

bookDir = os.fsencode("./books")

from readability import senCount
from stats import charsDictToSortedList, countChars, countWords
from utils import (
    estimateReadingTime,
    getAuthor,
    getBookText,
    getGutenbergId,
    getSentenceCount,
    getSyllableTotal,
    getTitle,
    printLogged,
    rateBook,
    removeHeader,
)

if len(sys.argv) not in (2, 3, 4):
    print(
        "Usage: python3 main.py analyze/log <path_to_book> OR python3 main.py logged to view log"
    )
    sys.exit(1)

mode = sys.argv[1]
if len(sys.argv) > 2:
    path_to_file = sys.argv[2]
dataLocation = "./data/books.json"
corpusLocation = "./data/corpus.json"

with open(dataLocation, "r") as j:
    bookList = json.load(j)

with open(corpusLocation, "r") as c:
    corpus = json.load(c)
# bookList = json.load(dataLocation)


def main():
    if mode == "logged":
        printLogged(bookList)
        return
    if mode == "rate" and int(sys.argv[3]) in range(1, 11):
        rateBook(bookList, path_to_file, sys.argv[3])
        return ()
    if mode == "fill":
        fillCorpus()
        return ()
    elif mode == "rate":
        print("Select a rating between 1 and 10")
        return
    headeredText = getBookText(path_to_file)
    bookText = removeHeader(headeredText)
    wordCount = countWords(bookText)
    charCount = countChars(bookText)
    charList = charsDictToSortedList(charCount)
    sentenceCount = getSentenceCount(bookText)
    syllableCount = getSyllableTotal(bookText)
    author = getAuthor(headeredText)
    title = getTitle(headeredText)
    readingTime = estimateReadingTime(wordCount)
    gutenbergId = getGutenbergId(headeredText)
    fkReadingGrade = (
        0.39 * (wordCount / sentenceCount) + 11.8 * (syllableCount / wordCount) - 15.59
    )
    fkFLoored = int(fkReadingGrade)
    if mode == "analyze":
        printReport(
            path_to_file,
            wordCount,
            charList,
            sentenceCount,
            syllableCount,
            fkFLoored,
            author,
            title,
            readingTime,
        )
    elif mode == "log":
        readBook(
            title,
            author,
            wordCount,
            sentenceCount,
            syllableCount,
            fkReadingGrade,
            gutenbergId,
        )
        print(f"Succesfuly logged {title} by {author}!")
        return ()
    else:
        print("Usage: python3 main.py analyze/log <path_to_book>")
        return ()


def readBook(
    title, author, wordCount, sentenceCount, syllableCount, fkReadingGrade, gutenbergId
):
    if bookList["books"]:
        newId = bookList["books"][-1]["id"] + 1
    else:
        newId = 1
    foundBook = None
    for book in bookList["books"]:
        if book["Title"] == title:
            foundBook = book
            break
    if foundBook != None:
        # if book["Read Count"] > 0:
        foundBook["Read Count"] += 1
    else:
        tempDict = {
            "gutenberg_id": gutenbergId,
            "id": newId,
            "Title": title,
            "Author": author,
            "Path": path_to_file,
            "word_count": wordCount,
            "sentence_count": sentenceCount,
            "syllable_count": syllableCount,
            "Flesch-Kincaid": fkReadingGrade,
            "Read Count": 1,
            "Rating": None,
        }
        bookList["books"].append(tempDict)
    with open(dataLocation, "w") as d:
        json.dump(bookList, d, indent=4)


def printReport(
    path_to_file,
    wordCount,
    charList,
    sentenceCount,
    syllableCount,
    fkFloored,
    author,
    title,
    readingTime,
):
    print(
        f"============ BOOKBOT ============\nAnalyzing {title} by {author}.\n----------- Word Count ----------\nFound {wordCount} total words\n--------- Character Count -------"
    )
    for char, count in charList:
        if not char.isalpha():
            continue
        print(f"{char}: {count}")
    print(f"--------- Sentence Count ---------\nNumber of sentences: {sentenceCount}")
    print(f"--------- Syllable Count ---------\nNumber of syllables: {syllableCount}")
    print(f"--------- Flesch-Kincaid Reading Grade---------\n {fkFloored}th grade")
    print(
        f"--------- Estimated reading time ---------\n {readingTime} hours at 260 WPM"
    )
    print("============= END ===============")


def dotCount():
    bookText = getBookText(path_to_file)
    dotList = senCount(bookText)


def basicCorpusAnalysis(path):
    headeredText = getBookText(path)
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
        "Path": str(path),
        "word_count": wordCount,
        "sentence_count": sentenceCount,
        "syllable_count": syllableCount,
        "Flesch-Kincaid": fkReadingGrade,
        "Reading time": readingTime,
    }
    return tempDict


def fillCorpus():
    for path in Path("./books").glob("*.txt"):
        result = basicCorpusAnalysis(path)
        result["subjects"] = None
        result["bookshelves"] = None

        corpus["books"].append(result)

    with open(corpusLocation, "w") as d:
        json.dump(corpus, d, indent=4)


main()
