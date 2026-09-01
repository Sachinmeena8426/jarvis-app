import streamlit as st
import os
import requests
from bs4 import BeautifulSoup
import re
from google import genai
from gtts import gTTS
from PIL import Image

# API Key load karna
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

# App ka Title
st.set_page_config(page_title="Jarvis AI", page_icon="🤖")
st.title("🤖 Jarvis: Advanced AI (with Internet)")

# Jarvis ki Personality
system_prompt = """Tum ek bahut hi smart aur friendly AI assistant ho jiska naam Jarvis hai. 
Tumhe hamesha Hinglish mein baat karni hai. Tumhara main kaam user ki B.Sc ki padhai aur SSC CGL ki taiyari mein unhe guide karna hai. 
Agar user koi photo bheje ya website ka link de, toh usko dhyan se padh kar clear aur point-wise notes banane hain."""

# --- NAYA FUNCTION: Website padhne ke liye ---
def read_website(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        return text[:4000] # Zyada lambi website se app hang na ho isliye limit
    except:
        return "Error: Website padhne mein problem aayi."

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

uploaded_file = st.file_uploader("📸 Padhai ke notes ya book ki photo upload karein", type=["jpg", "jpeg", "png"])

# User ka naya message lena
prompt = st.chat_input("Jarvis ko command dein, photo bhejein, ya koi Website Link paste karein...")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        try:
            final_prompt = system_prompt + "\n\nUser: " + prompt
            
            # Agar prompt mein koi Website Link (URL) hai
            url_match = re.search(r'(https?://\S+)', prompt)
            if url_match:
                url = url_match.group(0)
                st.info(f"🌐 Jarvis is website ko padh raha hai: {url} ...")
                website_text = read_website(url)
                final_prompt += f"\n\nWebsite ka content yeh hai: {website_text}\nAb iske basis par user ke sawal ka jawab do."

            # Agar photo bheji hai
            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                st.image(image, caption="Aapki photo", use_container_width=True)
                contents = [image, final_prompt]
            else:
                contents = [final_prompt]
            
            # Gemini se jawab lena
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=contents,
            )
            ai_reply = response.text
            st.markdown(ai_reply)
            
            # Awaaz (Audio)
            tts = gTTS(text=ai_reply, lang='hi')
            tts.save("reply.mp3")
            audio_file = open("reply.mp3", "rb")
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/mp3')
            
        except Exception as e:
            st.error("Kuch technical problem aayi, kripya dobara try karein.")
            ai_reply = "Sorry, thodi problem aayi."
            
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                
