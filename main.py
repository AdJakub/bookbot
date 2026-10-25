import json
import os
import sys
from pathlib import Path

import requests
from reccomender import recommend

bookDir = os.fsencode("./books")

from library import addBook, analyzeText
from readability import senCount
from stats import charsDictToSortedList, countChars
from utils import (
    getBookText,
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
    if mode == "recommend":
        for rec in recommend(bookList, corpus):
            print(f"{rec['Score']:.3f} {rec['Title']} by {rec['Author']}")
        return

    if mode == "rate" and int(sys.argv[3]) in range(1, 11):
        rateBook(bookList, path_to_file, sys.argv[3])
        return ()
    if mode == "fill":
        fillCorpus()
        return ()
    if mode == "enrich":
        enrichCorpus()
        return
    elif mode == "rate":
        print("Select a rating between 1 and 10")
        return
    headeredText = getBookText(path_to_file)
    bookText = removeHeader(headeredText)
    charCount = countChars(bookText)
    charList = charsDictToSortedList(charCount)
    result = analyzeText(headeredText)
    wordCount = result["word_count"]
    sentenceCount = result["sentence_count"]
    syllableCount = result["syllable_count"]
    author = result["Author"]
    title = result["Title"]
    readingTime = result["Reading time"]
    gutenbergId = result["gutenberg_id"]
    fkReadingGrade = result["Flesch-Kincaid"]
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
        readBook(result)
        print(f"Succesfuly logged {title} by {author}!")
        return ()
    else:
        print("Usage: python3 main.py analyze/log <path_to_book>")
        return ()


def readBook(result):
    addBook(bookList, result, path_to_file)
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
    result = analyzeText(headeredText)
    result["Path"] = str(path)
    return result


def fillCorpus():
    for path in Path("./books").glob("*.txt"):
        result = basicCorpusAnalysis(path)
        result["subjects"] = None
        result["bookshelves"] = None

        corpus["books"].append(result)

    with open(corpusLocation, "w") as d:
        json.dump(corpus, d, indent=4)


def enrichCorpus():
    list = []
    index = {}
    for book in corpus["books"]:
        index[book["gutenberg_id"]] = book
    for book in corpus["books"]:
        if book["subjects"] is None:
            list.append(book["gutenberg_id"])
    for start in range(0, len(list), 32):
        chunk = list[start : start + 32]
        response = requests.get(
            "https://gutendex.com/books", params={"ids": ",".join(map(str, chunk))}
        )
        data = response.json()
        for item in data["results"]:
            record = index[item["id"]]
            record["subjects"] = item["subjects"]
            record["bookshelves"] = item["bookshelves"]
    text = json.dumps(corpus, indent=4)
    with open(corpusLocation, "w") as f:
        f.write(text)


main()
