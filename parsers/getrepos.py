from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
import shutil
import git
import os
import re
from loguru import logger
from secret import (
    AZURE_ORG_URL,
    AZURE_PAT,
    REPO_PROCESS_DIRECTORY,
    REPO_BASE_DIRECTORY,
    REPO_LIBRARY_DIRECTORY,
    REPO_OTHER_DIRECTORY,
)


def clone_repos(clone_directory: str = REPO_BASE_DIRECTORY):
    # Personal access token authentication
    credentials = BasicAuthentication("", AZURE_PAT)

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
            repo_url = repo.ssh_url  # Cloned with SSH Key
            if re.search(r"[a-zA-z]{2}\d{3}_", repo_name):  # Processes
                destination_path = os.path.join(clone_directory, REPO_PROCESS_DIRECTORY, repo.name)
            elif re.search(r"RPA\.\d{3}|UI\.\d{3}", repo_name):
                destination_path = os.path.join(clone_directory, REPO_LIBRARY_DIRECTORY, repo.name)
            else:
                destination_path = os.path.join(clone_directory, REPO_OTHER_DIRECTORY, repo.name)
            logger.info(f"Cloning: {repo_name}")
            git.Git().clone(repo_url, destination_path)
            logger.info(f"Successfully cloned: {repo_name}")
        except Exception as e:
            logger.error(e)

    logger.info("Cloning completed.")


if __name__ == "__main__":
    clone_repos()
