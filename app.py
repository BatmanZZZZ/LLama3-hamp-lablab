import streamlit as st
from dotenv import load_dotenv
from src.Chatbot.gantt_bot import Bot as GanttBot
from src.Chatbot.pert_bot import Bot as PertBot

load_dotenv()

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "gantt_messages" not in st.session_state:
    st.session_state.gantt_messages = []
if "pert_messages" not in st.session_state:
    st.session_state.pert_messages = []
if "gantt_bot" not in st.session_state:
    st.session_state.gantt_bot = GanttBot()
if "pert_bot" not in st.session_state:
    st.session_state.pert_bot = PertBot()
if "img_base64" not in st.session_state:
    st.session_state.img_base64 = ""



def home():
    col1 , col2, col3 = st.columns(3)
    with col1:
        st.write("\n\n\n\n")
        st.image("logo.png", width=100)
    with col2:
        st.title("Chart Generator")
    
    st.write("\n\n\n\n\n\n\n\n\n")
    st.write("\n\n\n\n\n\n\n\n\n")
    st.write("\n\n\n\n\n\n\n\n\n")
    
    st.write("Selct the type of chart you want to generate")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Gantt Chart Generator"):
            st.session_state.page = "Gantt"
            st.experimental_rerun()
    with col2:
        if st.button("PERT Chart Generator"):
            st.session_state.page = "PERT"
            st.experimental_rerun()

def gantt_chart_generator():
    st.title("Gantt Chart Bot")
    if st.button("Go to Home"):
        st.session_state.page = "Home"
        st.experimental_rerun()

    for i, message in enumerate(st.session_state.gantt_messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"], unsafe_allow_html=True)

    if prompt := st.chat_input("Query"):
        st.session_state.gantt_messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)
        assistant_message_placeholder = st.empty()
        with assistant_message_placeholder.chat_message("assistant"):
            stream_container = st.empty()
            
            with st.spinner("Thinking..."):
                response = st.session_state.gantt_bot.handle_query(prompt)
        
                if isinstance(response, str):
                    if "Gantt chart created successfully" in response:
                        stream_container.markdown(response, unsafe_allow_html=True)
                        st.session_state.gantt_messages.append({"role": "assistant", "content": response})
                        # Extract the base64 image from the response
                        img_base64 = response.split('src="data:image/png;base64,')[1].split('"')[0]
                        st.session_state.img_base64 = img_base64
                        st.markdown(
                            f'<a href="data:image/png;base64,{img_base64}" download="gantt_chart.png">Download Gantt Chart</a>',
                            unsafe_allow_html=True
                        )
                    else:
                        complete_answer = ""
                        for r in response:
                            complete_answer += r
                            stream_container.markdown(complete_answer, unsafe_allow_html=True)
                        st.session_state.gantt_messages.append({"role": "assistant", "content": response})

def pert_chart_generator():
    st.title("PERT Chart Bot")
    if st.button("Go to Home"):
        st.session_state.page = "Home"
        st.experimental_rerun()

    for i, message in enumerate(st.session_state.pert_messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"], unsafe_allow_html=True)

    if prompt := st.chat_input("Query"):
        st.session_state.pert_messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)
        assistant_message_placeholder = st.empty()
        with assistant_message_placeholder.chat_message("assistant"):
            stream_container = st.empty()
            
            with st.spinner("Thinking..."):
                response = st.session_state.pert_bot.handle_query(prompt)
                
                if isinstance(response, str):
                    if "PERT chart created successfully" in response:
                        st.session_state.pert_messages.append({"role": "assistant", "content": response})
                        # Extract the base64 image from the response
                        img_base64 = response.split('src="data:image/png;base64,')[1].split('"')[0]
                        st.session_state.img_base64 = img_base64
                        st.image(f"data:image/png;base64,{img_base64}", caption='PERT Chart')
                        st.markdown(
                            f'<a href="data:image/png;base64,{img_base64}" download="pert_chart.png">Download PERT Chart</a>',
                            unsafe_allow_html=True
                        )
                    else:
                        complete_answer = ""
                        for r in response:
                            complete_answer += r
                            stream_container.markdown(complete_answer, unsafe_allow_html=True)
                        st.session_state.pert_messages.append({"role": "assistant", "content": response})

# Render the appropriate page based on the session state
if st.session_state.page == "Home":
    home()
elif st.session_state.page == "Gantt":
    gantt_chart_generator()
   
elif st.session_state.page == "PERT":
    pert_chart_generator()
