import os

def list_files(directory):
    try:
        files = os.listdir(directory)  # Get all files and directories
        for file in files:
            print(file)
    except FileNotFoundError:
        print(f"Error: The directory '{directory}' was not found.")
    except PermissionError:
        print(f"Error: Permission denied for accessing '{directory}'.")

# Example usage
directory_path = "./"  # Change this to the desired directory
list_files(directory_path)