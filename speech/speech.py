import streamlit as st
from utils import get_answer, text_to_speech, autoplay_audio,speech_to_text
from streamlit_float import *
import os

float_init()

def initialize_session_state():
    if "messages" not in st.session_state:
        {"role": "assistant", "content":"Hi! How may I assist you today?"}

def text_to_speech(text):
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",#choose one that sounds like it could be gaia
        input=text
    )
    temp_audio_path = "temp_assist_speech.mp3"
    with open(temp_audio_path, "wb") as f:
        response.stream_to_file(temp_audio_path)
    return temp_audio_path

def speech_to_text(audio_data):
    with open(audio_data, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            response_format="text",
            file=audio_file
        )
    return transcript

def get_answer(messages):
    sys_msg = [{"role":"system", "content":"You are a helpful AI chatbot helping the user by answering their queries."}]
    messages = sys_msg + messages
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106", #get api key
        messages = messages
    )
    return response.choices[0].message.content

def audioplay_audio(path:str):
    with open(path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    md=f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)
    
def main():
    mic_container = st.container()
    with mic_container:
        audio_bytes = audio_recorder()

    if audio_bytes:
        with st.spinner("Analysing audio..."):
            temp_audio_path = "temp_audio_file.mp3"
            with open(temp_audio_path, "wb") as f:
                f.write(audio_bytes)

        #entering transcribed audio in chat
        #transcription endpoint from apenai
        transcript = speech_to_text(temp_audio_path)
        if transcript:
            st.session.state.messages.append({"role":"user","content":transcript})
            with st.chat_message("user"):
                st.write(transcript)

            os.remove(temp_audio_path)

        #last message from user or assistant?
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response= get_answer(st.session_state.messages)
                with st.spinner("Generating audio response..."):
                    audio_file = text_to_speech(response)
                    audioplay(audio_file) 
                st.write(response)
                st.session_state.messages.append({"role":"assistant", "content":response})
                os.remove(audio_file)

        mic_container.float("bottom: 0rem;")


        
