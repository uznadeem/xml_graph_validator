import sys
import json

import download_xml
import xml_validator
import db_handler

DEFAULT_XML = "sample.xml"

db_handler.create_tables()

filename = DEFAULT_XML
if len(sys.argv) > 1:
    filename = sys.argv[1]

xml_data = download_xml.download_xml_file(filename)

if xml_data:
    try:
        print(xml_validator.validate_xml(xml_data))

        db_handler.data_insert(xml_data)

        print(db_handler.find_cycles_in_graph('g0'))

        with open('frontend_query.json', 'r') as file:
            json_query= json.load(file)

        json_response=db_handler.process_queries(json_query)

        print(json_response)
        with open('response.json','w') as file:
            file.write(json_response)

    except Exception as e:
        print(f"XML is Invalid '{e}'")
