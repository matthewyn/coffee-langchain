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
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.rating,places.googleMapsLinks,places.photos",
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

@tool
def geocode_place(place_name: str):
    """Get latitude and longitude for a place name using Google Geocoding API."""
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={place_name}&key={os.environ['GPLACES_API_KEY']}"
    response = requests.get(url)
    data = response.json()

    if data["status"] != "OK" or not data["results"]:
        return f"Could not find location for '{place_name}'."

    location = data["results"][0]["geometry"]["location"]
    return {"lat": location["lat"], "lng": location["lng"]}