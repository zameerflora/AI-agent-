import streamlit as st
import time
from datetime import datetime as dt
from Agents import recommendation_expert
from Tasks import recommendation_task
from crewai import Crew, Process
import json

st.title("Gaia")

#initialise chat & history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

#setup messages from gaia
def reply_stream(stream_msg):
        for word in stream_msg.split():
            yield word + " "
            time.sleep(0.05)

def gaia_(gaia_msg):
    with st.chat_message("assistant"):
        st.write_stream(reply_stream(gaia_msg))
        #st.write(gaia_msg)

    st.session_state.chat_history.append(
    {
    "role": "assistant",
    "content": gaia_msg
    }
    )

#re display history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#trying(and failing) to make this welcome message appear only once
#welcome_msg = "Hello there! How can I assist you today?"
#if welcome_msg not in st.session_state.chat_history:
#    gaia_(welcome_msg)

if prompt:= st.chat_input("Type in query/prompt..."):
    #enter user prompt

    with st.chat_message("user"):
        st.markdown(prompt)
    
    #add to text thread
    st.session_state.chat_history.append(
        {
        "role": "user",
        "content": prompt
        }
    )
    st.write(f"Generating answer for: '{prompt}'")
    
    #generating response
    rec_task = recommendation_task(recommendation_expert, prompt)

    #defining crew
    crew = Crew(
        agents = [recommendation_expert],
        tasks= [rec_task],
        process=Process.sequential, #try other patterns later
        full_output=True, #??
        verbose=True #??
    )

    result = crew.kickoff()

    # Try parsing as JSON (if it's a string)
    try:
        data = json.loads(str(result))  # Convert to string first
        output_value = data.get("raw", str(result))  # Extract "raw" if exists
    except json.JSONDecodeError:
        output_value = str(result)  # Fallback to raw string

    st.write("Results:")
    gaia_(output_value)
