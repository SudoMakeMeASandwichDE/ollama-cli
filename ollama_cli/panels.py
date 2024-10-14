from rich import print as rprint
from rich.panel import Panel

def welcome_panel():
    welcome_message = Panel(
        """
        Welcome to ollama-cli!
        ^ ^
        (°0°)
        (   )
        (   )

        A simple but useful command line interface for Ollama to execute LLMs in the terminal.

        ollama-cli works with Linux and Windows (experimental).

        THIS IS NOT AN OFFICIAL OLLAMA PRODUCT! NO WARRANTY!
        """,
        title="ollama-cli",
        border_style="blue"
    )
    rprint(welcome_message)

def help_panel():
    help_panel = Panel(
            """
            /save \[chat name] to save chat
            /load \[chat name] to load chat
            /list to list chats
            /new to start a new chat
            /delete \[chat name] to delete chat
            /file \[file path] to upload a text file (experimental)
            /write \[file path] to write the LLM's last answer to a file
            /info \[model name] to show some information about a model
            /info to show some information about the current model
            /changemodel \[model name] to change model
            /setdefault \[model name] to change the default model
            /exit to exit
            """,
            title="Commands",
            border_style="blue"
    )
    rprint(help_panel)
