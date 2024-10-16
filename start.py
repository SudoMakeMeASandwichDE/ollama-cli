# Execute this script to start ollama-cli. Needed for arguments.
import argparse

parser = argparse.ArgumentParser(description="ollama-cli, a simple but useful command line interface for Ollama to execute LLMs in the terminal.")
parser.add_argument('-m', '--model', type=str, help='Start ollama-cli directly into a certain model')
args = parser.parse_args()

# Start main.py script
import main
