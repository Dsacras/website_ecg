import streamlit as st
import requests
from dotenv import load_dotenv
import os
from img_preprocessing import process_ecg_image
from PIL import Image

# Set page tab display
st.set_page_config(
   page_title="ECG Image Uploader",
   page_icon= '🖼️',
   layout="centered",
   initial_sidebar_state="expanded",
)

load_dotenv()
url = os.getenv('API_URL')


# App title and description
st.title('ECG Image Uploader 📸')

### Create a native Streamlit file upload input
# labels = st.markdown("### Let's see if your ECG is healthy 👇")
img_file_buffer = st.file_uploader("Let's see if your ECG is healthy")
st.text("")


if img_file_buffer is not None:
    image_array = process_ecg_image(img_file_buffer)
    if image_array is not None:
        processed_image = Image.fromarray(image_array)
        st.image(processed_image, caption='ECG')
