import os
import shutil

from loguru import logger

from config.uipapiconfig import uipclient_libraries


def get_versions(host: str) -> list:
    """Get list of versions for libraries

    Args:
        token (str): access token

    Returns:
        list: _description_
    """
    #Update token
    if host != "":
        uipclient_libraries.api_client.configuration.host = host
    select="key, id"
    filter="startswith(key, 'ClarkeModetRPA') or startswith(key, 'ClarkeModetUI')"
    libs = uipclient_libraries.libraries_get(select=select, filter=filter)
    versionsflat=[]
    for library in libs.value:
        logger.info(library.id)
        select="key"
        versions = uipclient_libraries.libraries_get_versions_by_packageid(package_id=library.id)
        for version in versions.value:
            versionsflat.append(version.key)
    return versionsflat
    
def clear_output():
    folder_path = os.path.join("librarysync", "OUTPUT")
    try:
        shutil.rmtree(folder_path)
        logger.info(f"The folder '{folder_path}' and its contents have been deleted.")
    except FileNotFoundError:
        logger.info(f"The folder '{folder_path}' does not exist.")
    except Exception as e:
        logger.info(f"An error occurred: {e}")

def compare_versions(listpre, listpro):
    setpre = set(listpre)
    setpro = set(listpro)
    result = list(setpre - setpro)
    return result

def download_libs(versions: list[str]) -> list[str]:
    downloaded = []
    for version in versions:
        try:
            logger.info(version)
            response = uipclient_libraries.libraries_download_package_by_key(key=version, _preload_content=False)
            if response.status == 200:
                file_name = f"{version.replace(':','_')}.nupkg"
                folder_base = os.path.join("librarysync", "OUTPUT")
                # Open the local file in binary write mode
                local_folder_path = os.path.join(os.getcwd(), folder_base)
                # Create the "OUTPUT" folder if it doesn't exist
                if not os.path.exists(local_folder_path):
                    os.makedirs(local_folder_path)
                # Combine the folder path and file name to get the full local file path
                local_file_path = os.path.join(local_folder_path, file_name)
                with open(local_file_path, 'wb') as local_file:
                    # Read data from the HTTPResponse and write it to the local file
                    local_file.write(response.data)          
                logger.info("File downloaded")  
                downloaded.append(local_file_path)
        except Exception as e:
            logger.error(e)
    return downloaded

def upload_libs(downloaded: list[str]):
    for file in downloaded:
        logger.debug(file)
        try:
            resp = uipclient_libraries.libraries_upload_package(file=file, _request_timeout=10)
            logger.info(resp)
        except Exception as e:
            logger.error(e)
        