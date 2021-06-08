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
        for declaration in Declaration.objects.raw('SELECT * from business_register_declaration WHERE id=%s', [pep_id]):
            self.declarations_id.append(declaration.id)

    @abstractmethod
    def calculate_wage(self):
        pass


class IsRealEstateWithoutValue(BaseScoringRule):  # 3 rule

    def calculate_wage(self):
        for declaration_id in self.declarations_id:
            for pep_property in Property.objects.raw('SELECT * from business_register_property WHERE declaration_id=%s',
                                                     [declaration_id]):
                print(pep_property.valuation)
                if (pep_property.valuation is None) and (pep_property.type == 2) and (
                        str(pep_property.created_at.date()) > '2014-12-31'):
                    return 0.4
                else:
                    pass
        return 0


x = IsRealEstateWithoutValue(1)
print(x.calculate_wage())
