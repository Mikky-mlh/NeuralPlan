import streamlit as st
import pandas as pd

st.header("📅 Weekly Timetable")

# 1. Load Data from Memory
if 'schedule' not in st.session_state:
    st.warning("No schedule data found. Please restart the app.")
    st.stop()

df = st.session_state.schedule

# 2. The Interactive Table
st.info("💡 Tip: Tick the box in 'Status' or change it to 'Cancelled' to free up time.")

# We use the experimental data editor to let them edit directly
edited_df = st.data_editor(
    df,
    num_rows="dynamic",
    column_config={
        "Status": st.column_config.SelectboxColumn(
            "Class Status",
            help="Is the class active?",
            width="medium",
            options=["Active", "Cancelled"],
            required=True,
        )
    },
    hide_index=True,
)

# 3. Save Logic
if st.button("Update Schedule"):
    st.session_state.schedule = edited_df
    st.success("Schedule updated successfully!")
    
    # Check for cancellations
    cancelled_count = len(edited_df[edited_df["Status"] == "Cancelled"])
    if cancelled_count > 0:
        st.toast(f"You have {cancelled_count} cancelled classes. Go to Neural Coach!", icon="🧠")