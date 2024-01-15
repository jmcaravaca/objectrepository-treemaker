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
from filehelpers import read_template, sanitize_path
import sys, os
from generatemd import generate_md_files

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
import markdown2
from pathlib import Path

logger.remove()
logger.add(sys.stderr, level="DEBUG")

app = FastAPI()



index_template = read_template(os.path.join("templates", "index_template.html"))
markdown_template = read_template(os.path.join("templates","markdown_template.html"))

@app.get("/", response_class=HTMLResponse)
async def redirect_to_index():
    return RedirectResponse(url="/index")


@app.get("/index", response_class=HTMLResponse)
async def index():
    return HTMLResponse(content="<html><body><h1>Index!</h1></body></html>")


@app.post("/librarydocs/generate", response_class=HTMLResponse)
async def libdocsgenerate(folderpath: str = None):
    """Generate library docs.

    Args:
        folderpath (str): Relative path. ex: Repos/Libraries/ClarkeModetRPA.000WindowsExplorer

    Returns:
        _type_: _description_
    """
    generate_md_files(sanitize_path(folderpath))
    return HTMLResponse(content="<html><body><h1>Files generated!</h1></body></html>")


@app.get("/librarydocs", response_class=HTMLResponse)
async def libdocsindex():
    librarydocs = Path("librarydocs") 
    folder_list = [folder.name for folder in librarydocs.iterdir() if folder.is_dir()]
    folder_list.sort()
    index_content = index_template.format(file_list="".join(f'<li><a href="/librarydocs/{folder_name}">{folder_name}</a></li>' for folder_name in folder_list))
    return HTMLResponse(content=index_content)

@app.get("/librarydocs/{lib_name}", response_class=HTMLResponse)
async def libdocsindex(lib_name: str):
    markdown_folder = Path(os.path.join("librarydocs", lib_name)) #Placeholder 
    file_list = [file.stem for file in markdown_folder.glob("*.md")]
    file_list.sort()
    index_content = index_template.format(file_list="".join(f'<li><a href="/librarydocs/{lib_name}/{file_name}">{file_name}</a></li>' for file_name in file_list))
    return HTMLResponse(content=index_content)

@app.get("/librarydocs/{lib_name}/{file_name}", response_class=HTMLResponse)
async def read_markdown(file_name: str, lib_name: str):
    markdown_file_path = Path(os.path.join("librarydocs", lib_name, file_name + ".md")) #Placeholder 
    if not markdown_file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    with open(markdown_file_path, "r", encoding="utf-8") as file:
        markdown_content = file.read()
    html_content = markdown2.markdown(markdown_content)
    html_content_with_styles = markdown_template.format(html_content=html_content)
    return HTMLResponse(content=html_content_with_styles)



@app.get("/librarydocs/{file_name}", response_class=HTMLResponse)
def init_db(delete: str = "no"):
    if delete == "yes":
        os.remove("uidata.db")
        logger.info("DB Removed")
    create_db()
    logger.info("DB Created")

@app.post("/db/loadactivities", response_class=HTMLResponse)
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

@app.post("/db/loaduiobjects", response_class=HTMLResponse)
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

@app.post("/db/loadactivityreferences", response_class=HTMLResponse)
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

@app.post("/db/loaduireferences", response_class=HTMLResponse)
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

@app.post("/db/loadconfigreferences", response_class=HTMLResponse)
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

@app.post("/db/loadconfigs", response_class=HTMLResponse)
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
