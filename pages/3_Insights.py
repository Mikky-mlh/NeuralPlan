import streamlit as st
import pandas as pd
import plotly.express as px
from src.utils import minutes_to_hours
from src.logo_helper import get_logo_html
import datetime
import os

# Sidebar with logo
with st.sidebar:
    st.markdown(get_logo_html(), unsafe_allow_html=True)

st.header("📊 Accountability Tracker")

# Sample data notice
st.info("ℹ️ **Note:** The data shown is sample data for demonstration. Upload your own schedule in the [Schedule](Schedule) page to replace it with your actual timetable.")

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
    
    # Initialize Custom_Subject column if it doesn't exist
    if "Custom_Subject" not in df.columns:
        df["Custom_Subject"] = ""
        st.session_state.schedule = df
    else:
        # Ensure Custom_Subject is string type to prevent data_editor errors
        df["Custom_Subject"] = df["Custom_Subject"].fillna("").astype(str)
    
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
            cancelled_df[["Day", "Time", "Subject", "Duration", "Actual_Study", "Custom_Subject"]],
            column_config={
                "Duration": st.column_config.NumberColumn("Goal (Min)", disabled=True),
                "Subject": st.column_config.TextColumn("Planned Subject", disabled=True),
                "Actual_Study": st.column_config.NumberColumn(
                    "Actual Work (Min)", 
                    min_value=0, 
                    max_value=180, 
                    step=5,
                    help="How many minutes did you actually study?"
                ),
                "Custom_Subject": st.column_config.TextColumn(
                    "What Did You Study?",
                    help="Leave blank if you studied the planned subject, or enter what you actually studied"
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
            st.session_state.schedule.to_csv("data/daily_state.csv", index=False)
            
            # Save to historical data
            history_file = "data/history.csv"
            today = datetime.date.today()
            
            time_saved = cancelled_df["Duration"].sum()
            time_used = edited_df["Actual_Study"].sum()
            efficiency = int((time_used / time_saved * 100)) if time_saved > 0 else 0
            classes_cancelled = len(cancelled_df)
            
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
                    history_df.loc[history_df['Date'] == today, ['Time_Saved', 'Time_Used', 'Efficiency', 'Classes_Cancelled']] = [time_saved, time_used, efficiency, classes_cancelled]
                else:
                    history_df = pd.concat([history_df, new_entry], ignore_index=True)
            else:
                history_df = new_entry
            
            history_df.to_csv(history_file, index=False)
            st.success("Progress logged! Checking your stats...")
            st.rerun()

        # 3. THE ANALYTICS (PLANNED VS ACTUAL) 📈
        st.markdown("---")
        st.subheader("⚡ Reality Check: Goal vs. Execution")
        
        # Create display subject (show custom if filled, otherwise original)
        display_df = edited_df.copy()
        display_df["Display_Subject"] = display_df.apply(
            lambda row: f"{row['Custom_Subject']} ⭐" if row['Custom_Subject'] else row['Subject'],
            axis=1
        )
        
        # Prepare data for Plotly
        chart_data = display_df.melt(
            id_vars=["Display_Subject"],
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
            x="Display_Subject", 
            y="Minutes", 
            color="Type", 
            barmode="group",
            text_auto=True,
            color_discrete_map={"Goal Time 🎯": "#3b8ed0", "Actual Work 🔥": "#e05353"},
            title="Are you hitting your targets?",
            labels={"Minutes": "Minutes", "Display_Subject": "Subject"}
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
                st.components.v1.html("""
                <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
                <script>
                confetti({
                    particleCount: 100,
                    spread: 70,
                    origin: { y: 0.6 }
                });
                </script>
                """, height=0)
                st.success("🎯 PERFECT! 100% efficiency. You hit every target!")
            else:
                st.balloons()
                st.success(f"🔥 OVERACHIEVER! {efficiency}% efficiency. You exceeded your goals!")

    # --- HISTORY SECTION ---
    st.markdown("---")
    st.subheader("📅 Your Long-Term Growth")

    history_file = "data/history.csv"
    if os.path.exists(history_file):
        hist_df = pd.read_csv(history_file)
        
        if not hist_df.empty:
            hist_df['Date'] = pd.to_datetime(hist_df['Date'])
            
            # Filter for last 7 days
            cutoff_date = pd.to_datetime('today').normalize() - pd.Timedelta(days=7)
            hist_df = hist_df[hist_df['Date'] >= cutoff_date].sort_values('Date')
            
            metric = st.radio(
                "Select Trend:", 
                ["Efficiency %", "Time Saved vs. Used"], 
                horizontal=True
            )
            
            if metric == "Efficiency %":
                fig_hist = px.line(
                    hist_df, 
                    x="Date", 
                    y="Efficiency", 
                    markers=True,
                    title="Efficiency Trend (Last 7 Days)",
                    template="plotly_dark",
                    line_shape="spline"
                )
                fig_hist.add_hline(y=50, line_dash="dash", line_color="red", annotation_text="Goal Threshold")
                fig_hist.update_traces(line_color="#00FF00", line_width=3)
                fig_hist.update_yaxes(range=[0, 110], title_text="Efficiency (%)")
                fig_hist.update_xaxes(title_text="Date")
            else:
                fig_hist = px.bar(
                    hist_df, 
                    x="Date", 
                    y=["Time_Saved", "Time_Used"],
                    barmode="group",
                    title="Minutes Saved vs. Actually Studied",
                    template="plotly_dark",
                    color_discrete_map={"Time_Saved": "#3b8ed0", "Time_Used": "#e05353"}
                )

            st.plotly_chart(fig_hist, use_container_width=True)
            
            total_saved_all_time = hist_df["Time_Saved"].sum()
            total_used_all_time = hist_df["Time_Used"].sum()
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Lifetime Hours Recovered", minutes_to_hours(total_saved_all_time))
            m2.metric("Lifetime Hours Studied", minutes_to_hours(total_used_all_time))
            m3.metric("Avg Efficiency", f"{int(hist_df['Efficiency'].mean())}%")
        else:
            st.info("No history data found yet. Start using the app to build your streak!")
    else:
        st.info("History file missing.")

else:
    st.warning("No schedule data found. Go to Schedule page first.")