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
    try:
        if verbose:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        else:
            print(f" - Calling function: {function_call_part.name}")
    except Exception as error:
        print(f"Error: {error} fail calling function")

    function_name = function_call_part.name

    args: dict = {}
    if function_call_part.args:
        args = function_call_part.args

    function_result = ""
    print("\n2")
    if function_name:
        print(f"CALLING: {function_dict[function_name]("calculator", **args)}")
    print("\n2")

    try:
        if function_name:
            function_result = function_dict[function_name]("calculator", **args)
    except Exception as error:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name= f"{function_name}",
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name= f"{function_name}",
                response={"result": function_result},
            )
        ],
    )
