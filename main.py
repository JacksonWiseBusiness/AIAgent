import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse

def main() -> None:

    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="User prompt to send to the LLM")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY environment variable not set")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    messages = [
        {"role": "user", "content": args.user_prompt},
    ]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    generate_content(client, messages, args.verbose)


def generate_content(client: OpenAI, messages: list, verbose: bool) -> None:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )
    if response.usage is None:
        raise RuntimeError("Failed API request")
    if verbose:
        print("Prompt tokens:", response.usage.prompt_tokens)
        print("Response tokens:", response.usage.completion_tokens)
    print("Response:")
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
