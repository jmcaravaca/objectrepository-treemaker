import os, pathlib
from db.schemas import ActivityReferenceSchema
from db.models import ActivityReference
from lxml import etree
from db.startdb import session
from loguru import logger
from filehelpers import find_xaml_files


# Get Reference (Invokes) of library activities in workflow

def get_filtered_namespaces(strfilter: str, root) -> dict:
    # Define a dictionary to store the namespaces
    namespaces = {}
    # Iterate through the attributes of the root element to find the namespaces
    for key, value in root.nsmap.items():
        if strfilter in value:
            # Extract the namespace prefix and assembly name (library)
            library = value.split('assembly=')[-1]
            namespaces[key] = library
    return namespaces

def generate_schemas(file_path: str, directory: str) -> list[ActivityReferenceSchema]:
    outlist = []
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            # Parse the XML with lxml
            tree = etree.parse(file_path)
            root = tree.getroot()
            namespaces = get_filtered_namespaces(strfilter="Clarke", root=root)
            for namespace, assembly in namespaces.items():
                nselements = root.xpath(f"//*[starts-with(name(), '{namespace}:')]")
                for element in nselements:
                    tagname = element.tag.split('}')[-1]
                    if "." in tagname:
                        # "Fake" element, skip
                        continue
                    displayname = element.get("DisplayName") 
                    displayname = displayname if displayname else tagname # If displayname is empty, just use tagname
                    processname = os.path.basename(directory)
                    relative_path: str = os.path.join(processname, pathlib.Path(file_path).relative_to(directory).name)
                    pydant_instance = ActivityReferenceSchema(ActivityName=tagname, DisplayName=displayname, Assembly=assembly,
                                                              FilePath=relative_path, ProcessName=processname)
                    logger.info(pydant_instance)
                    outlist.append(pydant_instance)
        return outlist
    except Exception as e:
        print(e)
        logger.error(e)

def add_to_db(activschema: ActivityReferenceSchema) -> ActivityReference:
    activobj = ActivityReference()
    activobj.ActivityName = activschema.ActivityName
    activobj.FilePath = activschema.FilePath
    activobj.DisplayName = activschema.DisplayName
    activobj.Assembly = activschema.Assembly
    activobj.ProcessName = activschema.ProcessName
    with session:
        session.add(activobj)
        session.commit()
        
def main_activityreferences():        
    logger.debug("Testing...")
    folderpath = r"C:\Users\Desarrollo1.rpa\Documents\PE004_OPE_GTM_GestionTitulosMarcas"
    files = find_xaml_files(folderpath)
    for file in files:
        schemas = generate_schemas(file_path=file, directory=folderpath)
        for schema in schemas:
            try:
                add_to_db(schema)
            except Exception as e:
                logger.error(e)    

if __name__ == '__main__':
    main_activityreferences()

    