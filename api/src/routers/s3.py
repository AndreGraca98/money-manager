from pathlib import Path
from re import L
from tempfile import TemporaryDirectory

import aiofiles
from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from src.io.pdf import convert_pdf_to_images
from src.io.s3 import MinioBucket, MinioBucketDownloader, MinioFileType
from src.utils.logging import getLogger
from src.utils.responses import (
    JSONBadRequest,
    JSONConflict,
    JSONInternalServerError,
    SelfDestructFileResponse,
)

_log = getLogger(__name__)

router = APIRouter(prefix="/storage", tags=["Files"])


@router.get("")
async def list_files(bucket_name: str) -> JSONResponse:
    bucket = MinioBucket(bucket_name)
    if not bucket.exists():
        return JSONBadRequest(f"Bucket {bucket_name!r} does not exist.")
    _log.debug(f"Listing files in bucket {bucket_name!r}")
    return JSONResponse({"files": list(MinioBucket(bucket_name).list_files())})


@router.get("/file")
def get_file(bucket_name: str, object_name: str) -> FileResponse:
    _log.debug(f"Downloading file {object_name!r} from bucket {bucket_name!r}")
    with MinioBucketDownloader(bucket_name, object_name, False) as downloader:
        file = downloader.download()[object_name]
        suffix = Path(object_name).suffix.upper().lstrip(".")
        return SelfDestructFileResponse(file, media_type=str(MinioFileType[suffix]))


@router.post("/file")
async def post_file(in_file: UploadFile = File(...)) -> JSONResponse:
    try:
        assert in_file.filename, "filename is missing (?)"
        file_name: str = Path(in_file.filename).name

        pdf_bucket = MinioBucket("pdf")
        if pdf_bucket.file_exists(file_name):
            return JSONConflict(f"File {file_name!r} already exists.")

        with TemporaryDirectory() as local_dir:
            local_file = Path(local_dir) / "file.pdf"

            _log.debug(f"Saving file {file_name} to {local_file}")
            async with aiofiles.open(local_file, "wb") as out_file:
                while content := await in_file.read(1024):
                    await out_file.write(content)

            _log.debug(f"Converting PDF {local_file} to images")
            img_paths = convert_pdf_to_images(local_file)

            _log.debug(f"Uploading {len(img_paths)} files to Minio")
            MinioBucket("pdf").store_file(file_name, local_file)
            for img_path in img_paths:
                MinioBucket("images").store_file(
                    f"{file_name}/{img_path.name}", img_path, MinioFileType.JPEG
                )

        return JSONResponse({"message": "File uploaded successfully"}, 201)

    except Exception as err:
        return JSONInternalServerError(err=err)
