import pytest
from reccomender import buildProfile, closeness, jaccardSimilarity, recommend, scoreBook

testBookAC = {
    "Author": "x",
    "Title": "t",
    "gutenberg_id": 1,
    "subject_records": [{"main_subject": "A"}, {"main_subject": "C"}],
    "Flesch-Kincaid": 10,
    "word_count": 26000,
    "bookshelves": [],
}

testBookC = {
    "Author": "x",
    "Title": "t",
    "gutenberg_id": 1,
    "subject_records": [{"main_subject": "C"}],
    "Flesch-Kincaid": 10,
    "word_count": 26000,
    "bookshelves": [],
}

testBookNoSubjects = {
    "Author": "x",
    "Title": "t",
    "gutenberg_id": 1,
    "subject_records": [],
    "Flesch-Kincaid": 10,
    "word_count": 26000,
    "bookshelves": [],
}

testBookA = {
    "Author": "x",
    "Title": "t",
    "gutenberg_id": 1,
    "subject_records": [{"main_subject": "A"}],
    "Flesch-Kincaid": 10,
    "word_count": 26000,
    "bookshelves": [],
}

testBookB = {
    "Author": "x",
    "Title": "t",
    "gutenberg_id": 1,
    "subject_records": [{"main_subject": "B"}],
    "Flesch-Kincaid": 10,
    "word_count": 26000,
    "bookshelves": [],
}

testProfile = {
    "likedSubjects": {"A", "B"},
    "subjectWeights": {"A": 2, "B": 3, "C": 4},
    "share": {"A": 1.0, "B": 0.5},
    "likedShelves": set(),
    "fk": 10,
    "rt": 5,
    "fkRange": 10,
    "rtRange": 2,
}

emptyProfile = {
    "likedSubjects": set(),
    "subjectWeights": {},
    "share": {},
    "likedShelves": set(),
    "fk": 10,
    "rt": 5,
    "fkRange": 10,
    "rtRange": 2,
}

shareProfile = {
    "likedSubjects": {"A", "B"},
    "subjectWeights": {"A": 3, "B": 3},
    "share": {"A": 1.0, "B": 0.5},
    "likedShelves": set(),
    "fk": 10,
    "rt": 5,
    "fkRange": 10,
    "rtRange": 2,
}

testCorpus1 = {
    "books": [
        {
            "gutenberg_id": 1,
            "Author": "x",
            "Title": "t",
            "subject_records": [{"main_subject": "A"}],
            "Flesch-Kincaid": 10,
            "word_count": 26000,
            "bookshelves": [],
        }
    ]
}

testCorpus2 = {
    "books": [
        {
            "gutenberg_id": 67,
            "Author": "x",
            "Title": "t",
            "subject_records": [],
            "Flesch-Kincaid": 10,
            "word_count": 26000,
            "bookshelves": [],
        },
        {
            "gutenberg_id": 2137,
            "Author": "x",
            "Title": "t",
            "subject_records": [],
            "Flesch-Kincaid": 12,
            "word_count": 213700000,
            "bookshelves": [],
        },
    ]
}

testLibrary = {
    "books": [{"gutenberg_id": 1, "Rating": None}, {"gutenberg_id": 2, "Rating": 5}]
}

testLibrary2 = {"books": [{"gutenberg_id": 67, "Rating": 10}]}


def testClosenessSameValues():
    test = closeness(5, 5, 10)
    assert test == 1


def testClosenessDistance5():
    test = closeness(15, 10, 10)
    assert test == 0.5


def testClosenessDistanceEqualToRange():
    test = closeness(20, 10, 10)
    assert test == 0


def testClosenessDistanceFarBeyondRange():
    test = closeness(110, 10, 10)
    assert test == 0


def testJaccardHalfShared():
    test = jaccardSimilarity({1, 2, 3}, {2, 3, 4})
    assert test == 0.5


def testJaccardNoShared():
    test = jaccardSimilarity({1}, {2})
    assert test == 0


def testJaccardTwoEmpty():
    test = jaccardSimilarity(set(), set())
    assert test == 0


def testJaccardAllShared():
    test = jaccardSimilarity({1, 2}, {1, 2})
    assert test == 1


def testSubjectScorePartialOverlap():
    result = scoreBook(testBookAC, testProfile)
    test = result["Subject"]
    assert test == pytest.approx(2 / 9)


def testSubjectScoreNoOverlap():
    result = scoreBook(testBookC, testProfile)
    test = result["Subject"]
    assert test == 0


def testSubjectScoreEmptyGuard():
    result = scoreBook(testBookNoSubjects, emptyProfile)
    test = result["Subject"]
    assert test == 0


def testSubjectScoreHigherShareScoresHigher():
    resultA = scoreBook(testBookA, shareProfile)
    resultB = scoreBook(testBookB, shareProfile)
    testA = resultA["Subject"]
    testB = resultB["Subject"]
    assert testA > testB


def testReccomendNoLikedBokosReturnsEmpty():
    test = recommend(testLibrary, testCorpus1)
    assert test == []


def testReccomendLikedBookWithNoSubjects():
    test = recommend(testLibrary2, testCorpus2)
    assert len(test) == 1
