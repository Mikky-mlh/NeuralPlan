"""Main app entry point - YUVRAJ: Handles session state and global config."""
import streamlit as st
import pandas as pd
import os
import datetime

# 1. Page Configuration (Must be the first command)
st.set_page_config(
    page_title="Neural Plan",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Lottie Animation
try:
    from streamlit_lottie import st_lottie
    import json
    
    with open("assets/animation.json") as f:
        lottie_animation = json.load(f)
except:
    lottie_animation = None

# 2. Session State Initialization (The Memory)
# We create these variables ONCE so they don't reset when switching pages.

if 'schedule' not in st.session_state:
    current_date = str(datetime.date.today()) # e.g., "2023-10-27"
    daily_file = "data/daily_state.csv"
    master_file = "data/user_schedule.csv"
    default_file = "data/default_schedule.csv"
    
    # LOGIC: Try to load today's existing progress
    loaded = False
    if os.path.exists(daily_file):
        df_daily = pd.read_csv(daily_file)
        # Check if the file belongs to TODAY
        if "Date" in df_daily.columns and df_daily["Date"].iloc[0] == current_date:
            st.session_state.schedule = df_daily
            loaded = True
    
    # If not loaded (file missing OR date mismatch -> It's a new day!), load fresh
    if not loaded:
        # Prefer user's master schedule, fallback to default
        if os.path.exists(master_file):
            df = pd.read_csv(master_file)
        else:
            df = pd.read_csv(default_file)
        
        # FORCE RESET FOR THE NEW DAY
        df["Status"] = "Active"       # Un-cancel everything
        df["Date"] = current_date     # Stamp it with today's date
        df["Actual_Study"] = 0        # Initialize with 0 minutes
        
        st.session_state.schedule = df

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
col1, col2 = st.columns([2, 1])

with col1:
    st.title("Welcome to Neural Plan 🚀")
    st.markdown("""
    ### Turn Dead Time into Growth.
    Navigate to the **Schedule** page to manage your classes,
    or go to **Neural Coach** to generate a study plan.
    """)

with col2:
    if lottie_animation:
        st_lottie(lottie_animation, height=250, key="welcome")