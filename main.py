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

    for _ in range(0, 19, 1):

        response = geneai(client, messages)

        if response and response.usage_metadata:
            prompt_token += response.usage_metadata.prompt_token_count or 0
            candidates_token += response.usage_metadata.candidates_token_count or 0

        print(f"RESPONSE : {response}\n\n")

        if not hasattr(response, 'text'):
            if messages and hasattr(messages[-1], 'parts') and messages[-1].parts:
                final_part = messages[-1].parts[0]
                if hasattr(final_part, 'text'):
                    print(getattr(final_part, 'text'))
            break

        messages = add_canditates(messages, response.candidates)

        try:
            function_response_extract(response, messages, verbose_flags)
            print(f"MESSAGES: {messages}\n\n")
        except Exception as error:
            print(f"Error: {error} Check the API")
 
    if verbose_flags == True:
        print("")
        print(f"User prompt: {strprompt}")
        print(f"Prompt tokens: {prompt_token}")
        print(f"Response tokens: {candidates_token}")

def function_response_extract(response,messages, verbose_flags):
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
                messages.append(types.Content(role="user", parts=call_result.parts ))
            else:
                return f"Nothing was return from the call"
        except Exception as error:
            return f"Error: {error} failed to see call_results"
 
        results_responses: list[str] = [] 
        try:
            for function_call in function_results:
                response_call = dict(function_call)
                #print(f"response call {response_call}\n\n")
                if response_call["function_response"]:
                    response = response_call["function_response"]
                    results_responses.append(f"-> {response.response["result"]}")
                    print(f"-> {response.response["result"]}")
                else:
                    results_responses.append(f"-> {response.response["result"]}")
                    return f"{response_call["text"]}"
        except Exception as error:
            print(f"Error: {error} failed at call_parts_result")

        return "\n".join(results_responses)

def geneai(client, messages):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages,
        config=configs
    )
    return response

def add_canditates(messages, response):
    results: list = messages.copy()
    for item in response:
        results.append(item.content)
    return results


if __name__ == "__main__":
    main()
