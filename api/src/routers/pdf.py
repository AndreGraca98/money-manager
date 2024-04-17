from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from ..engine.extractor import extract_text
from ..io.s3 import MinioBucket
from ..utils.responses import JSONNotFound

router = APIRouter(prefix="/text", tags=["pdf"])

# OCR_CACHE: dict[Path, str] = {}
# """This is a cache for the OCR results. It is a dictionary that maps the image
# path to the extracted text."""


@router.get("/")
def get_text(image_path: Path):
    file = Path(image_path).resolve()
    # file = MinioStore(bucket_name=bucket_name).get_file(object_name)
    if not file.exists():
        return JSONNotFound("Local file not found.")
    text = extract_text(file)
    return JSONResponse({"file": str(file), "text": text})
