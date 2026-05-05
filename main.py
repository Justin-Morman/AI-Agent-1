import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt



parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
user_prompt = args.user_prompt
verbose = args.verbose

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]



load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not set")
client = genai.Client(api_key=api_key)
response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.0,
        )
    )
if verbose is True:
    if response.usage_metadata is not None:
        print(f"User prompt: {args.user_prompt}")
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
    else:
        raise RuntimeError("No usage metadata found")

print(response.text)

def main():
    pass
    

if __name__ == "__main__":
    main()
