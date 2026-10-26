import json
from pathlib import Path

import streamlit as st
from library import newLibrary
from reccomender import MIN_RATING, recommend
from storage import loadLibrary


@st.cache_data
def loadCorpus():
    with open(Path(__file__).parent / "data" / "corpus.json", "r") as c:
        return json.load(c)


corpus = loadCorpus()


def enterDemo():
    st.session_state["demo"] = True


def exitDemo():
    st.session_state["demo"] = False


def loadDemoLibrary():
    with open(Path(__file__).parent / "data" / "demo_books.json", "r") as d:
        return json.load(d)


loggedIn = st.user.is_logged_in
demoOn = st.session_state.get("demo", False)

if not loggedIn:
    if not demoOn:
        st.title("Welcome to Shelfwise!")
        st.button("Log in with Google", on_click=st.login)
        st.button("Enter demo", on_click=enterDemo)
        st.stop()

if loggedIn:
    owner = st.user.sub
else:
    owner = "demo"

if "library" not in st.session_state or st.session_state["libraryOwner"] != owner:
    if owner == "demo":
        library = loadDemoLibrary()
    else:
        library = loadLibrary(owner)
        if library is None:
            library = newLibrary()
    st.session_state["library"] = library
    st.session_state["libraryOwner"] = owner

st.title("Shelfwise")

with st.sidebar:
    if loggedIn:
        st.button("Log out", on_click=st.logout)
    elif demoOn:
        st.button("Exit demo", on_click=exitDemo)

recTab, libTab = st.tabs(["You might like", "My books"])

with recTab:
    recommenderResults = recommend(st.session_state["library"], corpus)
    if not recommenderResults:
        st.info(
            "Please rate atleast one book with a score of 7 or higher to get recommendations."
        )
    else:

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

with libTab:
    st.write(len(st.session_state["library"]["books"]), "books logged")
    st.dataframe(
        st.session_state["library"]["books"],
        column_order=("Title", "Author", "Rating", "Read Count"),
    )
    with st.expander("stats for nerds"):
        st.dataframe(st.session_state["library"]["books"])
