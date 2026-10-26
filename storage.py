import streamlit as st
from pymongo import MongoClient

client = MongoClient(st.secrets["MONGODB_URI"])

collection = client["shelfwise"]["user_libraries"]


def saveLibrary(userId, library):
    collection.replace_one(
        {"user_id": userId}, {"user_id": userId, "library": library}, upsert=True
    )


def loadLibrary(userId):
    user_lib = collection.find_one({"user_id": userId})
    if user_lib is None:
        return None
    return user_lib["library"]
