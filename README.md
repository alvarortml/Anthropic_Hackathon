# Code Tutor

We implement an AI tutor to help professors delivering programming classes.

Given a series of programming problems with reference solutions provided by the 
professor, the students will be able to ask questions while doing their homework
to the AI tutor to get hints if they get stuck. The tutor has been prompted to give
helpful hints to the student, but to never give out the complete solution.

The tutor will evaluate the student's solutions both in terms of correctness and
of runtime. If the student producess a valid solution but with worse runtime than the reference solution, the totor will ask them to improve it.

Once the student has finished, or doesn't know how to continue even with the hints from
the tutor, he will be able to press the "Finish problem" button. Upon triggering
this, a new "grader" agent will read at the conversation that the student and the tutor
agent had, and will produce a JSON output. The JSON output will have to keys. A "result" key
that will take values 1 or 0, depending on whether the studnt managed to solve the problem
or not, and a "summary" key, summarizing any problems that the student had while trying to
solve the problem. These JSON files are meant to be used by the human professor, to understand esily where students are having more trouble.

### Tutor agent

The code for the tutor agent we used is under :src/agents/python_tutor/python_tutor_without_interpreter.py

The tutor agent is a conversational agent, that knows both the statement and the solution
to the problem, and it has been prompted to give useful hints to the student, while 
not giving away the solution. It has also the task of judging the student's solution
correctness, and its runtime aganst the reference solution.

When designing the "Human:", "Assistant:" prompts that we initially pass to the agent for it
to have context of the task, we found it important to use xml tags to very clearly specify
the requirements for the agent in the human part of the prompt. We also found it useful for the assistant prompt to agree and repeat on the procedure it was going to follow to grade, to obtain the desired behaviour. The assistant tended to ignore the reference solution, and 
by repeating that it was going to use it to grade we managed to make it attend to it.

We also had to pass again the problem statement in the assistant part of the prompt. First
we were only passing it in the human part, and telling the assistant to work on the problem 
"as defined before". However we found that by doing this the assistent didn't really know the statement of the problem, and would grade the students solutions based only on whether they code submitted compiled or not

We also tried to provide the agent with access to a Python interpreter tool, so that it could run python code and check the students solution correctness against some examples.
We tried to use the Anthropic Functions in Langchain, but we were getting a list index out
of range error when running the chain that we didn't manage to debug.

The code for this agent would be in src/agents/python_tutor/python_tutor.py

We also tried to use a conversational react agent (code at src/agents/python_tutor/python_tutor_react.py), with access to the python interpreter tool. However, this agent didn't work very well. It tended to use the python tool too often and felt less conversational than the basic one, so we decided to go with the original python_tutor_without_intepreter.py

### Grader agent

Code at: src/agents/grader/grader_agent.py

Once the student has decided to finish the problem, the grader agent will kick in and read the conversation between the tutor and the student, and will produce a json outoput indicating if the student managed to solve the problem, and a summary of any troubles it faced.

When designing the human and assistant prompts to specify the task, we again found it useful to have the assistant repeat and agree to the method it was going to follow. A problem we were having was that, when feeding the conversation to the agent to grade, it tended to try to continue the last reply of the assistant.

For example, if the assistant last message was:

"Assistant: That is not the correct solution"

The grader agent would output

"Try again"

To mitigate this we add human prompt at the end of the conversation between the human and the tutor, to signal more clearly the grader that the conversation between the human and the tutor has ended and that it is time to grade.

The only remaining problem that we had was that sometimes, even when specifying the grader to only output a JSON, it would add additional text like "here is my json". To circunvent this we added some postprocessing to the output of the grader, to extract the valid json substring from its output. We found this to work quite well.

### Parser Agent (Future Work)

Code at: src/agents/parser/parser_agent.py

We also tried to implement a parser agent that, given a pdf with problems and solutions provided by the profesor, would parse the problem title, problems and solutions. This then could be used to create pages for our streamlit app on the fly, as all the pages follow the same template, with the only difference beeing the problem statement and solution.

The problem that we found was that, when trying to parse the output XML, if any of the code solutions contained something like:

" if x < 0", the < 0 would make the xml crash due to incorrect use of the <. We didn't find a way around this problem.


### Monitoring

All thechains are logged in Langsmith. We automatically create new projects for each agent in each problem page, so everything is logged nicely in different places