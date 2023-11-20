import os, pathlib
import json
from db.schemas import UIObjectSchema
from db.models import UIObject
from db.startdb import session
from loguru import logger
from filehelpers import find_metadata_files


# Get metadata of ui objects


def generate_schema(file_path: str, directory: str) -> UIObjectSchema:
    try:
        with open(file_path, "r", encoding="utf-8-sig") as file:
            data = json.load(file)
            if "Reference" in data:
                libraryname = os.path.basename(directory)
                relative_path: str = os.path.join(
                    libraryname, pathlib.Path(file_path).relative_to(directory).name
                )
                pydant_instance = UIObjectSchema(
                    Id=data["Id"],
                    Reference=data["Reference"],
                    ParentRef=data["ParentRef"],
                    Name=data["Name"],
                    Type=data["Type"],
                    Created=data["Created"],
                    FilePath=relative_path,
                    LibraryName=libraryname,
                )
                logger.info(pydant_instance)
                return pydant_instance
    except Exception as e:
        print(e)
        logger.error(e)


def add_to_db(uischema: UIObjectSchema) -> UIObject:
    uiobj = UIObject()
    uiobj.Id = uischema.Id
    uiobj.Created = uischema.Created
    uiobj.FilePath = uischema.FilePath
    uiobj.Name = uischema.Name
    uiobj.ParentRef = uischema.ParentRef
    uiobj.Reference = uischema.Reference
    uiobj.Type = uischema.Type
    with session:
        session.add(uiobj)
        session.commit()


def main_uiobjects(folderpath=None):
    if folderpath is None:
        folderpath = r"C:\Users\Desarrollo1.rpa\Documents\ClarkeModetUI.006Apiges"
    files = find_metadata_files(folderpath)
    for file in files:
        try:
            schema = generate_schema(file, folderpath)
            add_to_db(schema)
        except Exception as e:
            logger.error(e)


if __name__ == "__main__":
    main_uiobjects()
