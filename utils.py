import re

abrList = ["Mr", "Mrs"]
abrSet = frozenset(abrList)


def getBookText(path_to_file):
    with open(path_to_file) as f:
        file_contents = f.read()

    return file_contents


def removeHeader(text):
    startBook = text.index("START OF THE PROJECT GUTENBERG EBOOK")
    endBook = text.index("*** END OF")
    noHeader = text[startBook:endBook]
    return noHeader


def getSentenceCount(text):
    sentences = 0
    pattern = re.compile(
        r"((?<=[a-z0-9][.?!])|(?<=[a-z0-9][.?!]\"))(\s|\r\n)(?=\"?[A-Z])"
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


#        if match in abrSet:
#            continue
#       else:
#           sentences += 1
