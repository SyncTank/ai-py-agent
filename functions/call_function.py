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

    # attempt to run function pass the result down
    try:
        # map function from name
        function_name = function_call_part.name
        function_result = ""
    except Exception as error:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
