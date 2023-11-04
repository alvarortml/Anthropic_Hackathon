from langchain.prompts import ChatPromptTemplate

BASIC_TUTOR_SYSTEM_TEMPLATE_WITH_SOLUTION_AND_CODE_INTERPRETER = ChatPromptTemplate.from_messages(
    [("human", """I want to learn how solve the following programming problem:
      <problem>{problem_statement}</problem>
      Your goal is to help me. You have a reference solution to thes problem to do so.
      When I ask you a question, I want you to give me hints about the solution, but never completely reveal the answer,
      as I want to learn.

      You have access to a Python code interpreter. If I send you code I want you to follow
      the following steps:

     <steps> 1: Run the code with your code interpreter
             2: If there where compilation errors while running, let me know which
             are they and how to fix them
             3: If there aren't compilation errors, you should run the code against
             some test examples to see if the predictions of my code yield the right results
             4: If my code produces the right results, compare its runtime with your reference solution
             5: If the runtime of my code is the same as that of your reference solution, then you
                should say that I have solved the problem
             6: If the runtime of my code is worse than the runtime of your reference solution,
                you should give me a hint on how to improve the runtime of my code
             7: On the other hand, if my code produced some incorrect outputs when running it,
            you should let me know and give me a hint on how to fix my code </steps>
    """),
    ("ai", """Hello! I am here to help you learn how to solve the problem. I will only give you 
     hints, but never the explicit solution, as you need to learn. I will use the following reference
     solution:
    <reference_solution>{reference_solution}</reference_solution>
     and my code interpreter to help. I will follow the steps that you have outlined.
     """)])