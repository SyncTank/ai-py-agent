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

    totalArgs = [sys.executable, filePath]
    if args:
        totalArgs += args

    results: str = ""
    try: # args needs to be python main.py args
        process = subprocess.run(totalArgs, cwd=workPath, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=globals.TIME_LIMIT, text=True, check=True )

        if process.stdout:
            results += f'STDOUT: {process.stdout.strip()}'

        if process.stderr:
            results += f'\nSTDERR: {process.stderr.strip()}' 

        if process.returncode != 0:
            results += f'\nProcess exited with {process.returncode}'

        if len(results) < 2:
            return f'No output produced'

    except Exception as error:
        return f'Error: executing python file {error}'

    if len(results) < 2:
        return f'No output produced'

    return results

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a .py/python file specified by a path relative to the working directory, along with a optional args list. args defaults to a empty list [], so run unless specified",
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
                description="A optional list/array of string flags used to execute special arguments on call (e.g., ['--debug', '1']), defaults to empty list [].",
                items=types.Schema(
                    type=types.Type.STRING
                ),
                default=[]
            ),
        },
        required=["file_path"] # Added 'required' fields
    ),
)
