import json
from pathlib import Path

import streamlit as st
from reccomender import MIN_RATING, recommend


@st.cache_data
def loadCorpus():
    with open(Path(__file__).parent / "data" / "corpus.json", "r") as c:
        return json.load(c)


corpus = loadCorpus()


def loadLibrary():
    with open(Path(__file__).parent / "data" / "demo_books.json", "r") as d:
        return json.load(d)


if "library" not in st.session_state:
    st.session_state["library"] = loadLibrary()

recommenderResults = recommend(st.session_state["library"], corpus)
if not recommenderResults:
    st.info(
        "Please rate atleast one book with a score of 7 or higher to get recommendations."
    )
    st.stop()


def relativeResult():
    highestSoFar = 0
    for result in recommenderResults:
        if result["Score"] > highestSoFar:
            highestSoFar = result["Score"]
    withMatch = []

    for result in recommenderResults:
        relativePercentages = round(result["Score"] / highestSoFar * 100)
        withMatch.append({**result, "Match": relativePercentages})
    return withMatch


relativePercentage = relativeResult()

st.dataframe(
    relativePercentage,
    column_order=("Title", "Author", "Match"),
    column_config={"Match": st.column_config.NumberColumn(format="%d%%")},
    hide_index=True,
)
with st.expander("Details"):
    st.dataframe(recommenderResults)
