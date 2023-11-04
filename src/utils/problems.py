class LeetCodeProblem:
    def __init__(self, statement:str, **kwargs):
        self.statement = statement
        if kwargs.get('solution', None):
            self.solution = kwargs.get('solution')
        if kwargs.get('public_test_cases', None):
            self.public_test_cases = kwargs.get('public_test_cases')
        if kwargs.get('private_test_cases', None):
            self.private_test_cases = kwargs.get('private_test_cases')