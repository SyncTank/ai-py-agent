import os
import subprocess
import globals
import sys
from google.genai import types

def run_python_file(working_directory : str, file_path : str, args=[]) -> str:
    try :
        workPath = os.path.abspath(working_directory)
    except Exception as error:
        return f"Error: {error} the file does not exist"

    filePath = os.path.abspath(working_directory + "/" + file_path)

    if not filePath.startswith(workPath):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(filePath):
        return f'Error: File "{file_path}" not found'

    if not filePath.endswith(".py"):
        return f'Error: "{file_path}" is not a python file.'

    if len(args) == 0:
        args.append(" ")

    totalArgs = [f"{sys.executable}", f"{filePath}"]
    for i in args:
        totalArgs.append(i)

    try: # args needs to be python main.py args
        process = subprocess.run(totalArgs, cwd=workPath, capture_output=True , timeout=globals.TIME_LIMIT, text=True, check=True )
        results = f'STDOUT: {process.stdout}\nSTDERR: {process.stderr}'
        if process.returncode != 0:
            results += f'\nProcess exited with {process.returncode}'
        if len(process.stdout) < 2:
            return f'No output produced'

    except Exception as error:
        return f'Error: executing python file {error}'

    if len(results) < 1:
        return f'No output produced'

    return results

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a .py/python file specified by a path relative to the working directory, along with optional arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The root working directory of the program/project.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the Python file (e.g., 'script.py') to be executed, relative to the 'working_directory'.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="A list/array of string optional flag arguments (e.g., ['--debug', '1']) to pass to the python file.",
                items=types.Schema(
                    type=types.Type.STRING
                )
            ),
        },
        required=["working_directory", "file_path"] # Added 'required' fields
    ),
)
