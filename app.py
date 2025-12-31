"""Main app entry point - Handles session state and global config."""
import streamlit as st
import pandas as pd
import os
import datetime

# 1. Page Configuration
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

# 2. Daily Reset Check (Fixes midnight reset bug)
def check_daily_reset():
    """Resets daily state when date changes."""
    today = datetime.date.today()
    
    if 'last_reset_date' not in st.session_state:
        st.session_state.last_reset_date = today
    
    if st.session_state.last_reset_date != today:
        daily_file = "data/daily_state.csv"
        if os.path.exists(daily_file):
            os.remove(daily_file)
        
        if 'schedule' in st.session_state:
            del st.session_state.schedule
        
        st.session_state.last_reset_date = today
        st.rerun()

check_daily_reset()

# 3. Session State Initialization (The Memory)
# We create these variables ONCE so they don't reset when switching pages.

if 'schedule' not in st.session_state:
    daily_file = "data/daily_state.csv"
    master_file = "data/user_schedule.csv"
    default_file = "data/default_schedule.csv"
    
    # LOGIC: Try to load today's existing progress
    if os.path.exists(daily_file):
        st.session_state.schedule = pd.read_csv(daily_file)
    elif os.path.exists(master_file):
        df = pd.read_csv(master_file)
        df["Status"] = "Active"
        df["Actual_Study"] = 0
        df["Custom_Subject"] = ""
        st.session_state.schedule = df
    else:
        df = pd.read_csv(default_file)
        df["Status"] = "Active"
        df["Actual_Study"] = 0
        df["Custom_Subject"] = ""
        st.session_state.schedule = df
    
    # Remove Date column if it exists
    if "Date" in st.session_state.schedule.columns:
        st.session_state.schedule = st.session_state.schedule.drop(columns=["Date"])

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
st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h1 style="font-size: 3.5rem; margin-bottom: 0.5rem;">🧠 Neural Plan</h1>
    <p style="font-size: 1.3rem; color: #9aa0a6; margin-bottom: 3rem;">Turn Dead Time into Growth</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("""
    ### 🎯 What is Neural Plan?
    
    **Neural Plan** is an AI-driven productivity engine that transforms unexpected free time into personalized learning sprints. 
    When classes get cancelled, don't waste those precious minutes—let our AI coach create a custom study plan matched to your energy level.
    
    ### ⚡ Key Features
    
    - **📅 Smart Schedule Management**: Track your classes and instantly identify free time
    - **🤖 AI-Powered Study Plans**: Get personalized plans using Google's Gemini AI
    - **🎭 Neural State Matching**: Plans adapt to your mood (Zombie 🧟 to Beast Mode 🦁)
    - **📊 Accountability Tracking**: Log actual study time vs. planned time
    - **🔍 Vision AI**: Upload timetable images—AI extracts your schedule automatically
    
    ### 🚀 How to Use
    
    **Step 1: Set Your Schedule** 📋  
    Go to **Schedule** page → Upload your timetable image OR manually edit the table → Save
    
    **Step 2: Mark Cancelled Classes** ❌  
    When a class gets cancelled → Change status to "Cancelled" → Save Daily Status
    
    **Step 3: Get Your AI Plan** 🧠  
    Go to **Neural Coach** → Select subject & time available → Choose your energy level → Generate Plan
    
    **Step 4: Track Progress** 📈  
    Go to **Insights** → Log actual study minutes → See your efficiency score
    
    ### 💡 Pro Tips
    
    - Be honest with your Neural State—better plans come from accurate energy levels
    - The app resets daily at midnight, so cancelled classes become active again
    - Use "Beast Mode" for your hardest subjects when you're most alert
    - Track your actual study time to build accountability
    
    ---
    
    **Ready to stop wasting cancelled class time?** 👉 Start with the **Schedule** page!
    """)

with col2:
    if lottie_animation:
        st_lottie(lottie_animation, height=300, key="welcome")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(46, 49, 146, 0.2), rgba(255, 140, 66, 0.2)); 
                border-radius: 16px; padding: 1.5rem; margin-top: 2rem; border: 1px solid rgba(255, 255, 255, 0.1);">
        <h4 style="color: #FF8C42; margin-bottom: 1rem;">📊 Quick Stats</h4>
        <p style="margin: 0.5rem 0;">✓ AI-Powered Study Plans</p>
        <p style="margin: 0.5rem 0;">✓ 5 Energy Level Modes</p>
        <p style="margin: 0.5rem 0;">✓ Vision AI Timetable Parser</p>
        <p style="margin: 0.5rem 0;">✓ Real-Time Progress Tracking</p>
    </div>
    
    <div style="background: linear-gradient(135deg, rgba(39, 174, 96, 0.2), rgba(16, 185, 129, 0.2)); 
                border-radius: 16px; padding: 1.5rem; margin-top: 1.5rem; border: 1px solid rgba(255, 255, 255, 0.1);">
        <h4 style="color: #27AE60; margin-bottom: 1rem;">🎓 Perfect For</h4>
        <p style="margin: 0.5rem 0;">• College Students</p>
        <p style="margin: 0.5rem 0;">• Self-Learners</p>
        <p style="margin: 0.5rem 0;">• Anyone with unpredictable schedules</p>
    </div>
    """, unsafe_allow_html=True)