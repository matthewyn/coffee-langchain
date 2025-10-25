from dotenv import load_dotenv
import streamlit as st

load_dotenv()

st.set_page_config(
    page_title="CoffeeGPT - About",
    page_icon="public/logo.png",
)

st.markdown("""
<style>
    #coffee-gpt {
        padding-top: 0;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.logo("public/logo.png", size="large")
    st.page_link("main.py", label="New Chat", icon=":material/new_window:")
    st.page_link("pages/about.py", label="About", icon=":material/info:")
    st.markdown("---")
    st.markdown("Developed by [Kenneth Matthew](https://www.linkedin.com/in/kennethmatthew/)")

with st.container(horizontal_alignment="center", gap="large"):
    with st.container(horizontal_alignment="center"):
        st.html("<h1 style='text-align: center; font-size: 2.75rem; font-weight: 700; margin: 0; line-height: 3rem;'>The number #1 Coffee Expert Assistant powered by Gemini</h1>", width="content")
        st.html("<p style='text-align: center;'>CoffeeGPT is an AI-powered assistant designed to help coffee enthusiasts find the best coffee shops, brewing techniques, and coffee-related information. Built using Streamlit and Google Gemini, CoffeeGPT leverages advanced language models to provide accurate and personalized responses to user queries about coffee.</p>")
        st.code("git clone https://github.com/matthewyn/coffee-langchain.git", language="bash")
        st.link_button("Read the docs", "https://github.com/matthewyn/coffee-langchain", type="primary", icon=":material/import_contacts:")
        st.markdown("Currently version **1.0.0**&nbsp;&nbsp;·&nbsp;&nbsp;[Download](https://github.com/matthewyn/coffee-langchain)", width="content")
    st.video("https://www.youtube.com/watch?v=ip2mwfG83KE&list=RDip2mwfG83KE&start_radio=1")