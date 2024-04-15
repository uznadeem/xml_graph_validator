import sys

import download_xml
import xml_validator

DEFAULT_XML = "sample.xml"

filename = DEFAULT_XML
if len(sys.argv) > 1:
    filename = sys.argv[1]

xml_data = download_xml.download_xml_file(filename)

if xml_data:
    try:
        xml_validator.validate_xml(xml_data)
        print('XML is Valid')
    except Exception as e:
        print(f"XML is Invalid '{e}'")
