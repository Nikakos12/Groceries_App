import streamlit as st

from agent import GroceryAgent

st.title("🤖 AI Assistant")

agent = GroceryAgent()


if "messages" not in st.session_state:
    st.session_state.messages = []


# Εμφάνιση προηγούμενων μηνυμάτων
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])


# Input χρήστη
question = st.chat_input(
    "Ρώτησε κάτι..."
)


if question:

    # Εμφάνιση ερώτησης
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.write(question)


    # Agent
    answer = agent.run(
        question,
        st.session_state.user_id
    )


    # Εμφάνιση απάντησης
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    with st.chat_message("assistant"):

        st.write(answer)