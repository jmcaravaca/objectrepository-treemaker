import json
import os
import pathlib

from loguru import logger

from db.models import Activity
from db.schemas import ActivitySchema
from db.startdb import session
from filehelpers import find_project_files, find_xaml_files

# Get Activities from library


def generate_schema(
    file_path: str, directory: str, test_cases: list[str], type: str = None
) -> list[ActivitySchema]:
    try:
        libraryname: str = os.path.basename(directory)
        relative_path: str = os.path.join(
            libraryname, pathlib.Path(file_path).relative_to(directory).name
        )
        name: str = os.path.splitext(os.path.basename(file_path))[0]
        if type is None:
            if name in test_cases:
                type = "Test Case"
            else:
                type = "Activity"
        pydant_instance = ActivitySchema(
            LibraryName=libraryname, Name=name, FilePath=relative_path, Type=type
        )
        logger.debug(pydant_instance)
        return pydant_instance
    except Exception as e:
        print(e)
        logger.error(e)


def get_test_cases(file_path: str) -> list[str]:
    with open(file_path, "r", encoding="utf-8") as file:
        jsondata = json.load(file)
        # Get the filename without extension of all test cases
        list_files = [
            os.path.splitext(item["fileName"].split("\\")[-1])[0]
            for item in jsondata["designOptions"]["fileInfoCollection"]
        ]
        return list_files


def add_to_db(activschema: ActivitySchema) -> Activity:
    activobj = Activity()
    activobj.LibraryName = activschema.LibraryName
    activobj.FilePath = activschema.FilePath
    activobj.Name = activschema.Name
    activobj.Type = activschema.Type
    with session:
        session.add(activobj)
        session.commit()


def main_activities(folderpath: str = None, foldertype: str = None):
    if folderpath is None:
        folderpath = r"C:\Users\Desarrollo1.rpa\Documents\ClarkeModetRPA.006Apiges"
    # Build test case list
    project_files = find_project_files(folderpath)
    logger.info(f"Generating Activity Schemas for: {project_files}")
    test_cases = []
    for file in project_files:
        temp_test_cases = get_test_cases(file)
        test_cases = test_cases + temp_test_cases
    activity_files = find_xaml_files(folderpath)
    for file in activity_files:
        schema = generate_schema(
            file_path=file, directory=folderpath, test_cases=test_cases, type=foldertype
        )
        try:
            add_to_db(schema)
        except Exception as e:
            logger.error(e)


if __name__ == "__main__":
    main_activities()
