"""Neural Coach page - YUVRAJ: Handles AI study plan generation based on mood and free time."""
import streamlit as st
from src import gemini_client

st.header("🧠 Neural Coach")

# 1. Check for Free Time
if 'schedule' in st.session_state:
    df = st.session_state.schedule
    cancelled_classes = df[df["Status"] == "Cancelled"]
    
    if cancelled_classes.empty:
        st.info("You have no cancelled classes right now. Great work!")
    else:
        st.success(f"Opportunity Detected: {len(cancelled_classes)} cancelled slots found.")
        
        # 2. Input Form
        with st.form("neural_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                # Dropdown only shows the subjects that are actually cancelled
                subject = st.selectbox("Select Subject to Recover", cancelled_classes["Subject"].unique())
            
            with col2:
                time = st.slider("Time Available (minutes)", 15, 120, 60, step=15)
            
            # The Mood Selector (Crucial Feature)
            mood = st.select_slider(
                "Select your Neural State (Energy Level)",
                options=["Zombie 🧟", "Tired 😴", "Neutral 😐", "Focused 🧘", "Beast Mode 🦁"],
                value="Neutral 😐"
            )
            
            submitted = st.form_submit_button("Generate Adaptive Plan 🚀")
            
            if submitted:
                with st.spinner("Synthesizing optimal study path..."):
                    # Call the AI function from src/gemini_client.py
                    result = gemini_client.get_study_plan(subject, time, mood)
                    st.session_state.generated_plan = result
                    st.rerun()

# 3. Display Results
if st.session_state.generated_plan:
    st.markdown("---")
    
    col1, col2 = st.columns([4, 1])
    with col1:
        st.subheader("Your Adaptive Study Plan")
    with col2:
        if st.button("Clear Plan 🗑️"):
            st.session_state.generated_plan = None
            st.rerun()
            
    with st.container():
        result = st.session_state.generated_plan
        if result["success"]:
            st.markdown(result["message"])
        else:
            st.error(result["message"])