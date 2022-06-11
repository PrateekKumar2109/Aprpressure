import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.title("# Multi-Page Streamlit Web Application")
st.write("# Welcome to Pressure Made Esay! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    We are here to make your life easy by analyzing pressures and temperatures gradients
    
"""
)
