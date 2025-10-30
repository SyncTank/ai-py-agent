from google.genai import types
from functions.get_files_info import * 
from functions.get_file_content import * 
from functions.write_file import * 
from functions.run_python_file import * 

function_dict = {
    "get_files_info" : get_files_info,
    "get_file_content" : get_file_content,
    "write_file" : write_file,
    "run_python_file" : run_python_file,
}

# arg1 name and .args properties, verbose prints them
def call_function(function_call_part: types.FunctionCall, verbose=False):
    args: dict = {"working_directory" : "calculator"}

    function_name = getattr(function_call_part, "name")
    function_args = getattr(function_call_part, "args", None)

    if function_args:
        args.update(function_args) 

    try:
        if verbose:
            print(f"Calling function: {function_name}({args})")
        else:
            print(f" - Calling function: {function_name}")
    except Exception as error:
        print(f"Error: {error} fail calling function")

    try:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name= f"{function_name}",
                    response={"result": function_dict[function_name](**args)},
                )
            ],
        )
    except Exception as error:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name or "Unknown",
                    response={"error": f"Unknown function: {error}"},
                )
            ],
        )

