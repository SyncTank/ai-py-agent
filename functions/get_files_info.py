import platform
import os

def get_files_info(working_directory : str, directory="."):
    os_name = platform.system()
    match os_name:
        case "Linux":
            print(f"OS : {os_name}")
            print(f"{os.path.join(directory, working_directory)}")
        case "Window":
            print(f"OS : {os_name}")
            print(f"{os.path.join(working_directory, directory)}")
        case _:
            print(f"OS not implemented {os_name}")
            return
