import requests
from PIL import Image
from io import BytesIO

images=[]
link = "https://storage.googleapis.com/ecg_photo/images/00018_hr.jpg"

response = requests.get(link)
img = Image.open(BytesIO(response.content))

print(type(img))
