import requests
import os
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()

@tool
def find_places_nearby(lat: float, lng: float, query: str, radius: int = 3000):
    """Find places nearby a given location using Google Places API."""
    url = "https://places.googleapis.com/v1/places:searchNearby"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": os.environ["GPLACES_API_KEY"],
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.rating",
    }
    payload = {
        "includedTypes": ["cafe", "coffee_shop"],
        "maxResultCount": 5,
        "locationRestriction": {
            "circle": {"center": {"latitude": lat, "longitude": lng}, "radius": radius}
        },
    }
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    if "places" not in data:
        return f"Error: {data}"

    return data["places"]