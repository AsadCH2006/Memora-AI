import os
import streamlit as st
from dotenv import load_dotenv
from mem0 import MemoryClient

load_dotenv()

class MemoryHandler:
    """Handles persistent long-term memory using Mem0 Cloud API."""

    def __init__(self, user_id: str = "user_demo"):
        self.user_id = user_id
        
        # Safely retrieve key from environment variables or Streamlit Secrets
        api_key = os.getenv("MEM0_API_KEY")
        if not api_key and hasattr(st, "secrets"):
            api_key = st.secrets.get("MEM0_API_KEY")

        if not api_key:
            raise ValueError("Missing MEM0_API_KEY in environment variables or Streamlit Secrets.")

        self.client = MemoryClient(api_key=api_key)

    def add_memory(self, user_message: str):
        """Passes ONLY user message to ensure only user facts are extracted."""
        messages = [{"role": "user", "content": user_message}]
        self.client.add(messages, user_id=self.user_id)

    def get_memories(self, query: str) -> str:
        """Retrieves semantically relevant memories using Mem0's filters syntax."""
        results = self.client.search(query=query, filters={"user_id": self.user_id})
        
        if isinstance(results, dict) and "results" in results:
            items = results["results"]
        elif isinstance(results, list):
            items = results
        else:
            items = []

        if not items:
            return ""

        memory_strings = [item["memory"] for item in items if "memory" in item]
        return "\n".join(f"- {mem}" for mem in memory_strings)

    def get_all_memories_detailed(self) -> list:
        """Gets all saved memory objects (with IDs and text) for sidebar deletion."""
        all_mems = self.client.get_all(filters={"user_id": self.user_id})
        
        if isinstance(all_mems, dict) and "results" in all_mems:
            items = all_mems["results"]
        elif isinstance(all_mems, list):
            items = all_mems
        else:
            items = []

        return items

    def delete_single_memory(self, memory_id: str):
        """Deletes a specific memory by its ID."""
        self.client.delete(memory_id=memory_id)

    def wipe_all_memories(self):
        """Wipes all memories stored on Mem0 for this specific user."""
        self.client.delete_all(user_id=self.user_id)
