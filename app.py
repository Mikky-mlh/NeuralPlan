"""Entry point - manages session state and daily resets"""
import streamlit as st
import pandas as pd
import datetime
import os
from src.logo_helper import get_logo_html

# Page config
st.set_page_config(
    page_title="Neural Plan",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Particle.js background
st.components.v1.html("""
<script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
<div id="particles-js" style="position: fixed; width: 100%; height: 100%; top: 0; left: 0; z-index: -1;"></div>
<script>
particlesJS('particles-js', {
    particles: {
        number: { value: 50, density: { enable: true, value_area: 800 } },
        color: { value: '#2E3192' },
        shape: { type: 'circle' },
        opacity: { value: 0.3, random: true },
        size: { value: 3, random: true },
        move: { enable: true, speed: 1, direction: 'none', out_mode: 'out' }
    }
});
</script>
""", height=0)

# Lottie Animation
from streamlit_lottie import st_lottie
import json

with open("assets/animation.json") as f:
    lottie_animation = json.load(f)

# Daily reset logic - clears progress at midnight
def check_daily_reset():
    """Wipes daily state when date changes"""
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

# Session state - persists across page navigation

if 'schedule' not in st.session_state:
    daily_file = "data/daily_state.csv"
    master_file = "data/user_schedule.csv"
    default_file = "data/default_schedule.csv"
    
    # Load today's progress if it exists
    if os.path.exists(daily_file):
        st.session_state.schedule = pd.read_csv(daily_file)
        # Fix type conflicts in data editor
        if "Custom_Subject" in st.session_state.schedule.columns:
            st.session_state.schedule["Custom_Subject"] = st.session_state.schedule["Custom_Subject"].fillna("").astype(str)
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

# Sidebar
with st.sidebar:

    st.markdown(get_logo_html(), unsafe_allow_html=True)
    
    st.title("🧠 Neural Plan")
    st.write(f"Welcome, **{st.session_state.user_name}**")
    

    if st.button("🔄 Restore Sample Data"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
            

        if os.path.exists("data/user_schedule.csv"):
            os.remove("data/user_schedule.csv")
            
        # Generate sample history
        today = datetime.date.today()
        history_data = [
            {"Date": today - datetime.timedelta(days=1), "Time_Saved": 60, "Time_Used": 60, "Efficiency": 100, "Classes_Cancelled": 1},
            {"Date": today - datetime.timedelta(days=2), "Time_Saved": 120, "Time_Used": 90, "Efficiency": 75, "Classes_Cancelled": 2},
            {"Date": today - datetime.timedelta(days=3), "Time_Saved": 60, "Time_Used": 20, "Efficiency": 33, "Classes_Cancelled": 1},
            {"Date": today - datetime.timedelta(days=4), "Time_Saved": 90, "Time_Used": 90, "Efficiency": 100, "Classes_Cancelled": 1},
            {"Date": today - datetime.timedelta(days=5), "Time_Saved": 180, "Time_Used": 150, "Efficiency": 83, "Classes_Cancelled": 3},
        ]
        pd.DataFrame(history_data).to_csv("data/history.csv", index=False)
        
        # Generate sample daily state
        if os.path.exists("data/default_schedule.csv"):
            df = pd.read_csv("data/default_schedule.csv")
            if len(df) > 0:
                df.at[0, "Status"] = "Cancelled"
                df.at[0, "Actual_Study"] = 45
                df.at[0, "Custom_Subject"] = "AI Research"
            df.to_csv("data/daily_state.csv", index=False)
            
        st.rerun()

# Main page
st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h1 style="font-size: 3.5rem; margin-bottom: 0.5rem;">🧠 Neural Plan</h1>
    <p style="font-size: 1.3rem; color: #9aa0a6; margin-bottom: 3rem;">AI-Powered Study Planner for Cancelled Classes</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("""
    ### 🎯 What is Neural Plan?
    
    **Neural Plan** transforms wasted time from cancelled classes into productive study sessions using AI.
    
    > ℹ️ **First-time user?** The schedule you see is sample data. Go to the [Schedule](Schedule) page to upload your own timetable.
    
    ### ⚡ Core Features
    
    - **📅 Schedule Management**: Track your weekly class schedule
    - **🤖 AI Study Plans**: Get personalized plans from Google Gemini AI
    - **🎭 Mood-Adaptive**: Plans match your energy (Zombie 🧟 → Beast Mode 🦁)
    - **📊 Progress Tracking**: Monitor actual vs. planned study time
    - **🔍 Vision AI**: Upload timetable images for automatic extraction
    
    ### 🚀 Quick Start Guide
    
    **1. Setup Your Schedule** 📋  
    Navigate to [Schedule](Schedule) → Upload timetable image OR manually edit → Click Save
    
    **2. Mark Cancelled Classes** ❌  
    When class is cancelled → Change status to "Cancelled" in [Schedule](Schedule) → Save Daily Status
    
    **3. Generate AI Study Plan** 🧠  
    Go to [Neural Coach](Neural_Coach) → Select subject & duration → Pick energy level → Generate
    
    **4. Track Your Progress** 📈  
    Visit [Insights](Insights) → Log actual study time → View efficiency metrics
    
    ### 💡 Best Practices
    
    - **Be honest** with your energy level for better AI recommendations
    - **Daily reset** at midnight restores all classes to active status
    - **Use Beast Mode** for challenging subjects when you're most alert
    - **Track consistently** to build accountability and see trends
    
    ---
    
    **Ready to maximize your free time?** 👉 Start with the [Schedule](Schedule) page or check the [Guide](Guide) for detailed instructions!
    """)

with col2:
    st_lottie(lottie_animation, height=300, key="welcome")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(46, 49, 146, 0.2), rgba(255, 140, 66, 0.2)); 
                border-radius: 16px; padding: 1.5rem; margin-top: 2rem; border: 1px solid rgba(255, 255, 255, 0.1);">
        <h4 style="color: #FF8C42; margin-bottom: 1rem;">📊 App Capabilities</h4>
        <p style="margin: 0.5rem 0;">✓ Google Gemini AI Integration</p>
        <p style="margin: 0.5rem 0;">✓ 5 Energy-Based Study Modes</p>
        <p style="margin: 0.5rem 0;">✓ Vision AI Timetable Parser</p>
        <p style="margin: 0.5rem 0;">✓ Real-Time Progress Analytics</p>
    </div>
    
    <div style="background: linear-gradient(135deg, rgba(39, 174, 96, 0.2), rgba(16, 185, 129, 0.2)); 
                border-radius: 16px; padding: 1.5rem; margin-top: 1.5rem; border: 1px solid rgba(255, 255, 255, 0.1);">
        <h4 style="color: #27AE60; margin-bottom: 1rem;">🎓 Ideal For</h4>
        <p style="margin: 0.5rem 0;">• College & University Students</p>
        <p style="margin: 0.5rem 0;">• Self-Directed Learners</p>
        <p style="margin: 0.5rem 0;">• Anyone with Variable Schedules</p>
    </div>
    """, unsafe_allow_html=True)