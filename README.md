# 🇫🇷 AI French Tutor — Local Generative AI Language Coach

An interactive, multi-level French language learning application powered entirely on your local machine. This project utilizes **Ollama** for privacy-first, zero-cost inference and **Streamlit** to deliver a responsive, production-ready user interface. 

The application implements dynamic system prompting to adapt its vocabulary, grammar explanations, error-correction mechanisms, and TCF examination prep according to standard **CEFR language levels (A1 - C1)**.

---

## 🚀 Key Engineering & Architecture Highlights

*   **OpenAI-Compatible Local Pipeline:** Built using the `openai` Python SDK mapped directly to Ollama’s local API endpoint (`/v1`). This makes the codebase modular; switching to cloud infrastructure (OpenAI, DeepSeek, Anthropic) requires only changing environment variables.
*   **Stateful UI Management:** Implements Streamlit's `st.session_state` to handle seamless chat persistence and context synchronization, tracking user level switches to purge memory safely.
*   **Token Streaming Architecture:** Utilizes generator-based streaming (`stream=True`) to deliver real-time token rendering, minimizing perceived latency and providing an excellent user experience.
*   **Robust Fault Tolerance:** Features contextual exception handling to catch local infrastructure bottlenecks, such as verifying if the Ollama daemon is active via `ollama serve` or catching missing weights via `ollama pull`.
*   **Dynamic Context Engine:** The AI acts as a rigid language examiner, real-time translator, and conversational coach simultaneously, relying on granular structured prompts to enforce systematic Markdown output (e.g., `❌ wrong → ✅ correct | Rule: explanation`).

---

## 🛠️ Tech Stack & Prerequisites

*   **Frontend UI:** Streamlit
*   **AI Engine:** Ollama (Local LLM Runner)
*   **API Protocol:** OpenAI Python SDK (Local Wrapper)
*   **Recommended Models:** `llama3.1`, `mistral`, `llama3.2`, or `gemma2`

---

## ⚙️ Installation & Local Setup

### 1. Clone the Repository

2. Set Up Your Local AI Engine (Ollama)
Ensure you have Ollama installed, then run the daemon and pull your model of choice:

Bash
# Start the local LLM server
ollama serve

# In a new terminal, download the default recommended model
ollama pull llama3.1
3. Install Dependencies & Run the App
Bash
# Install required libraries
pip install streamlit openai

# Launch the Streamlit application using the core script
streamlit run french_tutor.py
