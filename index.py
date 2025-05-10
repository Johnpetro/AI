

import streamlit as st
import speech_recognition as sr
import google.generativeai as genai # Renamed import for clarity
import os

# --- Configuration ---
# For local development, set GOOGLE_API_KEY as an environment variable
# For Streamlit Cloud, set it in st.secrets
try:
    GOOGLE_API_KEY ="AIzaSyCBu7V1fpkjCBc8VORgoojSFqFj7J4Ro3Q"
except (KeyError, AttributeError):
    
    st.error("🚨 GOOGLE_API_KEY not found. Please set it as an environment variable or in Streamlit secrets.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)
gemini_model = genai.GenerativeModel("gemini-1.5-flash") # Using 1.5-flash as 2.0-flash might not be a public name

# --- Initialize Recognizer (do this once) ---
recognizer = sr.Recognizer()

# --- Helper Functions ---
def save_to_file(text_input, ai_response_text):
    with open("conversation_log.txt", "a", encoding="utf-8") as file:
        file.write(f"You: {text_input}\n")
        file.write(f"AI: {ai_response_text}\n---\n")

def get_gemini_response(prompt_text):
    try:
        response = gemini_model.generate_content(prompt_text)
        return response.text
    except Exception as e:
        st.error(f"Error communicating with Gemini: {e}")
        return None

def listen_for_speech():
    with sr.Microphone() as source:
        st.info("Adjusting for ambient noise... Please wait.")
        try:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            st.info("Listening... Speak now!")
            # Increased timeouts for better capture
            audio = recognizer.listen(source, timeout=7, phrase_time_limit=15)
            st.info("Processing speech...")
            text = recognizer.recognize_google(audio).lower()
            st.success(f"Recognized: {text}")
            return text
        except sr.WaitTimeoutError:
            st.warning("No speech detected within the time limit.")
            return None
        except sr.UnknownValueError:
            st.warning("Google Speech Recognition could not understand audio.")
            return None
        except sr.RequestError as e:
            st.error(f"Could not request results from Google Speech Recognition service; {e}")
            return None
        except Exception as e:
            st.error(f"An unexpected error occurred during speech recognition: {e}")
            return None

# --- Streamlit App UI ---
st.title("🗣️ AI Voice & Speech Recognition")
st.write("Interact with DIT  model using text or your voice.")

# --- Session State Initialization ---
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user_input_method' not in st.session_state:
    st.session_state.user_input_method = "text"


# --- Display previous messages ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Input Method Selection ---
input_method = st.radio("Choose input method:", ("Text", "Voice"), horizontal=True, key="input_choice")

user_prompt = None

if input_method == "Text":
    text_input = st.chat_input("Type your message here...")
    if text_input:
        user_prompt = text_input
        st.session_state.user_input_method = "text"

elif input_method == "Voice":
    if st.button("🎤 Start Listening", key="listen_button"):
        with st.spinner("Listening..."):
            recognized_text = listen_for_speech()
        if recognized_text:
            user_prompt = recognized_text
            st.session_state.user_input_method = "voice"
            # Display recognized text immediately for user confirmation
            st.info(f"You (voice): {recognized_text}")


# --- Process input and get AI response ---
if user_prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Get AI response
    with st.spinner("AI is thinking..."):
        ai_response = get_gemini_response(user_prompt)

    if ai_response:
        # Add AI response to chat history
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        with st.chat_message("assistant"):
            st.markdown(ai_response)
        save_to_file(user_prompt, ai_response)
    else:
        st.error("Failed to get a response .")

st.sidebar.markdown("---")
st.sidebar.subheader("About")
st.sidebar.info(
    "This use of API to create the speech recogition and text generation... "
    "simple script "
)
st.sidebar.subheader("Technology used")
st.sidebar.info(
    "streamlit, google gemini,python,GPT4"
)
