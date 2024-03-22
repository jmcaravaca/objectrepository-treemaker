import asyncio
from typing import Union

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from loguru import logger

from config.settings import settings
from config.uipapiconfig import FetchUIPathToken, uipclient_folders, uipclient_libraries
from librarysync.helpers import (
    clear_output,
    compare_versions,
    download_libs,
    get_versions,
    upload_libs,
)

router = APIRouter()


@router.post("/synclibraries")
def sync_libraries():
    html_content = """
    <html>
        <head>
            <title>Librerías sincronizadas</title>
        </head>
        <body>
            <h1>Librerías sincronizadas</h1>
        </body>
    </html>
    """
    UpdateLibs()
    return HTMLResponse(content=html_content, status_code=200)


# Get PRE versions

def UpdateLibs():
    host_pre = f"https://cloud.uipath.com/{settings.UIP_LOGICAL_NAME}/{settings.UIP_TENANT_PRE}/orchestrator_"
    host_pro = f"https://cloud.uipath.com/{settings.UIP_LOGICAL_NAME}/{settings.UIP_TENANT_PRO}/orchestrator_"
    uipclient_libraries.api_client.configuration.access_token = FetchUIPathToken()
    clear_output()
    versionspre = get_versions(host_pre)
    versionspro = get_versions(host_pro)
    compared = compare_versions(versionspre, versionspro)
    logger.info(compared)
    uipclient_libraries.api_client.configuration.host = host_pre
    downloaded = download_libs(compared)
    uipclient_libraries.api_client.configuration.host = host_pro
    upload_libs(downloaded)
    
