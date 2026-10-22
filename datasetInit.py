import sys
from collections import Counter

from utils import getBookText

if len(sys.argv) != 2:
    print("Usage: python3 datasetInit.py <path_to_book>")
    sys.exit(1)

book = sys.argv[1]
bookText = getBookText(book)

c = Counter()

for word in bookText.split():
    if word.endswith("."):
        wordProcessed = word.strip("""" ' “ ” ‘ ’ .""")
        c[wordProcessed] += 1

print(c.most_common(50))
