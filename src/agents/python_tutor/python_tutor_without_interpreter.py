import os
import sys
sys.path.append(os.getcwd())
import pdb

from dotenv import load_dotenv
_ = load_dotenv('.env.anthropic')

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = f"Tutor Anthropic Original"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"


from langchain.chat_models import ChatAnthropic
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from src.prompts.prompts_coding_tutor import HUMAN_TUTOR_WITHOUT_CODE_INTERPRETER, AI_TUTOR_WITHOUT_CODE_INTERPRETER
from langchain.chains import LLMChain
from langsmith import Client

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

inst_2 = """
        My new attempt is:

        def twoSum(self, nums, target):
        remainders = {}
        for i in range(len(nums)):
            complement = target - nums[i]
            if complement in remainders:
                return [remainders[complement], i]
            remainders[nums[i]] = i
"""


instructions = """
    This is my attempt at solving the problem

    def sum(a,b):
        c = a + b
        return c
    
"""



if __name__ == "__main__":

    client = Client()
    chat_model = ChatAnthropic(temperature=0, model = "claude-2", 
                anthropic_api_key = os.environ['ANTHROPIC_API_KEY'])
    human_system_message = HUMAN_TUTOR_WITHOUT_CODE_INTERPRETER.format(problem_statement = BASIC_PROBLEM_STATEMENT)
    ai_system_message = AI_TUTOR_WITHOUT_CODE_INTERPRETER.format(reference_solution = REFERENCE_SOLUTION, problem_statement = BASIC_PROBLEM_STATEMENT)
    prompt = ChatPromptTemplate.from_messages([
        human_system_message,
        ai_system_message,
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])
    memory = ConversationBufferMemory(return_messages=True, memory_key="chat_history")
    conversation_chain = LLMChain(llm=chat_model, prompt=prompt, verbose=True, memory=memory)
    conversation_chain.invoke({"input": instructions})
    result = conversation_chain.invoke({"input": instructions})
    result