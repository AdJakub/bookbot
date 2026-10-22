import sys

from stats import charsDictToSortedList, countChars, countWords

if len(sys.argv) != 2:
    print("Usage: python3 main.py <path_to_book>")
    sys.exit(1)

path_to_file = sys.argv[1]


def getBookText(path_to_file):
    with open(path_to_file) as f:
        file_contents = f.read()

    return file_contents


def main():
    bookText = getBookText(path_to_file)
    wordCount = countWords(bookText)
    charCount = countChars(bookText)
    charList = charsDictToSortedList(charCount)
    printReport(path_to_file, wordCount, charList)


def printReport(path_to_file, wordCount, charList):
    print(
        f"============ BOOKBOT ============\nAnalyzing book found at {path_to_file}...\n----------- Word Count ----------\nFound {wordCount} total words\n--------- Character Count -------"
    )
    for char, count in charList:
        if not char.isalpha():
            continue

        print(f"{char}: {count}")
    print("============= END ===============")


main()
