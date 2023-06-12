import cv2
import numpy as np
from skimage import transform
from torchvision import transforms
import torch.nn.functional as F
import glob
import os
from PIL import Image


def read_templates():
    """
    Read folder with input photo templates
    """
    return [cv2.imread("./templates/"+file, cv2.IMREAD_GRAYSCALE) for file in os.listdir("./templates") if file.lower().endswith(('.png'))]

def load_image(file_bytes):
    nparr = np.frombuffer(file_bytes, np.uint8)
    img_color = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # Convert byte array into an image
    img = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    return img, img_color


def match_template(img, templates, scale_start = 0.6, scale_end = 1.2,scale_step = 0.1):
    max_val = -np.inf
    max_loc = None
    max_w = max_h = None
    for template in templates:
        for scale in np.arange(scale_start, scale_end, scale_step):
            resized_template = cv2.resize(template, (0, 0), fx=scale, fy=scale)
            h, w = resized_template.shape[:2]
            if img.shape[0] < h or img.shape[1] < w:
                break
            res = cv2.matchTemplate(img, resized_template, cv2.TM_CCOEFF_NORMED)
            min_val, temp_max_val, min_loc, temp_max_loc = cv2.minMaxLoc(res)
            if temp_max_val > max_val:
                max_val = temp_max_val
                max_loc = temp_max_loc
                max_w = w
                max_h = h
    return max_val, max_loc, max_w, max_h

def crop_and_draw(img_color, max_loc, max_w, max_h, padding):
    top_left = max(max_loc[0] - padding, 0), max(max_loc[1] - padding, 0)
    bottom_right = min(top_left[0] + max_w + 2 * padding, img_color.shape[1]), min(top_left[1] + max_h + 2 * padding, img_color.shape[0])
    cv2.rectangle(img_color, top_left, bottom_right, (0, 255, 0), 2)
    cropped = img_color[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    return cropped

def transform_image(cropped):
    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Grayscale(num_output_channels=3),
        transforms.Resize((700, 1400)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    if len(cropped.shape) == 2 or cropped.shape[2] == 1:
        cropped = cv2.cvtColor(cropped, cv2.COLOR_GRAY2RGB)
    # return tensor image
    return transform(cropped)

def process_ecg_image(file, padding, templates):
    img, img_color = load_image(file)
    max_val, max_loc, max_w, max_h = match_template(img, templates)
    return img_color, max_loc, max_w, max_h

def crop_manual(image_array, top, left, bottom, right):
    """
    This function receives an image array and cropping coordinates, and returns the cropped image array.
    """
    img = Image.fromarray(image_array)
    img_cropped = img.crop((left, top, right, bottom))
    return np.array(img_cropped)
