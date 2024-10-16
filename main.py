# Made in Germany
from rich.console import Console
import os
import ollama_cli.panels as panels
import ollama_cli.save as save
from start import args
import ollama_cli.loop as loop
import ollama_cli.vars as vars

vars.console = Console()

panels.welcome_panel()

chat_folder_path, default_model_path = save.paths()
vars.chat_folder_path = chat_folder_path
vars.default_model_path = default_model_path

readmodels = save.readmodels()

if not readmodels:
    exit()
else:
    models_array, models_string = readmodels

useargmodel = False
argmodel = args.model

if argmodel:
    if argmodel in models_array:
        model = argmodel
        useargmodel = True
        vars.console.print(f"Welcome to [bold green]{model}![/bold green]")
    else:
        vars.console.print("Error: Model does not exist", style="bold red")
        exit()

defaultmodelbool = False
maybemodel = ""

if not useargmodel:
    if os.path.exists(default_model_path):
        try:
            with open(default_model_path, 'r') as file:
                maybemodel = file.read().strip()
            if maybemodel in models_array:
                defaultmodelbool = True
            else:
                vars.console.print("The model which has been set as default isn't existing.\n", style="bold red")
                os.remove(default_model_path)
        except Exception as e:
            vars.console.print(f"Error reading default model: [bold red]{str(e)}[/bold red]", style="bold red")

    if defaultmodelbool:
        model = maybemodel
        vars.console.print(f"Welcome to [bold green]{model}![/bold green]")
    else:
        while True:
            print(f"Choose one of the following models:\n\n{models_string}")
            try:
                model = input("> ").strip()
            except KeyboardInterrupt:
                vars.console.print("\nexited with ^C", style="bold red")
                exit()
            if model in models_array:
                if not os.path.exists(default_model_path):
                    vars.console.print(f"Do you want to set [bold green]{model}[/bold green] as default? [y/n] ", end='')
                    setdeafaultyn = input("> ").lower().strip()
                    if setdeafaultyn == "y":
                        try:
                            with open(default_model_path, 'w') as file:
                                file.write(model)
                        except Exception as e:
                            vars.console.print(f"Error setting default model: [bold red]{str(e)}[/bold red]", style="bold red")
                vars.console.print(f"\nWelcome to [bold green]{model}![/bold green]")
                break
            else:
                vars.console.print("Error: Model does not exist\n", style="bold red")

vars.console.print("Ask me anything\nFor further commands, type '/?'.", style="bold cyan")

vars.model = model

loop.main_loop()
