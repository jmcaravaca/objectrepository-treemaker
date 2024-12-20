import os
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from loguru import logger
from config.secret import (
    REPO_BASE_DIRECTORY,
    REPO_LIBRARY_DIRECTORY,
    REPO_OTHER_DIRECTORY,
    REPO_PROCESS_DIRECTORY,
)

from db.startdb import create_db
from filehelpers import sanitize_path
from parsers.activities import main_activities
from parsers.activityreferences import main_activityreferences
from parsers.configreferences import main_configreferences
from parsers.configs import main_configs
from parsers.getrepos import clone_repos
from parsers.uiobjects import main_uiobjects
from parsers.uireferences import main_uireferences

router = APIRouter()


@router.post("/startdb", response_class=HTMLResponse)
def init_db(delete: str = "no"):
    if delete == "yes":
        os.remove("uidata.db")
        logger.info("DB Removed")
    create_db()
    logger.info("DB Created")

@router.post("/loadactivities", response_class=HTMLResponse)
def get_activities(findsubfolder: str = "yes", librarylocation: str = None):
    logger.debug(f"{librarylocation} : {findsubfolder}")
    if findsubfolder == "yes":
        liblist = [
            os.path.join(librarylocation, foldername)
            for foldername in next(os.walk(librarylocation))[1]
        ]
        for lib in liblist:
            main_activities(folderpath=lib)
    else:
        main_activities(folderpath=librarylocation)

@router.post("/loaduiobjects", response_class=HTMLResponse)
def get_uiobjects(findsubfolder: str = "yes", librarylocation: str = None):
    if findsubfolder == "yes":
        liblist = [
            os.path.join(librarylocation, foldername)
            for foldername in next(os.walk(librarylocation))[1]
        ]
        for lib in liblist:
            main_uiobjects(folderpath=lib)
    else:
        main_uiobjects(folderpath=librarylocation)

@router.post("/loadactivityreferences", response_class=HTMLResponse)
def get_activityreferences(findsubfolder: str = "yes", librarylocation: str = None):
    if findsubfolder == "yes":
        liblist = [
            os.path.join(librarylocation, foldername)
            for foldername in next(os.walk(librarylocation))[1]
        ]
        for lib in liblist:
            main_activityreferences(folderpath=lib)
    else:
        main_activityreferences(folderpath=librarylocation)

@router.post("/loaduireferences", response_class=HTMLResponse)
def get_uireferences(findsubfolder: str = "yes", librarylocation: str = None):
    if findsubfolder == "yes":
        liblist = [
            os.path.join(librarylocation, foldername)
            for foldername in next(os.walk(librarylocation))[1]
        ]
        for lib in liblist:
            main_uireferences(folderpath=lib)
    else:
        main_uireferences(folderpath=librarylocation)

@router.post("/loadconfigreferences", response_class=HTMLResponse)
def get_configreferences(findsubfolder: str = "yes", librarylocation: str = None):
    if findsubfolder == "yes":
        liblist = [
            os.path.join(librarylocation, foldername)
            for foldername in next(os.walk(librarylocation))[1]
        ]
        for lib in liblist:
            main_configreferences(folderpath=lib)
    else:
        main_configreferences(folderpath=librarylocation)

@router.post("/loadconfigs", response_class=HTMLResponse)
def get_configs(findsubfolder: str = "yes", librarylocation: str = None):
    if findsubfolder == "yes":
        liblist = [
            os.path.join(librarylocation, foldername)
            for foldername in next(os.walk(librarylocation))[1]
        ]
        for lib in liblist:
            main_configs(folderpath=lib)
    else:
        main_configs(folderpath=librarylocation)


if __name__ == "__main__":
    proc_path = os.path.join(REPO_BASE_DIRECTORY, REPO_PROCESS_DIRECTORY)
    lib_path = os.path.join(REPO_BASE_DIRECTORY, REPO_LIBRARY_DIRECTORY)
    other_path = os.path.join(REPO_BASE_DIRECTORY, REPO_OTHER_DIRECTORY)
    init_db(delete='yes')
    #clone_repos()
    get_activities(findsubfolder="yes", librarylocation=lib_path)
    get_activityreferences(findsubfolder="yes", librarylocation=proc_path)
    get_configreferences(findsubfolder="yes", librarylocation=proc_path)
    get_configs(findsubfolder="yes", librarylocation=proc_path)
    #get_uiobjects(findsubfolder="yes", librarylocation=lib_path)
    #get_uireferences(findsubfolder="yes", librarylocation=lib_path)
    #get_uireferences(findsubfolder="yes", librarylocation=proc_path)
