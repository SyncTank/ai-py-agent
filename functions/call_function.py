from google.genai import types

# arg1 name and .args properties, verbose prints them
def call_function(function_call_part: types.FunctionCall, verbose=False):
    try:
        if verbose:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        else:
            print(f" - Calling function: {function_call_part.name}")
    except Exception as error:
        print(f"Error: {error} fail calling function")

    return ""
