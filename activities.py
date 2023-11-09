import os
from db.schemas import ActivitySchema
from db.models import Activity
from lxml import etree
from startdb import session
from loguru import logger
from filehelpers import find_xaml_files

# TODO: Get activities from library


def generate_schemas(file_path: str, directory: str) -> list[ActivitySchema]:
    outlist = []
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            # Parse the XML with lxml
            tree = etree.parse(file_path)
            elements_with_reference = tree.xpath("//*[@Reference]")
            # Iterate through the elements and get the "Reference" and "DisplayName" values
            for element in elements_with_reference:
                reference_value = element.get("Reference")
                parent_element = element.getparent()
                grandparent_element = parent_element.getparent()
                display_name_value = grandparent_element.get("DisplayName")
                activity_type_value = grandparent_element.tag.split('}')[-1]
                relative_path = os.path.relpath(file_path).replace('..\\', '')
                pydant_instance = ActivitySchema(Reference=reference_value , DisplayName=display_name_value,
                                                 ActivityType=activity_type_value,FilePath=relative_path)
                logger.info(pydant_instance)
                outlist.append(pydant_instance)
        return outlist
    except Exception as e:
        print(e)
        logger.error(e)

def add_to_db(activschema: ActivitySchema) -> Activity:
    activobj = Activity()
    activobj.DisplayName = activschema.DisplayName
    activobj.FilePath = activschema.FilePath
    activobj.ActivityType = activschema.ActivityType
    activobj.Reference = activschema.Reference
    with session:
        session.add(activobj)
        session.commit()
        
        
    
if __name__ == '__main__':
    logger.debug("Testing...")
    folderpath = r"C:\Users\Desarrollo1.rpa\Documents\ClarkeModetRPA.006Apiges"
    files = find_xaml_files(folderpath)
    for file in files:
        schemas = generate_schemas(file_path=file, directory=folderpath)
        for schema in schemas:
            try:
                add_to_db(schema)
            except Exception as e:
                logger.error(e)
    