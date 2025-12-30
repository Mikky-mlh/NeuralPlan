"""Insights dashboard - SIDHIKA: Add more charts (pie/line), weekly trends, and export stats as PDF."""
import streamlit as st
import pandas as pd
from src.utils import calculate_time_saved, minutes_to_hours

st.header("📊 Your Productivity Stats")

# Get schedule from session state
if 'schedule' in st.session_state:
    df = st.session_state.schedule
    cancelled_classes = df[df["Status"] == "Cancelled"]
    
    # Calculate metrics using utils.py functions
    time_saved = calculate_time_saved(df)
    time_saved_formatted = minutes_to_hours(time_saved)
    
    # Show metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Time Recovered", time_saved_formatted)
    
    with col2:
        cancelled_count = len(cancelled_classes)
        st.metric("Classes Cancelled", cancelled_count)
    
    with col3:
        active_count = len(df[df["Status"] == "Active"])
        st.metric("Classes Active", active_count)
    
    # Show chart only if there are cancelled classes
    if not cancelled_classes.empty:
        st.subheader("Schedule Overview")
        status_counts = df["Status"].value_counts()
        st.bar_chart(status_counts)
    else:
        st.success("🎉 All classes are active! Keep up the great work!")
    
else:
    st.warning("No schedule data found. Go to Schedule page first.")