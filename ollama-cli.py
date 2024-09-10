from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import ollama
import os
import ast
import platform
import argparse

console = Console()

parser = argparse.ArgumentParser(description="ollama-cli, a simple but useful command line interface for Ollama to execute LLMs in the Terminal.")
parser.add_argument('-m', '--model', type=str, help='Start ollama-cli directly into a certain model')
args = parser.parse_args()

welcome_message = Panel(
    """
    Welcome to ollama-cli!
     ^ ^
    (°0°)
    (   )
    (   )

    A simple but useful command line interface for Ollama to execute LLMs in the Terminal.

    ollama-cli works with Linux and Windows (experimental).

    THIS IS NOT AN OFFICIAL OLLAMA PRODUCT! NO WARRANTY!
    """,
    title="ollama-cli",
    border_style="blue"
)
rprint(welcome_message)

# Paths for saved chats and configurations
if platform.system() == 'Linux':
    chat_folder_path = os.path.expanduser("~/.config/ollama-cli/chats/")
    default_model_path = os.path.expanduser("~/.config/ollama-cli/default.txt")

if platform.system() == 'Windows':
    console.print("It seems like you're using Windows. Experimental here!\n", style="bold yellow")
    appdata_path = os.getenv('APPDATA')
    chat_folder_path = os.path.join(appdata_path, 'ollama-cli', 'chats')
    default_model_path = os.path.join(appdata_path, 'ollama-cli', 'default.txt')

os.makedirs(chat_folder_path, exist_ok=True)

def save(chat_name):
    try:
        with open(os.path.join(chat_folder_path, f"{chat_name}.txt"), "w") as file:
            file.write(str(messages))
    except Exception as e:
        console.print(f"Error saving chat: [bold red]{str(e)}[/bold red]", style="bold red")

# List installed Ollama models
try:
    models_list = ollama.list()
    models_array = [model["name"] for model_group in models_list.values() for model in model_group]
    models_string = "\n".join(models_array)
except Exception as e:
    console.print(f"Error listing models: [bold red]{str(e)}[/bold red]", style="bold red")
    exit()

if not models_list:
    console.print("No models available. Please install one.", style="bold red")
    exit()

argmodelbool = False
argmodel = args.model

if argmodel:
    if argmodel in models_array:
        model = argmodel
        argmodelbool = True
        console.print(f"Welcome to [bold green]{model}![/bold green]")
    else:
        console.print("Error: Model does not exist", style="bold red")
        exit()

defaultmodelbool = False
maybemodel = ""

if not argmodelbool:
    if os.path.exists(default_model_path):
        try:
            with open(default_model_path, 'r') as file:
                maybemodel = file.read().strip()
            if maybemodel in models_array:
                defaultmodelbool = True
        except Exception as e:
            console.print(f"Error reading default model: [bold red]{str(e)}[/bold red]", style="bold red")

    if defaultmodelbool:
        model = maybemodel
        console.print(f"Welcome to [bold green]{model}![/bold green]")
    else:
        while True:
            console.print(f"Choose one of the following models:\n\n{models_string}")
            model = input("> ")
            if model in models_array:
                console.print(f"\nWelcome to [bold green]{model}![/bold green]")
                if not os.path.exists(default_model_path):
                    if input(f"Do you want to set [bold green]{model}[/bold green] as default? [y/n] > ").lower() == "y":
                        try:
                            with open(default_model_path, 'w') as file:
                                file.write(model)
                        except Exception as e:
                            console.print(f"Error setting default model: [bold red]{str(e)}[/bold red]", style="bold red")
                break
            else:
                console.print("Error: Model does not exist\n", style="bold red")

console.print("Ask me anything\nFor further commands, type '/?'.", style="bold cyan")

messages = []
savedchat = False

def list_chats():
    try:
        chats = os.listdir(chat_folder_path)
        if chats:
            table = Table(title="Saved Chats")
            table.add_column("Chat Name", style="cyan")
            for chat in chats:
                table.add_row(chat[:-4])
            console.print(table)
        else:
            console.print("No chats yet", style="bold yellow")
    except Exception as e:
        console.print(f"Error listing chats: [bold red]{str(e)}[/bold red]", style="bold red")

def load_chat(chat_name):
    global messages
    try:
        with open(os.path.join(chat_folder_path, f"{chat_name}.txt"), "r") as file:
            messages = ast.literal_eval(file.readline())
        for message in messages:
            console.print(f"[bold]{message['role']}:[/bold] {message['content']}\n")
    except Exception as e:
        console.print(f"Error loading chat: [bold red]{str(e)}[/bold red]", style="bold red")

while True:
    file = False
    websearch = False
    user_prompt = input("> ").strip()

    if user_prompt == "/?":
        console.print(Panel(
            """
            /save [chat name] to save chat
            /load [chat name] to load chat
            /list to list chats
            /new to start a new chat
            /delete [chat name] to delete chat
            /file [file path] to upload a text file (experimental)
            /write [file path] to write the LLM's last answer to a file
            /changemodel [model name] to change model
            /exit to exit
            """,
            title="Commands",
            border_style="blue"
        ))


    elif user_prompt.startswith("/save "):
        chat_name = user_prompt[6:].strip()
        if chat_name:
            save(chat_name)
            savedchat = True
            console.print(f"chat saved as '[bold green]{chat_name}[/bold green]'\nThis chat will be saved automatically after every interaction.", style="bold green")
        else:
            console.print("Please specify the name of your chat.", style="bold red")

    elif user_prompt.startswith("/load "):
        chat_name = user_prompt[6:].strip()
        if os.path.exists(os.path.join(chat_folder_path, f"{chat_name}.txt")):
            load_chat(chat_name)
            savedchat = True
        else:
            console.print("Chat not found. Type /list to list all your chats.", style="bold red")

    elif user_prompt == "/list":
        list_chats()

    elif user_prompt.startswith("/delete "):
        chat_name = user_prompt[8:].strip()
        chat_path = os.path.join(chat_folder_path, f"{chat_name}.txt")
        if os.path.exists(chat_path):
            try:
                os.remove(chat_path)
                console.print(f"Deleted chat: [bold green]{chat_name}[/bold green]", style="bold green")
            except Exception as e:
                console.print(f"Error deleting chat: [bold red]{str(e)}[/bold red]", style="bold red")
        else:
            console.print("Chat not found. Type /list to list all your chats.", style="bold red")

    elif user_prompt == "/new":
        if not savedchat:
            if input("Do you want to save chat? [y/n] > ").lower() == "y":
                chat_name = input("Chat name: > ").strip()
                save(chat_name)
            messages = []
        else:
            messages = []
            console.print("Started a new conversation", style="bold green")
            savedchat = False

    elif user_prompt.startswith("/changemodel "):
        new_model = user_prompt[13:].strip()
        if new_model in models_array:
            model = new_model
            console.print(f"Now using [bold green]{model}.[/bold green]", style="bold green")
        else:
            console.print(f"Model is not installed or existing. Choose one of your installed ones:\n\n{models_string}", style="bold red")

    

    elif user_prompt.startswith("/file "):
        file_path = user_prompt[6:].strip()
        print(file_path)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    file_content = file.read()
                file = True
                file_name = os.path.basename(file_path)
                user_prompt_file = input("Your Prompt > ")
                messages.append({'role':'user', 'content':f"""Given to you is a file called "{file_name}". This is, what the user wants you to do or to answer: "{user_prompt_file}". 
                                 And this is the file content: 
                                 "{file_content}" """})
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
            except Exception as e:
                print(f"Error: File not found or isn't a text file")

    elif user_prompt.startswith("/write "):
        write_file_name = user_prompt[7:].strip()
        if '.' not in write_file_name:
            write_file_name += ".txt"
        for entry in reversed(messages):
            if entry['role'] == 'assistant':
                last_assistant_entry = entry['content']
                break
        with open(write_file_name, 'w') as f:
            f.write(last_assistant_entry)

    elif user_prompt == "/exit":
        exit()

    elif not user_prompt.startswith("/"):
        messages.append({'role': 'user', 'content': user_prompt})
        console.print("assistant: ", end='', style="bold cyan")
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
            console.print(f"Error while trying to use model: [bold red]{str(e)}[/bold red]", style="bold red")

    else:
        console.print("Command not found", style="bold red")