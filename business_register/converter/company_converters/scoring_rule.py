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
from business_register.models.pep_models import (RelatedPersonsLink,)

# docstring

class BaseScoringRule(ABC):

    def __init__(self, pep_id):
        self.declarations_id = []
        category = 'family'
        for family_member in RelatedPersonsLink.objects.raw('SELECT * FROM business_register_relatedpersonslink WHERE '
                                                            'from_person_id=%s AND category=%s', [pep_id, category]):
            print(family_member.to_person_id)
            for declaration in Declaration.objects.raw('SELECT * FROM business_register_declaration WHERE id=%s',
                                                       [family_member.to_person_id]):
                self.declarations_id.append(declaration.id)

        for declaration in Declaration.objects.raw('SELECT * FROM business_register_declaration WHERE id=%s',
                                                   [pep_id]):
            self.declarations_id.append(declaration.id)
        print(self.declarations_id)

    @abstractmethod
    def calculate_wage(self):
        pass


class IsRealEstateWithoutValue(BaseScoringRule):  # 3_1 rule

    def calculate_wage(self):
        for declaration_id in self.declarations_id:
            for pep_property in Property.objects.raw('SELECT * from business_register_property WHERE declaration_id=%s',
                                                     [declaration_id]):
                if (pep_property.valuation is None) and (pep_property.type == 2) and (
                        str(pep_property.created_at.date()) > '2014-12-31'):
                    return 0.4
                else:
                    pass
        return 0


class IsLandWithoutValue(BaseScoringRule):  # 3_2 rule

    def calculate_wage(self):
        for declaration_id in self.declarations_id:
            for pep_property in Property.objects.raw('SELECT * from business_register_property WHERE declaration_id=%s',
                                                     [declaration_id]):
                if (pep_property.valuation is None) and (pep_property.type == 7) and (
                        str(pep_property.created_at.date()) > '2014-12-31'):
                    return 0.1
                else:
                    pass
        return 0


class IsAutoWithoutValue(BaseScoringRule):  # 3_3 rule

    def calculate_wage(self):
        for declaration_id in self.declarations_id:
            for pep_car in Vehicle.objects.raw('SELECT * from business_register_vehicle WHERE declaration_id=%s',
                                               [declaration_id]):
                print(pep_car.valuation)
                if (pep_car.valuation is None) and (str(pep_car.created_at.date()) > '2014-12-31'):
                    return 0.4
                else:
                    pass
        return 0


x = IsRealEstateWithoutValue(2)
print(x.calculate_wage())
