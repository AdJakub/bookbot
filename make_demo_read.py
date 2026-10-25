import json

ratings = {2600: 8, 2554: 10, 345: 7, 768: 8, 5200: 8, 65238: 3}

with open("data/corpus.json", "r") as f:
    corpus = json.load(f)

corpusById = {b["gutenberg_id"]: b for b in corpus["books"]}

books = []
for i, (gid, rating) in enumerate(ratings.items(), start=1):
    if gid not in corpusById:
        print(f"Not in corpus. skipping {gid}")
        continue
    b = corpusById[gid]
    books.append(
        {
            "gutenberg_id": gid,
            "id": i,
            "Title": b["Title"],
            "Author": b["Author"],
            "word_count": b["word_count"],
            "sentence_count": b["sentence_count"],
            "syllable_count": b["syllable_count"],
            "Flesch-Kincaid": b["Flesch-Kincaid"],
            "Read Count": 1,
            "Rating": rating,
        }
    )
with open("data/demo_books.json", "w") as f:
    json.dump({"version": corpus.get("version", 1), "books": books}, f, indent=4)

    print(f"wrote {len(books)} books")
