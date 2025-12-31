import streamlit as st
from src import gemini_client

# ---- session state initialization ----
if "generated_plan" not in st.session_state:
    st.session_state.generated_plan = None

st.header("🧠 Neural Coach")

# 1. Check for Free Time
if 'schedule' in st.session_state:
    df = st.session_state.schedule
    cancelled_classes = df[df["Status"] == "Cancelled"]
    
    if cancelled_classes.empty:
        st.info("You have no cancelled classes right now. Great work!")
    else:
        st.success(f"Opportunity Detected: {len(cancelled_classes)} cancelled slots found.")
        
        # 2. Subject Selection
        subject_options = list(cancelled_classes["Subject"].unique()) + ["🤖 Let AI Decide", "✏️ Custom Subject"]
        subject_choice = st.selectbox("Select Subject to Recover", subject_options)
        
        # Handle custom subject input
        if subject_choice == "✏️ Custom Subject":
            subject = st.text_input("Enter your subject/topic:", placeholder="e.g., Guitar Practice, Reading, Coding")
            max_time = 180  # Default max for custom subjects
        elif subject_choice == "🤖 Let AI Decide":
            subject = "AI will suggest the most productive activity"
            max_time = 180  # Default max for AI choice
        else:
            subject = subject_choice
            # Get the duration of the selected subject
            max_time = int(cancelled_classes[cancelled_classes["Subject"] == subject]["Duration"].iloc[0])
        
        # 3. Input Form
        with st.form("neural_form"):
            time = st.slider("Time Available (minutes)", 15, max_time, min(60, max_time), step=15)
            
            # The Mood Selector (Crucial Feature)
            mood = st.select_slider(
                "Select your Neural State (Energy Level)",
                options=["Zombie 🧟", "Tired 😴", "Neutral 😐", "Focused 🧘", "Beast Mode 🦁"],
                value="Neutral 😐"
            )
            
            submitted = st.form_submit_button("Generate Adaptive Plan 🚀")
            
            if submitted:
                if subject_choice == "✏️ Custom Subject" and not subject:
                    st.error("Please enter a subject/topic!")
                else:
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