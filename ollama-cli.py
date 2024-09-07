# Made in Germany
"""
This file is part of ollama-cli.

ollama-cli is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

ollama-cli is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with ollama-cli. If not, see <http://www.gnu.org/licenses/>.
"""
import ollama
import os
import ast
import platform

print("""
Welcome to ollama-cli!
 ^ ^
(°0°)
(   )
(   )

A simple but useful command line interface for Ollama to execute LLMs in the Terminal.

ollama-cli works with Linux and Windows (experimental).

For help type '/?'
      
THIS IS NOT AN OFFICIAL OLLAMA PRODUCT! NO WARRATY!

""")

# Paths for saved chats and configurations
# print(platform.system())
if platform.system() == 'Linux':
    chat_folder_path = os.path.expanduser("~/.config/ollama-cli/chats/")
    default_model_path = os.path.expanduser("~/.config/ollama-cli/default.txt")

if platform.system() == 'Windows':
    appdata_path = os.getenv('APPDATA')
    chat_folder_path = os.path.join(appdata_path, 'ollama-cli', 'chats')
    default_model_path = os.path.join(appdata_path, 'ollama-cli', 'default.txt')
    print("It seems like, you're using Windows. Experimental here!\n")

os.makedirs(chat_folder_path, exist_ok=True)

def save(chat_name):
    with open(os.path.join(chat_folder_path, f"{chat_name}.txt"), "w") as file:
        file.write(str(messages))

# List installed Ollama models
models_list = ollama.list()
models_string = "\n".join(model["name"] for model_group in models_list.values() for model in model_group)
models_array = [model["name"] for model_group in models_list.values() for model in model_group]

if not models_list:
    print("No models available. Please install one.")
    exit()

defaultmodelbool = False
maybemodel = ""

if os.path.exists(default_model_path):
    with open(default_model_path, 'r') as file:
        maybemodel = file.read().strip()
    if maybemodel in models_array:
        defaultmodelbool = True

if defaultmodelbool:
    model = maybemodel
    print(f"Welcome to {model}!")
else:
    while True:
        print(f"Choose one of the following models:\n\n{models_string}")
        model = input("> ")
        if model in models_array:
            print(f"\nWelcome to {model}!")
            if not os.path.exists(default_model_path):
                if input(f"Do you want to set {model} as default? [y/n] > ").lower() == "y":
                    with open(default_model_path, 'w') as file:
                        file.write(model)
            break
        else:
            print("Error: Model does not exist\n")

print("""Ask me anything\nFor further commands, type '/?'.""")

messages = []
savedchat = False

def list_chats():
    chats = os.listdir(chat_folder_path)
    if chats:
        print("\n".join(chat[:-4] for chat in chats))
    else:
        print("No chats yet")

def load_chat(chat_name):
    global messages
    with open(os.path.join(chat_folder_path, f"{chat_name}.txt"), "r") as file:
        messages = ast.literal_eval(file.readline())
    for message in messages:
        print(f"{message['role']}: {message['content']}\n")

while True:
    user_prompt = input("> ").strip()

    if user_prompt == "/?":
        print("/save [chat name] to save chat\n/load [chat name] to load chat\n/list to list chats\n/new to start a new chat\n/delete [chat name] to delete chat\n/changemodel [model name] to change model\n/exit to exit")

    elif user_prompt.startswith("/save "):
        chat_name = user_prompt[6:].strip()
        if chat_name:
            save(chat_name)
            savedchat = True
        else:
            print("Please specify the name of your chat.")

    elif user_prompt.startswith("/load "):
        chat_name = user_prompt[6:].strip()
        if os.path.exists(os.path.join(chat_folder_path, f"{chat_name}.txt")):
            load_chat(chat_name)
            savedchat = True
        else:
            print("Chat not found. Type /list to list all your chats.")

    elif user_prompt == "/list":
        list_chats()

    elif user_prompt.startswith("/delete "):
        chat_name = user_prompt[8:].strip()
        chat_path = os.path.join(chat_folder_path, f"{chat_name}.txt")
        if os.path.exists(chat_path):
            os.remove(chat_path)
            print(f"Deleted chat: {chat_name}")
        else:
            print("Chat not found. Type /list to list all your chats.")

    elif user_prompt in ["/new", "/new "]:
        if not savedchat:
            if input("Do you want to save chat? [y/n] > ").lower() == "y":
                chat_name = input("Chat name: > ").strip()
                save(chat_name)
            messages = []
        else:
            messages = []
            savedchat = False

    elif user_prompt.startswith("/changemodel "):
        new_model = user_prompt[13:].strip()
        if new_model in models_array:
            model = new_model
            print(f"Now using {model}.")
        else:
            print(f"Model is not installed or existing. Choose one of your installed ones:\n\n{models_string}")

    elif user_prompt == "/exit":
        exit()

    elif not user_prompt.startswith("/"):
        messages.append({'role': 'user', 'content': user_prompt})
        print("assistant: ", end='')
        try:
            response = ""
            for part in ollama.chat(model=model, messages=messages, stream=True):
                print(part['message']['content'], end='', flush=True)
                response += part['message']['content']
            print()
            messages.append({'role': 'assistant', 'content': response})
            if savedchat:
                save(chat_name)
        except Exception as e:
            print(f"Error while trying to start model: {str(e)}")

    else:
        print("Command not found")
