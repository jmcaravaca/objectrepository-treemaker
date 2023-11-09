import os

def find_xaml_files(directory: str) -> list[str]:
    xaml_files = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.xaml'):
                xaml_files.append(os.path.join(root, filename))
    return xaml_files

def find_metadata_files(directory: str) -> list[str]:
    metadata_files = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.metadata'):
                metadata_files.append(os.path.join(root, filename))
    return metadata_files