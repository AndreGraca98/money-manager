from tempfile import NamedTemporaryFile

import aiofiles
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from src.io.s3 import MinioStore

app = FastAPI()


@app.get("/")
def read_root():
    return FileResponse("public/index.html")


@app.get("/favicon.ico")
async def favicon():
    return FileResponse("public/money.png")


@app.post("/new-file")
async def post_new_file(bucket_name: str, in_file: UploadFile = File(...)):
    tmp = NamedTemporaryFile()
    async with aiofiles.open(tmp.name, "wb") as out_file:
        while content := await in_file.read(1024):  # async read chunk
            await out_file.write(content)  # async write chunk

    MinioStore(bucket_name=bucket_name).store_file(
        object_name=in_file.filename or tmp.name, file_path=tmp.name
    )

    return {"Result": "OK"}


@app.get("/get-file")
async def get_file(bucket_name: str, object_name: str):
    file_path = MinioStore(bucket_name=bucket_name).get_file(object_name)
    return FileResponse(file_path)


@app.get("/list-files")
async def list_files(bucket_name: str):
    return MinioStore(bucket_name=bucket_name).list_files()


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
