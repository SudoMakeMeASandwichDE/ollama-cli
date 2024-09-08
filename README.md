# ollama-cli
Simple but useful command line interface for Ollama. 

To use it, download `ollama-cli.py` and execute it with `python3 ollama-cli.py`. Make sure, you have the ollama python library installed (if not, do it with the command `pip install ollama`), Ollama installed (If not, visit https://ollama.com/download) and the model(s) of your choice installed (if not, do it with the command `ollama pull [model]`, e.g. `llama3.1`).

Supports Linux and Windows (experimental)

On Linux, chats and configurations will be saved in `~/.config/ollama-cli/`

On Windows, these will be saved in `C:\Users\<username>\AppData\ollama-cli`

## Features
- **Easy to use:** ollama-cli is programmed to be easy to use. You can type `/?` at every time to see all commands. 
- **Models:** You can use ollama-cli with every text-based LLM available on the [Ollama library](https://ollama.com/library) (File upload coming soon...). You can even change the model **during a conversation** with `/changemodel [model_name]` and load **one conversation into different models.**
- **Easy chat management:** You can save your current chat with `/save [chat_name]`, list all your chats with `/list`, load one of them with `/load [chat_name]` and delete one of them with `/delete [chat_name]`.

NO OFFICIAL OLLAMA PRODUCT

ollama-cli is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
