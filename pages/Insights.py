import streamlit as st
import pandas as pd

st.header("📊 Productivity Insights")

# Mock Metrics (Teammate B will eventually make these real)
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Hours Recovered", value="4.5 hrs", delta="+1.5 hrs")

with col2:
    st.metric(label="Top Subject", value="Python")

with col3:
    st.metric(label="Study Streak", value="3 Days", delta="On Fire 🔥")

st.divider()

# Simple Chart
st.subheader("Time Utilization by Mood")
chart_data = pd.DataFrame({
    'Mood': ['Zombie', 'Focused', 'Beast Mode'],
    'Hours': [2, 5, 3]
})
st.bar_chart(chart_data, x='Mood', y='Hours')

st.info("This dashboard tracks how much 'dead time' you have successfully converted into learning.")