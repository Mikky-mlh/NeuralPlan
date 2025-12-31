"""Historical data tracking - Shows all past productivity stats."""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.utils import minutes_to_hours
import datetime
import os

st.header("📈 Historical Data & Analytics")

# Load custom CSS
with open("assets/style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

with open("assets/data_page.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load historical data
history_file = "data/history.csv"

if os.path.exists(history_file):
    history_df = pd.read_csv(history_file)
    
    # Check if there's actual data
    if history_df.empty or len(history_df) == 0:
        st.info("📊 No historical data yet. Start tracking your productivity!")
        st.stop()
    
    history_df['Date'] = pd.to_datetime(history_df['Date'])
else:
    st.info("📊 No historical data yet. Start tracking your productivity!")
    st.stop()

# SUMMARY METRICS
total_time_saved = history_df['Time_Saved'].sum()
total_time_used = history_df['Time_Used'].sum()
total_days = len(history_df)
avg_efficiency = history_df['Efficiency'].mean()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card metric-total">
        <div class="metric-icon">📅</div>
        <div class="metric-content">
            <div class="metric-value">{total_days}</div>
            <div class="metric-label">Days Tracked</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card metric-saved">
        <div class="metric-icon">⏰</div>
        <div class="metric-content">
            <div class="metric-value">{minutes_to_hours(total_time_saved)}</div>
            <div class="metric-label">Total Time Saved</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card metric-used">
        <div class="metric-icon">🔥</div>
        <div class="metric-content">
            <div class="metric-value">{minutes_to_hours(total_time_used)}</div>
            <div class="metric-label">Time Actually Used</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card metric-efficiency">
        <div class="metric-icon">⚡</div>
        <div class="metric-content">
            <div class="metric-value">{int(avg_efficiency)}%</div>
            <div class="metric-label">Avg Efficiency</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# EFFICIENCY TREND CHART
st.subheader("📊 Efficiency Trend Over Time")
fig_line = px.line(
    history_df, 
    x='Date', 
    y='Efficiency',
    markers=True,
    title="Your Productivity Journey",
    labels={'Efficiency': 'Efficiency (%)', 'Date': 'Date'}
)
fig_line.update_traces(line_color='#667eea', marker=dict(size=10, color='#f093fb'))
fig_line.update_layout(hovermode='x unified')
st.plotly_chart(fig_line, use_container_width=True)

# TIME SAVED VS USED
st.subheader("⏱️ Time Saved vs Time Used")
fig_bar = go.Figure()
fig_bar.add_trace(go.Bar(
    x=history_df['Date'],
    y=history_df['Time_Saved'],
    name='Time Saved',
    marker_color='#3b8ed0'
))
fig_bar.add_trace(go.Bar(
    x=history_df['Date'],
    y=history_df['Time_Used'],
    name='Time Used',
    marker_color='#e05353'
))
fig_bar.update_layout(barmode='group', title="Daily Time Comparison (Minutes)")
st.plotly_chart(fig_bar, use_container_width=True)

# DETAILED TABLE
st.subheader("📋 Detailed History")
display_df = history_df.copy()
display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d')
display_df['Time_Saved'] = display_df['Time_Saved'].apply(lambda x: f"{int(x)} min")
display_df['Time_Used'] = display_df['Time_Used'].apply(lambda x: f"{int(x)} min")
display_df['Efficiency'] = display_df['Efficiency'].apply(lambda x: f"{int(x)}%")

st.dataframe(
    display_df,
    column_config={
        "Date": "Date",
        "Time_Saved": "Time Saved",
        "Time_Used": "Time Used",
        "Efficiency": "Efficiency",
        "Classes_Cancelled": "Classes Cancelled"
    },
    hide_index=True,
    use_container_width=True
)

# EXPORT OPTION
st.markdown("---")
if st.button("📥 Export Data as CSV"):
    csv = history_df.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"neuralplan_history_{datetime.date.today()}.csv",
        mime="text/csv"
    )
