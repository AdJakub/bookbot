import json
import sys

from readability import senCount
from stats import charsDictToSortedList, countChars, countWords
from utils import (
    getAuthor,
    getBookText,
    getSentenceCount,
    getSyllableTotal,
    getTitle,
    printLogged,
    removeHeader,
)

if len(sys.argv) not in (2, 3):
    print(
        "Usage: python3 main.py analyze/log <path_to_book> OR python3 main.py logged to view log"
    )
    sys.exit(1)

mode = sys.argv[1]
if len(sys.argv) < 2:
    path_to_file = sys.argv[2]
dataLocation = "./data/books.json"

with open(dataLocation, "r") as j:
    bookList = json.load(j)

# bookList = json.load(dataLocation)


def main():
    if mode == "logged":
        printLogged(bookList)
        return ()
    headeredText = getBookText(path_to_file)
    bookText = removeHeader(headeredText)
    wordCount = countWords(bookText)
    charCount = countChars(bookText)
    charList = charsDictToSortedList(charCount)
    sentenceCount = getSentenceCount(bookText)
    syllableCount = getSyllableTotal(bookText)
    author = getAuthor(headeredText)
    title = getTitle(headeredText)
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
        )
    elif mode == "log":
        readBook(title, author, wordCount, sentenceCount, syllableCount, fkReadingGrade)
        print(f"Succesfuly logged {title} by {author}!")
        return ()
    else:
        print("Usage: python3 main.py analyze/log <path_to_book>")
        return ()


def readBook(title, author, wordCount, sentenceCount, syllableCount, fkReadingGrade):
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
            "id": newId,
            "Title": title,
            "Author": author,
            "Path": path_to_file,
            "word_count": wordCount,
            "sentence_count": sentenceCount,
            "syllable_count": syllableCount,
            "Flesch-Kincaid": fkReadingGrade,
            "Read Count": 1,
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
    print("============= END ===============")


def dotCount():
    bookText = getBookText(path_to_file)
    dotList = senCount(bookText)


main()
