import os
import json
from db.schemas import UIObjectSchema
from db.models import UIObject
from startdb import session
from loguru import logger
from filehelpers import find_metadata_files



def generate_schema(file_path: str, directory: str) -> UIObjectSchema:
    try:
        with open(file_path, 'r', encoding="utf-8-sig") as file:
            data = json.load(file)
            if 'Reference' in data:
                relative_path = os.path.relpath(file_path).replace('..\\', '')
                libraryname = os.path.basename(folderpath)
                pydant_instance = UIObjectSchema(Id=data['Id'], Reference=data['Reference'], ParentRef=data['ParentRef'],
                                                 Name=data['Name'], Type=data['Type'], Created=data['Created'],
                                                 FilePath=relative_path, LibraryName=libraryname)
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
        
if __name__ == '__main__':
    logger.debug("Testing...")
    folderpath = r"C:\Users\Desarrollo1.rpa\Documents\ClarkeModetUI.006Apiges"
    files = find_metadata_files(folderpath)
    for file in files:
        try:
            schema = generate_schema(file, folderpath)
            add_to_db(schema)
        except Exception as e:
            logger.error(e)