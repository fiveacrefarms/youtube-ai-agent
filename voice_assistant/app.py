import streamlit as st
from conversation_handler import GPTConversationHandler
from memory_manager import MemoryManager
from tts_manager import TTSManager
import os

# Initialize components
conversation_handler = GPTConversationHandler()
memory_manager = MemoryManager("logs/conversation_log.txt")
tts_manager = TTSManager()

# Streamlit UI
st.title("Personal AI Assistant")
st.markdown("Your personal assistant with a cloned voice and memory.")

# Input section
user_input = st.text_input("Ask your assistant something:")

if st.button("Submit"):
    if user_input:
        # Retrieve memory and enhance context
        conversation_history = memory_manager.load_memory()
        response = conversation_handler.get_response(user_input, conversation_history)

        # Save conversation to memory
        memory_manager.save_memory(user_input, response)

        # Display response
        st.text_area("Assistant:", value=response, height=200)

        # Generate and play audio
        audio_file = tts_manager.text_to_speech(response)
        st.audio(audio_file, format="audio/wav")
    else:
        st.warning("Please enter a message.")
