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
        
        if result["success"]:
            st.success("✅ Gemini is working!")
            st.markdown(result["message"])
        else:
            st.error("API call failed!")
            st.code(result["message"])

st.markdown("---")
st.subheader("🔍 Debugging")
st.write("If you see a 404 error, check which models are available to your API key.")
if st.button("List Available Models"):
    if "GEMINI_API_KEY" in st.secrets:
        result = gemini_client.list_available_models(st.secrets["GEMINI_API_KEY"])
        if result["success"]:
            st.success(f"Found {len(result['models'])} models.")
            st.code(result["models"])
        else:
            st.error(f"Error listing models: {result['error']}")
    else:
        st.error("⚠️ GEMINI_API_KEY not found in secrets.toml")