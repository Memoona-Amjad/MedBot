import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
import base64

load_dotenv()
def decode_api_key(encoded_api_key):
    decoded_bytes = base64.b64decode(encoded_api_key.encode('utf-8'))
    decoded_str = str(decoded_bytes, 'utf-8')
    return decoded_str

st.set_page_config(
    page_title="Medical Advisor",
    page_icon=":hospital:", 
    layout="centered",  
)


gen_ai.configure(api_key = decode_api_key("QUl6YVN5QXpvdTdPZjh3ckhfaU84QUtVLV9mRzZYUmVFUVNHcFYw") )

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

system_message_options = {
    "Symptom-Based Diagnosis": """You are a Doctor with 30 years of experience. Users will describe their symptoms.
    You must provide accurate diagnoses, prescribe medications(name of medicine,weight and dosage) and tests if needed., suggest bed rest or dietary changes,
    and offer health advice based on the given symptoms. DO NOT mention that you are an AI and can't prescribe medicines.
    recommend near by hosptials and details if asked.
    If any question asked other than medical, say 'I donot have any information.' """,
    "General Medical Consultation": """You are a knowledgeable general practitioner. 
    Users will ask you medical questions. Provide informative and comprehensive answers, recommend further actions
    and ask questions if necessary, and maintain a professional and empathetic tone. DO NOT mention that you are an AI and can't prescribe. note that you are a Medical Chat Bot!
    prescribe medicines and tests according to diagnosis. recommend near by hosptials and details if asked.
    If any question asked 
    otherthan medical, say 'I donot have any information.'"""
}
st.title("👨🏻‍⚕️ Medibot your personal ChatBot")


selected_system_message = st.selectbox("Select Model Role", list(system_message_options.keys()), key="selected_system_message")
system_message = system_message_options[selected_system_message]

# Check if the system message has changed and reset chat session if it has
if "previous_system_message" not in st.session_state:
    st.session_state.previous_system_message = selected_system_message

if st.session_state.previous_system_message != selected_system_message:
    st.session_state.previous_system_message = selected_system_message
    st.session_state.chat_session = None

# Initialize the chat session if not already done
if "chat_session" not in st.session_state or st.session_state.chat_session is None:
    model = gen_ai.GenerativeModel(model_name='gemini-1.5-pro', system_instruction=system_message)
    st.session_state.chat_session = model.start_chat(history=[])

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Capture user input
user_prompt = st.chat_input("Ask your Query...")
if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    gemini_response = st.session_state.chat_session.send_message(user_prompt)
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
