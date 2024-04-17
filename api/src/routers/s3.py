from tempfile import NamedTemporaryFile

import aiofiles
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from src.io.s3 import MinioStore

router = APIRouter(prefix="/storage", tags=["Files"])


@router.get("")
async def list_files(bucket_name: str) -> JSONResponse:
    return JSONResponse(
        {"files": list(MinioStore(bucket_name=bucket_name).list_files())}
    )


@router.get("/file")
async def get_file(bucket_name: str, object_name: str) -> FileResponse:
    file_path = MinioStore(bucket_name=bucket_name).get_file(object_name)
    return FileResponse(file_path)


@router.post("/file")
async def post_file(bucket_name: str, in_file: UploadFile = File(...)) -> JSONResponse:
    tmp = NamedTemporaryFile()
    async with aiofiles.open(tmp.name, "wb") as out_file:
        while content := await in_file.read(1024):  # async read chunk
            await out_file.write(content)  # async write chunk

    MinioStore(bucket_name=bucket_name).store_file(
        object_name=in_file.filename or tmp.name, file_path=tmp.name
    )
    return JSONResponse({"message": "File uploaded successfully"}, 201)
