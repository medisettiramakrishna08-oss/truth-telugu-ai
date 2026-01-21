import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- పేజీ డిజైన్ ---
st.set_page_config(page_title="Truth Telugu AI Director", page_icon="🎬", layout="centered")

st.title("🎬 Image to Video Prompt AI")
st.write("ఒక ఫోటోను అప్‌లోడ్ చేయండి. ఈ AI దాన్ని చూసి సినిమాటిక్ వీడియో ప్రాంప్ట్ ఇస్తుంది.")

# --- సైడ్‌బార్ లో API Key ---
st.sidebar.header("🔑 Setup")
api_key = st.sidebar.text_input("Google Gemini API Key:", type="password")

if api_key:
    # API ని కాన్ఫిగర్ చేయడం
    genai.configure(api_key=api_key)
    
    # ఇమేజ్ అప్‌లోడ్ బాక్స్
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # ఇమేజ్ చూపించు
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # బటన్
        if st.button("Generate Video Prompt 🚀"):
            with st.spinner("AI ఫోటోను గమనిస్తోంది... (Analyzing)"):
                try:
                    # మోడల్ సెలక్షన్ (Gemini 1.5 Flash - ఇది ఫాస్ట్ & ఫ్రీ)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    # AI కి ఇచ్చే ఆర్డర్ (Prompt)
                    prompt = """
                    You are an expert AI Film Director. Analyze this image deeply.
                    Write a high-quality text prompt to generate a video from this image using AI tools like Runway Gen-2, Pika, or Sora.
                    
                    Include details about:
                    1. Subject Action (What is moving?)
                    2. Camera Angle & Movement (Drone shot, Zoom in, Pan right?)
                    3. Lighting & Atmosphere (Cinematic, Foggy, Golden Hour?)
                    4. Style (Photorealistic, 8k, Unreal Engine 5 render)

                    Give the output in English first, then provide a Telugu translation/explanation below it.
                    """
                    
                    # AI ని అడగడం
                    response = model.generate_content([prompt, image])
                    
                    # రిజల్ట్ చూపించడం
                    st.success("Done!")
                    st.subheader("🎥 Video Prompt:")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Error: {e}")
else:
    st.warning("👈 దయచేసి ఎడమ వైపున మీ Google API Key ఎంటర్ చేయండి.")