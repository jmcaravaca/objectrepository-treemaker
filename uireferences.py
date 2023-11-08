import os
from db.schemas import UIReferenceSchema
from db.models import UIReference
from lxml import etree
from startdb import session
from loguru import logger


def find_xaml_files(directory: str) -> list[str]:
    xaml_files = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.xaml'):
                xaml_files.append(os.path.join(root, filename))
    return xaml_files

def generate_schemas(file_path: str, directory: str) -> list[UIReference]:
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
                processname = os.path.basename(directory)
                pydant_instance = UIReferenceSchema(Reference=reference_value , DisplayName=display_name_value,
                                                 ActivityType=activity_type_value,FilePath=relative_path, ProcessName=processname)
                logger.info(pydant_instance)
                outlist.append(pydant_instance)
        return outlist
    except Exception as e:
        print(e)
        logger.error(e)

def add_to_db(uirefschema: UIReferenceSchema) -> UIReference:
    uirefobj = UIReference()
    uirefobj.DisplayName = uirefschema.DisplayName
    uirefobj.FilePath = uirefschema.FilePath
    uirefobj.ActivityType = uirefschema.ActivityType
    uirefobj.Reference = uirefschema.Reference
    with session:
        session.add(uirefobj)
        session.commit()
    return uirefobj
        
        
    
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
    