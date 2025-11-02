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
from globals import TIME_OUT 

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)
system_prompt = globals.SYS_PROMPT
configs = types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt
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

    messages = [
    types.Content(role="user", parts=[types.Part(text=strprompt.strip())]),
    ]

    prompt_token: int = 0
    candidates_token: int = 0

    for _ in range(0, TIME_OUT-1, 1):
        #print("\n CALLING EXTRACT \n")
        response = geneai(client, messages)

        if response and response.usage_metadata:
            prompt_token += response.usage_metadata.prompt_token_count or 0
            candidates_token += response.usage_metadata.candidates_token_count or 0

        #print(f"\n-> RESPONSE : \n{response}\n\n")

        #print(f"\n-> MESSAGES: \n{messages}\n\n")
        if not response or response.candidates == None:
            if messages[-1].parts:
                print(f"\n{messages[-1].parts[0].text}")
            break

        #print(f"\n-> ADDING CANDIDATES: \n{response.candidates}\n")
        messages = add_canditates(messages, response.candidates)

        try:
            #print(f"\n FUNCTION EXTRACT \n")
            # the end_result is optional as its appended to the messages list
            end_result = function_response_extract(response, messages, verbose_flags)
            if end_result :
                print(f"-> FAILURE : \n{end_result}")

            #print(f"\n-> MESSAGES: \n{messages}\n\n")
        except Exception as error:
            print(f"Error: {error} Check the API")
 
    if verbose_flags == True:
        print("")
        print(f"User prompt: {strprompt}")
        print(f"Prompt tokens: {prompt_token}")
        print(f"Response tokens: {candidates_token}")

def function_response_extract(response,messages, verbose_flags):
    if response and response.candidates:
        for can in response.candidates:
            if can.content.parts:
                parts = can.content.parts
            else:
                return f"Candidates is empty"

            for item in parts:
                if hasattr(item, "function_call"):
                    call = getattr(item, "function_call")
                    if call:
                        call_response : types.Content = call_function(call, verbose_flags)
                        #print(f"-> CALL RESULT: \n {call_response}\n\n")
                        if call_response and call_response.parts:
                            messages.append(types.Content(role="user", parts=call_response.parts))
                else:
                    return f"NO FUNCTION CALL {item}"

def geneai(client, messages):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages,
        config=configs
    )
    return response

def add_canditates(messages, response):
    results: list = messages.copy()
    iterable = list(response)
    for item in iterable:
        results.append(item.content)
    return results

if __name__ == "__main__":
    main()
