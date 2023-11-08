import os
import json
from schemas import UIObjectSchema
from models import UIObject
from startdb import session
from loguru import logger


def find_metadata_files(directory: str) -> list[str]:
    metadata_files = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.metadata'):
                metadata_files.append(os.path.join(root, filename))
    return metadata_files

def generate_schema(file_path: str) -> UIObjectSchema:
    try:
        with open(file_path, 'r', encoding="utf-8-sig") as file:
            data = json.load(file)
            if 'Reference' in data:
                pydant_instance = UIObjectSchema(Id=data['Id'], Reference=data['Reference'], ParentRef=data['ParentRef'],
                                                 Name=data['Name'], Type=data['Type'], Created=data['Created'], FilePath=file_path)
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
        
        