"""Gemini API client for generating adaptive study plans."""
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
    api_key = st.secrets.get("GEMINI_API_KEY")
    
    if not api_key:
        return "⚠️ API Key not configured. Add GEMINI_API_KEY to .streamlit/secrets.toml"

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    
    # 2. Map mood to energy level
    mood_mapping = {
        "Zombie 🧟": "extremely low energy, can barely focus",
        "Tired 😴": "low energy, needs easy material",
        "Neutral 😐": "moderate energy, can handle normal difficulty",
        "Focused 🧘": "high energy, ready for challenging work",
        "Beast Mode 🦁": "peak performance, tackle hardest material"
    }
    
    energy_description = mood_mapping.get(mood, "moderate energy")
    
    # 3. The Prompt
    prompt = f"""You are a study coach helping a college student make the most of unexpected free time.

SITUATION:
- A class was cancelled, giving the student {time_available} minutes of free time
- They want to study: {subject}
- Current mental/physical state: {energy_description}

YOUR TASK:
Create a practical, time-specific study plan that matches their energy level.

RULES:
1. Break the plan into EXACTLY {time_available} minutes (e.g., "0-15 min: ...", "15-30 min: ...")
2. For low energy states: Suggest watching videos, reading summaries, reviewing notes (passive learning)
3. For high energy states: Suggest solving problems, writing code, practicing questions (active learning)
4. Be SPECIFIC: Name actual resources (Khan Academy, YouTube channels, specific topics to review)
5. Include a 5-minute break if time > 60 minutes
6. Format in Markdown with headers and bullet points

EXAMPLE OUTPUT STRUCTURE:
## Your {time_available}-Minute {subject} Study Sprint

**Given your energy level ({mood}), here's an optimized plan:**

### 📍 0-15 min: [Activity name]
- [Specific action 1]
- [Specific action 2]

[Continue for full duration]

Now create the plan:"""
    
    # 4. Call API
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error: {str(e)}\n\nTry again or check your internet connection."