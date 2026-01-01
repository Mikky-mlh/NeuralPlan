import streamlit as st
import pandas as pd
import datetime
from streamlit_lottie import st_lottie
import json
from src.gemini_client import parse_timetable_image
import os

with open("assets/style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

with open("assets/stylesh.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Lottie Animation
with open("assets/animation.json", encoding="utf-8") as f:
    lottie_animation = json.load(f)

# Load schedule from CSV
if 'schedule' not in st.session_state:
    try:
        st.session_state.schedule = pd.read_csv("data/default_schedule.csv")
    except FileNotFoundError:
        st.error("Default schedule file not found. Please check data/default_schedule.csv")
        st.stop()

# Remove Date column if it exists
if "Date" in st.session_state.schedule.columns:
    st.session_state.schedule = st.session_state.schedule.drop(columns=["Date"])

# Initialize Actual_Study column if it doesn't exist
if "Actual_Study" not in st.session_state.schedule.columns:
    st.session_state.schedule["Actual_Study"] = 0

# Initialize Custom_Subject column if it doesn't exist
if "Custom_Subject" not in st.session_state.schedule.columns:
    st.session_state.schedule["Custom_Subject"] = ""

# HERO SECTION
import datetime
current_date = datetime.date.today().strftime("%A, %B %d, %Y")
current_time = datetime.datetime.now().strftime("%I:%M %p")

st.markdown(f"""
<div class="hero-section">
    <div class="hero-content">
        <div class="hero-icon-wrapper">
            <span class="hero-icon">📅</span>
        </div>
        <h1 class="hero-title">My Class Schedule</h1>
        <p class="hero-subtitle">Smart Time Management</p>
        <div class="hero-date-badge">
            <span class="date-icon">📆</span>
            <span class="date-text">{current_date}</span>
            <span class="time-divider">•</span>
            <span class="time-icon">🕐</span>
            <span class="time-text">{current_time}</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# METRICS DASHBOARD
total_classes = len(st.session_state.schedule)
active_classes = len(st.session_state.schedule[st.session_state.schedule["Status"] == "Active"])
cancelled_classes = len(st.session_state.schedule[st.session_state.schedule["Status"] == "Cancelled"])
free_time = st.session_state.schedule[st.session_state.schedule["Status"] == "Cancelled"]["Duration"].sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card metric-total">
        <div class="metric-icon">📚</div>
        <div class="metric-content">
            <div class="metric-value">{total_classes}</div>
            <div class="metric-label">Total Classes</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card metric-active">
        <div class="metric-icon">✓</div>
        <div class="metric-content">
            <div class="metric-value">{active_classes}</div>
            <div class="metric-label">Active Classes</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card metric-cancelled">
        <div class="metric-icon">✗</div>
        <div class="metric-content">
            <div class="metric-value">{cancelled_classes}</div>
            <div class="metric-label">Cancelled</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card metric-time">
        <div class="metric-icon">⏱️</div>
        <div class="metric-content">
            <div class="metric-value">{free_time}</div>
            <div class="metric-label">Free Minutes</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# UPLOAD SECTION
with st.expander("📤 Upload New Timetable (PDF/Image)"):
    st.markdown("""
    <div class="upload-instructions">
        <p>🎯 <strong>Quick Import:</strong> Upload your timetable image or PDF</p>
        <p>🤖 <strong>AI-Powered:</strong> Neural Vision will automatically extract your schedule</p>
    </div>
    """, unsafe_allow_html=True)
    
    st_lottie(lottie_animation, height=150, key="upload")
    
    uploaded_file = st.file_uploader("Drop your timetable here", type=['png', 'jpg', 'jpeg', 'pdf'])
    
    if uploaded_file is not None:
        if st.button("Analyze & Import"):
            with st.spinner("Neural Vision is reading your schedule..."):
                new_df = parse_timetable_image(uploaded_file)
                
                if new_df is not None and not new_df.empty:
                    new_df.to_csv("data/user_schedule.csv", index=False)
                    st.session_state.schedule = new_df
                    st.success("Timetable updated! The AI has learned your new schedule.")
                    st.rerun()

# STATUS LEGEND
st.markdown("""
<div class="status-legend">
    <span class="legend-title">Status Guide:</span>
    <span class="status-badge status-active">● Active</span>
    <span class="status-badge status-cancelled">● Cancelled</span>
</div>
""", unsafe_allow_html=True)

# TABLE SECTION
st.markdown("""
<div class="table-header">
    <h3>📊 Schedule Editor</h3>
    <p class="table-subtitle">Click any cell to edit • Changes are saved when you click Save</p>
</div>
""", unsafe_allow_html=True)

edited = st.data_editor(
    st.session_state.schedule,
    column_config={
        "Duration": st.column_config.NumberColumn(
            "Duration",
            format="%d min",
            min_value=1,
            max_value=480
        ),
        "Status": st.column_config.SelectboxColumn(
            options=["Active", "Cancelled"]
        ),
        "Actual_Study": st.column_config.NumberColumn(
            "Actual Study (Min)",
            min_value=0,
            max_value=480,
            step=5,
            help="How many minutes did you actually study?"
        ),
        "Custom_Subject": st.column_config.TextColumn(
            "What You Studied",
            help="If you studied something different, enter it here"
        )
    },
    use_container_width=True,
    hide_index=True
)

st.markdown(f"<p class='last-updated'>Last updated: {datetime.datetime.now().strftime('%I:%M %p')}</p>", unsafe_allow_html=True)

# SAVE BUTTON
st.markdown("<br>", unsafe_allow_html=True)
if st.button("💾 Save Daily Status", use_container_width=True):
    st.session_state.schedule = edited
    edited.to_csv("data/daily_state.csv", index=False)
    
    # Save to historical data
    history_file = "data/history.csv"
    today = datetime.date.today()
    
    cancelled = edited[edited["Status"] == "Cancelled"]
    time_saved = cancelled["Duration"].sum()
    time_used = cancelled["Actual_Study"].sum()
    efficiency = int((time_used / time_saved * 100)) if time_saved > 0 else 0
    classes_cancelled = len(cancelled)
    
    # Create new history entry
    new_entry = pd.DataFrame([{
        'Date': today,
        'Time_Saved': time_saved,
        'Time_Used': time_used,
        'Efficiency': efficiency,
        'Classes_Cancelled': classes_cancelled
    }])
    
    # Append to history
    if os.path.exists(history_file):
        history_df = pd.read_csv(history_file)
        history_df['Date'] = pd.to_datetime(history_df['Date']).dt.date
        
        # Update today's entry if exists, otherwise append
        if today in history_df['Date'].values:
            mask = history_df['Date'] == today
            history_df.loc[mask, 'Time_Saved'] = time_saved
            history_df.loc[mask, 'Time_Used'] = time_used
            history_df.loc[mask, 'Efficiency'] = efficiency
            history_df.loc[mask, 'Classes_Cancelled'] = classes_cancelled
        else:
            history_df = pd.concat([history_df, new_entry], ignore_index=True)
    else:
        history_df = new_entry
    
    history_df.to_csv(history_file, index=False)
    
    cancelled_count = len(cancelled)
    if cancelled_count > 0:
        st.success(f"✅ Saved! {cancelled_count} classes cancelled for TODAY. Resets at midnight.")
    else:
        st.info("✅ Daily status saved. All classes active.")