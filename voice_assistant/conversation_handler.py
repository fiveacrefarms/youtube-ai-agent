
import openai

class GPTConversationHandler:
    def __init__(self):
        # Initialize OpenAI API
        openai.api_key = "YOUR_OPENAI_API_KEY"

    def get_response(self, user_input, conversation_history):
        # Combine history with the new input
        prompt = "\n".join(conversation_history + [f"User: {user_input}", "Assistant:"])
        
        # Get response from GPT
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
