import streamlit as st


def build_sidebar():

    with st.sidebar:

        st.title("💰 Finance Tracker")

        st.write(
            f"Welcome,\n\n**{st.session_state['name']}**"
        )

        st.divider()

        st.success("Track • Save • Grow")

        st.divider()

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            st.session_state.clear()

            st.switch_page("pages/Login.py")