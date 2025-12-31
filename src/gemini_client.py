"""Gemini API client for generating adaptive study plans."""
import google.generativeai as genai
import streamlit as st
import pandas as pd
import io

# Helper function to configure the API
def configure_genai(api_key):
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        st.error(f"API Error: {e}")
        return False

# The Main Function to get the study plan
@st.cache_data(show_spinner=False, ttl=300)
def get_study_plan(subject, time_available, mood, _timestamp=None):
    """Generate a time-specific study plan tailored to the given subject, available minutes, and mood.
    
    Parameters:
        subject (str): Topic or course to study (e.g., "Calculus", "Organic Chemistry").
        time_available (int): Total available time in minutes to allocate across the plan.
        mood (str): One of the predefined emoji-labeled energy states influencing activity choice.
        _timestamp (float): Cache-busting parameter (ignored by function, forces fresh API call).
    
    Returns:
        dict: {"success": bool, "message": str}
    """
    # Collect all API keys
    keys = [st.secrets.get(f"GEMINI_API_KEY_{i}") for i in range(1, 10)]
    valid_keys = [k for k in keys if k]
    
    if not valid_keys:
        return {"success": False, "message": "⚠️ No API keys configured!"}
    
    # 2. Map mood to energy level
    mood_mapping = {
        "Zombie 🧟": "extremely low energy, can barely focus",
        "Tired 😴": "low energy, needs easy material",
        "Neutral 😐": "moderate energy, can handle normal difficulty",
        "Focused 🧘": "high energy, ready for challenging work",
        "Beast Mode 🦁": "peak performance, tackle hardest material"
    }
    
    energy_description = mood_mapping.get(mood, "moderate energy")
    
    # Determine tone based on mood
    if "Beast Mode" in mood:
        tone_instruction = "Use aggressive, high-pressure, 'no-excuses' language. Act like a drill sergeant."
    elif "Zombie" in mood or "Tired" in mood:
        tone_instruction = "Use very simple sentences and high encouragement. Be gentle."
    else:
        tone_instruction = "Use a helpful, clear, and motivating coaching tone."

    # 3. Sanitize inputs
    subject = str(subject)[:100]
    time_available = max(1, min(int(time_available), 480))
    mood = str(mood) if mood in mood_mapping else "Neutral 😐"
    
    # 4. The Prompt
    prompt = f"""You are a study coach helping a college student make the most of unexpected free time.

SITUATION:
- A class was cancelled, giving the student {time_available} minutes of free time
- They want to study: {subject}
- Current mental/physical state: {energy_description}

YOUR TASK:
Create a practical, time-specific study plan that matches their energy level.

TONE:
{tone_instruction}

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

DO NOT ASK ANY FOLLOW BACK QUESTION! BUT GIVE A PERSONALIZED MESSAGE!

Now create the plan:"""
    
    # 5. Try each API key until one works
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
    generation_config = {"max_output_tokens": 2048, "temperature": 0.7}
    
    last_error = None
    for api_key in valid_keys:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-flash-latest')
            response = model.generate_content(prompt, safety_settings=safety_settings, generation_config=generation_config)
            return {"success": True, "message": response.text}
        except Exception as e:
            last_error = str(e)
            if "429" not in last_error and "quota" not in last_error.lower():
                return {"success": False, "message": f"❌ Error: {last_error}\n\nTry again or check your internet connection."}
    
    error_msg = f"❌ All API keys exceeded rate limits. Last error: {last_error}" if last_error else "❌ All API keys exceeded rate limits."
    return {"success": False, "message": error_msg}


def list_available_models(api_key):
    """List all available Gemini models for the given API key.
    
    Parameters:
        api_key (str): Gemini API key
    
    Returns:
        dict: {"success": bool, "models": list or None, "error": str or None}
    """
    try:
        genai.configure(api_key=api_key)
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        return {"success": True, "models": models, "error": None}
    except Exception as e:
        return {"success": False, "models": None, "error": str(e)}

def parse_timetable_image(uploaded_file):
    """Uses Gemini to read a timetable image/PDF and convert it to structured DataFrame."""
    keys = [st.secrets.get(f"GEMINI_API_KEY_{i}") for i in range(1, 10)]
    valid_keys = [k for k in keys if k]
    
    if not valid_keys:
        st.error("⚠️ No API keys configured!")
        return None

    genai.configure(api_key=valid_keys[0])
    model = genai.GenerativeModel('gemini-flash-latest')

    bytes_data = uploaded_file.getvalue()
    
    prompt = """
    Analyze this image of a timetable. Extract all classes into CSV format.
    
    CRITICAL RULES:
    1. Columns: Day, Time, Subject, Duration
    2. Day: Monday, Tuesday, etc. (capitalized)
    3. Time: 12-hour format (10:00 AM, 2:00 PM)
    4. Duration: Minutes as integer (60, 90, 120)
    5. Subject: Course name exactly as shown
    6. RETURN ONLY CSV DATA. NO MARKDOWN. NO BACKTICKS. NO EXPLANATIONS.
    
    Example output:
    Day,Time,Subject,Duration
    Monday,10:00 AM,Calculus,60
    Monday,2:00 PM,Physics,90
    
    Now extract:
    """

    try:
        image_part = {"mime_type": uploaded_file.type, "data": bytes_data}
        response = model.generate_content([prompt, image_part])
        csv_data = response.text.strip()
        
        # Remove markdown artifacts
        csv_data = csv_data.replace("```csv", "").replace("```", "").strip()
        
        # Validate CSV structure before parsing
        if not csv_data.startswith("Day,Time,Subject,Duration"):
            st.error("❌ AI didn't return valid CSV format. Try a clearer image.")
            with st.expander("🔍 See what AI returned"):
                st.code(csv_data[:500])
            return None
        
        csv_io = io.StringIO(csv_data)
        df = pd.read_csv(csv_io)
        csv_io.close()
        
        # Validate columns
        required_cols = ["Day", "Time", "Subject", "Duration"]
        if not all(col in df.columns for col in required_cols):
            st.error(f"❌ Missing required columns. Expected: {required_cols}")
            return None
        
        # Validate data types
        if not pd.api.types.is_numeric_dtype(df["Duration"]):
            st.error("❌ Duration column must be numeric (minutes)")
            return None
        
        df["Status"] = "Active"
        st.success(f"✅ Extracted {len(df)} classes successfully!")
        return df
        
    except Exception as e:
        st.error(f"❌ Failed to parse timetable: {str(e)}")
        st.warning("💡 Tip: Use a clear, high-contrast image with legible text")
        return None
