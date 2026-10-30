# Shelfwise

## About

Shelfwise is a book analyzer, reader and recommendation algorithm build on jaccard index. Made for project gutenberg eBooks, with more eBook support planned
Works both in CLI and web.
self-hosting is a work in progress, it works in the CLI with python3 main.py, but web isnt yet set up to allow self hosting

### To use in CLI:

python3 main.py in directory, with arguments analyze <project_gutenberg txt filepath> to view the stats, log <path> to log it as read, logged to view the logged list, rate <path> <1-10 rating> to rate it. and reccomend to get your recommendations

### To use in web (recommended)

Visit https://bookbot-jwywe39kc5jktzmczxzv6u.streamlit.app/ . Self hosted support planned.

## How the reccomendation engine works

The reccomendation engine works on data from the analyzer. For each book you've logged as read, it takes the reading time and difficulty for that book, and using percentile values (linear for difficulty, logarithmic for reading time) compares each candidate book(so book not logged as read, and not excluded for other reasons such as dictionaries) to your preffered reading time and difficulty, Rt and Fk respectively. Then, it takes the subjects and "bookshelves" from the gutenberg project data, and using jaccard similarity index, compares the subjects and shelves from the books you logged and liked (so rated 7 or higher) to each candidate book, and scores it based on that. The subjects are hyper-specific in nature, so they are split into main subject and sub-subjects. Originally, i planned on comparing the main subjects, and then add algorithm weight credit based on the sub-subject similarity. However, running Leave-One-Out tests on the benchmark library showed me that it ends up making the reccomendations weaker, no matter the weight added. Therefore, for now i'm parking that idea and only main subjects will provide any real useful data for reccomendation. I tried setting it to only distinguish fiction from non fiction, but it still ended up making the reccomendation engine less accurate, according to the leave one out tests at least.
