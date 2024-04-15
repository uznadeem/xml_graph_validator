import subprocess
import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
from db_handler import clean_data

clean_data()

def test_main_script_output_default():
    clean_data()
    result = subprocess.run(['python3', 'main.py'], stdout=subprocess.PIPE, text=True)
    expected_output = (
        "XML file downloaded successfully and saved in the 'downloaded_xml_files' directory.\n"
        "XML is Valid\n"
        "[('a', 'a')]\n"
        "{\"answers\": [{\"paths\": {\"from\": \"a\", \"to\": \"e\", \"paths\": [[\"a\", \"e\"]]}}, {\"cheapest\": {\"from\": \"a\", \"to\": \"e\", \"path\": [\"a\", \"e\"]}}]}\n"
    )
    assert result.stdout.strip() == expected_output.strip()

def test_main_script_output_with_filename():
    clean_data()
    result = subprocess.run(['python3', 'main.py', 'sample.xml'], stdout=subprocess.PIPE, text=True)
    expected_output = (
        "XML file downloaded successfully and saved in the 'downloaded_xml_files' directory.\n"
        "XML is Valid\n"
        "[('a', 'a')]\n"
        "{\"answers\": [{\"paths\": {\"from\": \"a\", \"to\": \"e\", \"paths\": [[\"a\", \"e\"]]}}, {\"cheapest\": {\"from\": \"a\", \"to\": \"e\", \"path\": [\"a\", \"e\"]}}]}\n"
    )
    assert result.stdout == expected_output

def test_main_script_output_with_valid_samples():
    valid_samples = [
        'valid_sample_01.xml',
        'valid_sample_02.xml',
    ]

    for sample in valid_samples:
        clean_data()
        result = subprocess.run(['python3', 'main.py', f'sample_xml_files/{sample}'], stdout=subprocess.PIPE, text=True)
        expected_output = (
            "XML file downloaded successfully and saved in the 'downloaded_xml_files' directory.\n"
            "XML is Valid\n"
            "[]\n"
            "{\"answers\": [{\"paths\": {\"from\": \"a\", \"to\": \"e\", \"paths\": []}}, {\"cheapest\": {\"from\": \"a\", \"to\": \"e\", \"path\": false}}]}\n"
        )
        assert result.stdout == expected_output

def test_main_script_output_with_invalid_samples():
    invalid_samples = [
        ('invalid_sample_01.xml', "XML is Invalid 'Root element must be 'graph''"),
        ('invalid_sample_02.xml', "XML is Invalid 'Graph must have an id and a name'"),
        ('invalid_sample_03.xml', "XML is Invalid 'Graph must have an id and a name'"),
        ('invalid_sample_04.xml', "XML is Invalid '<nodes> groups must be present'"),
        ('invalid_sample_05.xml', "XML is Invalid 'There must be at least one <node> in the <nodes> group'"),
        ('invalid_sample_06.xml', "XML is Invalid 'All nodes must have <id> tags'"),
        ('invalid_sample_07.xml', "XML is Invalid ''NoneType' object has no attribute 'text''"),
        ('invalid_sample_08.xml', "XML is Invalid 'All nodes must have unique <id> tags, but 'e' is repeated'"),
        ('invalid_sample_09.xml', "XML is Invalid '<edges> groups must be present'"),
        ('invalid_sample_10.xml', "XML is Invalid 'Each <edge> must have a <id>, <from> and a <to> tag'"),
        ('invalid_sample_11.xml', "XML is Invalid 'Each <edge> must have a <id>, <from> and a <to> tag'"),
        ('invalid_sample_12.xml', "XML is Invalid 'Each <edge> must have a <id>, <from> and a <to> tag'"),
        ('invalid_sample_13.xml', "XML is Invalid 'Each <edge> must have a <id>, <from> and a <to> tag'"),
        ('invalid_sample_14.xml', "XML is Invalid ''NoneType' object has no attribute 'text''"),
    ]

    for sample, expected_error in invalid_samples:
        result = subprocess.run(['python3', 'main.py', f'sample_xml_files/{sample}'], stdout=subprocess.PIPE, text=True)
        expected_output = f"XML file downloaded successfully and saved in the 'downloaded_xml_files' directory.\n{expected_error}\n"
        assert result.stdout == expected_output

clean_data()
