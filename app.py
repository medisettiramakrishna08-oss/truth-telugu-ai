import streamlit as st
import requests
from PIL import Image
import io
import base64

# --- పేజీ డిజైన్ ---
st.set_page_config(page_title="Truth Telugu AI Director", page_icon="🎬", layout="centered")
st.title("🎬 Image to Video Prompt (Hugging Face)")
st.write("Updated for new Hugging Face Router API.")

# --- సైడ్‌బార్ ---
st.sidebar.header("🔑 Setup")
api_key = st.sidebar.text_input("Hugging Face Access Token:", type="password")
st.sidebar.info("Get token from: HuggingFace.co -> Settings -> Access Tokens")

# --- API సెటప్ (Updated URL) ---
# గమనిక: ఇక్కడ పాత లింక్ మార్చి కొత్త 'router' లింక్ పెట్టాము
API_URL = "https://router.huggingface.co/hf-inference/models/llava-hf/llava-1.5-7b-hf"

def query(payload, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

if api_key:
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # ఇమేజ్ చూపించు
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        if st.button("Generate Prompt 🚀"):
            with st.spinner("AI ఫోటోను ప్రాసెస్ చేస్తోంది..."):
                try:
                    # ఇమేజ్‌ని Base64 లోకి మార్చడం
                    img_byte_arr = io.BytesIO()
                    image.save(img_byte_arr, format=image.format)
                    img_byte_arr = img_byte_arr.getvalue()
                    img_str = base64.b64encode(img_byte_arr).decode()

                    # LLaVA మోడల్ కోసం ఇన్‌పుట్ ఫార్మాట్
                    # LLaVA కి టెక్స్ట్ మరియు ఇమేజ్ కలిపి పంపాలి
                    prompt_text = "USER: <image>\nDescribe this image in detail for a cinematic video creation. Include lighting, camera angles, and action.\nASSISTANT:"
                    
                    payload = {
                        "inputs": prompt_text,
                        "image": img_str,
                        "parameters": {"max_new_tokens": 200}
                    }

                    # API కాల్ చేయడం
                    output = query(payload, api_key)

                    # ఎర్రర్ చెకింగ్
                    if isinstance(output, dict) and "error" in output:
                        st.error(f"Error form Hugging Face: {output['error']}")
                        st.info("Tip: ఫ్రీ మోడల్ కాబట్టి కొన్నిసార్లు 'Loading' అని వస్తుంది. ఒక 30 సెకన్లు ఆగి మళ్ళీ ట్రై చేయండి.")
                    
                    elif isinstance(output, list) and len(output) > 0:
                        # రిజల్ట్ చూపించడం
                        generated_text = output[0]['generated_text']
                        # క్లీన్ చేయడం
                        clean_text = generated_text.replace(prompt_text, "").replace("USER:", "").strip()
                        
                        st.success("Done!")
                        st.subheader("🎥 Video Prompt:")
                        st.write(clean_text)
                    else:
                        st.warning("Unexpected response format. Try again.")
                        st.write(output) # డీబగ్గింగ్ కోసం
                        
                except Exception as e:
                    st.error(f"System Error: {e}")
else:
    st.warning("👈 దయచేసి ఎడమ వైపున మీ Hugging Face Token ఎంటర్ చేయండి.")
