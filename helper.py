import time
from typing import List
from langchain_core.tools import Tool
import os
import requests
import streamlit as st

def stream_data(input_string: str):
    """A generator that yields one character at a time from the input string."""
    for char in input_string.split(" "):
        yield char + " "
        time.sleep(0.02)

def get_photo_from_place(photo_resource: str):
    """Get the photo URI from a photo name returned by the Google Places API."""
    url = (
        f"https://places.googleapis.com/v1/{photo_resource}/media"
        f"?maxHeightPx=400&maxWidthPx=400&key={os.environ['GPLACES_API_KEY']}"
    )
    response = requests.get(url)

    if response.status_code != 200:
        return "NOT_FOUND"

    return response.url

@st.cache_data(show_spinner=False)
def cached_photo(photo_ref):
    return get_photo_from_place(photo_ref)