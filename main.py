import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import * 
from functions.get_file_content import * 
from functions.write_file import * 
from functions.run_python_file import * 
from functions.call_function import * 

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    if len(sys.argv) <= 1:
        sys.exit(1)

    strprompt = ""
    verbose_flags: bool = False
    for prompt in sys.argv[1::]:
        if "--verbose" in prompt:
            verbose_flags = True
        else:
            strprompt += (prompt + " ")

    response = geneai(strprompt.strip(), client)

    try:
        result = function_response_extract(response, verbose_flags)
        if result :
            print(result)
    except Exception as error:
        print(f"Error: {error} Check the API")
 
    if response.usage_metadata is not None and verbose_flags == True:
        print(f"User prompt: {strprompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


def function_response_extract(response, verbose_flags):
    #print(f"TEST \n {response} \n\n")
    try:
        if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
            result_part = response.candidates and response.candidates[0].content and response.candidates[0].content.parts
        else :
            return "API no response"
    except Exception as error:
        return f"Error: {error} failed parts"

    for item in result_part:
        result_item = dict(item)
        call = result_item["function_call"]
        if call :
            call_result = call_function(call, verbose_flags)
        elif item.text:
            return f"{item.text}"
        else:
            return f"AI did not call any function see response {result_item}"

        #print(f"CALL RESULT: \n {call_result}\n\n")

        try:
            if call_result and call_result.parts:
                function_results = call_result.parts
            else:
                return f"Nothing was return from the call"
        except Exception as error:
            return f"Error: {error} failed to see call_results"
 
        try:
            for function_call in function_results:
                response_call = dict(function_call)
                #print(f"response call {response_call}\n\n")
                if response_call["function_response"]:
                    response = response_call["function_response"]
                    print(f"-> {response.response["result"]}")
                else:
                    return f"{response_call["text"]}"
        except Exception as error:
            print(f"Error: {error} failed at call_parts_result")

def geneai(content : str, client):
    system_prompt = globals.SYS_PROMPT
    messages = [
    types.Content(role="user", parts=[types.Part(text=content)]),
    ]
    configs = types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages,
        config=configs
    )
    return response

if __name__ == "__main__":
    main()
