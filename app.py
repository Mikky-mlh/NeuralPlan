import streamlit as st
import pandas as pd

# 1. Page Configuration (Must be the first command)
st.set_page_config(
    page_title="Neural Plan",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Session State Initialization (The Memory)
# We create these variables ONCE so they don't reset when switching pages.

if 'schedule' not in st.session_state:
    # Default dummy schedule for the hackathon demo
    data = {
        "Day": ["Monday", "Monday", "Monday", "Tuesday", "Tuesday"],
        "Time": ["10:00 AM", "11:00 AM", "02:00 PM", "09:00 AM", "01:00 PM"],
        "Subject": ["Data Structures", "Calculus II", "Python Lab", "Physics", "English"],
        "Status": ["Active", "Active", "Active", "Active", "Active"]
    }
    st.session_state.schedule = pd.DataFrame(data)

if 'user_name' not in st.session_state:
    st.session_state.user_name = "Student"

if 'generated_plan' not in st.session_state:
    st.session_state.generated_plan = None

# 3. Sidebar Global Settings
with st.sidebar:
    st.title("🧠 Neural Plan")
    st.write(f"Welcome, **{st.session_state.user_name}**")
    
    # Simple Reset Button for Debugging
    if st.button("Reset App Memory"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

# 4. Main Page Welcome
st.title("Welcome to Neural Plan 🚀")
st.markdown("""
### Turn Dead Time into Growth.
Navigate to the **Schedule** page to manage your classes, 
or go to **Neural Coach** to generate a study plan.
""")