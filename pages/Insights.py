"""Insights dashboard - SIDDHIKA: Add more charts (pie/line), weekly trends, and export stats as PDF."""
import streamlit as st
import pandas as pd
import plotly.express as px
from src.utils import calculate_time_saved, minutes_to_hours
import datetime

st.header("📊 Accountability Tracker")

# Load custom CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if 'schedule' in st.session_state:
    df = st.session_state.schedule
    
    # Defensive check: if the table is empty or column is missing
    if df.empty or "Duration" not in df.columns or "Status" not in df.columns:
        st.warning("⚠️ Schedule is empty or invalid. Add some classes first!")
        st.stop()
    
    # Initialize Actual_Study column if it doesn't exist
    if "Actual_Study" not in df.columns:
        df["Actual_Study"] = 0
        st.session_state.schedule = df
    
    # Filter for only CANCELLED classes (the ones we are recovering)
    cancelled_mask = df["Status"] == "Cancelled"
    cancelled_df = df[cancelled_mask].copy()
    
    if cancelled_df.empty:
        st.info("No cancelled classes to track yet. Go to Schedule and free up some time!")
    else:
        # 1. THE LOGGING INTERFACE 📝
        st.subheader("📝 Log Your Study Session")
        st.caption("Be honest. How much of the cancelled time did you actually use?")
        
        # We allow editing ONLY the 'Actual_Study' column
        edited_df = st.data_editor(
            cancelled_df[["Day", "Time", "Subject", "Duration", "Actual_Study"]],
            column_config={
                "Duration": st.column_config.NumberColumn("Goal (Min)", disabled=True),
                "Actual_Study": st.column_config.NumberColumn(
                    "Actual Work (Min)", 
                    min_value=0, 
                    max_value=180, 
                    step=5,
                    help="How many minutes did you actually study?"
                )
            },
            hide_index=True,
            use_container_width=True,
            key="study_logger"
        )
        
        # 2. SAVE LOGIC 💾
        if st.button("Save Progress"):
            # Update the main session state with these new values
            st.session_state.schedule.update(edited_df)
            
            # Save to daily state file so it persists on refresh
            current_date = str(datetime.date.today())
            st.session_state.schedule["Date"] = current_date
            st.session_state.schedule.to_csv("data/daily_state.csv", index=False)
            
            st.success("Progress logged! Checking your stats...")
            st.rerun()

        # 3. THE ANALYTICS (PLANNED VS ACTUAL) 📈
        st.markdown("---")
        st.subheader("⚡ Reality Check: Goal vs. Execution")
        
        # Prepare data for Plotly
        chart_data = edited_df.melt(
            id_vars=["Subject"], 
            value_vars=["Duration", "Actual_Study"], 
            var_name="Type", 
            value_name="Minutes"
        )
        
        # Rename for clarity in legend
        chart_data["Type"] = chart_data["Type"].replace({
            "Duration": "Goal Time 🎯", 
            "Actual_Study": "Actual Work 🔥"
        })

        # Generate the comparison chart
        fig = px.bar(
            chart_data, 
            x="Subject", 
            y="Minutes", 
            color="Type", 
            barmode="group",
            text_auto=True,
            color_discrete_map={"Goal Time 🎯": "#3b8ed0", "Actual Work 🔥": "#e05353"},
            title="Are you hitting your targets?",
            labels={"Minutes": "Minutes", "Subject": "Subject"}
        )
        fig.update_yaxes(title_text="Minutes")
        st.plotly_chart(fig, use_container_width=True)

        # 4. TOTAL EFFICIENCY SCORE
        total_goal = cancelled_df["Duration"].sum()
        total_actual = edited_df["Actual_Study"].sum()
        
        if total_goal > 0:
            efficiency = int((total_actual / total_goal) * 100)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Goal Time", minutes_to_hours(total_goal))
            col2.metric("Actual Time", minutes_to_hours(total_actual))
            col3.metric("Efficiency", f"{efficiency}%", delta=f"{efficiency-100}%")
            
            if efficiency == 0:
                st.error("💀 Zero effort detected. You wasted all your free time!")
            elif efficiency < 25:
                st.error("🚨 Critical failure! Less than 25% efficiency. Stop procrastinating!")
            elif efficiency < 50:
                st.warning(f"⚠️ You're slacking! Only {efficiency}% efficiency. Lock in.")
            elif efficiency < 75:
                st.info(f"📈 Decent effort at {efficiency}%, but there's room to improve.")
            elif efficiency < 100:
                st.success(f"💪 Strong performance! {efficiency}% efficiency. Almost perfect!")
            elif efficiency == 100:
                st.balloons()
                st.success("🎯 PERFECT! 100% efficiency. You hit every target!")
            else:
                st.balloons()
                st.success(f"🔥 OVERACHIEVER! {efficiency}% efficiency. You exceeded your goals!")
else:
    st.warning("No schedule data found. Go to Schedule page first.")