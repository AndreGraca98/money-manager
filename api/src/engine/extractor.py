from pathlib import Path

import pytesseract

# Set the path to the Tesseract binary
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

OCR_CACHE: dict[Path, str] = {}
"""This is a cache for the Tesseract OCR results. It is a dictionary that maps the image 
path to the extracted text."""


def extract_text(image_path: Path | str) -> str:
    """Extract text from an image using Tesseract OCR."""
    image_path = Path(image_path).resolve()
    if image_path in OCR_CACHE:
        return OCR_CACHE[image_path]
    # Use Tesseract https://github.com/tesseract-ocr/tesseract to extract text from the image
    text = pytesseract.image_to_string(str(image_path), timeout=10)
    OCR_CACHE[image_path] = text
    return text
