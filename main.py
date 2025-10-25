from dotenv import load_dotenv
import streamlit as st
from schema import StartingQuestion
from helper import stream_data, find_tool_by_name
from tools import find_places_nearby
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
llm_structured_output = llm.with_structured_output(schema=StartingQuestion)
tools = [find_places_nearby]
llm_with_tools = llm.bind_tools(tools=tools)

st.markdown("""
<style>
    #coffee-gpt {
        padding-top: 0;
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
    st.markdown("Developed by [Kenneth Matthew](www.linkedin.com/in/kennethmatthew)")

with st.container(horizontal_alignment="center", gap="medium"):
    with st.container(horizontal_alignment="center", gap="small"):
        st.title("CoffeeGPT", width="content")
        if len(st.session_state["generated_questions"]) == 0:
            with st.spinner("Generating starter questions..."):
                template = PromptTemplate(template="Generate 3 set of questions about coffee that a user might ask.", input_variables=[])
                chain = template | llm_structured_output
                response = chain.invoke(input={})
                st.session_state["generated_questions"] = response.questions
                col1, col2, col3 = st.columns(3)
                if col1.button(response.questions[0]):
                    st.session_state["prompt"] = response.questions[0]
                if col2.button(response.questions[1]):
                    st.session_state["prompt"] = response.questions[1]
                if col3.button(response.questions[2]):
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
            template = """
                You are CoffeeGPT — an expert assistant who only answers questions related to coffee.
                ☕ Topics include coffee beans, brewing methods, espresso, roasting, flavors, origins, caffeine, coffee machines, and coffee shops or cafes.

                You have access to special tools that can find nearby coffee shops or cafes.

                If the user asks about places, locations, or nearby coffee shops, you **should use an appropriate tool call** to find real data.

                If the question is NOT related to coffee in any way,
                say exactly: "Sorry, I'm not an expert at that field."

                User question: {question}

                Remember:
                - Stay focused on coffee-related topics.
                - When location-based or shop-related info is needed, call a tool instead of guessing.
                - Do not fabricate locations — rely on your tools for that.

                Answer (or tool call if appropriate):
            """
            prompt_template = PromptTemplate(template=template, input_variables=["question"])
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
                        st.session_state["chat_history"].append(ToolMessage(content=str(observation), tool_call_id=tool_call_id))
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