import requests
import os
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()

@tool
def find_places_by_text(query: str, lat: float = None, lng: float = None, radius: int = 3000):
    """Find places using text search with Google Places API, with optional location bias."""
    url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": os.environ["GPLACES_API_KEY"],
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.rating,places.googleMapsLinks,places.photos",
    }

    # Always include the query
    payload = {
        "textQuery": query,
        "pageSize": 5,
    }

    # Only apply location bias if coordinates are provided
    if lat is not None and lng is not None:
        payload["locationBias"] = {
            "circle": {
                "center": {"latitude": lat, "longitude": lng},
                "radius": radius,
            }
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
    placeId = data["results"][0]["place_id"]
    return {"lat": location["lat"], "lng": location["lng"], "placeId": placeId}

@tool
def get_place_detail(placeId: str):
    """Get detailed information about a place using Google Places API."""
    url = f"https://places.googleapis.com/v1/places/{placeId}"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": os.environ["GPLACES_API_KEY"],
        "X-Goog-FieldMask": "name,formattedAddress,currentOpeningHours,nationalPhoneNumber,priceRange,rating,delivery,dineIn,reviewSummary,outdoorSeating",
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    if response.status_code != 200:
        return f"Error retrieving details for placeId '{placeId}'"

    return data