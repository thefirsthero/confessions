import pytesseract
# pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

# Function to extract text using Tesseract OCR
def extract_text_with_tesseract(image):
    config = "--psm 3"
    extracted_text = pytesseract.image_to_string(image, config=config)
    return extracted_text
