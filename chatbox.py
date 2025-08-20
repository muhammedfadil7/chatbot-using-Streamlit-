import streamlit as st
import pandas as pd
import os

# 🔵 Add background using custom CSS
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] > .main {
        background: linear-gradient(135deg, #e0f7fa, #fce4ec);
        background-attachment: fixed;
    }
    [data-testid="stHeader"] {
        background: transparent;
    }
    [data-testid="stSidebar"] {
        background: #f0f0f0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 🟢 Title and intro
st.title("Buddybot: friendly AI! 🤖")
st.write("Hey there! I'm Buddybot, your friendly AI companion. Let's get to know each other better — if you're bored just say 'stop' or 'bye'! 😊")

# 🔁 Questions to ask (20 total now)
questions = [
    ("day", "Hey there! How’s your day going?"),
    ("job", "Cool! Are you currently looking for a job opportunity?"),
    ("email", ""),  # Will update based on job response
    ("name", "By the way, what should I call you? 😊"),
    ("age", "Just curious — how old are you?"),
    ("hobby", "What do you enjoy doing in your free time?"),
    ("gender", "If you're comfortable, how do you identify your gender?"),
    ("city", "Where are you living currently?"),
    ("dream_job", "If you could do anything in the world, what would your dream job be?"),
    ("tech_interest", "Any tech tools or gadgets you're loving lately?"),
    ("travel", "Is there a place you've always wanted to visit? 🌍"),
    ("coffee_or_tea", "Quick one: coffee or tea? ☕🍵"),
    ("music", "What kind of music do you enjoy? 🎶"),
    ("movies", "Do you have a favorite movie or TV series? 🎬"),
    ("food", "What’s your favorite food? 🍕🍔🍝"),
    ("pets", "Do you have any pets, or would you like one? 🐶🐱"),
    ("sport", "Do you follow any sports or play any games? ⚽🏀"),
    ("learn", "Is there something new you’d like to learn this year? 📚"),
    ("superpower", "If you could have a superpower, what would it be? 🦸"),
    ("gratitude", "What’s one thing you’re grateful for today? 🙏"),
]

fields_to_save = ["name", "city", "age", "email"]

# 🔄 Session state init
if "messages" not in st.session_state:
    st.session_state.messages = []
if "step" not in st.session_state:
    st.session_state.step = 0
if "user_data" not in st.session_state:
    st.session_state.user_data = {}
if "asked_first" not in st.session_state:
    st.session_state.asked_first = False
if "data_saved" not in st.session_state:
    st.session_state.data_saved = False

# 💬 Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 🟡 Ask first question
if not st.session_state.asked_first:
    st.session_state.messages.append({
        "role": "assistant",
        "content": questions[0][1]
    })
    st.session_state.asked_first = True
    st.rerun()

# 🧠 Handle chat input
if prompt := st.chat_input("Your response here..."):
    if prompt.strip().lower() in ["bye", "stop"]:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Alright, have a nice day! 👋"
        })
        if not st.session_state.data_saved:
            row = {f: st.session_state.user_data.get(f, "") for f in fields_to_save}
            if any(row.values()):
                df = pd.DataFrame([row])
                file_exists = os.path.isfile("user_data.csv")
                df.to_csv("user_data.csv", mode="a", header=not file_exists, index=False)
                st.session_state.data_saved = True
        st.stop()

    step = st.session_state.step
    key, _ = questions[step]

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.user_data[key] = prompt
    st.session_state.step += 1

    # 🎯 Update email question after job
    if key == "job":
        if prompt.strip().lower() == "yes":
            questions[2] = ("email", "If you don’t mind sharing your email, I can let you know when companies are hiring.")
        else:
            questions[2] = ("email", "If you don’t mind sharing your email, I can reach out whenever you're looking for work.")

    # ✨ Compliment on name
    if key == "name":
        compliment = f"Hi {prompt}, what a lovely name you have! 😊"
        st.session_state.messages.append({"role": "assistant", "content": compliment})

    # ⏭ Ask next question or end
    if st.session_state.step < len(questions):
        _, next_q = questions[st.session_state.step]
        st.session_state.messages.append({"role": "assistant", "content": next_q})
    else:
        if not st.session_state.data_saved:
            row = {f: st.session_state.user_data.get(f, "") for f in fields_to_save}
            df = pd.DataFrame([row])
            file_exists = os.path.isfile("user_data.csv")
            df.to_csv("user_data.csv", mode="a", header=not file_exists, index=False)
            st.session_state.data_saved = True

        st.session_state.messages.append({
            "role": "assistant",
            "content": "Thanks for the chat! Wishing you a great day ahead. 😊"
        })

    st.rerun()
