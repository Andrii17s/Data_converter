from abc import ABC, abstractmethod


# docstring

class BaseScoringRule(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def calculate_wage(self):
        pass

class IsRealEstateWithoutValue(BaseScoringRule): #3 rule
    def __init__(self):
        pass

    def calculate_wage(self):
        pass
