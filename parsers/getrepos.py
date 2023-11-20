from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
import shutil
import git
import os
import re
from loguru import logger
from secret import AZURE_ORG_URL, AZURE_PAT



def clone_repos(clone_directory: str = 'Repos'):
    # Personal access token authentication
    credentials = BasicAuthentication('', AZURE_PAT)
    
    # Create a connection to the Azure DevOps organization
    connection = Connection(base_url=AZURE_ORG_URL, creds=credentials)
    
    # Get a Git client
    git_client = connection.clients.get_git_client()
    
    # Get the list of repositories
    repos = git_client.get_repositories()
    
    # Specify the directory where you want to clone the repositories and init
    shutil.rmtree(clone_directory, ignore_errors=True)
    os.makedirs(clone_directory)
    
    # Iterate through each repository and clone it
    for repo in repos:
        try:
            repo_name = repo.name
            repo_url = repo.ssh_url #Cloned with SSH Key
            if re.match(r'[a-zA-z]{2}\d{3}_', repo_name): #Processes
                destination_path = os.path.join(clone_directory, 'Processes')
            elif re.match(r'RPA\.\d{3}|UI\.\d{3}', repo_name):
                destination_path = os.path.join(clone_directory, 'Libraries')
            else:
                destination_path = os.path.join(clone_directory, 'Others')
            logger.info(f"Cloning: {repo_name}")
            git.Git().clone(repo_url, destination_path)
            logger.info(f'Successfully cloned: {repo_name}')
        except Exception as e:
            logger.error(e)
    
    logger.info('Cloning completed.')

if __name__ == '__main__':
    clone_repos()