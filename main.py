
import sys

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from loguru import logger

from routers.db import router as dbrouter
from routers.librarydocs import router as libdocrouter
from routers.librarysync import router as libsyncrouter

logger.remove()
logger.add(sys.stderr, level="DEBUG")

app = FastAPI()
app.include_router(libdocrouter, prefix="/librarydocs", tags=["librarydocs"])
app.include_router(dbrouter, prefix="/db", tags=["db"])
app.include_router(libsyncrouter, prefix="/librarysync", tags=["librarysync"])


@app.get("/", response_class=HTMLResponse)
async def redirect_to_index():
    return RedirectResponse(url="/index")


@app.get("/index", response_class=HTMLResponse)
async def index():
    return HTMLResponse(content="<html><body><h1>Index!</h1></body></html>")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
