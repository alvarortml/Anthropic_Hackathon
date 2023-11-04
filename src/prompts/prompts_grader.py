from langchain.schema.messages import AIMessage, HumanMessage

GRADER_SYSTEM_PROMPT = [HumanMessage(content=("""
    I hav been using an AI tutor to learn how to code. In the following
    you will see a converstion with me and the AI tutor, in which I try to solve
    a programming problem. You have to look at the conversation and assess
    if I managed to solve the problem. Your output will be a JSON file. One
    key will be result, which will take the value 1 if I solved the problem,
    and 0 otherwise. The other key will be summary, in which you will print a 
    summary of the difficultes I encountered whtn trying to solve the problem.
     
    Only output the JSON file. Don't output any additional text
    """)),
    AIMessage(content=("""
    Hello! I'll do as you say. I will read the conversation that follows, and produce
     the desired JSON. I will only produce a JSON as my output, and won't add any additional text outside
     of it
"""))
]

GRADER_FINALIZING_PROMPT = [HumanMessage(content=("What's the veredict?"))]

