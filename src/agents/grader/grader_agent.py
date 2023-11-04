import os
import sys
sys.path.append(os.getcwd())
import pdb

from dotenv import load_dotenv
_ = load_dotenv('.env.anthropic')


from langchain.chat_models import ChatAnthropic
from langchain.schema.messages import AIMessage, HumanMessage

if __name__ == "__main__":

    chat_model = ChatAnthropic(temperature=0, model = 'claude-2')
    prompt = [
        HumanMessage(content=("""You are a grader. Your task is to look at a
                    conversation between an AI and myself, and assess if the I solved the problem.
                    Your output should be a json with one key called success, with value 1 if I solved the problem
                    and value 0 otherwise, and another key called summary, summarizing any issues I had when 
                    trying to solve the problem. Don't include any other information in your output, onlhy the JSON""")),
        AIMessage(content=("")),
        HumanMessage(content=("The solution to the problem is 1 + 1 = 3")),
        AIMessage(content=("That's incorrect. Check your calculations")),
        HumanMessage(content="")
    ]
    response = chat_model(prompt).content
    pdb.set_trace()