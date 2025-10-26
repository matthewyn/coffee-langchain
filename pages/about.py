import base64
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv
import streamlit_shadcn_ui as ui

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

image_path = Path("public/iclean.png")
base64_image = base64.b64encode(image_path.read_bytes()).decode()

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
    with st.container(horizontal_alignment="center"):
        st.header("Another project", width="content", anchor=False, divider="rainbow")
        with ui.card(key="iclean-card"):
            ui.element(
                "img",
                src=f"data:image/png;base64,{base64_image}",
            )
            ui.element("h3", children=["Iclean"], className="text-3xl font-bold mt-4")
            ui.element("p", children=["Beautifully designed website with the theme of environmentally friendly cleaning services. Made with Next.js and Tailwind CSS."], className="mt-2", style={"marginBottom": "1.5rem"})
            ui.element(
                "a",
                children=["Go to Website"],
                href="https://iclean-latest.vercel.app",
                target="_blank",
                className="inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0 bg-primary text-primary-foreground shadow hover:bg-primary/90 h-9 px-4 py-2",
            )
