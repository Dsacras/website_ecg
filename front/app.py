import streamlit as st
import requests
from dotenv import load_dotenv
import os
import base64
from streamlit_extras.switch_page_button import switch_page

from streamlit_card import card

from img_preprocessing import load_image

# Set page tab display
st.set_page_config(
   page_title="ECG Image Uploader",
   page_icon= '🖼️',
   layout="centered",
   initial_sidebar_state="collapsed",
)

def background_image_style(image_path):
    encoded = load_image(image_path)
    style = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
    }}
    </style>
    '''
    return style

def image_tag(path):
    encoded = load_image(path)
    tag = f'<img src="data:image/png;base64,{encoded}" width="800" height="800">'
    return tag


image_path = 'images/heart_background.jpg'
image_link = 'http://localhost:8501/ecg_uploader'


hasClicked = card(
  title="Hello World!",
  text="Some description",
  image="http://placekitten.com/200/300"
)
if hasClicked:
    switch_page("ecg_uploader")
