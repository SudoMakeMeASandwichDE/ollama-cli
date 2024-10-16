from rich.table import Table
import ollama
import os
import ollama_cli.save as save
import ollama_cli.vars as vars
import ollama_cli.usemodel as usemodel

chat_folder_path, default_model_path = save.paths(False)
models_array, models_string = save.readmodels()

def read_file(file_path):

    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                file_content = file.read()
            file_name = os.path.basename(file_path)
            try:
                user_prompt_file = input("Your Prompt > ")
            except KeyboardInterrupt:
                vars.console.print("exited with ^C", style="bold red")
            usemodel.chat(user_prompt=f"""<system_message>: Given to you is a file called "{file_name}". This is, what the user requests you to do or to answer: "{user_prompt_file}". \nAnd this is the file content: \n"{file_content}" """)
        except Exception as e:
            vars.console.print(f"Error: File not found or isn't a text file", style="bold red")
    else:
        vars.console.print(f"Error: File not found", style="bold red")

def save_chat():
    if vars.chat_name:
        save.save(vars.chat_name, vars.messages)
        vars.savedchat = True
        vars.console.print(f"chat saved as '[bold green]{vars.chat_name}[/bold green]'\nThis chat will be saved automatically after every interaction.", style="bold green")
    else:
        vars.console.print("Please specify the name of your chat.", style="bold red")

def load_chat():
    if os.path.exists(os.path.join(vars.chat_folder_path, f"{vars.chat_name}.txt")):
        vars.messages = save.load_chat(vars.chat_name)
        vars.savedchat = True
    else:
        vars.console.print("Chat not found. Type /list to list all your chats.", style="bold red")

def new_chat():
    if not vars.savedchat:
        if input("Do you want to save chat? [y/n] > ").lower().strip() == "y":
            chat_name = input("Chat name: > ").strip()
            save.save(chat_name, vars.messages)
        vars.messages = []
    else:
        vars.messages = []
        vars.console.print("Started a new conversation", style="bold green")
        vars.savedchat = False

def change_model(new_model):
    if new_model in models_array:
        vars.model = new_model
        vars.console.print(f"Now using [bold green]{vars.model}.[/bold green]", style="bold green")
    else:
        vars.console.print("Model is not installed or existing. Choose one of your installed ones:\n", style="bold red")
        print(models_string)

def write_to_file(write_file_name):
    if '.' not in write_file_name:
        write_file_name += ".txt"
    for entry in reversed(vars.messages):
        if entry['role'] == 'assistant':
            last_assistant_entry = entry['content']
            break
    with open(write_file_name, 'w') as f:
        f.write(last_assistant_entry)

def read_image(image_path):
    if os.path.exists(image_path[0]):
        try:
            user_prompt_image = input("Your prompt > ")
        except KeyboardInterrupt:
            vars.console.print("exited with ^C", style="bold red")
        usemodel.chat(user_prompt=user_prompt_image, image_path=image_path)

    else:
        vars.console.print("Image file not found.", style="bold red")

def show_info(model_info):
    try:
        info = ollama.show(model_info)
        info_dict = {}
        try:
            info_dict['basename'] = info['model_info']['general.basename']
        except:
            pass
        try:
            info_dict['family'] = ', '.join(info['details']['families'])
        except:
            pass
        try:
            info_dict['parameter size'] = info['details']['parameter_size']
        except:
            pass
        try:
            info_dict['supported languages'] = ', '.join(info['model_info']['general.languages'])
        except:
            pass
        try:
            info_dict['tags'] = ', '.join(info['model_info']['general.tags'])
        except:
            pass

        table = Table(title=f"info for {model_info}",show_header=False)

        table.add_column("name", justify="left", style="cyan", no_wrap=True)
        table.add_column("entry", justify="left", style="magenta")

        for name, entry in info_dict.items():
            table.add_row(name, entry)

        vars.console.print(table)

    except Exception as e:
        vars.console.print(f"error: {str(e)}", style='bold red')

def set_new_default(newdefault):
    try:
        if newdefault in models_array:
            with open(vars.default_model_path, 'w') as file:
                file.write(newdefault)
            vars.console.print(f"Changed default model to {newdefault}", style='bold green')
        else:
            vars.console.print("model does not exist", style='bold red')
    except Exception as e:
        vars.console.print(f"error: {str(e)}")
