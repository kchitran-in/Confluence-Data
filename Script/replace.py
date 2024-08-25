import os
import re
import argparse

def replace_spaces_in_files(directory):
    # Regular expression to match image paths starting with storage/ and ending with .png, .jpg, or .jpeg
    pattern = re.compile(r'storage/.*?\.(png|jpg|jpeg)')

    # Traverse through all files in the given directory
    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.md'):
                file_path = os.path.join(root, file_name)
                
                # Read the file content
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                except (UnicodeDecodeError, FileNotFoundError):
                    # Skip files that can't be read as text or are not found
                    continue

                # Replace spaces within the pattern with %20
                updated_content = pattern.sub(lambda m: m.group(0).replace(' ', '%20'), content)

                # Write the updated content back to the file
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(updated_content)

    print("Replacement completed.")

if __name__ == "__main__":
    # Parse the directory path from the command line
    parser = argparse.ArgumentParser(description='Replace spaces with %20 in image paths within .md files.')
    parser.add_argument('directory', type=str, help='Path to the directory')

    args = parser.parse_args()

    # Run the replacement function with the provided directory
    replace_spaces_in_files(args.directory)
