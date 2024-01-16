import os

def sanitize_path(user_input):
    # Split the user input into components
    path_components = user_input.split('/')

    # Join the components using os.path.join() to create a platform-independent path
    sanitized_path = os.path.join(*path_components)

    return sanitized_path


def find_xaml_files(directory: str) -> list[str]:
    xaml_files = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".xaml"):
                xaml_files.append(os.path.join(root, filename))
    return xaml_files

def read_html(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def find_metadata_files(directory: str) -> list[str]:
    metadata_files = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".metadata"):
                metadata_files.append(os.path.join(root, filename))
    return metadata_files


def find_project_files(directory: str) -> list[str]:
    metadata_files = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename == "project.json":
                metadata_files.append(os.path.join(root, filename))
    return metadata_files


def find_config_files(directory: str) -> list[str]:
    configfiles = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".xlsx") and "config" in filename.lower():
                configfiles.append(os.path.join(root, filename))
    return configfiles
