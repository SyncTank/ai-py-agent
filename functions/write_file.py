import os
from google.genai import types

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try :
        workPath = os.path.abspath(working_directory)
    except Exception as error:
        return f"Error: {error} the file does not exist"

    filePath = os.path.abspath(working_directory + "/" + file_path)

    if not filePath.startswith(workPath):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(filePath):
        try :
            os.makedirs(os.path.dirname(filePath), exist_ok=True)
        except Exception as error:
            return f'Error: {error} creating directory'

        if not os.path.isdir(filePath):
            return f'Error: {filePath} is a directory, and not a file'

    try :
        with open(filePath, "+w") as file:
            file.write(content)
    except Exception as error:
        return f"Error: {error} could not write to file"

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite a file in a specified directory given context, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="Working directory (root) of the program",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="A path to a file to perform a operation on",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="data that will be copied over or pasted into a new or existing file",
            ),
        },
    ),
)

