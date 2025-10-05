import os
import subprocess
import globals

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

    result = ""
    try:
        process = subprocess.run(args, cwd=filePath, stderr=subprocess.PIPE, stdout=subprocess.PIPE , timeout=globals.TIME_LIMIT, text=True )
        #results = f'STDOUT: {subprocess.CompletedProcess.stdout}\nSTDERR: {subprocess.CompletedProcess.stderr}'

    except Exception as error:
        return f'Error: executing python file {error}'

    if len(result) < 1:
        return f'No output produced'

    return result
