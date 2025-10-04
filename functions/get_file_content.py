import os
import globals

def get_file_content(working_directory: str, file_path: str)-> str:
    try :
        workPath = os.path.abspath(working_directory)
    except Exception as error:
        return f"{error} the file does not exist"

    try :
        filePath = os.path.abspath(working_directory + "/" + file_path)
    except Exception as error:
        return f"{error} the file does not exist"

    if not filePath.startswith(workPath):
        return f"Error: Cannot read {file_path} as it is outside the permitted working directory\n"

    if not os.path.isfile(filePath):
        return f"Error: file not found or is not a regular file: {filePath}"

    results = ""
    with open(filePath, "r") as f:
        results += f.read(globals.READ_LIMIT)

    if os.path.getsize(filePath) > globals.READ_LIMIT:
        results += "[...File " + file_path + " truncated at 10000 characters]"

    return results
