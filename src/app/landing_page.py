import os
import sys
sys.path.append(os.getcwd())

import streamlit as st
from langchain.chat_models import ChatAnthropic
from src.prompts.prompts_grader import GRADER_SYSTEM_PROMPT, GRADER_FINALIZING_PROMPT



if __name__ == "__main__":

    st.title("Code Tutor")

    st.text("""Welcome to Code Tutor! On the left you will see some tabs containing the exercices
            your professor has created for you. You will count with an AI Assistant that will help you
            when you get stuck, and will evaluate your solutions.
            
            Jump to any problem to get started, Happy coding!""")
    
    #Define the model
    if "model" not in st.session_state:
        st.session_state.model = "claude-2"
    
    if "langchain_endpoint" not in st.session_state:
        st.session_state.langchain_endpoint = "https://api.smith.langchain.com"

    if "leetcode_problem" not in st.session_state:
        st.session_state.leetcode_problem = {}
    
    if "system_message" not in st.session_state:
        st.session_state.system_message = {}

    if "grader_agent" not in st.session_state:
        st.session_state.grader_agent = ChatAnthropic(model=st.session_state.model,
                                temperature=0, anthropic_api_key=st.secrets["ANTHROPIC_API_KEY"])

    if "grader_agent_system_message" not in st.session_state:
        st.session_state.grader_agent_system_message = GRADER_SYSTEM_PROMPT

    if "grader_agent_finalizing_message" not in st.session_state:
        st.session_state.grader_agent_finalizing_message = GRADER_FINALIZING_PROMPT