from pathlib import Path
from tempfile import mkdtemp

import aiofiles
from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse

from ..io.pdf import convert_pdf_to_images
from ..io.s3 import MinioBucket, MinioBucketDownloader, MinioFileType
from ..utils.responses import (
    JSONBadRequest,
    JSONConflict,
    JSONInternalServerError,
    SelfDestructFileResponse,
)

router = APIRouter(prefix="/storage", tags=["Files"])


@router.get("")
async def list_files(bucket_name: str) -> JSONResponse:
    bucket = MinioBucket(bucket_name)
    if not bucket.exists():
        return JSONBadRequest(f"Bucket {bucket_name!r} does not exist.")
    return JSONResponse({"files": list(MinioBucket(bucket_name).list_files())})


@router.get("/file")
def get_file(bucket_name: str, object_name: str) -> FileResponse:
    with MinioBucketDownloader(bucket_name, object_name) as downloader:
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

        local_dir = Path("/tmp") / "mm"
        local_file = local_dir / file_name / "file.pdf"
        local_file.parent.mkdir(parents=True, exist_ok=True)
        # Local file in format: /tmp/mm/<filename>/file.pdf

        # mkdtemp(dir=str(local_dir))

        async with aiofiles.open(local_file, "wb") as out_file:
            while content := await in_file.read(1024):
                await out_file.write(content)

        img_paths = convert_pdf_to_images(local_file)

        MinioBucket("pdf").store_file(file_name, local_file)
        for img_path in img_paths:
            MinioBucket("images").store_file(
                f"{file_name}/{img_path.name}", img_path, MinioFileType.JPEG
            )

        return JSONResponse({"message": "File uploaded successfully"}, 201)

    except Exception as err:
        return JSONInternalServerError(err=err)
