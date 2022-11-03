import requests
from shipyard_utils import files as shipyard
import argparse
import sys
import os
try:
    import exit_codes as ec 
except BaseException:
    from . import exit_codes as ec


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--organization-id', dest = 'org_id', required = True)
    parser.add_argument("--api-key", dest = 'api_key', required = True)
    parser.add_argument("--file-name", dest = "file_name", required = True)
    parser.add_argument('--folder-name', dest = 'folder_name', required = False)
    return parser.parse_args()
 

def form_url(organization_id):
    """
    Returns the url that will be used to form the request
    """
    return f"https://api.app.shipyardapp.com/orgs/{organization_id}/voyages"


def form_request(url,api_key):
    """
    Forms the GET request to the shipyard API and returns the response in CSV format
    """
    headers = {"X-Shipyard-API-Key":api_key}
    try:
        results = requests.get(url, headers = headers)
        return results

    except Exception as e:
        print(f"Error in making the request, ensure that your API key and organzation ID are correct")
        print(e)
        sys.exit(ec.EXIT_CODE_INVALID_CREDENTIALS)


def write_file(response_txt, file, folder_name = None):
    """
    Writes the csv response from the api to a file. If the folder name is not provided, then it will be 
    written in the current working directory
    """
    ## ensure that the file type is a csv
    if str(file).find('.csv') == -1:
        print("Error: The file name must be a csv. Please add the .csv suffix to the file")
        sys.exit(ec.EXIT_CODE_INVALID_FILE_TYPE)
    if folder_name is not None:
        ## create the directory if it does not exist
        shipyard.create_folder_if_dne(folder_name)
        dest_path = shipyard.combine_folder_and_file_name(folder_name,file)
        message_path = os.path.join(os.getcwd(), folder_name, file)
        message = f"Saved {file} in {os.path.normpath(message_path)}"
    else:
        dest_path = file
        message_path = os.path.join(os.getcwd(),file)
        message = f"Saved {file} in {os.path.normpath(message_path)}"
    with open(dest_path,'w') as csv_file:
        csv_file.write(response_txt)
    print(f"Saved {file} to {message}")


def main():
    args = get_args()
    org_id = args.org_id
    api_key = args.api_key
    file_name = args.file_name
    folder_name = args.folder_name
    url = form_url(org_id)
    response = form_request(url,api_key)
    write_file(response.text, file_name, folder_name)


if __name__ == '__main__':
    main()


