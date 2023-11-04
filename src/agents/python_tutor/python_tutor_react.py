import os
import sys
sys.path.append(os.getcwd())
import pdb


from dotenv import load_dotenv
_ = load_dotenv('.env.anthropic')


from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatAnthropic
from langchain_experimental.tools import PythonREPLTool
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

instructions = """
    Execute the following Python code, and tell me what is wrong with
    it and how to fix it

    def sum(a,b):
        c = a + b
        return c
    
"""

if __name__ == "__main__":

    tools = [PythonREPLTool()]
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a useful assistant. You have a python interpreter to run code when needed"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
    ])
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    llm = ChatAnthropic(temperature=0, model="claude-2", 
                                        anthropic_api_key = os.environ['ANTHROPIC_API_KEY'])
    agent_chain = initialize_agent(
        tools,
        llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        verbose=True,
        memory=memory,
    )

    result = agent_chain.invoke({"input": instructions})
    pdb.set_trace()

