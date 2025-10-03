import os
import globals

def get_file_content(working_directory: str, file_path: str)-> str:
    try :
        filePath = os.path.abspath(file_path)
    except Exception as error:
        return f"{error} the file does not exist"

    try :
        workPath = os.path.abspath(working_directory)
    except Exception as error:
        return f"{error} the file does not exist"

    if not (filePath in workPath):
        return f"Error: Cannot read {file_path} as it is outside the permitted working directory\n"

    if not os.path.isfile(workPath):
        return f"Error: file not found or is not a regular file: {filePath}"

    if os.path.getsize(workPath) > globals.LIMIT:
        pass
    else:
        pass

    return "work"
