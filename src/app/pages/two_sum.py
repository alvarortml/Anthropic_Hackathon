import os
import streamlit as st
import json
from langchain.chat_models import ChatAnthropic
from src.prompts.prompts_coding_tutor import HUMAN_TUTOR_WITHOUT_CODE_INTERPRETER, AI_TUTOR_WITHOUT_CODE_INTERPRETER
from src.utils.problems import LeetCodeProblem
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langsmith import Client
from langchain.callbacks import LangChainTracer
from langchain.schema.runnable import RunnableConfig
from langchain.chains import LLMChain
import re

pattern = r'\{[^}]+\}'

BASIC_PROBLEM_STATEMENT = """
    Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

    You may assume that each input would have exactly one solution, and you may not use the same element twice.

    You can return the answer in any order.
"""

REFERENCE_SOLUTION = """

    def twoSum(self, nums, target):
        remainders = {}
        for i in range(len(nums)):
            complement = target - nums[i]
            if complement in remainders:
                return [remainders[complement], i]
            remainders[nums[i]] = i

"""

if __name__ == "__main__":

    file_name = os.path.basename(__file__)
    file_name = os.path.splitext(file_name)[0]

    st.title("Two Sum")

    if file_name not in st.session_state.leetcode_problem.keys():
        st.session_state.leetcode_problem[file_name] = LeetCodeProblem(statement=BASIC_PROBLEM_STATEMENT, solution=REFERENCE_SOLUTION)
    
    if file_name not in st.session_state.tutor_agent_human_system_message.keys():
        st.session_state.tutor_agent_human_system_message[file_name] = \
            HUMAN_TUTOR_WITHOUT_CODE_INTERPRETER.format(
            problem_statement = st.session_state.leetcode_problem[file_name].statement)
        st.session_state.tutor_agent_ai_system_message[file_name] = \
            AI_TUTOR_WITHOUT_CODE_INTERPRETER.format(
                reference_solution = st.session_state.leetcode_problem[file_name].solution,
                problem_statement = st.session_state.leetcode_problem[file_name].statement)
    
    client = Client(api_url=st.session_state.langchain_endpoint, api_key=st.secrets['LANGCHAIN_API_KEY'])
    ls_tracer_tutor = LangChainTracer(project_name=f"{file_name}_tutor", client=client)
    ls_tracer_grader = LangChainTracer(project_name=f"{file_name}_grader", client=client)

    msgs = StreamlitChatMessageHistory(key=f"messages_{file_name}")
    memory = ConversationBufferMemory(chat_memory=msgs, return_messages=True, memory_key="chat_history")

    with st.chat_message("assistant"):
        st.markdown(st.session_state.leetcode_problem[file_name].statement)
    
    for msg in msgs.messages:
        st.chat_message(msg.type).write(msg.content)

    chat_model = ChatAnthropic(model=st.session_state.model, temperature=0, 
                               anthropic_api_key=st.secrets["ANTHROPIC_API_KEY"])
    
    prompt = ChatPromptTemplate.from_messages([
        st.session_state.tutor_agent_human_system_message[file_name],
        st.session_state.tutor_agent_ai_system_message[file_name],
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])
    
    conversation_chain = LLMChain(llm=chat_model, prompt=prompt, verbose=True, memory=memory)

    if user_input := st.chat_input("Type here"):
        st.chat_message("user").write(user_input)
        response = conversation_chain.invoke(input= {"input": user_input}, config=RunnableConfig(callbacks=[ls_tracer_tutor]))
        st.chat_message("assistant").write(response['text'])

    if st.button('Finish Problem'):
        messages = st.session_state.grader_agent_system_message + msgs.messages + st.session_state.grader_agent_finalizing_message
        grader_response = st.session_state.grader_agent.invoke(messages, config=RunnableConfig(callbacks=[ls_tracer_grader]))
        matches = re.findall(pattern, grader_response.content)
        processed_response = matches[0].replace('\n', '')
        graded_json = json.loads(processed_response)
        file_path = f'/Users/alvaro/Documents/ML_Projects/ANTHROPIC_HACKATHON/src/grades/{file_name}.json'
        with open(file_path, 'w') as json_file:
            json.dump(graded_json, json_file)