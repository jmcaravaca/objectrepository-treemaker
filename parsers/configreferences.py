import os, pathlib
from db.schemas import ConfigReferenceSchema
from db.models import ConfigReference
from db.startdb import session
from loguru import logger
from filehelpers import find_xaml_files
import re


# Get Reference of Config values

def generate_schemas(file_path: str, directory: str) -> list[ConfigReferenceSchema]:
    outlist = []
    repattern = re.compile(r'Config\(\"(.*?)\"\)|Config\(&quot;(.*?)&quot;\)')
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            file_content = file.read()
            matches = repattern.findall(file_content)
            results = [match[0] if match[0] else match[1] for match in matches]
        for result in results:
            keyreference = result
            processname = os.path.basename(directory)
            workflowname = os.path.basename(file_path)
            relative_path: str = os.path.join(processname, pathlib.Path(file_path).relative_to(directory).name)
            pydant_instance = ConfigReferenceSchema(ProcessName=processname, WorkflowName=workflowname, KeyReference=keyreference,
                                                    FilePath=relative_path)
            logger.info(pydant_instance)
            outlist.append(pydant_instance)
        return outlist
    except Exception as e:
        print(e)
        logger.error(e)

def add_to_db(activschema: ConfigReferenceSchema) -> ConfigReference:
    activobj = ConfigReference()
    activobj.ProcessName = activschema.ProcessName
    activobj.WorkflowName = activschema.WorkflowName
    activobj.KeyReference = activschema.KeyReference
    activobj.FilePath = activschema.FilePath
    with session:
        session.add(activobj)
        session.commit()
        
def main_configreferences(folderpath=None):        
    if folderpath is None:
        folderpath = r"C:\Users\Desarrollo1.rpa\Documents\PE004_OPE_GTM_GestionTitulosMarcas"
    files = find_xaml_files(folderpath)
    logger.debug(files)
    for file in files:
        schemas = generate_schemas(file_path=file, directory=folderpath)
        for schema in schemas:
            try:
                add_to_db(schema)
            except Exception as e:
                logger.error(e)    

if __name__ == '__main__':
    main_configreferences()

    