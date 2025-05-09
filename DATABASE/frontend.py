from streamlit_card import card
from samplejson import product_dict
import streamlit as st

st.title("📋 Manager Output")

# Session state to hold edited text
if "vision_text" not in st.session_state:
    st.session_state.vision_text = product_dict["vision"]
    print("helllo✅✅⭐")
    print(st.session_state.vision_text)
def custom_click_handler():
    st.session_state.edit_mode = True

# Maintain edit mode flag in session state
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False

# Display card
clicked = card(
    title="Vision",
    text=st.session_state.vision_text,
    image="https://www.spacex.com/static/images/share.jpg",
    url=None,
    on_click=custom_click_handler,
    styles={
        "card": {
            "background-color": "#0b0c10",
            "border": "2px solid #45a29e",
            "border-radius": "15px",
            "box-shadow": "0 4px 12px rgba(0, 255, 255, 0.3)",
        },
        "text": {
            "color": "#66fcf1",
            "font-size": "16px",
            "text-align": "center",
        }
    },
    key="vision_card"
)

# If clicked or edit mode enabled, show editable text
if clicked or st.session_state.edit_mode:
    new_text = st.text_area("✏️ Edit Vision", st.session_state.vision_text, height=150)
    if st.button("💾 Save"):
        st.session_state.vision_text = new_text
        st.session_state.edit_mode = False
        st.success("Vision updated!")

        card(
            title="Vision",
            text=st.session_state.vision_text,
            image="https://www.spacex.com/static/images/share.jpg",
            url=None,
            on_click=custom_click_handler,
            styles={
                "card": {
                    "background-color": "#0b0c10",
                    "border": "2px solid #45a29e",
                    "border-radius": "15px",
                    "box-shadow": "0 4px 12px rgba(0, 255, 255, 0.3)",
                },
                "text": {
                    "color": "#66fcf1",
                    "font-size": "16px",
                    "text-align": "center",
                }
            },
            key="vision_card2"
        )