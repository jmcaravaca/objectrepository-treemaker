import json
import os
from pathlib import Path

import markdown2
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader, Template
from loguru import logger

from filehelpers import read_template, sanitize_path

router = APIRouter()


# Helper function to generate MD files from path
def generate_md_files(libfolder: str = None):
    if libfolder is None:
        raise ValueError("Invalid Argument")
    logger.info("Generating Markdown files for: " + libfolder)
    # Step 4: Define output directory
    output_directory = os.path.join("librarydocs", os.path.basename(libfolder))
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)
    # Step 2: Identify JSON files in the folder and its subfolders
    json_files = [os.path.join(root, f) for root, dirs, files in os.walk(libfolder) for f in files if f.endswith('.json')]
    # Step 3: Read Jinja Template from file
    template_filename = "mdtemplate.jinja"
    template_path = os.path.join(os.path.dirname(__file__), "templates", template_filename)

    # Create Jinja Environment and Template
    env = Environment(loader=FileSystemLoader(os.path.dirname(template_path)))
    template = env.get_template(template_filename)
    # Step 4: Process each JSON file
    for json_file in json_files:
        try:
            #json_file_path = os.path.join(libfolder, json_file)
            json_file_path = json_file
            # Read JSON file
            with open(json_file_path, 'r') as json_file_content:
                json_data = json.load(json_file_content)

            # Extract information
            activity_name = json_data["DisplayName"]
            tooltip = json_data["Tooltip"]

            # Extract information from the Arguments array
            argument_info = []
            for argument in json_data["Arguments"]:
                argument_name = argument["Name"]
                argument_tooltip = argument["Tooltip"]
                argument_category = argument["Category"]
                argument_info.append({"Name": argument_name, "Tooltip": argument_tooltip, "Category": argument_category})


            # Fill in Jinja template
            filled_template = template.render(activity_name=activity_name, tooltip=tooltip,
                                              argument_info=argument_info)  # Add more variables as needed

            # Save the filled template to a new file
            # Create output file path
            output_file_name = os.path.splitext(os.path.splitext(os.path.basename(json_file_path))[0])[0] + ".md"
            output_file_path = os.path.join(output_directory, output_file_name)

            # Save the filled template to the output file
            with open(output_file_path, 'w') as output_file:
                output_file.write(filled_template)
        except Exception as e:
          logger.error(f"File {json_file} error {e}")

    logger.info("Files processed successfully.")


if __name__ == '__main__':
    generate_md_files(sanitize_path("Repos/Libraries/ClarkeModetRPA.000WindowsExplorer"))



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

