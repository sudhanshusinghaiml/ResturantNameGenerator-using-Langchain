import streamlit as st
from src.langchain_helper import generate_resturant_name_and_items

st.title("Resturant Name Generator")

cuisine = st.sidebar.selectbox("Pick a Cuisine", ("Indian", "Italian", "Mexican", "Arabic", "American"))

if cuisine:
    response = generate_resturant_name_and_items(cuisine)
    st.header(response["restaurant_name"].strip())

    menu_items = response["menu_items"].strip().split(",")
    st.write("**Menu Items**")
    for item in menu_items:
        st.write("-", item)