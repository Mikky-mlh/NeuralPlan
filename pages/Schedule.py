"""
Schedule management page - SOURABH: Add CSV upload, better UI styling, and Duration column validation.
Make THIS work. Don't change the logic. You can change colors if you want, but the table must work.
"""
import streamlit as st
import pandas as pd
from src.gemini_client import parse_timetable_image

st.header("📅 My Class Schedule")

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load schedule from CSV
if 'schedule' not in st.session_state:
    st.session_state.schedule = pd.read_csv("data/default_schedule.csv")

# 1. The "Neural Import" Section
with st.expander("📤 Upload New Timetable (PDF/Image)"):
    uploaded_file = st.file_uploader("Drop your timetable here", type=['png', 'jpg', 'jpeg', 'pdf'])
    
    if uploaded_file is not None:
        if st.button("Analyze & Import"):
            with st.spinner("Neural Vision is reading your schedule..."):
                new_df = parse_timetable_image(uploaded_file)
                
                if new_df is not None and not new_df.empty:
                    # Save it as the new permanent user schedule
                    new_df.to_csv("data/user_schedule.csv", index=False)
                    
                    # Update session state immediately
                    st.session_state.schedule = new_df
                    st.success("Timetable updated! The AI has learned your new schedule.")
                    st.rerun()

# Initialize Actual_Study column if it doesn't exist
if "Actual_Study" not in st.session_state.schedule.columns:
    st.session_state.schedule["Actual_Study"] = 0

# Show editable table with validation
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
        )
    }
)

# Save button
if st.button("Save Daily Status"):
    # 1. Update Session State
    st.session_state.schedule = edited
    
    # 2. Save to Disk (So it remembers if they close the tab but stays within the same day)
    # We ensure the Date column is set to today so app.py accepts it later
    import datetime
    edited["Date"] = str(datetime.date.today())
    edited.to_csv("data/daily_state.csv", index=False)
    
    cancelled = len(edited[edited["Status"] == "Cancelled"])
    if cancelled > 0:
        st.success(f"✅ Saved! {cancelled} classes cancelled for TODAY. Resets at midnight.")
    else:
        st.info("✅ Daily status saved. All classes active.")