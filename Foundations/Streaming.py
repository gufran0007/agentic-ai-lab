from dotenv import load_dotenv
load_dotenv()

from anthropic import Anthropic
client = Anthropic()

model = "claude-sonnet-5"

def stream_chat(prompt):
    # stream() opens a live connection instead of waiting for the full reply
    with client.messages.stream(
        model=model,
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        # text_stream yields each chunk as it's generated
        for chunk in stream.text_stream:
            print(chunk, end="", flush=True)  # flush=True makes it appear live
    print()

stream_chat("What is Earth?")