# ☕ CoffeeGPT - The Coffee Expert Assistant

CoffeeGPT is an intelligent conversational assistant built with LangChain and Streamlit that helps users discover, learn about, and find coffee shops. Powered by Google Generative AI, it combines natural language processing with real-world location data to provide personalized coffee recommendations and information.

## Features

- **Expert Coffee Knowledge**: Get answers to questions about coffee beans, brewing methods, espresso, roasting, flavors, origins, caffeine, and coffee machines
- **Coffee Shop Discovery**: Find nearby coffee shops and cafes based on text descriptions (e.g., "third wave coffee", "cozy cafe with wifi", "specialty espresso")
- **Location-Based Search**: Automatically detects your location or accepts manual location input to provide relevant recommendations
- **Detailed Place Information**: Access comprehensive details about specific coffee shops including ratings, addresses, photos, and Google Maps links
- **Real-Time Information**: Leverage Tavily Search to find the latest coffee trends, news, and emerging brewing methods
- **Interactive Chat Interface**: Streamlit-powered web interface for seamless conversation with the AI assistant

## Technology Stack

- **Framework**: [Streamlit](https://streamlit.io/) - Fast web app development in Python
- **LLM**: [Google Generative AI](https://ai.google.dev/) (Gemini 2.5 Flash)
- **LangChain**: Agent framework for building tool-powered AI applications
- **APIs**:
  - Google Places API - For finding and getting details about coffee shops
  - Google Geocoding API - For converting place names to coordinates
  - Tavily Search API - For searching latest coffee information
- **UI Components**: Streamlit Shadcn UI for enhanced user interface

## Project Structure

```
coffee-langchain/
├── main.py              # Main chat interface and agent logic
├── pages/
│   └── about.py        # About page with project information
├── schema.py           # Pydantic models for data validation
├── tools.py            # Tool definitions for the AI agent
├── helper.py           # Utility functions for streaming and caching
├── pyproject.toml      # Project dependencies and metadata
├── public/             # Static assets (logo, images)
└── README.md           # This file
```

## Installation

### Prerequisites

- Python >= 3.13
- Google API Keys (Places API, Geocoding API)
- Tavily API Key

### Setup

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd coffee-langchain
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -e .
   ```

   Or install packages directly:

   ```bash
   pip install googlemaps langchain langchain-community langchain-google-genai langchain-tavily python-dotenv streamlit streamlit-js-eval streamlit-shadcn-ui
   ```

4. **Create a `.env` file** in the project root:
   ```
   GPLACES_API_KEY=your_google_api_key_here
   GOOGLE_API_KEY=your_google_generative_ai_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   ```

## Usage

### Running the Application

Start the Streamlit application:

```bash
streamlit run main.py
```

The app will open in your default web browser at `http://localhost:8501`.

### How to Interact

1. **Ask Coffee Questions**: Type any question related to coffee, brewing methods, shops, or recommendations
2. **Find Coffee Shops**: Describe the type of cafe you're looking for (e.g., "specialty coffee near me", "quiet cafe with good wifi")
3. **Get Details**: Ask about specific coffee shops to receive detailed information including ratings and photos
4. **Search Trends**: Request information about latest coffee trends, news, or emerging brewing methods

### Example Queries

- "What's the difference between espresso and Americano?"
- "Find specialty coffee shops near me"
- "What are the latest coffee trends in 2025?"
- "Tell me about coffee roasting levels"
- "Where can I find a quiet cafe with good wifi?"

## Core Components

### `main.py`

The main application entry point featuring:

- Streamlit page configuration with logo and title
- Geolocation detection for location-based searches
- LangChain agent setup with multiple tools
- Chat interface and message history management
- LLM initialization with Google Generative AI

### `tools.py`

Implements four primary tools:

- `find_places_by_text()` - Search for coffee shops by text query with optional location bias
- `geocode_place()` - Convert place names to geographic coordinates
- `get_place_detail()` - Retrieve detailed information about a specific coffee shop
- `TavilySearch()` - Search for latest coffee-related information

### `schema.py`

Pydantic models for data validation:

- `ToolsToUse` - Schema for agent's tool selection decision
- `PlacesNearby` - Format for nearby places responses
- `SearchResult` - Format for search results with sources

### `helper.py`

Utility functions:

- `stream_data()` - Streams text character by character for smooth UI display
- `cached_photo()` - Caches and retrieves place photos efficiently

### `pages/about.py`

Informational page with project details and developer information

## Environment Variables

| Variable          | Description                                 |
| ----------------- | ------------------------------------------- |
| `GPLACES_API_KEY` | Google Places API key for location services |
| `GOOGLE_API_KEY`  | Google Generative AI API key for LLM access |
| `TAVILY_API_KEY`  | Tavily API key for web search functionality |

## Dependencies

- **langchain** (>=1.0.2) - AI agent framework
- **langchain-community** (>=0.4) - Community integrations
- **langchain-google-genai** (>=3.0.0) - Google Generative AI integration
- **langchain-tavily** (>=0.2.12) - Tavily search integration
- **googlemaps** (>=4.10.0) - Google Maps API client
- **streamlit** (>=1.50.0) - Web app framework
- **streamlit-js-eval** (>=0.1.7) - JavaScript evaluation in Streamlit
- **streamlit-shadcn-ui** (>=0.1.19) - UI component library
- **python-dotenv** (>=1.1.1) - Environment variable management

## Future Enhancements

- Multi-language support for international users
- User preferences and saved favorite coffee shops
- Coffee recipe suggestions and brewing guides
- Integration with coffee subscription services
- Advanced filtering and sorting options for search results
- User reviews and ratings system

## Author

Developed by [Kenneth Matthew](https://www.linkedin.com/in/kennethmatthew/)
