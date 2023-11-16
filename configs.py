import os, pathlib
from db.schemas import ConfigSchema
from db.models import Config
from db.startdb import session
from loguru import logger
from filehelpers import find_config_files
import polars as pl
import pandas as pd


# Get Reference of Config values

def get_sheet_names(file_path):
    # We need to use pandas for this because polars doesn't have a get sheets
    xls = pd.ExcelFile(file_path)
    sheet_names = xls.sheet_names
    return sheet_names


def generate_schemas(file_path: str, directory: str) -> list[ConfigSchema]:
    outlist = []
    try:
        # Iterate through each sheet in the Excel file
        for sheet_name in get_sheet_names(file_path):
            # Read the specific range (A:B) in each sheet
            df = pl.read_excel(file_path, sheet_name=sheet_name)
            # Iterate through rows in the DataFrame and extract data
            for row in df.iter_rows():
                # Create a Pydantic model instance for each row if Column B has value
                if row[1]: # If row has value
                    try:
                        processname = os.path.basename(directory)
                        relative_path: str = os.path.join(processname, pathlib.Path(file_path).relative_to(directory).name)
                        pydant_instance = ConfigSchema(Name=row[0], Sheet=sheet_name, Value=row[1], ProcessName=processname,
                                                            FilePath=relative_path)
                        logger.info(pydant_instance)
                        outlist.append(pydant_instance)
                    except Exception as e:
                        print(e)
                        logger.error(e)
        return outlist
    except Exception as e:
        print(e)
        logger.error(e)
        return outlist

def add_to_db(activschema: ConfigSchema) -> Config:
    activobj = Config()
    activobj.ProcessName = activschema.ProcessName
    activobj.Name = activschema.Name
    activobj.Sheet = activschema.Sheet
    activobj.Value = activschema.Value
    activobj.FilePath = activschema.FilePath
    with session:
        session.add(activobj)
        session.commit()
        
def main_activityreferences(folderpath=None):        
    if folderpath is None:
        folderpath = r"C:\Users\Desarrollo1.rpa\Documents\PE004_OPE_GTM_GestionTitulosMarcas"
    files = find_config_files(folderpath)
    logger.debug(files)
    for file in files:
        schemas = generate_schemas(file_path=file, directory=folderpath)
        for schema in schemas:
            try:
                add_to_db(schema)
            except Exception as e:
                logger.error(e)    

if __name__ == '__main__':
    main_activityreferences()

    