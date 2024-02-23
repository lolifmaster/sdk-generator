import os
import shutil


def move_files(source_directory, target_directory):
    for root, dirs, files in os.walk(source_directory):
        for file in files:
            old_file_path = os.path.join(root, file)
            # Replace source_directory from the old file path and replace path separator with underscore
            new_file_name = old_file_path.replace(source_directory, '').replace(os.sep, '_')
            new_file_path = os.path.join(target_directory, new_file_name)
            shutil.move(str(old_file_path), str(new_file_path))


source = '../data/openapi-directory-main/APIs'
target = '../data/downloaded_openapi_specifications'

# Ensure the target directory exists
os.makedirs(target, exist_ok=True)

move_files(source, target)
