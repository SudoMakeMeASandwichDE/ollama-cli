from rich.console import Console
from rich.table import Table
import ollama
import os
import ollama_cli.panels as panels
import ollama_cli.save as save

def main_loop():
    console = Console()
    chat_folder_path, default_model_path = save.paths(False)
    models_array, models_string = save.readmodels()
    
    from main import model

    messages = []
    savedchat = False

    while True:
        try:
            user_prompt = input("> ").strip()
        except KeyboardInterrupt:
            console.print("\nexited with ^C", style="bold red")
            exit()

        if user_prompt == "/?":
            panels.help_panel()

        elif user_prompt.startswith("/save "):
            chat_name = user_prompt[6:].strip()
            if chat_name:
                save.save(chat_name, messages)
                savedchat = True
                console.print(f"chat saved as '[bold green]{chat_name}[/bold green]'\nThis chat will be saved automatically after every interaction.", style="bold green")
            else:
                console.print("Please specify the name of your chat.", style="bold red")

        elif user_prompt.startswith("/load "):
            chat_name = user_prompt[6:].strip()
            if os.path.exists(os.path.join(chat_folder_path, f"{chat_name}.txt")):
                messages = save.load_chat(chat_name)
                savedchat = True
            else:
                console.print("Chat not found. Type /list to list all your chats.", style="bold red")

        elif user_prompt == "/list":
            save.list_chats()

        elif user_prompt.startswith("/delete "):
            chat_name = user_prompt[8:].strip()
            save.delete(chat_name)

        elif user_prompt == "/new":
            if not savedchat:
                if input("Do you want to save chat? [y/n] > ").lower().strip() == "y":
                    chat_name = input("Chat name: > ").strip()
                    save.save(chat_name, messages)
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
                console.print("Model is not installed or existing. Choose one of your installed ones:\n", style="bold red")
                print(models_string)

        elif user_prompt.startswith("/file "):
            file_path = user_prompt[6:].strip()
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        file_content = file.read()
                    file_name = os.path.basename(file_path)
                    try:
                        user_prompt_file = input("Your Prompt > ")
                    except KeyboardInterrupt:
                        console.print("exited with ^C", style="bold red")
                    messages.append({'role':'user', 'content':f"""Given to you is a file called "{file_name}". This is, what the user wants you to do or to answer: "{user_prompt_file}". 
                                    And this is the file content: 
                                    "{file_content}" """})
                    console.print("assistant: ", end='', style="bold cyan")
                    try:
                        response = ""
                        for part in ollama.chat(model=model, messages=messages, stream=True):
                            print(part['message']['content'], end='', flush=True)
                            response += part['message']['content']
                        print()
                        messages.append({'role': 'assistant', 'content': response})
                        if savedchat:
                            save.save(chat_name, messages)
                    except Exception as e:
                        print(f"Error while trying to use model: {str(e)}")
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
        
        elif user_prompt.startswith("/image "):
            image_path = []
            image_path.append(user_prompt[7:])
            print(image_path)
            if os.path.exists(user_prompt[7:]):
                try:
                    user_prompt_image = input("Your prompt > ")
                except KeyboardInterrupt:
                    console.print("exited with ^C", style="bold red")
                messages.append({'role':'user','content':user_prompt_image,'images':image_path})
                console.print("assistant: ", end='', style="bold cyan")
                try:
                    response = ""
                    for part in ollama.chat(model=model, messages=messages, stream=True):
                        print(part['message']['content'], end='', flush=True)
                        response += part['message']['content']
                    print()
                    messages.append({'role': 'assistant', 'content': response})
                    if savedchat:
                        save.save(chat_name, messages)
                except Exception as e:
                    print(f"Error while trying to use model: {str(e)}")
            else:
                console.print("Image file not found.", style="bold red")
        
        elif user_prompt.startswith("/info"):
            if user_prompt.startswith("/info "):
                model_info = user_prompt[6:]
            else:
                model_info = model
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

                for name, eintrag in info_dict.items():
                    table.add_row(name, eintrag)

                console.print(table)

            except Exception as e:
                console.print(f"error: {str(e)}", style='bold red')

        elif user_prompt.startswith("/setdefault "):
            try:
                newdefault = user_prompt[12:]
                if newdefault in models_array:
                    with open(default_model_path, 'w') as file:
                        file.write(newdefault)
                    console.print(f"Changed default model to {newdefault}", style='bold green')
                else:
                    console.print("model does not exist", style='bold red')
            except Exception as e:
                console.print(f"error: {str(e)}")

        elif user_prompt == "/exit":
            exit()

        elif not user_prompt.startswith("/"):
            messages.append({'role': 'user', 'content': user_prompt})
            console.print("assistant: ", end='', style="bold cyan")
            try:
                response = ""
                try:
                    for part in ollama.chat(model=model, messages=messages, stream=True):
                        print(part['message']['content'], end='', flush=True)
                        response += part['message']['content']
                except KeyboardInterrupt:
                    print(end='')
                print()
                messages.append({'role': 'assistant', 'content': response})
                if savedchat:
                    save.save(chat_name, messages)
            except Exception as e:
                console.print(f"Error while trying to use model: [bold red]{str(e)}[/bold red]", style="bold red")

        else:
            console.print("Command not found", style="bold red")
