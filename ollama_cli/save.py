from rich import console
from rich.console import Console
from rich.table import Table
import ollama
import os
import ast
import platform

console = Console()

def paths(make=True):
    global chat_folder_path
    global default_model_path
    if platform.system() == 'Linux':
        chat_folder_path = os.path.expanduser("~/.config/ollama-cli/chats/")
        default_model_path = os.path.expanduser("~/.config/ollama-cli/default.txt")

    elif platform.system() == 'Windows':
        console.print("It seems like you're using Windows. Experimental here!\n", style="bold yellow")
        appdata_path = os.getenv('APPDATA')
        chat_folder_path = os.path.join(appdata_path, 'ollama-cli', 'chats')
        default_model_path = os.path.join(appdata_path, 'ollama-cli', 'default.txt')

    else:
        console.print("Your OS is not yet compatible with ollama-cli. Please use Linux or Windows", style='bold red')
        return False

    if make:
        os.makedirs(chat_folder_path, exist_ok=True)
    return chat_folder_path, default_model_path

def readmodels():
    try:
        models_list = ollama.list()
        if not models_list:
            console.print("No models available. Please install one.", style="bold red")
            return False
        models_array = [model["name"] for model_group in models_list.values() for model in model_group]
        models_string = "\n".join(models_array)
        return models_array, models_string
    except Exception as e:
        console.print(f"Error reading models: [bold red]{str(e)}[/bold red]", style="bold red")
        return False

def save(chat_name, messages):
    try:
        with open(os.path.join(chat_folder_path, f"{chat_name}.txt"), "w") as file:
            file.write(str(messages))
    except Exception as e:
        console.print(f"Error saving chat: [bold red]{str(e)}[/bold red]", style="bold red")

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
    try:
        with open(os.path.join(chat_folder_path, f"{chat_name}.txt"), "r") as file:
            messages = ast.literal_eval(file.readline())
        for message in messages:
            console.print(f"[bold]{message['role']}:[/bold] {message['content']}\n")
        return messages
    except Exception as e:
        console.print(f"Error loading chat: [bold red]{str(e)}[/bold red]", style="bold red")

def delete(chat_name):
    chat_path = os.path.join(chat_folder_path, f"{chat_name}.txt")
    if os.path.exists(chat_path):
        try:
            os.remove(chat_path)
            console.print(f"Deleted chat: [bold green]{chat_name}[/bold green]", style="bold green")
        except Exception as e:
            console.print(f"Error deleting chat: [bold red]{str(e)}[/bold red]", style="bold red")
    else:
        console.print("Chat not found. Type /list to list all your chats.", style="bold red")
