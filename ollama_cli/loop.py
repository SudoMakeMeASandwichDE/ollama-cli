import ollama_cli.panels as panels
import ollama_cli.save as save
import ollama_cli.commands as commands
import ollama_cli.usemodel as usemodel

def main_loop():
    
    import ollama_cli.vars as vars

    while True:
        try:
            user_prompt = input("> ").strip()
        except KeyboardInterrupt:
            vars.console.print("\nexited with ^C", style="bold red")
            exit()

        match user_prompt.split(" ", 1):
            case ["/?"]:
                panels.help_panel()

            case ["/list"]:
                save.list_chats()

            case ["/new"]:
                commands.new_chat()

            case ["/save", chat_name]:
                vars.chat_name = chat_name.strip()
                commands.save_chat()

            case ["/load", chat_name]:
                vars.chat_name = chat_name.strip()
                commands.load_chat()

            case ["/delete", chat_name]:
                save.delete(chat_name.strip())

            case ["/changemodel", new_model]:
                commands.change_model(new_model.strip())

            case ["/file", file_path]:
                commands.read_file(file_path.strip())

            case ["/write", write_file_name]:
                commands.write_to_file(write_file_name.strip())

            case ["/image", image_path_string]:
                image_path = [image_path_string.strip()]
                commands.read_image(image_path)

            case ["/info"]:
                commands.show_info(vars.model)

            case ["/info", model_info]:
                commands.show_info(model_info.strip())

            case ["/setdefault", newdefault]:
                commands.set_new_default(newdefault.strip())

            case ["/exit"]:
                exit()

            case _ if not user_prompt.startswith("/"):
                usemodel.chat(user_prompt)
