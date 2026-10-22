def countWords(text):
    words = text.split()
    wordCount = len(words)
    return wordCount


def countChars(text):
    charCount = {}
    lowerText = text.lower()
    for char in lowerText:
        if char in charCount:
            charCount[char] += 1
        else:
            charCount[char] = 1
    return charCount


def sortOn(list: tuple[str, int]):
    return list[1]


def charsDictToSortedList(charCount: dict[str, int]):
    list = []
    for char in charCount:
        list.append((char, charCount[char]))

    sortedList = sorted(list, reverse=True, key=sortOn)

    return sortedList
