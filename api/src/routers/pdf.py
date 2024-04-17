from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.engine.extractor import extract_text
from src.io.s3 import MinioBucketDownloader
from src.utils.logging import getLogger
from src.utils.responses import JSONNotFound

_log = getLogger(__name__)

router = APIRouter(prefix="/text", tags=["pdf"])


@router.get("/")
def get_text(object_name: str):
    with MinioBucketDownloader("images", [object_name]) as downloader:
        _log.debug(
            f"Downloading file {object_name!r} from "
            f"bucket {downloader._bucket._bucket_name!r}"
        )
        file = downloader.download()[object_name]
        text = extract_text(file)
    return JSONResponse({"file": str(file), "text": text})
