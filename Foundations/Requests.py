# Load the API key from a .env file into the environment.
from dotenv import load_dotenv
load_dotenv()

# Create the client
from anthropic import Anthropic
client = Anthropic()

model = "claude-sonnet-5"

# The system prompt sets Claude's role for the whole conversation.
system_prompt = """You are a tutor. Do not give the full solution directly.
Instead, give hints and guiding questions that help the student solve it themselves."""

# The API has no memory, so we keep every turn in a list and resend it each call.
def user_message(messages, text):
    messages.append({"role": "user", "content": text})

def assistant_message(messages, text):
    messages.append({"role": "assistant", "content": text})

# Send the full conversation so far and return Claude's text reply.
def chat(messages):
    message = client.messages.create(
        model=model,
        max_tokens=1000,       #max length
        messages=messages,     # list that get send back with every request
        system=system_prompt,  #applying system prompt (tutor described above)
    )
    #content print text only
    return message.content[0].text

messages = []  # conversation starts empty

while True:
    user_input = input("You: ")

    if user_input.lower() in ["stop", "exit", "quit"]:
        print("Session ended.")
        break

    user_message(messages, user_input)    # add what the user said
    answer = chat(messages)               # send history, get reply
    assistant_message(messages, answer)   # save reply so Claude "remembers" it
    print("Claude:", answer)