import cv2
from typing import Callable

# Function to preprocess an image
def preprocess_image(image):
    # Up-sample for better OCR accuracy (2x)
    img = cv2.resize(image, (0, 0), fx=2, fy=2)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return image

# Function to extract and reformat text from an image using the given OCR library
def extract_and_reformat_text(image_path, ocr_function: Callable):
    image = cv2.imread(image_path)
    preprocessed_image = preprocess_image(image)
    extracted_text = ocr_function(preprocessed_image)
    return extracted_text
