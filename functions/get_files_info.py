import os
from google.genai import types 

def get_files_info(working_directory : str, directory: str =".")-> str:
    try :
        workDirectory : str = os.path.abspath(working_directory) # parent path where work is done
    except Exception as error:
        return f"   Error: {error} {working_directory} could not be found check if directory exists\n"

    try :
        currentDirectory: str = os.path.join(workDirectory, directory) # full path
    except Exception as error:
        return f"   Error: {directory} is not a directory"

    if not (workDirectory in os.path.abspath(currentDirectory)) :
        return f"   Error: Cannot list {directory} as it is outside the permitted working directory\n"

    list_Files: list = os.listdir(currentDirectory)
    results = f"Results for {currentDirectory} directory:\n"
    try :
        for i in list_Files:
            sizeInfo = os.path.getsize(currentDirectory+"/"+i)
            isFile = os.path.isfile(i)
            results += f"   - {i}: file_size={sizeInfo} bytes, is_dir={isFile}\n"
    except Exception as error:
        return f"   Error: {error} \nissue with file check access or make sure it exists\n"

    return results

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
