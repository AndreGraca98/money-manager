from fastapi import FastAPI
from fastapi.responses import FileResponse
from src.env import ENV
from src.routers.pdf import router as pdf_router
from src.routers.s3 import router as s3_router

ENV()  # Validate environment variables

app = FastAPI()
app.include_router(s3_router)
app.include_router(pdf_router)


@app.get("/")
def root() -> FileResponse:
    return FileResponse("public/index.html")


@app.get("/favicon.ico")
async def favicon() -> FileResponse:
    return FileResponse("public/money.png")


# import tempfile
# from pathlib import Path

# import pytesseract
# from pdf2image import convert_from_path
# from pdf2image.exceptions import (
#     PDFInfoNotInstalledError,
#     PDFPageCountError,
#     PDFSyntaxError,
# )


# def pdf2image(pdf_path: Path | str):
#     with tempfile.TemporaryDirectory() as path:
#         images_from_path = convert_from_path(
#             Path(pdf_path).resolve(), output_folder=path
#         )
#         # Do something here


# def extract_text_from_image(image):
#     text = pytesseract.image_to_string(image)
#     return text
