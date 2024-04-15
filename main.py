import sys
import download_xml

DEFAULT_XML = "sample.xml"

filename = DEFAULT_XML
if len(sys.argv) > 1:
    filename = sys.argv[1]

download_xml.download_xml_file(filename)
