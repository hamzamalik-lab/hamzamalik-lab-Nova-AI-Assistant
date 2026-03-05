# Import required libraries
from AppOpener import close, open as appopen   # Import functions to open and close apps.      # Import web browser functionality.
from pywhatkit import search, playonyt         # Import functions for Google search and YouTube playback.
from dotenv import dotenv_values               # Import dotenv to manage environment variables.
from bs4 import BeautifulSoup                  # Import BeautifulSoup for parsing HTML content.
from rich import print                         # Import rich for styled console output.
from groq import Groq                          # Import Groq for AI chat functionalities.
import webbrowser                              # Import webbrowser for opening URLs.
import subprocess                              # Import subprocess for interacting with the system.                             # Import requests for making HTTP requests.
import keyboard                                # Import keyboard for keyboard-related actions.
import asyncio                                 # Import asyncio for asynchronous programming.
import os                                      # Import os for operating system functionalities.
import webbrowser
import requests

sess = requests.Session()

from AppOpener import open as appopen
# Load environment variables from the .env file.
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")   # Retrieve the Groq API key.

# Define CSS classes for parsing specific elements in HTML content
classes = [
    "zCubwf", "hgKElc", "LTKOO sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee",
    "tw-data-text tw-text-small tw-ta",
    "IZ6rdc", "05uR6d LTKOO lxsY6d", "webanswers-webanswers_table__webanswers-table",
    "dDoNo ikb4Bb gsrt", "sXLa0e",
    "LwKfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"
]

# Define a user-agent for making web requests
useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"

# Initialize the Groq client with the API key.
client = Groq(api_key=GroqAPIKey)

# Predefined professional responses for user interactions.
professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need—don't hesitate to ask.",
]

# List to store chatbot messages.
messages = []

# System message to provide context to the chatbot.
SystemChatBot = [{
    "role": "system",
    "content": f"Hello, I am {os.environ['Username']}, You're a friendly content writer. You have to write content professionally."
}]

# Function to perform a Google search.
def extract_links(html):
    soup = BeautifulSoup(html, "html.parser")
    links = []

    for a in soup.find_all("a", href=True):
        href = a["href"]

        if "/url?q=" in href:
            link = href.split("/url?q=")[1].split("&")[0]
            links.append(link)

    return links

def GoogleSearch(Topic):
    search(Topic)   # Use pywhatkit's search function to perform a Google search.
    return True     # Indicate success.

# Function to generate content using AI and save it to a file.
# Function to generate content using AI and save it to a file.
def Content(Topic):
    # Nested function to open a file in Notepad.
    def OpenNotepad(File):
        default_text_editor = "notepad.exe"   # Default text editor.
        subprocess.Popen([default_text_editor, File])   # Open the file in Notepad.
    # Nested function to generate content using the AI chatbot.
    def ContentWriterAI(prompt):

        messages.append({"role": "user", "content": f"{prompt}"})  # Add the user's prompt to messages.

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",   # Specify the AI model.
            messages=SystemChatBot + messages,   # Include system instructions and chat history.
            max_tokens=2048,   # Allow up to maximum tokens in the response.
            temperature=0.7,   # Adjust response randomness.
            top_p=1,   # Use nucleus sampling for response diversity.
            stream=True,   # Enable streaming response.
            stop=None   # Allow the model to determine stopping conditions.
        )

        Answer = ""   # Initialize an empty string for the response.

        # Process streamed response chunks.
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "")   # Remove unwanted tokens from the response.
        messages.append({"role": "assistant", "content": Answer})   # Add the AI's response to messages.
        return Answer

    Topic = str(Topic).replace("Content", "")   # Remove 'Content' from the topic.
    ContentByAI = ContentWriterAI(Topic)   # Generate content using AI.

    # Save the generated content to a text file.
    with open(f"Data\\{Topic.lower().replace(' ', '')}.txt", "w", encoding="utf-8") as file:
        file.write(ContentByAI)   # Write the content to the file.
        file.close()

    OpenNotepad(f"Data\\{Topic.lower().replace(' ', '')}.txt")   # Open the file in Notepad.
    return True

def YouTubeSearch(Topic):
    UrlSearch = f"https://www.youtube.com/results?search_query={Topic}"   # Construct the YouTube search URL.
    webbrowser.open(UrlSearch)   # Open the search URL in a web browser.
    return True   # Indicate success.

def PlayYouTube(query):
    playonyt(query)   # Use pywhatkit's playonyt function to play the video.
    return True   # Indicate success.
def OpenApp(app):

    app = app.lower()

    # 🌐 Websites mapping
    websites = {
        "facebook": "https://www.facebook.com",
        "instagram": "https://www.instagram.com",
        "youtube": "https://www.youtube.com",
        "whatsapp": "https://web.whatsapp.com",
        "twitter": "https://twitter.com",
        "gmail": "https://mail.google.com"
    }

    try:
        # try opening installed app
        appopen(app, match_closest=True)

    except:

        # open website instead
        if app in websites:
            webbrowser.open(websites[app])
        else:
            webbrowser.open(
                f"https://www.google.com/search?q={app}"
            )

    print("No link found")
    return False

        # Nested function to perform a Google search and retrieve HTML.
def search_google(query):

    url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": useragent}

    response = sess.get(url, headers=headers)

    if response.status_code == 200:
        return response.text

    print("Failed to retrieve search results.")
    return None
    
    html = search_google(app)

    if html:
           links = extract_links(html)

    if links:
        link = links[0]
        webbrowser.open(link)
        return True

    print("No link found")
    return False

def CloseApp(app):

    if "chrome" in app:
        pass   # Skip if the app is Chrome.

    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)   # Attempt to close the app.
            return True   # Indicate success.
        except:
            return False

def System(command):

    # Nested function to mute the system volume.
    def mute():
        keyboard.press_and_release("volume mute")   # Simulate the mute key press.

    # Nested function to unmute the system volume.
    def unmute():
        keyboard.press_and_release("volume mute")   # Simulate the unmute key press.

    # Nested function to increase the system volume.
    def volume_up():
        keyboard.press_and_release("volume up")   # Simulate the volume up key press.

    # Nested function to decrease the system volume.
    def volume_down():
        keyboard.press_and_release("volume down")   # Simulate the volume down key press.


    # Execute the appropriate command.
    if command == "mute":
        mute()

    elif command == "unmute":
        unmute()

    elif command == "volume up":
        volume_up()

    elif command == "volume down":
        volume_down()

async def TranslateAndExecute(commands: list[str]):

    funcs = []   # List to store asynchronous tasks.

    for command in commands:

        if command.startswith("open "):   # Handle 'open' commands.

            if "open it" in command:   # Ignore 'open it' commands.
                pass

            elif "open file" in command:   # Ignore 'open file' commands.
                pass

            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
                funcs.append(fun)


        elif command.startswith("general "):   # Placeholder for general commands.
            pass


        elif command.startswith("realtime "):   # Placeholder for real-time commands.
            pass


        elif command.startswith("close "):   # Handle 'close' commands.
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))
            funcs.append(fun)
        
        elif command.startswith("play "):   # Handle 'play' commands.
              fun = asyncio.to_thread(PlayYouTube, command.removeprefix("play "))
              funcs.append(fun)

        elif command.startswith("content "):   # Handle 'content' commands.
             fun = asyncio.to_thread(Content, command.removeprefix("content "))
             funcs.append(fun)

        elif command.startswith("google search "):   # Handle Google search commands.
             fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))
             funcs.append(fun)
        
        elif command.startswith("youtube search "):   # Handle YouTube search commands.
             fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search "))
             funcs.append(fun)

        elif command.startswith("system "):   # Handle system commands.
             fun = asyncio.to_thread(System, command.removeprefix("system "))
             funcs.append(fun)

        else:
            print(f"No Function Found. For {command}")   # Print an error for unrecognized commands.

    results = await asyncio.gather(*funcs)   # Execute all tasks concurrently.

    for result in results:   # Process the results.
        if isinstance(result, str):
            yield result
        else:
            yield result

# Asynchronous function to automate command execution.
async def Automation(commands: list[str]):

    async for result in TranslateAndExecute(commands):   # Translate and execute commands.
        pass

    return True   # Indicate success.

if __name__ == "__main__":
    asyncio.run(Automation(["play arijit singh songs"]))
