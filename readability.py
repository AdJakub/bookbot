def senCount(text):
    count = 0
    middle = len(text) // 2
    text = text[middle:]
    for i, char in enumerate(text):
        if char == ".":
            testStart = i - 15
            testEnd = i + 15
            print(text[testStart:testEnd])
            count += 1
            if count == 15:
                break
