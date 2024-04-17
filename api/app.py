from fastapi import FastAPI
from fastapi.responses import FileResponse
from src.env import ENV
from src.routers.pdf import router as pdf_router
from src.routers.s3 import router as s3_router
from src.utils.logging import getLogger

ENV()  # Validate environment variables

_log = getLogger(__name__)

app = FastAPI()
app.include_router(s3_router)
app.include_router(pdf_router)

_log.info("Money-Manager API started")


@app.get("/")
def root() -> FileResponse:
    return FileResponse("public/index.html")


@app.get("/favicon.ico")
async def favicon() -> FileResponse:
    return FileResponse("public/money.png")
