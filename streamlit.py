import streamlit as st
from st_pages import Page, show_pages, add_page_title

#---PAGES-----------------------------------------------------------------------------------# 
add_page_title("EPL Predictor")

show_pages(
    [
        Page("streamlit_page1.py", "Home", "🏠"),
        Page("streamlit_page2.py", "Page 2", ":books:"),
    ]
)