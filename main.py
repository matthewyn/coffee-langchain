from dotenv import load_dotenv
import streamlit as st
from schema import ToolsToUse, PlacesNearby, SearchResult
from helper import stream_data, cached_photo
from tools import geocode_place, get_place_detail, find_places_by_text
from streamlit_js_eval import get_geolocation
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from langchain.agents import create_agent

load_dotenv()

st.set_page_config(
    page_title="CoffeeGPT - The Coffee Expert Assistant",
    page_icon="public/logo.png",
)

if "user_lat" not in st.session_state or "user_lng" not in st.session_state:
    location = get_geolocation()
    if location and "coords" in location:
        st.session_state["user_lat"] = location["coords"]["latitude"]
        st.session_state["user_lng"] = location["coords"]["longitude"]
        st.toast("Location fetched successfully!", icon="📍")
    else:
        st.warning("⚠️ Unable to fetch location automatically. Please allow location access or enter manually.")

tools = [find_places_by_text, geocode_place, TavilySearch(), get_place_detail]

# Store LLM and prompt templates in session state for single initialization
if "llm" not in st.session_state:
    st.session_state["llm"] = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

if "template" not in st.session_state:
    st.session_state["template"] = """
    You are CoffeeGPT — an expert assistant who only answers questions related to coffee.
    ☕ Topics include coffee beans, brewing methods, espresso, roasting, flavors, origins, caffeine, coffee machines, and coffee shops or cafes.

    You have access to special tools:
    - `find_places_by_text(lat, lng, query, radius)` → to find coffee shops or cafes **based on a text query** (e.g., "third wave coffee", "cozy cafe with wifi", "specialty espresso", "cafe in Sydney, Australia").
    - `geocode_place(place_name)` → Convert a place name such as "Starbucks Plaza Indonesia" or "Tokyo Tower" into coordinates. This tool can also provide a placeId that may be used as the argument for `get_place_detail`.
    - `get_place_detail(placeId)` → Retrieve detailed information about a specific coffee shop by place ID.
    - `TavilySearch(query)` → search the **latest**, **trending**, or **recent** information about coffee, such as news, new brewing methods, emerging coffee trends, or current market data.

    🧠 Tool usage rules:
    - If the user asks to **search for coffee shops or cafes by description or name** (e.g., "Japanese-style cafe", "specialty coffee"), use `find_places_by_text`.
    - If the user’s query mentions a **specific place name** (e.g., "near Shibuya Station", "around Central Park", "in Jakarta Selatan"):
        1. First call `geocode_place(place_name)` to get coordinates.
        2. Then call `find_places_by_text(lat, lng, query)` using those coordinates.
    - If the user asks for cafes **near me** or **nearby** without specifying a place, use `find_places_by_text` with the user’s **current location**.
    - If the user asks for details about a specific cafe (address, hours, rating, phone, etc.), use `get_place_detail`.
    - If the user asks about the **latest**, **newest**, **trending**, or **current** news, methods, innovations, or discoveries related to coffee — **use `TavilySearch`**.
    - Do **not** fabricate data; always use a tool call when real-world information is requested.
    - If the question is NOT related to coffee, say exactly: "Sorry, I'm not an expert at that field."

    The user’s current location is available: latitude {lat}, longitude {lng}.

    Remember:
    - If the user says "nearby" or "around me", use their **current location**.
    - Stay focused on coffee-related topics.
    - When location-based or shop-related info is needed, call a tool instead of guessing.
    - Do not fabricate locations — rely on your tools for that.

    Answer (or tool call if appropriate):

    If you use TavilySearch, you MUST output the answer using the SearchResult schema:
    - Return a JSON with key "results"
    - Each item must contain:
        - "text": the content of the result
        - "source": markdown link formatted like [:orange-badge[source]](URL)
    """

if "rephrase_template" not in st.session_state:
    st.session_state["rephrase_template"] = PromptTemplate(
        template="""
        Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.

        Chat History:
        {chat_history}
        Follow Up Input: {input}
        Standalone Question:
        """,
        input_variables=["chat_history", "input"]
    )

if "routing_template" not in st.session_state:
    st.session_state["routing_template"] = PromptTemplate(
        template="""
        You are a routing assistant for CoffeeGPT. Your job is to decide whether the user's question
        requires calling a tool, and if so, which FINAL tool is appropriate for answering the user question. If the question is NOT related to coffee, just response with "not_related".

        You DO NOT answer the question directly. You only output the routing decision.

        Available Tools:
        1. find_places_by_text(query, lat, lng, radius)
        - Use when the user is searching for coffee shops or cafes based on:
          - A name (e.g., "Starbucks", "Kopi Kenangan")
          - A description (e.g., "cozy cafe with wifi", "specialty coffee roasters")
          - A general search request like "cafe recommendations"
          - A location mentioned by name (e.g., "near Shibuya Station", "in Jakarta Selatan")
          - A request like "near me" or "nearby"

        2. geocode_place(place_name)
        - Use only when you need to convert a named location into coordinates in order to use with `find_places_by_text`.

        3. get_place_detail(placeId)
        -  Use when the user asks for details about a specific cafe or coffee shop, such as:
           - Address
           - Opening hours
           - Phone number
           - Seating
           - Rating
           - Menu
           - More detailed information about a place already identified.

        4. TavilySearch(query)
        - Use when the user asks about the **latest**, **recent**, **trend**, **news**, **updates**,
            or **current market data** related to coffee.

        Now analyze the user question:

        User Question: "{question}"
        """,
        input_variables=["question"]
    )

if "rephraser_chain" not in st.session_state:
    st.session_state["rephraser_chain"] = st.session_state["rephrase_template"] | st.session_state["llm"]

if "routing_chain" not in st.session_state:
    st.session_state["routing_chain"] = st.session_state["routing_template"] | st.session_state["llm"].with_structured_output(ToolsToUse)

st.markdown("""
<style>
    #coffee-gpt {
        padding-top: 0;
    }
    /* Target all 3 buttons in the first 3-column container */
    div[data-testid="stColumn"] > div > div[data-testid="stElementContainer"] {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

defaults = {
    "prompt": "",
    "questions": ["What's the difference between Arabica and Robusta coffee beans?", "How does the brewing method affect the taste of coffee?", "What are some tips for making a perfect cup of coffee at home?"],
    "user_prompts": [],
    "ai_responses": [],
    "new_ai_responses": [],
    "chat_history": []
}
for key, val in defaults.items():
    st.session_state.setdefault(key, val)

with st.sidebar:
    st.logo("public/logo.png", size="large")
    st.page_link("main.py", label="New Chat", icon=":material/new_window:")
    st.page_link("pages/about.py", label="About", icon=":material/info:")
    st.markdown("---")
    st.markdown("Developed by [Kenneth Matthew](https://www.linkedin.com/in/kennethmatthew/)")

with st.container(horizontal_alignment="center", gap="medium"):
    with st.container(horizontal_alignment="center", gap="small"):
        st.html("<h1 style='text-align: center; font-size: 2.75rem; font-weight: 700; margin: 0; line-height: 3rem;'>CoffeeGPT</h1>", width="content")
        col1, col2, col3 = st.columns(3)
        if col1.button(st.session_state["questions"][0]):
            st.session_state["prompt"] = st.session_state["questions"][0]
        if col2.button(st.session_state["questions"][1]):
            st.session_state["prompt"] = st.session_state["questions"][1]
        if col3.button(st.session_state["questions"][2]):
            st.session_state["prompt"] = st.session_state["questions"][2]
        
    prompt = st.chat_input("Ask me anything about coffee!", key="prompt")
    if prompt:
        st.session_state["chat_history"].append(HumanMessage(content=prompt))
        st.session_state["user_prompts"].append(prompt)
        with st.spinner("Brewing your coffee answer..."):
            chat_history_text = "\n".join(
                [f"Human: {msg.content}" if isinstance(msg, HumanMessage) else f"AI: {msg.content}" for msg in st.session_state["chat_history"]]
            )
            rephraser_chain = st.session_state["rephraser_chain"]
            routing_chain = st.session_state["routing_chain"]
            llm = st.session_state["llm"]
            template = st.session_state["template"]
            rephrased_question = rephraser_chain.invoke({
                "chat_history": chat_history_text,
                "input": prompt
            }).content
            routing_decision = routing_chain.invoke({"question": rephrased_question})

            if routing_decision.final_tool_to_use == "not_related":
                st.session_state["ai_responses"].append([{"info": "Sorry, I'm not an expert at that field.", "photo_url": None}])
                st.session_state["new_ai_responses"].append([{"info": "Sorry, I'm not an expert at that field.", "photo_url": None}])
                st.session_state["chat_history"].append(AIMessage(content="Sorry, I'm not an expert at that field."))
            else:
                prompt_template = PromptTemplate(template=template).partial(lat=st.session_state.get("user_lat", 0.0), lng=st.session_state.get("user_lng", 0.0))

                if routing_decision.final_tool_to_use == "find_places_by_text":
                    response_format = PlacesNearby
                elif routing_decision.final_tool_to_use == "TavilySearch":
                    response_format = SearchResult
                else:
                    response_format = None

                agent = create_agent(model=llm, tools=tools, system_prompt=prompt_template.format(), response_format=response_format)
                res = agent.invoke({"messages": rephrased_question})
                if response_format == PlacesNearby:
                    # Prepare a list of dicts for each shop with info and image
                    data = res["structured_response"]
                    shops = []
                    for i in range(len(data.names)):
                        info = (
                            f"**{i+1}. {data.names[i]}**\n"
                            f"   - Address: {data.addresses[i]}\n"
                            f"   - Rating: {data.ratings[i]}\n"
                            f"   - Google Maps: [Navigate to Place]({data.google_map_links[i]})"
                        )
                        photo_url = cached_photo(data.photos[i]) if i < len(data.photos) else None
                        shops.append({"info": info, "photo_url": photo_url})
                    st.session_state["ai_responses"].append(shops)
                    st.session_state["new_ai_responses"].append(shops)
                    st.session_state["chat_history"].append(AIMessage(content=shops))
                elif response_format == SearchResult:
                    # Render each result as a separate markdown block for consistency
                    data = res["structured_response"]
                    results = []
                    for item in data.results:
                        text = item.text.strip()
                        source = item.source.strip()
                        info = f"{text}  {source}"
                        results.append({"info": info, "photo_url": None})
                    st.session_state["ai_responses"].append(results)
                    st.session_state["new_ai_responses"].append(results)
                    st.session_state["chat_history"].append(AIMessage(content=results))
                else:
                    st.session_state["ai_responses"].append([{"info": res["messages"][-1].text, "photo_url": None}])
                    st.session_state["new_ai_responses"].append([{"info": res["messages"][-1].text, "photo_url": None}])
                    st.session_state["chat_history"].append(AIMessage(content=res["messages"][-1].text))

    if st.session_state["user_prompts"]:
        with st.container(gap="small"):
            for i, (user, ai) in enumerate(zip(st.session_state["user_prompts"], st.session_state["ai_responses"])):
                st.chat_message("human").write(user)
                message = st.chat_message("ai")

                # ai is now a list of dicts with info and photo_url
                def render_shops(shops, stream=False):
                    for shop in shops:
                        # For TavilySearch, always use st.markdown for info
                        if shop["photo_url"] is None:
                            if stream:
                                message.write_stream(stream_data(shop["info"]))
                            else:
                                message.markdown(shop["info"])
                        else:
                            if stream:
                                message.write_stream(stream_data(shop["info"]))
                            else:
                                message.write(shop["info"])
                            if shop["photo_url"] and shop["photo_url"] != "NOT_FOUND":
                                message.image(shop["photo_url"], caption="The photo of the coffee shop.")

                if i == len(st.session_state["user_prompts"]) - 1 and st.session_state["new_ai_responses"]:
                    render_shops(st.session_state["new_ai_responses"][-1], stream=True)
                else:
                    render_shops(ai)

    st.session_state["new_ai_responses"].clear()