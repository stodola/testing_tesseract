import sys
import pytesseract
from PIL import Image

dane = pytesseract.image_to_string(Image.open(sys.argv[1]) , lang='pol')

print(dane)
