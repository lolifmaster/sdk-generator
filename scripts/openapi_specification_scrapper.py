import requests
import os
import shutil
from concurrent.futures import ThreadPoolExecutor


def download_file(file_url, file_name):
    # Make a request to download the file
    file_response = requests.get(file_url)
    file_response = requests.get(file_response.json()['payload']["blob"]['displayUrl'])
    # Check if the download request was successful (status code 200)
    if file_response.status_code == 200:
        # Save the file to the target directory
        with open(file_name, 'wb') as file:
            file.write(file_response.content)
        print(f"Downloaded: {file_name}")
    else:
        print(f"Failed to download {file_name}. Status code: {file_response.status_code}")


def download_github_folder(current_api_url, current_target_directory):
    # Make a request to the GitHub API
    response = requests.get(current_api_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        contents = response.json()["payload"]['tree']["items"]

        # Create a ThreadPoolExecutor
        with ThreadPoolExecutor() as executor:
            # Loop through each file/folder in the directory
            for item in contents:
                if item['contentType'] == 'file':
                    # If it's a file, download it
                    file_url = f"{current_api_url}/{item['name']}"
                    file_name = os.path.join(current_target_directory, item['path'].replace("/", "_"))
                    # Submit the download task to the executor
                    executor.submit(download_file, file_url, file_name)
                elif item['contentType'] == 'directory':
                    # If it's a directory, call the function recursively
                    download_github_folder(f"{current_api_url}/{item['name']}", current_target_directory)
    else:
        print(f"Failed to fetch contents. Status code: {response.status_code}")


# Example usage:
api_url = f"https://github.com/APIs-guru/openapi-directory/tree/main/APIs"
target_directory = "../data/openapi_specifications"

# Recreate the target_directory on each script run
shutil.rmtree(target_directory, ignore_errors=True)
os.makedirs(target_directory, exist_ok=True)

download_github_folder(api_url, target_directory)
