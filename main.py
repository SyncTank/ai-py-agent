import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    if len(sys.argv) <= 1:
        sys.exit(1)

    strprompt = ""
    for prompt in sys.argv[1::]:
        strprompt += (prompt + " ")

    response = geneai(strprompt, client)
    print(strprompt)
    print(response.text)

    if response.usage_metadata is not None :
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
