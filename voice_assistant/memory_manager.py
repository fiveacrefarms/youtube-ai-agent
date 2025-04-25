
import os

class MemoryManager:
    def __init__(self, log_file):
        self.log_file = log_file
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

    def load_memory(self):
        # Load conversation history from file
        if os.path.exists(self.log_file):
            with open(self.log_file, "r") as file:
                return file.read().splitlines()
        return []

    def save_memory(self, user_input, assistant_response):
        # Save conversation to file
        with open(self.log_file, "a") as file:
            file.write(f"User: {user_input}\n")
            file.write(f"Assistant: {assistant_response}\n")
