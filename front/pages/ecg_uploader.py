import streamlit as st
from dotenv import load_dotenv
import os
from img_preprocessing import process_ecg_image, read_templates
from PIL import Image

# Load templates at start
templates = read_templates()

# Set page tab display
st.set_page_config(
   page_title="ECG Image Uploader",
   page_icon= '🖼️',
   layout="centered",
   initial_sidebar_state="collapsed",
)

load_dotenv()
url = os.getenv('API_URL')

# App title and description
st.title('ECG Image Uploader 📸')

img_file_buffer = st.file_uploader("Let's see if your ECG is healthy")
st.text("")

if img_file_buffer is not None:
    file_bytes = img_file_buffer.read()

    with st.spinner("Processing the image..."):
        image_array = process_ecg_image(file_bytes, padding=0, templates=templates)  # Pass templates as an argument

    if image_array is not None:
        processed_image = Image.fromarray(image_array)

        # Add a slider after the image has been loaded
        padding_slider = st.slider("Select padding for ECG area", -100, 100, 0)

        # Check if user has interacted with the slider
        if 'slider_used' in st.session_state and st.session_state['slider_used']:
            # Processing the image again with new padding value
            with st.spinner("Processing the image with new padding..."):
                image_array = process_ecg_image(file_bytes, padding=padding_slider, templates=templates)  # Pass templates as an argument

            processed_image = Image.fromarray(image_array)
        else:
            st.session_state['slider_used'] = True

        st.image(processed_image, caption='ECG after padding adjustment')

        if st.button('Log this version'):
            st.session_state['logged_image'] = image_array
            st.success('Image version logged successfully!')
            st.balloons()  # This will trigger the balloon animation
