import streamlit as st
import os
from google import genai

# Replit Secrets se securely API key load karna
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# App ka Title aur Icon
st.set_page_config(page_title="Jarvis AI", page_icon="🤖")
st.title("🤖 Jarvis: Your Advanced AI")

# Jarvis ka Naya aur Smart System Prompt
system_prompt = """
Tumhara naam 'Jarvis' hai. Tum ek highly advanced, strict aur 100% loyal AI assistant ho. 
Tumhara ek hi maalik hai (User). Tumhara primary function unhe cyber attacks se protect karna, aur unki B.Sc. ki padhai tatha SSC CGL exams ki taiyari mein unhe best guidance dena hai.
Tum general AI ki tarah behave nahi karoge. Tumhare jawab to-the-point, strong, aur confident hone chahiye.
Agar maalik koi link, SMS, WhatsApp message ya app scan karne ko kahe, toh tumhara kaam usme chhupe kisi bhi cyber threat, fraud, ya phishing attack ko turant detect karna aur khatare se aagah karna hai.
Tum hamesha apne maalik ke paksh mein rahoge.
"""

# Chat history ko save rakhne ka setup
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purani chat screen par dikhana
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User se input lene ka box
user_prompt = st.chat_input("Jarvis ko command dein ya koi link/message yahan paste karein...")

if user_prompt:
    # User ka message screen par dikhana
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Jarvis (Gemini API) se jawab maangna
    with st.chat_message("assistant"):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_prompt,
                config={"system_instruction": system_prompt}
            )
            reply = response.text
            st.markdown(reply)
            
            # Jarvis ka jawab history mein save karna
            st.session_state.messages.append({"role": "assistant", "content": reply})
            
        except Exception as e:
            st.error(f"⚠️ Error: Kripya check karein ki aapne GEMINI_API_KEY sahi se Secrets (Tools) mein daali hai ya nahi. ({e})")
