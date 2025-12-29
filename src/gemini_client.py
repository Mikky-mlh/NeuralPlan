import google.generativeai as genai
import streamlit as st

# Helper function to configure the API
def configure_genai(api_key):
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        st.error(f"API Error: {e}")
        return False

# The Main Function to get the study plan
def get_study_plan(subject, time_available, mood):
    
    # 1. Initialize Model
    # Note: Ideally API Key is in st.secrets, but for hackathon, passed or hardcoded
    # REPLACE THIS WITH YOUR ACTUAL KEY IF NOT USING SECRETS
    api_key = "YOUR_API_KEY_HERE" 
    genai.configure(api_key=api_key)
    
    model = genai.GenerativeModel('gemini-pro')
    
    # 2. The Prompt (Teammate C's domain)
    prompt = f"""
    Act as a world-class student productivity coach.
    
    CONTEXT:
    - Subject: {subject}
    - Time Available: {time_available} minutes
    - Student's Neural State: {mood}
    
    TASK:
    Create a highly specific, bulleted study plan.
    
    GUIDELINES based on state:
    - If "Zombie/Tired": Focus on passive learning (videos), no heavy math.
    - If "Focused/Beast Mode": Focus on hard problems and active recall.
    
    FORMAT:
    Return pure Markdown. Use bold headers.
    """
    
    # 3. Call API
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error connecting to Neural Engine: {e}"