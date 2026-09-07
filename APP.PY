import streamlit as st
from google import genai

# పేజీ టైటిల్ మరియు ఐకాన్ డిజైన్
st.set_page_config(
    page_title="DWARAKA AI - ద్వారకా అసిస్టెంట్", 
    page_icon="🖤", 
    layout="centered"
)

# మెయిన్ హెడ్డింగ్ వద్ద బ్లాక్ బ్యాక్‌గ్రౌండ్ తరహాలో DWARAKA పేరు కనిపించేలా డిజైన్
st.markdown("""
    <div style="background-color: #000000; padding: 15px; border-radius: 12px; text-align: center; margin-bottom: 20px;">
        <h1 style="color: #FFFFFF; font-family: sans-serif; letter-spacing: 3px; margin: 0;">DWARAKA</h1>
        <p style="color: #00FFCC; font-size: 14px; margin-top: 5px; margin-bottom: 0;">🤖 ద్వారకా AI అసిస్టెంట్ 🤖</p>
    </div>
""", unsafe_allow_html=True)

# API Key చెక్ చేయడం
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    st.error("API Key కనుగొనబడలేదు! Streamlit Secrets లో GEMINI_API_KEY జోడించండి.")
    st.stop()

client = genai.Client(api_key=api_key)

# చాట్ హిస్టరీ
if "messages" not in st.session_state:
    st.session_state.messages = []

# పాత చాట్ చూపించడం
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# యూజర్ ప్రశ్న తీసుకోవడం
if prompt := st.chat_input("ద్వారకా, నన్ను ఏదైనా అడగండి..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # ద్వారకా AI రెస్పాన్స్
    with st.chat_message("assistant"):
        system_instruction = "You are 'Dwaraka AI Assistant', a highly intelligent, fast, and polite personal AI assistant built for Dwaraka. Always address the user respectfully and answer accurately in the exact language they speak."
        full_prompt = f"{system_instruction}\n\nUser Question: {prompt}"
        
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=full_prompt,
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
