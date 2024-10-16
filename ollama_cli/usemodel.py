import ollama
import ollama_cli.vars as vars
import ollama_cli.save as save

def chat(user_prompt, image_path=None):
    if image_path:
        vars.messages.append({'role':'user', 'content':user_prompt, 'images':image_path})
    else:
        vars.messages.append({'role':'user', 'content':user_prompt})
    vars.console.print("assistant: ", end='', style="bold cyan")
    try:
        response = ""
        try:
            for part in ollama.chat(model=vars.model, messages=vars.messages, stream=True):
                print(part['message']['content'], end='', flush=True)
                response += part['message']['content']
        except KeyboardInterrupt:
            pass
        print()
        vars.messages.append({'role': 'assistant', 'content': response})
        if vars.savedchat:
            save.save(vars.chat_name, vars.messages)
    except Exception as e:
        vars.console.print(f"Error while trying to use model: [bold red]{str(e)}[/bold red]", style="bold red")
