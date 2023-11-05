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
agent had, and will produce a JSON output, indicating with a 1 or a 0 of the student
solved the problem or not, and 