import requests
import os
import sys

DOWNLOAD_DIR = "downloaded_xml_files"
BASE_URL = "https://raw.githubusercontent.com/uznadeem/xml_graph_validator/main/"
DEFAULT_XML = "sample.xml"

def validate_filename(filename):
    if not filename.endswith(".xml"):
        raise ValueError("Filename must have a valid extension (.xml).")

def download_xml_file(filename=DEFAULT_XML):
    try:
        validate_filename(filename)

        url = BASE_URL + filename
        response = requests.get(url)
        response.raise_for_status()

        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        with open(os.path.join(DOWNLOAD_DIR, filename), "w") as file:
            file.write(response.text)

        print(f"XML file downloaded successfully and saved as {filename} in the '{DOWNLOAD_DIR}' directory.")

    except requests.exceptions.HTTPError as e:
        print(f"Download error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
    except ValueError as e:
        print(f"Invalid filename: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    filename = DEFAULT_XML
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    download_xml_file(filename)
