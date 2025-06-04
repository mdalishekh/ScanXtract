import pytesseract
from PIL import Image
from pdf2image import convert_from_path


# Tesseract path for Docker
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

def ocr_image(image_path: str)-> str | None:
    """Performs OCR with images only

    Args:
        image_path (str): Takes image path to perform OCR.

    Returns:
        str | None: Returns extracted text from the image or None if no text is found.
    """
    try:
        with Image.open(image_path) as image:
            text = pytesseract.image_to_string(image)
        if not text:
            return None
        return text
    except Exception as error:
        return error # type: ignore
        
def ocr_pdf(pdf_path: str)-> str | None:
    """Perform OCR with PDF only

    Args:
        pdf_path (str): Takes PDF path to perform OCR.

    Returns:
        str | None: Returns extracted text from the PDF or None if no text is found.
    """
    text_list = []
    images = convert_from_path(pdf_path)
    for img in images:
        text_list.append(pytesseract.image_to_string(img))
    texts = "".join(text_list)    
    if not texts:   
        return None
    return texts