import streamlit as st
from src import gemini_client
from src.logo_helper import get_logo_html


with st.sidebar:
    st.markdown(get_logo_html(), unsafe_allow_html=True)


with open("assets/neural_coach.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.header("🧠 Neural Coach")


st.info("ℹ️ **Note:** Currently using sample schedule data. Upload your own timetable in the [Schedule](Schedule) page for personalized study plans.")

# Check for cancelled classes
if 'schedule' in st.session_state:
    df = st.session_state.schedule
    cancelled_classes = df[df["Status"] == "Cancelled"]
    
    if cancelled_classes.empty:
        st.info("You have no cancelled classes right now. Go to [Schedule](Schedule) to mark cancelled classes, then return here to generate study plans!")
    else:
        st.success(f"Opportunity Detected: {len(cancelled_classes)} cancelled slots found.")
        
        # Subject selection
        subject_options = list(cancelled_classes["Subject"].unique()) + ["🤖 Let AI Decide", "✏️ Custom Subject"]
        subject_choice = st.selectbox("Select Subject to Recover", subject_options)
        
        # Handle custom input
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
        
        # Focus topic input
        focus_topic = st.text_input(
            "🎯 What specific part do you want to master?",
            placeholder="e.g., 'Recursion', 'Chapter 4', 'Binary Search Trees', or leave blank for general overview",
            help="Be specific! This helps the AI create a surgical, targeted plan instead of generic advice."
        )
        
        # Confidence slider
        confidence = st.slider(
            "💪 How well do you already know this subject?",
            1, 10, 5,
            help="1 = Complete beginner | 10 = Expert level"
        )
        
        # Input form
        with st.form("neural_form"):
            time_minutes = st.slider("Time Available (minutes)", 15, max_time, min(60, max_time), step=15)
            
            # Energy selector - core feature
            mood = st.select_slider(
                "Select your Neural State (Energy Level)",
                options=["Low Battery 😴", "Power Saving 😐", "Normal Mode 🙂", "Neural Sync 🧘", "Beast Mode 🦁"],
                value="Normal Mode 🙂"
            )
            
            submitted = st.form_submit_button("Generate Adaptive Plan 🚀")
            
            if submitted:
                if subject_choice == "✏️ Custom Subject" and not subject:
                    st.error("Please enter a subject/topic!")
                else:
                    with st.spinner("🧠 Synthesizing Neural Pathways... Consulting AI Brain..."):
                        import time as time_module
                        # Call AI
                        result = gemini_client.get_study_plan(subject, time_minutes, mood, focus_topic, confidence, _timestamp=time_module.time())
                        st.session_state.generated_plan = result
                        st.rerun()

# Display results
if st.session_state.generated_plan:
    st.markdown("---")
    
    result = st.session_state.generated_plan
    if result["success"]:
        # Header
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown("""
            <h2 style="color: #FF8C42; font-size: 2rem; font-weight: 800; margin-bottom: 0;">
                ✨ Your Personalized Study Plan
            </h2>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("Clear Plan 🗑️"):
                st.session_state.generated_plan = None
                st.rerun()
        
        # Styled container
        st.markdown("""
        <div style="
            background: linear-gradient(145deg, rgba(46, 49, 146, 0.15), rgba(255, 140, 66, 0.1));
            backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 2.5rem;
            border: 2px solid rgba(255, 140, 66, 0.3);
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1);
            margin-top: 1.5rem;
        ">
        <div style="
            background: rgba(255, 140, 66, 0.1);
            border-left: 4px solid #FF8C42;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
        ">
            <p style="margin: 0; color: #E8EAED; font-size: 0.95rem;">
                🎯 <strong>Pro Tip:</strong> Follow this plan step-by-step for maximum productivity. Take breaks as suggested to maintain focus.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(result["message"])
        
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.error(result["message"])