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

## Installation

### Prerequisites

- Python >= 3.13
- Google API Keys (Places API, Geocoding API)
- Tavily API Key

### Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/matthewyn/coffee-langchain.git
   cd coffee-langchain
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate
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

### How to Interact

1. **Ask Coffee Questions**: Type any question related to coffee, brewing methods, shops, or recommendations
2. **Find Coffee Shops**: Describe the type of cafe you're looking for (e.g., "specialty coffee near me", "quiet cafe with good wifi")
3. **Get Details**: Ask about specific coffee shops to receive detailed information including ratings and photos
4. **Search Trends**: Request information about latest coffee trends, news, or emerging brewing methods

## Future Enhancements

- Multi-language support for international users
- User preferences and saved favorite coffee shops
- Coffee recipe suggestions and brewing guides
- Integration with coffee subscription services
- Advanced filtering and sorting options for search results
- User reviews and ratings system
