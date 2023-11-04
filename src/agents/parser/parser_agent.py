import os
import sys
sys.path.append(os.getcwd())
import pdb

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv(".env.anthropic")) # read local .env file

from langchain.utils.openai_functions import convert_pydantic_to_openai_function
from langchain.prompts import ChatPromptTemplate
from langchain.document_loaders import PyPDFLoader
from langchain_experimental.llms.anthropic_functions import AnthropicFunctions
from src.utils.attributes import HomeWork



if __name__ == "__main__":

    loader = PyPDFLoader("/Users/alvaro/Documents/ML_Projects/ANTHROPIC_HACKATHON/homework/homework.pdf")
    pages = loader.load()
    chat_model = AnthropicFunctions(temperature=0, model = "claude-2", 
                anthropic_api_key = os.environ['ANTHROPIC_API_KEY'])
    extract_functions = [convert_pydantic_to_openai_function(HomeWork)]
    pdb.set_trace()
    prompt = ChatPromptTemplate.from_messages([
        ("human", "Extract the relevant information, if not explicitly provided do not guess. Extract partial info"),
        ("ai", ""),
        ("human", "{input}")
    ])
    pdb.set_trace()
    messages = prompt.format_messages(input=pages[0].page_content)
    response = chat_model(messages=messages, functions=extract_functions)
    pdb.set_trace()