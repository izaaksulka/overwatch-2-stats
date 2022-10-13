import pytesseract
from PIL import Image

full_image = Image.open('map_type_and_name.png')

# name_only = full_image.crop((538, 257, 824, 330))
# name_only.save('output.png')

print(pytesseract.image_to_string(
    full_image, config=("--psm 10")))
