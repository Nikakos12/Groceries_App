import streamlit as st
from database import get_or_create_user

if "user_id" not in st.session_state:
    st.session_state.user_id = None

st.set_page_config(page_title="Grocery App", page_icon="🛒")

if not st.user.is_logged_in:

    st.title("🛒 Grocery App")

    st.write("Please sign in with your Google account to continue.")

    if st.button("Sign in with Google"):
        st.login("google")

else:

    if st.session_state.user_id is None:

        st.session_state.user_id = get_or_create_user(
            google_id=st.user.sub,
            email=st.user.email,
            full_name=st.user.name
        )

    groceries = st.Page(
        "pages/groceries_app.py",
        title="Groceries"
    )

    ai = st.Page(
        "pages/AI_Agent.py",
        title="AI Assistant"
    )

    pg = st.navigation([groceries, ai])

    pg.run()