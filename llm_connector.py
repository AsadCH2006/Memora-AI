import os
import streamlit as st
from groq import Groq

class LLMConnector:
    """Handles response generation using Groq's fast LLaMA engine."""

    def __init__(self, model_name: str = "llama-3.3-70b-versatile"):
        # Safely fetch GROQ_API_KEY from env or Streamlit Secrets
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key and hasattr(st, "secrets"):
            api_key = st.secrets.get("GROQ_API_KEY")
            
        if not api_key:
            raise ValueError("Missing GROQ_API_KEY in environment variables or Streamlit Secrets.")
            
        self.client = Groq(api_key=api_key)
        self.model_name = model_name

    def generate_response(self, user_message: str, relevant_memories: str, chat_history: list) -> str:
        """Formats prompt with injected memory context and generates LLM output."""
        system_instruction = (
            "You are a helpful, personalized AI assistant.\n"
            "Use the provided user memories to personalize your response naturally.\n"
            "Do NOT explicitly state 'According to my memory' unless asked.\n\n"
            f"--- RELEVANT USER MEMORIES ---\n{relevant_memories}\n"
            "-----------------------------"
        )

        messages = [{"role": "system", "content": system_instruction}]

        # Append recent turns (last 3 turns / 6 messages)
        for msg in chat_history[-6:]:
            messages.append({"role": msg["role"], "content": msg["content"]})

        messages.append({"role": "user", "content": user_message})

        chat_completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=0.7,
        )

        return chat_completion.choices[0].message.content
