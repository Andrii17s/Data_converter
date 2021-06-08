from abc import ABC, abstractmethod
from business_register.models.declaration_models import (Declaration,
                                                         Property,
                                                         PropertyRight,
                                                         LuxuryItem,
                                                         LuxuryItemRight,
                                                         Vehicle,
                                                         VehicleRight,
                                                         Securities,
                                                         SecuritiesRight,
                                                         Income,
                                                         Money,
                                                         )


# docstring

class BaseScoringRule(ABC):

    def __init__(self, pep_id):
        self.declarations_id = []
        for declaration in Declaration.objects.raw('SELECT * from business_register_declaration WHERE id=pep_id'):
            self.declarations_id.append(declaration.id)

    @abstractmethod
    def calculate_wage(self):
        pass

class IsRealEstateWithoutValue(BaseScoringRule): #3 rule
    def calculate_wage(self):
        for declaration_id in self.declarations_id:
            for property in Property.objects.raw('SELECT * from business_register_property WHERE declaration_id=declaration_id'):
                print(property.valuation)

x = IsRealEstateWithoutValue(1)
x.calculate_wage()