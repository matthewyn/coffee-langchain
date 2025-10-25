from dotenv import load_dotenv
import streamlit as st
import json
from schema import StartingQuestion
from helper import stream_data, find_tool_by_name
from tools import find_places_nearby, geocode_place
from streamlit_js_eval import get_geolocation
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

st.set_page_config(
    page_title="CoffeeGPT - The Coffee Expert Assistant",
    page_icon="public/logo.png",
)

if "user_lat" not in st.session_state or "user_lng" not in st.session_state:
    # only call get_geolocation() once
    location = get_geolocation()
    if location and "coords" in location:
        st.session_state["user_lat"] = location["coords"]["latitude"]
        st.session_state["user_lng"] = location["coords"]["longitude"]
        st.success("✅ Location detected successfully.")
    else:
        st.warning("⚠️ Unable to fetch location automatically. Please allow location access or enter manually.")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
llm_structured_output = llm.with_structured_output(schema=StartingQuestion)
tools = [find_places_nearby, geocode_place]
llm_with_tools = llm.bind_tools(tools=tools)
template = """
    You are CoffeeGPT — an expert assistant who only answers questions related to coffee.
    ☕ Topics include coffee beans, brewing methods, espresso, roasting, flavors, origins, caffeine, coffee machines, and coffee shops or cafes.

    You have access to special tools:
    - `find_places_nearby(lat, lng, query, radius)` → to find nearby coffee shops by coordinates.
    - `geocode_place(place_name)` → to find coordinates for a named place (e.g., "Petronas Twin Towers").

    If the user asks about places, locations, or nearby coffee shops, you **should use an appropriate tool call** to find real data.

    If the question is NOT related to coffee in any way,
    say exactly: "Sorry, I'm not an expert at that field."

    User question: {question}
    The user’s current location is available: latitude {lat}, longitude {lng}.

    Remember:
    - If the user says "nearby" or "around me", use their **current location**.
    - Stay focused on coffee-related topics.
    - When location-based or shop-related info is needed, call a tool instead of guessing.
    - Do not fabricate locations — rely on your tools for that.

    Answer (or tool call if appropriate):
"""

st.markdown("""
<style>
    #coffee-gpt {
        padding-top: 0;
    }
    .st-key-q1, .st-key-q2, .st-key-q3 {
        margin: 0 auto;
    }
</style>
""", unsafe_allow_html=True)

if ("prompt" not in st.session_state and "generated_questions" not in st.session_state
    and "user_prompts" not in st.session_state and "ai_responses" not in st.session_state and "new_ai_responses" not in st.session_state and "chat_history" not in st.session_state):
    st.session_state["prompt"] = ""
    st.session_state["generated_questions"] = []
    st.session_state["user_prompts"] = []
    st.session_state["ai_responses"] = []
    st.session_state["new_ai_responses"] = []
    st.session_state["chat_history"] = []

with st.sidebar:
    st.logo("public/logo.png", size="large")
    st.page_link("main.py", label="New Chat", icon=":material/new_window:")
    st.page_link("pages/about.py", label="About", icon=":material/info:")
    st.markdown("---")
    st.markdown("Developed by [Kenneth Matthew](https://www.linkedin.com/in/kennethmatthew/)")

with st.container(horizontal_alignment="center", gap="medium"):
    with st.container(horizontal_alignment="center", gap="small"):
        st.html("<h1 style='text-align: center; font-size: 2.75rem; font-weight: 700; margin: 0; line-height: 3rem;'>CoffeeGPT</h1>", width="content")
        if len(st.session_state["generated_questions"]) == 0:
            with st.spinner("Generating starter questions..."):
                template = PromptTemplate(template="Generate 3 set of questions about coffee that a user might ask.", input_variables=[])
                chain = template | llm_structured_output
                response = chain.invoke(input={})
                st.session_state["generated_questions"] = response.questions
                col1, col2, col3 = st.columns(3)
                if col1.button(response.questions[0], key="q1"):
                    st.session_state["prompt"] = response.questions[0]
                if col2.button(response.questions[1], key="q2"):
                    st.session_state["prompt"] = response.questions[1]
                if col3.button(response.questions[2], key="q3"):
                    st.session_state["prompt"] = response.questions[2]
        else:
            col1, col2, col3 = st.columns(3)
            if col1.button(st.session_state["generated_questions"][0]):
                st.session_state["prompt"] = st.session_state["generated_questions"][0]
            if col2.button(st.session_state["generated_questions"][1]):
                st.session_state["prompt"] = st.session_state["generated_questions"][1]
            if col3.button(st.session_state["generated_questions"][2]):
                st.session_state["prompt"] = st.session_state["generated_questions"][2]
        
    prompt = st.chat_input("Ask me anything about coffee!", key="prompt")
    if prompt:
        st.session_state["chat_history"].append(HumanMessage(content=prompt))
        st.session_state["user_prompts"].append(prompt)
        with st.spinner("Brewing your coffee answer..."):
            prompt_template = PromptTemplate(template=template, input_variables=["question"]).partial(lat=st.session_state.get("user_lat", 0.0), lng=st.session_state.get("user_lng", 0.0))
            chain = prompt_template | llm_with_tools
            response = chain.invoke({"question": prompt})
            while True:
                if len(response.tool_calls) > 0:
                    st.session_state["chat_history"].append(AIMessage(content=response.content, tool_calls=response.tool_calls))
                    for tool_call in response.tool_calls:
                        tool_call_name = tool_call["name"]
                        tool_call_args = tool_call["args"]
                        tool_call_id = tool_call["id"]

                        tool = find_tool_by_name(tools, tool_call_name)
                        observation = tool.invoke(tool_call_args)
                        st.session_state["chat_history"].append(ToolMessage(content=json.dumps(observation, ensure_ascii=False), tool_call_id=tool_call_id))
                    response = llm_with_tools.invoke(st.session_state["chat_history"])
                else:
                    st.session_state["ai_responses"].append(response.text)
                    st.session_state["new_ai_responses"].append(response.text)
                    st.session_state["chat_history"].append(AIMessage(content=response.text))
                    break

    if st.session_state["user_prompts"]:
        with st.container(gap="small"):
            for i, (user, ai) in enumerate(zip(st.session_state["user_prompts"], st.session_state["ai_responses"])):
                st.chat_message("human").write(user)

                if i == len(st.session_state["user_prompts"]) - 1 and st.session_state["new_ai_responses"]:
                    st.chat_message("ai").write_stream(stream_data(st.session_state["new_ai_responses"][-1]))
                else:
                    st.chat_message("ai").write(ai)

    st.session_state["new_ai_responses"].clear()