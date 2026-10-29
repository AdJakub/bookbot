import json
import re
from math import floor

corpusLocation = "./data/corpus.json"
searchRe = re.compile(
    r"(^.+),\s[0-9]+[\?]?[\s]?(B\.C\.|A\.D\.)?-[0-9]+[\?]?[\s]?(B\.C\.|A\.D\.)?$"
)
with open(corpusLocation, "r") as c:
    corpus = json.load(c)


testBook = corpus["books"][0]


def normalizeSubjects(subjects):
    subjectRecords = []
    main_subject = None
    for subject in subjects:
        subParts = []
        splitSub = subject.split("--")
        for string in splitSub:
            cleanedString = string.strip()
            subParts.append(cleanedString)
        match_object = re.match(searchRe, subParts[0])
        if match_object is None:
            main_subject = subParts[0]
        else:
            main_subject = match_object.group(1)
        subjectRecord = {
            "original": subject,
            "main_subject": main_subject,
            "sub_subject": subParts[1:],
        }
        subjectRecords.append(subjectRecord)
    return subjectRecords


for book in corpus["books"]:
    records = normalizeSubjects(book["subjects"])
    book["subject_records"] = records
jsonized = json.dumps(corpus, indent=4)
with open(corpusLocation, "w") as c:
    c.write(jsonized)
