import sys

from readability import senCount
from stats import charsDictToSortedList, countChars, countWords
from utils import getBookText, getSentenceCount, removeHeader

if len(sys.argv) != 2:
    print("Usage: python3 main.py <path_to_book>")
    sys.exit(1)

path_to_file = sys.argv[1]


def main():
    headeredText = getBookText(path_to_file)
    bookText = removeHeader(headeredText)
    wordCount = countWords(bookText)
    charCount = countChars(bookText)
    charList = charsDictToSortedList(charCount)
    sentenceCount = getSentenceCount(bookText)
    printReport(path_to_file, wordCount, charList, sentenceCount)


def printReport(path_to_file, wordCount, charList, sentenceCount):
    print(
        f"============ BOOKBOT ============\nAnalyzing book found at {path_to_file}...\n----------- Word Count ----------\nFound {wordCount} total words\n--------- Character Count -------"
    )
    for char, count in charList:
        if not char.isalpha():
            continue

        print(f"{char}: {count}")
    print(f"--------- Sentence Count ---------\nNumber of sentences: {sentenceCount}")
    print("============= END ===============")


def dotCount():
    bookText = getBookText(path_to_file)
    dotList = senCount(bookText)


main()
