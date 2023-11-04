import os
import sys
sys.path.append(os.getcwd())
import json

from dotenv import load_dotenv
_ = load_dotenv('.env.anthropic')


from langchain.chat_models import ChatAnthropic
from langchain.schema.messages import AIMessage, HumanMessage
from src.prompts.prompts_grader import GRADER_SYSTEM_PROMPT, GRADER_FINALIZING_PROMPT

if __name__ == "__main__":

    chat_model = ChatAnthropic(temperature=0, model = 'claude-2')
    system_prompt = GRADER_SYSTEM_PROMPT
    finalizing_prompt = GRADER_FINALIZING_PROMPT
    conv = [
        HumanMessage(content=("The solution to the problem is 1 + 1 = 2")),
        AIMessage(content=("Well done! That's right")),
    ]
    response = chat_model.invoke(system_prompt + conv + finalizing_prompt)
    graded_json = json.loads(response.content)
    print(response)