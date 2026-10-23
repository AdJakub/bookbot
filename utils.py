import re

abrList = ["Mr", "Mrs"]
abrSet = frozenset(abrList)


def getBookText(path_to_file):
    with open(path_to_file) as f:
        file_contents = f.read()

    return file_contents


def getTitle(text):
    titlePos = text.index("Title:")
    title = text[titlePos + len("Title:") :].strip().split("\n")[0]
    return title


def getAuthor(text):
    authorPos = text.index("Author:")
    author = text[authorPos + len("Author:") :].strip().split("\n")[0]
    return author


def removeHeader(text):
    startBook = text.index("START OF THE PROJECT GUTENBERG EBOOK")
    endBook = text.index("*** END OF")
    noHeader = text[startBook:endBook]
    return noHeader


def getSentenceCount(text):
    sentences = 0
    pattern = re.compile(
        r"((?<=[a-z0-9I][.?!])|(?<=[a-z0-9I][.?!][\"“”‘’]))(\s+)(?=[\"“‘_]?[A-Z])"
    )
    for match in pattern.finditer(text):
        start = match.start()
        windowStart = max(0, start - 15)
        before = text[windowStart:start]
        word = before.split()[-1]
        wordProcessed = word.strip("""" ' “ ” ‘ ’ .""")

        if wordProcessed in abrSet:
            continue
        else:
            sentences += 1
    return sentences


def getSyllableCount(word):
    syllableCount = 0
    vowels = "aeiouy"
    if word[0] in vowels:
        syllableCount += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            syllableCount += 1
    if word.endswith("e"):
        syllableCount -= 1
    if word.endswith("le") and len(word) > 2 and word[-3] not in vowels:
        syllableCount += 1
    if syllableCount == 0:
        syllableCount += 1
    return syllableCount


def getSyllableTotal(text):
    count = 0
    for word in re.findall(r"[a-z]+(?:['’][a-z]+)?", text.lower()):
        count += getSyllableCount(word)
    return count


def printLogged(bookList):
    for book in bookList["books"]:
        print("ID: ", book["id"])
        print("\t Title:", book["Title"])
        print("\t Author:", book["Author"])
        print("\t Location:", book["Path"])
        print("\t Words:", book["word_count"])
        print("\t Sentences:", book["sentence_count"])
        print("\t Syllables:", book["syllable_count"])
        print("\t Flesch-Kincaid grade level:", int(book["Flesch-Kincaid"]))
        print("\t Read Count:", book["Read Count"])


#        if match in abrSet:
#            continue
#       else:
#           sentences += 1
