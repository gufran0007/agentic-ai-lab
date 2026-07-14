from dotenv import load_dotenv
load_dotenv()

import json
from anthropic import Anthropic
client = Anthropic()

model = "claude-haiku-4-5-20251001"   # small, fast, cheap — right tool for this job

def add_user_message(messages, text):
    messages.append({"role": "user", "content": text})

def add_assistant_message(messages, text):
    messages.append({"role": "assistant", "content": text})

def chat(messages, system=None, temperature=1.0, stop_sequences=[]):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature,
    }
    # only add the optional bits if they were actually passed in
    if system:
        params["system"] = system
    if stop_sequences:
        params["stop_sequences"] = stop_sequences

    response = client.messages.create(**params)   # unpack dict into arguments
    return response.content[0].text

def generate_dataset():
    prompt = """
Generate an evaluation dataset for a prompt evaluation. The dataset will be used to
evaluate prompts that generate Python, JSON, or Regex specifically for AWS-related tasks.
Generate an array of JSON objects, each representing a task that requires Python, JSON,
or a Regex to complete.

Example output:
[
  {"task": "Description of task"}
]

* Focus on tasks solvable by a single Python function, a single JSON object, or one regex
* Focus on tasks that do not require writing much code

Please generate 3 objects.
"""
    messages = []
    add_user_message(messages, prompt)
    add_assistant_message(messages, "```json")      # prefill: forces straight into JSON
    text = chat(messages, stop_sequences=["```"])   # stop: cuts off at the closing fence
    return json.loads(text)

dataset = generate_dataset()

with open("dataset.json", "w") as f:
    json.dump(dataset, f, indent=2)   # indent=2 makes the file human-readable

print(json.dumps(dataset, indent=2))