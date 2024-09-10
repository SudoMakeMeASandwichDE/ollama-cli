# ollama-cli
Simple but useful command line interface for Ollama to execute LLMs in the terminal.

To use it, download `ollama-cli.py` and execute it with `python3 ollama-cli.py`. Make sure, you have the ollama python library installed (if not, do it with the command `pip install ollama`), Ollama installed (If not, visit https://ollama.com/download) and the model(s) of your choice installed (if not, do it with the command `ollama pull [model]`, e.g. `llama3.1`).

Supports Linux and Windows (experimental)

On Linux, chats and configurations will be saved in `~/.config/ollama-cli/`

On Windows, these will be saved in `C:\Users\<username>\AppData\ollama-cli`

## Features
- **Easy to use:** ollama-cli is programmed to be easy to use. You can type `/?` at every time to see all commands. 
- **Models:** You can use ollama-cli with every text-based LLM available on the [Ollama library](https://ollama.com/library) (image upload coming soon). You can even change the model **during a conversation** with `/changemodel [model_name]` and load **one conversation into different models.**
- **Easy chat management:** You can save your current chat with `/save [chat_name]`, list all your chats with `/list`, load one of them with `/load [chat_name]` and delete one of them with `/delete [chat_name]`.
- **Upload text files:** You can upload text files by executing `/file [file_path]` or `/file [file_name]` with return key and than type your prompt.
- **Start instantly with a certian model:** You can execute ollama-cli with `python3 ollama-cli.py -m [model_name]` to skip the model seletion screen or to use in scripts.
- **Write LLM's answer into file:** You can write the last output of the model you use by typing `/write [file_path]` or `/write [file_name]`.

## What's new
- 1.0.1:
  - Added argument to directly start with a certian model (`python3 ollama-cli.py -m [model_name]`)
  - Better perforamnce and code readability
- 1.1.0
  - Text file upload with `/file [file_path]`
  - Write the LLM's last answer into a file with `/write [file_path]`
  - Better error messages
---
NO OFFICIAL OLLAMA PRODUCT

ollama-cli is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
