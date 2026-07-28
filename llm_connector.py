import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

class LLMConnector:
    """Handles chat completions using Groq's fast LLM engine."""

    def __init__(self, model_name: str = "llama-3.3-70b-versatile"):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("Missing GROQ_API_KEY in .env file.")
            
        self.client = Groq(api_key=api_key)
        self.model_name = model_name

    def generate_response(self, user_message: str, relevant_memories: str, chat_history: list) -> str:
        """Constructs prompt with memory context and sends request to Groq API."""
        
        system_instruction = (
            "You are a helpful, personalized AI assistant.\n"
            "Use the provided user memories to personalize your response naturally. "
            "Do NOT state 'According to my memory' unless explicitly asked. Simply know the facts.\n\n"
            f"--- RELEVANT USER MEMORIES ---\n{relevant_memories}\n"
            "-----------------------------"
        )

        # Build message history in standard OpenAI/Groq format
        messages = [{"role": "system", "content": system_instruction}]

        # Append last 3 turns (6 messages) for active conversation context
        for msg in chat_history[-6:]:
            messages.append({"role": msg["role"], "content": msg["content"]})

        messages.append({"role": "user", "content": user_message})

        # Request completion from Groq API
        chat_completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=0.7,
        )

        return chat_completion.choices[0].message.content