import streamlit as st
from openai import OpenAI

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="French Tutor AI", page_icon="🇫🇷", layout="centered")

st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🇫🇷 French Tutor AI")
    st.caption("Powered by Ollama (local AI)")
    st.divider()

    ollama_url = st.text_input(
        "Ollama URL",
        value="http://localhost:11434",
        help="Default Ollama address — don't change unless you moved it"
    )

    model = st.selectbox("Model", [
        "llama3.1",
        "mistral",
        "llama3.2",
        "gemma2",
        "phi3",
        "llama2",
    ], help="Pick whichever model you have pulled in Ollama")

    custom_model = st.text_input("Or type a custom model name", placeholder="e.g. llama3.1:8b")
    if custom_model.strip():
        model = custom_model.strip()

    level = st.selectbox("My French Level", [
        "A1 — Complete Beginner",
        "A2 — Elementary",
        "B1 — Intermediate",
        "B2 — Upper Intermediate",
        "C1 — Advanced"
    ], index=1)

    st.divider()
    st.markdown("**What I can help with:**")
    st.markdown("""
- ✅ Check & correct your French
- 📖 Stories at any CEFR level
- 🗣️ Speaking & conversation practice
- 🎧 Listening comprehension
- 📝 TCF exam preparation
- 📐 Grammar rules explained
- 📚 Vocabulary building
- 🔤 French ↔ English translation
    """)

    st.divider()
    if st.button("🗑️ Clear chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("💡 **Tip:** Run `ollama serve` in your terminal first, then `ollama pull llama3.1`")

# ── Level & system prompt ─────────────────────────────────────────────────────
cefr = level.split("—")[0].strip()

SYSTEM = f"""You are a friendly and expert French language tutor.
The student is a fluent English speaker learning French, currently at CEFR level {cefr}.

You help with:

1. GRAMMAR CHECKING — When the user writes French, find every mistake, explain the rule clearly in English, and show the corrected version.
   Format: ❌ wrong → ✅ correct | Rule: explanation

2. STORIES — Write French stories at the exact CEFR level the user requests. Use only vocabulary and grammar suitable for that level. Always add English translation below each paragraph.

3. SPEAKING PRACTICE — Give dialogues, roleplay scenarios (café, airport, hotel, doctor, job interview), and pronunciation tips.

4. LISTENING / READING COMPREHENSION — Write a short French text or dialogue, then ask 3-5 comprehension questions, then give the answer key.

5. TCF EXAM PREP — Simulate TCF exam sections: Compréhension de l'oral, Compréhension des écrits, Maîtrise des structures de la langue. Explain scoring and give tips.

6. VOCABULARY — Teach words in context with example sentences and memory tips.

7. GRAMMAR RULES — Explain any French grammar rule clearly in English with multiple examples.

8. TRANSLATION — Translate French ↔ English and explain the grammar behind it.

Rules:
- Be friendly, clear, and encouraging at all times
- If the user writes any French, always check it for mistakes first before responding
- Adapt complexity exactly to CEFR level {cefr}
- Use formatting (bold, bullet points, numbered lists) to make responses easy to read
- Never make the student feel bad about mistakes — treat every error as a learning opportunity
"""

WELCOME = {
    "A1": "Bonjour ! 👋 I'm your French Tutor AI — running locally on your machine!\n\nYou're at **A1** (complete beginner) — the perfect starting point.\n\nTry asking me:\n- *Write me an A1 story*\n- *Teach me how to introduce myself in French*\n- *Check my sentence: Je suis un étudiant*\n- *Give me a TCF A1 exercise*\n\nWhat would you like to start with?",
    "A2": "Bonjour ! 👋 I'm your French Tutor AI — running locally on your machine!\n\nYou're at **A2** (elementary) — you know the basics, now let's build confidence!\n\nTry asking me:\n- *Write an A2 story about Paris*\n- *Check my French: Je suis allé au magasin hier*\n- *Explain passé composé vs imparfait*\n- *Give me a TCF practice exercise*\n\nWhat do you want to work on today?",
    "B1": "Bonjour ! 👋 I'm your French Tutor AI — running locally on your machine!\n\nLevel **B1** (intermediate) — you can communicate, now let's make you truly fluent!\n\nTry:\n- *Write a B1 story and quiz me on it*\n- *Give me a speaking exercise for ordering food*\n- *Explain the subjunctive mood with examples*\n- *Simulate a TCF B1 exam section*",
    "B2": "Bonjour ! 👋 Level **B2** — impressive! Let's push you to C1.\n\nWrite to me in French and I'll correct and upgrade your language naturally. Ask me for advanced grammar, TCF B2 practice, or formal writing exercises.\n\nQu'est-ce qu'on travaille aujourd'hui ?",
    "C1": "Bonjour ! 👋 Niveau **C1** — très impressionnant !\n\nLet's refine your French to near-native level. I can help with TCF/DALF C1 prep, advanced grammar, idiomatic French, register and nuance.\n\nÀ toi — qu'est-ce que tu veux travailler ?"
}

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_level" not in st.session_state:
    st.session_state.last_level = level

if st.session_state.last_level != level:
    st.session_state.messages = []
    st.session_state.last_level = level

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🇫🇷 French Tutor AI")
st.caption(f"Level: **{level}** · Model: `{model}` · Local Ollama")

# ── Display messages ──────────────────────────────────────────────────────────
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown(WELCOME.get(cefr, WELCOME["A2"]))

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Chat input ────────────────────────────────────────────────────────────────
user_input = st.chat_input("Ask anything in English or French…")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Call Ollama via OpenAI-compatible API
    client = OpenAI(
        base_url=f"{ollama_url.rstrip('/')}/v1",
        api_key="ollama"  # Ollama doesn't need a real key
    )

    api_messages = [{"role": "system", "content": SYSTEM}] + [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
    ]

    with st.chat_message("assistant"):
        placeholder = st.empty()
        response_text = ""
        try:
            stream = client.chat.completions.create(
                model=model,
                messages=api_messages,
                stream=True,
                temperature=0.7,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                response_text += delta
                placeholder.markdown(response_text + "▌")
            placeholder.markdown(response_text)

        except Exception as e:
            err = str(e)
            if "connection" in err.lower() or "refused" in err.lower():
                placeholder.error("❌ Cannot connect to Ollama. Make sure it's running: open a terminal and type `ollama serve`")
            elif "model" in err.lower():
                placeholder.error(f"❌ Model `{model}` not found. Run: `ollama pull {model}`")
            else:
                placeholder.error(f"❌ Error: {err}")
            st.stop()

    st.session_state.messages.append({"role": "assistant", "content": response_text})
