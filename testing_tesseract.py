import pytesseract
from PIL import Image, ImageFilter
from image_utils import to_text


dane = pytesseract.image_to_string(Image.open('IMG_20170113_191448.jpg') , lang='pol')

dane2  = to_text(dane)

print(list(dane2))
