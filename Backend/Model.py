import cohere
from rich import print
from dotenv import dotenv_values

# Load environment variables from the .env file.
env_vars = dotenv_values(".env")

# Retrieve API key.
CohereAPIKey = env_vars.get("CohereAPIKey")

# Create a Cohere client using the provided API key.
co = cohere.Client(api_key=CohereAPIKey)

# Define a list of recognized function keywords for task categorization.
funcs = [
    "exit", "general", "realtime", "open", "close", "play",
    "generate image", "system", "content", "google search",
    "youtube search", "reminder"
]

# Initialize an empty list to store user messages.
messages = []

preamble = """
You are a very accurate Decision-Making Model, which decides what kind of a query is given to you.
You will decide whether a query is a 'general' query, a 'realtime' query, or is asking to perform any task or automation like 'open facebook'.

*** Do not answer any query, just decide what kind of query is given to you. ***

-> Respond with 'general ( query )' if a query can be answered by a llm model (conversational ai chatbot) and doesn't require any up to date information.
-> Respond with 'realtime ( query )' if a query can not be answered by a llm model (because they don't have realtime data) and requires up to date information.
-> Respond with 'open (application name or website name)' if a query is asking to open any application like 'open facebook', 'open telegram', etc.
-> Respond with 'close (application name)' if a query is asking to close any application like 'close notepad', 'close facebook', etc.
-> Respond with 'play (song name)' if a query is asking to play any song like 'play afsana by ys', 'play let her go', etc.
-> Respond with 'generate image (image prompt)' if a query is requesting to generate an image with given prompt like 'generate image of a lion'.
-> Respond with 'reminder (datetime with message)' if a query is requesting to set a reminder like 'set a reminder at 9:00pm on 25th june'.
-> Respond with 'system (task name)' if a query is asking to mute, unmute, volume up, volume down, etc.
-> Respond with 'content (topic)' if a query is asking to write any type of content like application, codes, emails or anything else.
-> Respond with 'google search (topic)' if a query is asking to search a specific topic on google.
-> Respond with 'youtube search (topic)' if a query is asking to search a specific topic on youtube.

*** If the query is asking to perform multiple tasks like 'open facebook, telegram and close whatsapp' respond with:
'open facebook, open telegram, close whatsapp'

*** If the user is saying goodbye or wants to end the conversation like 'bye jarvis.' respond with 'exit'.

*** Respond with 'general (query)' if you can't decide the kind of query or if a query is asking to perform a task which is not mentioned above.
"""

ChatHistory = [
    {"role": "User", "message": "how are you?"},
    {"role": "Chatbot", "message": "general how are you?"},
    {"role": "User", "message": "do you like pizza?"},
    {"role": "Chatbot", "message": "general do you like pizza?"},
    {"role": "User", "message": "open chrome and tell me about mahatma gandhi."},
    {"role": "Chatbot", "message": "open chrome, general tell me about mahatma gandhi."},
    {"role": "User", "message": "open chrome and firefox"},
    {"role": "Chatbot", "message": "open chrome, open firefox"},
    {"role": "User", "message": "what is today's date and by the way remind me that i have a dancing performance on 5th aug at 11pm"},
    {"role": "Chatbot", "message": "general what is today's date, reminder 11:00pm 5th aug dancing performance"},
    {"role": "User", "message": "chat with me."},
    {"role": "Chatbot", "message": "general chat with me."}
]


# Define the main function for decision-making on queries.
def FirstLayerDMM(prompt: str = "test"):
    
    # Add the user's query to the messages list.
    messages.append({"role": "user", "content": f"{prompt}"})

    # Create a streaming chat session with the Cohere model.
    stream = co.chat_stream(
        model="command-a-03-2025",
        message=prompt,
       temperature=0.7,
       chat_history=ChatHistory,
       prompt_truncation='OFF',
       connectors=[],
       preamble=preamble
)
    response = ""

    # Iterate over events in the stream and capture text generation events.
    for event in stream:
        if event.event_type == "text-generation":
            response += event.text

    # Remove newline characters and split responses into individual tasks.
    response = response.replace("\n", "")
    response = response.split(",")

    # Strip leading and trailing whitespaces from each task.
    response = [i.strip() for i in response]

    # Initialize an empty list to filter valid tasks.
    temp = []

    for task in response:
        for func in funcs:
            if task.startswith(func):
                temp.append(task)

    response = temp

    # If model confused → retry once
    if "(query)" in str(response):
        return FirstLayerDMM(prompt=prompt)
    else:
        return response
    
if __name__ == "__main__":
       while True:
        user = input(">>> ")
        print(FirstLayerDMM(user))