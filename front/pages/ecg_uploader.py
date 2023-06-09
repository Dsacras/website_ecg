import streamlit as st
from dotenv import load_dotenv
import os
from img_preprocessing import process_ecg_image, read_templates
from PIL import Image
from pdf2image import convert_from_bytes
import io

def convert_image_to_byte(image):
  # create BytesIO in the memory
  imgByteArr = io.BytesIO()
  # save image
  image.save(imgByteArr, format=image.format)
  # Turn object to byte image
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr

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

img_file = st.file_uploader("Let's see if your ECG is healthy")
st.text("")

if img_file is not None:
    #check file format
    file_format = str(img_file.name).split('.')[-1]
    if file_format == "pdf" or file_format == "jpg" or file_format == "png":
        if file_format == "pdf":
            file_bytes = convert_from_bytes(img_file.read())
            file_bytes=convert_image_to_byte(file_bytes[0])
        elif file_format == "jpg" or file_format == "png":
            file_bytes = img_file.read()

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
    else:
        st.markdown(":red[Input file must be an image in jpg or png format or a pdf file]")
