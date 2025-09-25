import os
import requests
import streamlit as st
from dotenv import load_dotenv
from transformers import pipeline

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()
HF_MODEL = "google/flan-t5-small"  # Small, fast model
#TRELLO_KEY = os.getenv("TRELLO_API_KEY")
#TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")

TRELLO_API_KEY = st.secrets["TRELLO_API_KEY"]
TRELLO_TOKEN = st.secrets["TRELLO_TOKEN"]

if not TRELLO_KEY or not TRELLO_TOKEN:
    st.warning("⚠️ Trello API Key/Token not found in .env file")

# -----------------------------
# Initialize Hugging Face pipeline (local inference)
# -----------------------------
@st.cache_resource
def load_model():
    return pipeline("text2text-generation", model=HF_MODEL)

nlp = load_model()

# -----------------------------
# Trello helpers
# -----------------------------
def get_trello_boards():
    """Fetch all Trello boards for the authenticated user."""
    url = "https://api.trello.com/1/members/me/boards"
    query = {"key": TRELLO_KEY, "token": TRELLO_TOKEN, "fields": "name,url"}
    resp = requests.get(url, params=query)
    if resp.status_code == 200:
        return resp.json()
    else:
        st.error(f"❌ Trello API Error: {resp.status_code}")
        return []

def add_card_to_list(list_id, task_name, task_desc=""):
    """Add a card to a given Trello list."""
    url = "https://api.trello.com/1/cards"
    query = {
        "key": TRELLO_KEY,
        "token": TRELLO_TOKEN,
        "idList": list_id,
        "name": task_name,
        "desc": task_desc,
    }
    resp = requests.post(url, params=query)
    return resp.status_code == 200

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Trello AI Task Assistant", layout="centered")
st.title("🤖 Trello AI Task Assistant")

st.write("Enter a high-level task and let AI break it down into subtasks. "
         "You can review and edit results before sending them to Trello.")

# Task input
task_input = st.text_area("Enter a task:", placeholder="e.g., Plan marketing campaign")

# --- Generate subtasks ---
if st.button("Generate Suggestions"):
    if not task_input.strip():
        st.warning("⚠️ Please enter a task first.")
    else:
        with st.spinner("AI is generating subtasks..."):
            try:
                result = nlp(
                    f"Break this task into 5 clear subtasks:\n{task_input}",
                    max_new_tokens=150,
                    do_sample=True
                )[0]['generated_text']

                # ✅ Clean up output
                subtasks = [line.strip("-•* ").strip() for line in result.split("\n") if line.strip()]

                # ✅ Save to session state
                st.session_state["ai_result"] = subtasks
                st.session_state["task_input"] = task_input

                st.success("✅ Subtasks generated!")

            except Exception as e:
                st.error(f"❌ AI error: {e}")

# --- Editable subtasks area ---
if "ai_result" in st.session_state:
    st.subheader("✏️ Review & Edit Subtasks")

    # Join list into editable text block
    editable_text = "\n".join(st.session_state["ai_result"])
    updated_text = st.text_area("Edit subtasks (one per line):", editable_text, height=200)

    # Save updated version back to session state
    st.session_state["ai_result"] = [line.strip() for line in updated_text.split("\n") if line.strip()]

# --- Trello Integration ---
if "ai_result" in st.session_state and st.session_state["ai_result"]:
    st.subheader("📌 Send to Trello")

    boards = get_trello_boards()
    if boards:
        board_map = {b["name"]: b["id"] for b in boards}
        board_choice = st.selectbox("Choose a board:", list(board_map.keys()))

        if board_choice:
            # Fetch lists for selected board
            lists_url = f"https://api.trello.com/1/boards/{board_map[board_choice]}/lists"
            query = {"key": TRELLO_KEY, "token": TRELLO_TOKEN}
            resp = requests.get(lists_url, params=query)

            if resp.status_code == 200:
                lists = resp.json()
                list_map = {l["name"]: l["id"] for l in lists}
                list_choice = st.selectbox("Choose a list:", list_map.keys())

                if st.button("Send Subtasks to Trello"):
                    subtasks = st.session_state["ai_result"]
                    success_count = 0
                    for sub in subtasks:
                        if sub:
                            if add_card_to_list(
                                list_map[list_choice],
                                sub,
                                f"From AI task assistant: {st.session_state['task_input']}"
                            ):
                                success_count += 1
                    st.success(f"✅ Sent {success_count} subtasks to Trello list: {list_choice}")
            else:
                st.error("❌ Could not fetch lists for this board")
