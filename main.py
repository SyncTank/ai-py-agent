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

    try: # nested check cause python
        if response.candidates:
            print("\n1")
            print(f"{response.candidates[0]}")
            if response.candidates[0].content:
                print("\n1")
                print(f"{response.candidates[0].content}")
                if response.candidates[0].content.parts:
                    for item in response.candidates[0].content.parts:
                        print("\n1")
                        print(f"{response.candidates[0].content.parts}")
                        print("\n1")
                        print(f"{item}")
                        if item.function_call:
                            function_call_result = call_function(item.function_call, verbose_flags)
                            print(f"-> {function_call_result.parts}")
                            #print(f"-> {function_call_result.parts[0].from_function_response().function_response.response}")
                            #print(f"Calling function: {item.function_call.name}({item.function_call.args})")
                        elif item.text:
                            print(f"{item.text}")

        if response.usage_metadata is not None and verbose_flags == True:
            print(f"User prompt: {strprompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    except AttributeError as error:
        print(f"Error: {error} Check the API")

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
