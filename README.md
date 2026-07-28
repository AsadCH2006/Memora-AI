# ⚡ Memora AI — Ultra-Fast Persistent Memory Assistant

> A modern, centered Streamlit chat interface powered by **Groq (LLaMA 3.3 70B)** and **Mem0 Cloud API** for ultra-fast, context-aware AI conversations.

---

## 📖 Project Overview

**Memora AI** is a persistent, context-aware AI assistant built with Streamlit, Groq, and Mem0 Cloud. Leveraging LLaMA 3.3 70B for near-instant inference speeds, it automatically extracts, stores, and retrieves user context across sessions, featuring an interactive sidebar vault for full memory management.

---

## 🌟 Key Features

* **🧠 Persistent Long-Term Memory (Mem0 Cloud):** Automatically extracts and stores key facts across chat restarts and sessions.
* **⚡ Ultra-Fast Groq Engine:** Powered by Groq's high-speed inference running `llama-3.3-70b-versatile`.
* **🎯 Centered UI Design:** Modern, sleek interface designed for comfortable reading on wide displays.
* **🔍 Real-Time Context Inspection:** Expandable tooltips inside chat turns showing exact vector memories retrieved from Mem0.
* **🛠️ Active Memory Vault:** Sidebar dashboard displaying saved user facts with single-fact delete capabilities and full cloud wipe support.

---

## 📁 Repository Structure

```text
├── app.py              # Main Streamlit UI & conversation flow logic
├── memory_handler.py   # Mem0 Cloud API client integration & memory operations
├── llm_connector.py    # Groq SDK wrapper targeting LLaMA 3.3 70B
├── requirements.txt    # Python dependency manifest
├── .env.example        # Environment variable template
└── README.md           # Project documentation
```

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **LLM Engine:** Groq API (`groq` SDK — `llama-3.3-70b-versatile`)
* **Memory Management:** Mem0 Cloud (`mem0ai` SDK)
* **Environment:** Python 3.10+

---

## 🚀 Quickstart Guide

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/Memora-AI.git
cd Memora-AI
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:

```env
MEM0_API_KEY=your_mem0_cloud_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run the Application
```bash
streamlit run app.py
```

---

## 🔒 Memory Management Features

* **Sync Memory Vault:** Click **`🔄 Sync`** in the sidebar to refresh saved facts.
* **Remove Specific Fact:** Click **`❌`** next to any memory card in the sidebar to remove individual incorrect entries.
* **Wipe All:** Click **`🗑️ Wipe All`** to clear all stored memories permanently from Mem0 Cloud.

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
