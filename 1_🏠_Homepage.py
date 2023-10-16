from datetime import time

import streamlit as st

st.set_page_config(
    page_title="Homepage",
)

st.title("Welcome !")

st.write('<span style="color: green; font-size: 23px;"> You are at the right place to visualize my study of the French diet </span>',
             unsafe_allow_html=True)
st.write('<span style="color: green; font-size: 23px;"> Ideal for future travellers coming to France </span>',
             unsafe_allow_html=True)

# my logo
image_path = "logo.png"
st.image(image_path, caption='Study code: ConsoFRAlim2021', use_column_width=True)

st.write('<span style="color: green; font-size: 22px;"> Enjoy your time here ! </span>',
             unsafe_allow_html=True)

# Sidebar customization

st.sidebar.success("Choose your interest topic.")

with st.sidebar:
    st.write("Author:")
    st.write("Emma DESTE")
    st.write("Efrei Paris - Promo 2025")
    st.write('<span style="color: red; font-size: 20px;"> #datavz2023efrei </span>',
             unsafe_allow_html=True)

    # Link to my other works
    image_path = "github.png"
    left_co, cent_co, last_co = st.columns(3)  # to center the logo (https://discuss.streamlit.io/t/how-can-i-center-a-picture/30995/3)
    with cent_co:
        st.image(image_path, width=50)
    st.write('<span style="color: gray; font-size: 13px;"> https://github.com/EmmaDeste </span>',
             unsafe_allow_html=True)

    image_path = "linkedin.png"
    left_co, cent_co, last_co = st.columns(3)  # to center the logo
    with cent_co:
        st.image(image_path, width=50)
    st.write('<span style="color: gray; font-size: 13px;"> www.linkedin.com/in/emmadeste/ </span>',
             unsafe_allow_html=True)



