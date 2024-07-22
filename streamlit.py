import streamlit as st
from st_pages import Page, show_pages, add_page_title

#---PAGES-----------------------------------------------------------------------------------# 
add_page_title("EPL Predictor")

show_pages(
    [
        Page("streamlit_page1.py", "Simulation Probabilities", "⚽️"),
        Page("streamlit_page2.py", "Points Prediction", "⚽️"),
    ]
)