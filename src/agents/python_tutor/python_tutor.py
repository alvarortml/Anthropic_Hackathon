import os
import sys
sys.path.append(os.getcwd())
import pdb

from dotenv import load_dotenv
_ = load_dotenv('.env.anthropic')

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = f"Tracing Walkthrough Anthropic"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"


from langchain_experimental.tools import PythonREPLTool
from langchain.tools.render import format_tool_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain_experimental.llms.anthropic_functions import AnthropicFunctions
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.agents import AgentExecutor
from langsmith import Client

instructions = """
    Execute the following Python code, and tell me what is wrong with
    it and how to fix it

    def sum(a,b):
        c = a + b
        return d
    
"""



if __name__ == "__main__":

    client = Client()
    tools = [PythonREPLTool()]
    functions = [format_tool_to_openai_function(tool) for tool in tools]
    pdb.set_trace()
    chat_model = AnthropicFunctions(temperature=0, model = "claude-2", 
                anthropic_api_key = os.environ['ANTHROPIC_API_KEY'])
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a useful assistant. You have a python interpreter to run code when needed"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])
    memory = ConversationBufferMemory(return_messages=True, memory_key="chat_history")
    chain = prompt | chat_model | OpenAIFunctionsAgentOutputParser()
    agent_chain = RunnablePassthrough.assign(
        agent_scratchpad = lambda x: format_to_openai_functions(x["intermediate_steps"])
    ) | chain
    agent_executor = AgentExecutor(agent=agent_chain, tools=tools, verbose=True, memory=memory)
    pdb.set_trace()