import os
import sys
sys.path.append(os.getcwd())

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv(".env.anthropic")) # read local .env file

from langchain.utils.openai_functions import convert_pydantic_to_openai_function
from langchain.prompts import ChatPromptTemplate
from langchain.document_loaders import PyPDFLoader
from langchain_experimental.llms.anthropic_functions import AnthropicFunctions
from src.utils.attributes import HomeWork
import xml.etree.ElementTree as ET
from langchain.chains import create_extraction_chain

start_tag = "<problems>"
end_tag = "</problems>"

schema = {
    "properties": {
        "problem_name": {"type": "string"},
        "problem_statement" : {"type": "string"},
        "reference_solution": {"type": "string"},
    },
    "required": ["problem_name", "problem_statement", "reference_solution"],
}

if __name__ == "__main__":

    loader = PyPDFLoader("/Users/alvaro/Documents/ML_Projects/ANTHROPIC_HACKATHON/homework/homework.pdf")
    pages = loader.load()
    chat_model = AnthropicFunctions(temperature=0, model = "claude-2", 
                anthropic_api_key = os.environ['ANTHROPIC_API_KEY'], max_tokens = 2000)
    prompt = ChatPromptTemplate.from_messages([
        ("human", "Extract the relevant information"),
        ("ai", ""),
        ("human", "{input}")
    ])
    chain = create_extraction_chain(schema=schema, llm=chat_model)
    results = chain.run(pages[0].page_content)
    messages = prompt.format_messages(input=pages[0].page_content)
    response = chat_model(messages=messages, functions=extract_functions)
    parsed_result = response.content
    start_index = parsed_result.find(start_tag)
    end_index = parsed_result.find(end_tag, start_index + len(start_tag) + 1)
    if start_index != -1 and end_index != -1:
      xml_string = parsed_result[start_index:end_index + len(end_tag)]
      xml_string = xml_string.replace('\n', '')
    response