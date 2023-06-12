import streamlit as st
from dotenv import load_dotenv
import os
from img_preprocessing import crop_manual, process_ecg_image, read_templates
from PIL import Image
from pdf2image import convert_from_bytes
import io

def convert_image_to_byte(image):
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, format=image.format)
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr

templates = read_templates()

st.set_page_config(
   page_title="ECG Image Uploader",
   page_icon= '🖼️',
   layout="centered",
   initial_sidebar_state="collapsed",
)

load_dotenv()
url = os.getenv('API_URL')

st.title('ECG Image Uploader 📸')

img_file = st.file_uploader("Let's see if your ECG is healthy")
st.text("")

if img_file is not None:
    file_format = str(img_file.name).split('.')[-1]
    if file_format == "pdf" or file_format == "jpg" or file_format == "png":
        if file_format == "pdf":
            file_bytes = convert_from_bytes(img_file.read())
            file_bytes=convert_image_to_byte(file_bytes[0])
        elif file_format == "jpg" or file_format == "png":
            file_bytes = img_file.read()

    # Check if a new file has been uploaded
    if 'last_file' not in st.session_state or st.session_state['last_file'] != file_bytes:
        # A new file has been uploaded. Reset the session state variables
        for key in list(st.session_state.keys()):
            if key in ['image_raw', 'max_loc', 'max_w', 'max_h', 'logged_image']:
                del st.session_state[key]

    st.session_state['last_file'] = file_bytes  # Update the last uploaded file in the session state

    if 'image_raw' not in st.session_state or 'max_loc' not in st.session_state or 'max_w' not in st.session_state or 'max_h' not in st.session_state:
        with st.spinner("Processing the image..."):
            st.session_state['image_raw'], st.session_state['max_loc'], st.session_state['max_w'], st.session_state['max_h'] = process_ecg_image(file_bytes, padding=0, templates=templates)

    padding_slider = st.slider("Select padding for ECG area", -100, 100, 0)
    max_loc, max_w, max_h = st.session_state['max_loc'], st.session_state['max_w'], st.session_state['max_h']

    # Calculate the cropping coordinates based on the padding value
    top = max(max_loc[1] - padding_slider, 0)
    left = max(max_loc[0] - padding_slider, 0)
    bottom = min(max_loc[1] + max_h + padding_slider, st.session_state['image_raw'].shape[0])
    right = min(max_loc[0] + max_w + padding_slider, st.session_state['image_raw'].shape[1])

    with st.spinner("Applying new padding..."):
        image_array = crop_manual(st.session_state['image_raw'], top, left, bottom, right)

    processed_image = Image.fromarray(image_array)
    st.image(processed_image, caption='ECG after padding adjustment')

    if st.button('Log this version'):
        st.session_state['logged_image'] = image_array
        st.success('Image version logged successfully!')
        st.balloons()  # This will trigger the balloon animation
