import os
import sys
import json
import globals
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import * 
from functions.get_file_content import * 

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    if len(sys.argv) <= 1:
        sys.exit(1)

    print(get_file_content("calculator","lorem.txt"))

    return

    strprompt = ""
    verbose_flags = 0 
    for prompt in sys.argv[1::]:
        if "--verbose" in prompt:
            verbose_flags = 1
        else:
            strprompt += (prompt + " ")

    response = geneai(strprompt, client)
    print(f"{response.text}")

    if response.usage_metadata is not None and verbose_flags == 1:
        print(f"User prompt: {strprompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")



def geneai(content : str, client):
    messages = [
    types.Content(role="user", parts=[types.Part(text=content)]),
    ]
    response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=messages)
    return response

if __name__ == "__main__":
    main()
