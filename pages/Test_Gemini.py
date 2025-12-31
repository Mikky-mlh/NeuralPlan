import streamlit as st
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src import gemini_client  # pylint: disable=import-error
import google.generativeai as genai

st.header("🧪 Gemini API Test")

st.write("This page tests if your API key works and Gemini returns good responses.")

if st.button("Test API Connection"):
    with st.spinner("Calling Gemini..."):
        test_plan = gemini_client.get_study_plan(
            subject="Data Structures",
            time_available=60,
            mood="Neutral 😐"
        )
        
        if "⚠️" in test_plan or "❌" in test_plan:
            st.error("API call failed!")
            st.code(test_plan)
        else:
            st.success("✅ Gemini is working!")
            st.markdown(test_plan)

st.markdown("---")
st.subheader("🔍 Debugging")
st.write("If you see a 404 error, check which models are available to your API key.")
if st.button("List Available Models"):
    try:
        if "GEMINI_API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            st.success(f"Found {len(models)} models.")
            st.code(models)
        else:
            st.error("⚠️ GEMINI_API_KEY not found in secrets.toml")
    except Exception as e:
        st.error(f"Error listing models: {e}")