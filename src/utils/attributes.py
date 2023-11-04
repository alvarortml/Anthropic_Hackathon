from pydantic.v1 import BaseModel, Field
from typing import List

class Problem(BaseModel):
    """Information about a problem"""
    problem_name: str = Field(description="The name of the problem")
    problem_statement: str = Field(description="The statement of the problem")
    reference_solution: str = Field(description="The code providing the solution to the problem")

class HomeWork(BaseModel):
    """Information to extract"""
    problems: List[Problem] = Field(description="List of information about the problems")