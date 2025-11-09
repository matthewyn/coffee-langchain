from typing import List, Literal
from pydantic import BaseModel, Field

class ToolsToUse(BaseModel):
    """Schema for AI model to decide the correct final tool to use for answering the user question."""
    final_tool_to_use: Literal["find_places_by_text", "geocode_place", "get_place_detail", "TavilySearch", "no_tool", "not_related"] = Field(description="The final apropriate tool to use for answering the user question.")

class PlacesNearby(BaseModel):
    """Schema required to format the AI responses when find_places_nearby tool is called."""
    names: List[str] = Field(description="The name of coffee shops/cafes available nearby.")
    addresses: List[str] = Field(description="The address of coffee shops/cafes available nearby.")
    ratings: List[str] = Field(description="The rating of coffee shops/cafes available nearby.")
    google_map_links: List[str] = Field(description="The google map link of coffee shops/cafes available nearby.")
    photos: List[str] = Field(description="The photo name of coffee shops/cafes available nearby.")

class SearchResultItem(BaseModel):
    text: str = Field(description="""
    Write a detailed multi-sentence explanation (at least 4–6 sentences)
    summarizing the key insights from this source. Provide depth, context,
    and meaningful details — not just a short summary."
    """)
    source: str = Field(description="Source link for this result in markdown format, e.g. [:orange-badge[source]](https://example.com). The source link in [source] **must** use the website's name as the link text. Example: [:orange-badge[Fox News]](https://www.foxnews.com/...), not [source](https://...).")

class SearchResult(BaseModel):
    """Schema required to format the AI responses when TavilySearch tool is called."""
    results: List[SearchResultItem] = Field(description="List of text content in search results, each paired with its own source link.")