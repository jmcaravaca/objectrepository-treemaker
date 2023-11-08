import os
import json

def find_metadata_files(directory):
    metadata_files = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.metadata'):
                metadata_files.append(os.path.join(root, filename))
    return metadata_files

def extract_references(metadata_files):
    reference_dict = {}
    for file_path in metadata_files:
        try:
            with open(file_path, 'r', encoding="utf-8-sig") as file:
                data = json.load(file)
                if 'Reference' in data:
                    reference = data['Reference']
                    reference_dict[reference] = file_path
        except Exception as e:
            print(e)
    return reference_dict

uiobjects_directory = '.uiobjects'
metadata_files = find_metadata_files(uiobjects_directory)
references_dict = extract_references(metadata_files)

# Print the dictionary with Reference as keys and file paths as values
for reference, file_path in references_dict.items():
    print(f'Reference: {reference}, File Path: {file_path}')
