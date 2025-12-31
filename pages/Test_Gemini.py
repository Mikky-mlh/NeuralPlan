import streamlit as st
from src import gemini_client

st.header("🧪 Gemini API Test")

st.write("This page tests if your API key works and Gemini returns good responses.")

if st.button("Test API Connection"):
    with st.spinner("Calling Gemini..."):
        result = gemini_client.get_study_plan(
            subject="Data Structures",
            time_available=60,
            mood="Neutral 😐"
        )
        
        if "⚠️" in result or "❌" in result:
            st.error("API call failed!")
            st.code(result)
        else:
            st.success("✅ Gemini is working!")
            st.markdown(result)

st.markdown("---")
st.subheader("🔍 Debugging")
st.write("If you see a 404 error, check which models are available to your API key.")
if st.button("List Available Models"):
    if "GEMINI_API_KEY" in st.secrets:
        import google.generativeai as genai
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            st.success(f"Found {len(models)} models.")
            st.code(models)
        except Exception as e:
            st.error(f"Error listing models: {e}")
    else:
        st.error("⚠️ GEMINI_API_KEY not found in secrets.toml")
