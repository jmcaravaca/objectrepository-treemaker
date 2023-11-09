import os
from db.schemas import ActivitySchema
from db.models import Activity
from startdb import session
from loguru import logger
from filehelpers import find_xaml_files

# Get Activities from library


def generate_schema(file_path: str, directory: str) -> list[ActivitySchema]:
    try:
        relative_path = os.path.relpath(file_path).replace('..\\', '')
        libraryname = os.path.basename(directory)
        name = os.path.basename(file_path)
        pydant_instance = ActivitySchema(LibraryName=libraryname, Name=name, FilePath=relative_path)
        logger.info(pydant_instance)
        return pydant_instance
    except Exception as e:
        print(e)
        logger.error(e)

def add_to_db(activschema: ActivitySchema) -> Activity:
    activobj = Activity()
    activobj.LibraryName = activschema.LibraryName
    activobj.FilePath = activschema.FilePath
    activobj.Name = activschema.Name
    with session:
        session.add(activobj)
        session.commit()
        
        
    
if __name__ == '__main__':
    logger.debug("Testing...")
    folderpath = r"C:\Users\Desarrollo1.rpa\Documents\ClarkeModetRPA.006Apiges"
    files = find_xaml_files(folderpath)
    for file in files:
        schema = generate_schema(file_path=file, directory=folderpath)
        try:
            add_to_db(schema)
        except Exception as e:
            logger.error(e)
    