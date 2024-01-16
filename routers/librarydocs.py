from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from pathlib import Path
import os

from filehelpers import sanitize_path, read_template
import os
from generatemd import generate_md_files
import markdown2

router = APIRouter()



@router.post("/generate", response_class=HTMLResponse)
async def libdocsgenerate(folderpath: str = None):
    """Generate library docs.

    Args:
        folderpath (str): Relative path. ex: Repos/Libraries/ClarkeModetRPA.000WindowsExplorer

    Returns:
        _type_: _description_
    """
    generate_md_files(sanitize_path(folderpath))
    return HTMLResponse(content="<html><body><h1>Files generated!</h1></body></html>")


@router.get("/", response_class=HTMLResponse)
async def libdocsindex():
    librarydocs = Path("librarydocs") 
    folder_list = [folder.name for folder in librarydocs.iterdir() if folder.is_dir()]
    folder_list.sort()
    template = read_template("mdindex.jinja")
    index_content = template.render(lib_list=folder_list)
    return HTMLResponse(content=index_content)

@router.get("/{lib_name}", response_class=HTMLResponse)
async def libdocsindex(lib_name: str):
    markdown_folder = Path(os.path.join("librarydocs", lib_name)) #Placeholder 
    file_list = [file.stem for file in markdown_folder.glob("*.md")]
    file_list.sort()
    template = read_template("mdlibindex.jinja")
    index_content = template.render(file_list=file_list, lib_name=lib_name)
    return HTMLResponse(content=index_content)

@router.get("/{lib_name}/{file_name}", response_class=HTMLResponse)
async def read_markdown(file_name: str, lib_name: str):
    markdown_file_path = Path(os.path.join("librarydocs", lib_name, file_name + ".md")) #Placeholder 
    if not markdown_file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    with open(markdown_file_path, "r", encoding="utf-8") as file:
        markdown_content = file.read()
    html_content = markdown2.markdown(markdown_content)
    template = read_template("mdfile.jinja")
    index_content = template.render(html_content=html_content)
    return HTMLResponse(content=index_content)

