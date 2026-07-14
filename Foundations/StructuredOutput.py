from dotenv import load_dotenv
load_dotenv()

import json
from anthropic import Anthropic
client = Anthropic()

model = "claude-sonnet-5"

system_prompt = """Extract the details into JSON with keys:
{"name": string, "role": string, "years_experience": number}"""

def extract(text):
    message = client.messages.create(
        model=model,
        max_tokens=500,
        system=system_prompt,
        messages=[
            {"role": "user", "content": text},
            {"role": "assistant", "content": "```json"},   # prefill: forces format
        ],
        stop_sequences=["```"],   # stops right when the closing fence would start
    )
    raw = message.content[0].text   # already clean JSON  no fences
    return json.loads(raw)

data = extract("Ghufran is a software engineer with about 2 years of experience.")
print(data)
print(data["role"])