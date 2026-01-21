import streamlit as st
from huggingface_hub import InferenceClient
from PIL import Image

# --- పేజీ డిజైన్ ---
st.set_page_config(page_title="Truth Telugu AI Director", page_icon="🎬", layout="centered")
st.title("🎬 Image to Video Prompt (Official)")
st.write("Stable Version using Hugging Face Official Client.")

# --- సైడ్‌బార్ ---
st.sidebar.header("🔑 Setup")
api_key = st.sidebar.text_input("Hugging Face Access Token:", type="password")
st.sidebar.info("Settings -> Access Tokens నుండి 'Write' పర్మిషన్ ఉన్న టోకెన్ వాడండి.")

if api_key:
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # ఇమేజ్ చూపించు
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        if st.button("Generate Prompt 🚀"):
            with st.spinner("AI ఆలోచిస్తోంది... (Connecting via Official Client)"):
                try:
                    # అఫీషియల్ క్లయింట్ సెటప్
                    client = InferenceClient(token=api_key)

                    # మోడల్: LLaVA (ఇమేజ్ గురించి చెప్పే బెస్ట్ ఫ్రీ మోడల్)
                    # ఇది ఇమేజ్‌ని చూసి మనం అడిగిన దానికి సమాధానం ఇస్తుంది
                    model_id = "llava-hf/llava-1.5-7b-hf"

                    # AI కి పంపాల్సిన ప్రశ్న
                    prompt = "USER: <image>\nDescribe this image in great detail for a cinematic video generation prompt. Mention the movement, camera angle, and lighting.\nASSISTANT:"
                    
                    # ఇమేజ్‌ని టెక్స్ట్‌గా మార్చే ప్రాసెస్
                    # stream=False అంటే మొత్తం ఆన్సర్ ఒకేసారి ఇస్తుంది
                    response = client.text_generation(
                        prompt, 
                        model=model_id, 
                        max_new_tokens=250, 
                        stream=False,
                        # ఇమేజ్‌ని డైరెక్ట్‌గా పంపిస్తున్నాం (మునుపటిలా base64 అవసరం లేదు)
                        images=[image] 
                    )

                    # రిజల్ట్ చూపించు
                    # కొన్నిసార్లు రిజల్ట్ లో మన ప్రశ్న కూడా కలిసి వస్తుంది, దాన్ని క్లీన్ చేస్తున్నాం
                    final_answer = response.replace("USER: <image>", "").replace(prompt, "").strip()
                    
                    st.success("Success!")
                    st.subheader("🎥 Video Prompt:")
                    st.write(final_answer)

                except Exception as e:
                    # ఎర్రర్ వస్తే క్లియర్ గా చూపిస్తుంది
                    st.error(f"Error: {e}")
                    st.warning("ఒకవేళ 'Model is loading' అని వస్తే, దయచేసి 30 సెకన్లు ఆగి మళ్ళీ బటన్ నొక్కండి.")
else:
    st.warning("👈 దయచేసి ఎడమ వైపున మీ Hugging Face Token ఎంటర్ చేయండి.")
