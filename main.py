from loguru import logger
import os
from parsers.activities import main_activities
from parsers.uiobjects import main_uiobjects
from parsers.uireferences import main_uireferences
from parsers.activityreferences import main_activityreferences
from parsers.configs import main_configs
from parsers.configreferences import main_configreferences
from parsers.getrepos import clone_repos
from db.startdb import create_db
from secret import (
    REPO_BASE_DIRECTORY,
    REPO_LIBRARY_DIRECTORY,
    REPO_PROCESS_DIRECTORY,
    REPO_OTHER_DIRECTORY,
)

import sys, os

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from pathlib import Path
from routers.librarydocs import router as libdocrouter
from routers.db import router as dbrouter
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

