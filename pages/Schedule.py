"""
Schedule management page - SOURABH: Add CSV upload, better UI styling, and Duration column validation.
Make THIS work. Don't change the logic. You can change colors if you want, but the table must work.
"""
import streamlit as st
import pandas as pd

st.header("📅 My Class Schedule")

# Hardcode a simple schedule for demo
if 'schedule' not in st.session_state:
    st.session_state.schedule = pd.DataFrame({
        "Day": ["Monday", "Monday", "Tuesday"],
        "Time": ["10:00 AM", "2:00 PM", "9:00 AM"],
        "Subject": ["Math", "Python", "Physics"],
        "Duration": [60, 90, 60],
        "Status": ["Active", "Active", "Active"]
    })

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
        )
    }
)

# Save button
if st.button("Save Changes"):
    st.session_state.schedule = edited
    cancelled = len(edited[edited["Status"] == "Cancelled"])
    if cancelled > 0:
        st.success(f"✅ {cancelled} classes cancelled. Go to Neural Coach!")
    else:
        st.info("All classes active.")