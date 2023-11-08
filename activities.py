from lxml import etree
import os, json

# Read the XML from the file
file_path = "Comun\SaveAs.xaml"

# Parse the XML with lxml
tree = etree.parse(file_path)

# Find all elements with the "Reference" attribute
elements_with_reference = tree.xpath("//*[@Reference]")

# Iterate through the elements and get the "Reference" and "DisplayName" values
for element in elements_with_reference:
    reference_value = element.get("Reference")
    parent_element = element.getparent()
    grandparent_element = parent_element.getparent()
    display_name_value = grandparent_element.get("DisplayName")
    print(f"Reference: {reference_value}, DisplayName: {display_name_value}")



