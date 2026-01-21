import streamlit as st
import requests
from PIL import Image
import io

# --- పేజీ డిజైన్ ---
st.set_page_config(page_title="Truth Telugu AI Director", page_icon="🎬", layout="centered")
st.title("🎬 Image to Video Prompt (Hugging Face)")
st.write("Google లేకుండా, Hugging Face ఉచిత API ద్వారా ఇది పనిచేస్తుంది.")

# --- సైడ్‌బార్ ---
st.sidebar.header("🔑 Setup")
api_key = st.sidebar.text_input("Hugging Face Access Token:", type="password")
st.sidebar.info("HuggingFace.co -> Settings -> Access Tokens నుండి కీ తెచ్చుకోండి.")

# --- API సెటప్ (LLaVA Model - Vision) ---
# ఇది ఉచితంగా ఇమేజ్‌ని చూసి వర్ణించే మోడల్
API_URL = "https://api-inference.huggingface.co/models/llava-hf/llava-1.5-7b-hf"

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
            with st.spinner("AI ఫోటోను లోడ్ చేస్తోంది (ఇది కొంచెం టైం తీసుకోవచ్చు)..."):
                try:
                    # ఇమేజ్‌ని API కి పంపడానికి మార్చడం
                    import base64
                    img_byte_arr = io.BytesIO()
                    image.save(img_byte_arr, format=image.format)
                    img_byte_arr = img_byte_arr.getvalue()
                    img_str = base64.b64encode(img_byte_arr).decode()

                    # AI కి పంపే సందేశం
                    prompt_text = "USER: <image>\nDescribe this image in extreme detail for a cinematic video. Include camera angles, lighting, and movement.\nASSISTANT:"
                    
                    # API కాల్ చేయడం
                    output = query({
                        "inputs": prompt_text,
                        "image": img_str,
                        "parameters": {"max_new_tokens": 200} 
                    }, api_key)

                    # ఎర్రర్ చెకింగ్
                    if isinstance(output, dict) and "error" in output:
                        st.error(f"Error: {output['error']}")
                        st.warning("Hugging Face ఫ్రీ మోడల్స్ అప్పుడప్పుడు బిజీగా ఉంటాయి. దయచేసి 1 నిమిషం ఆగి మళ్ళీ ట్రై చేయండి.")
                    else:
                        # రిజల్ట్ చూపించడం
                        generated_text = output[0]['generated_text']
                        # అనవసరమైన టెక్స్ట్ తీసేయడం
                        clean_text = generated_text.replace(prompt_text, "").replace("USER:", "").strip()
                        
                        st.success("Done!")
                        st.subheader("🎥 Video Prompt:")
                        st.write(clean_text)
                        
                except Exception as e:
                    st.error(f"System Error: {e}")
else:
    st.warning("👈 దయచేసి ఎడమ వైపున మీ Hugging Face Token ఎంటర్ చేయండి.")
