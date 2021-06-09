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
from business_register.models.pep_models import (RelatedPersonsLink, )
from location_register.models.ratu_models import (RatuCity, )


# docstring

class BaseScoringRule(ABC):

    def __init__(self, pep_id):
        self.pep_id = pep_id
        self.family_declarations_id = []
        self.pep_declarations_id = []
        category = 'family'
        for family_member in RelatedPersonsLink.objects.raw('SELECT * FROM business_register_relatedpersonslink WHERE '
                                                            'from_person_id=%s AND category=%s', [pep_id, category]):
            print(family_member.to_person_id)
            for declaration in Declaration.objects.raw('SELECT * FROM business_register_declaration WHERE id=%s',
                                                       [family_member.to_person_id]):
                self.family_declarations_id.append(declaration.id)

        for declaration in Declaration.objects.raw('SELECT * FROM business_register_declaration WHERE id=%s',
                                                   [pep_id]):
            self.pep_declarations_id.append(declaration.id)
        self.family_declarations_id.append(self.pep_declarations_id)

    @abstractmethod
    def calculate_wage(self):
        pass


class IsRealEstateWithoutValue(BaseScoringRule):  # 3_1 rule

    def calculate_wage(self):
        for declaration_id in self.family_declarations_id:
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
        for declaration_id in self.family_declarations_id:
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
        for declaration_id in self.family_declarations_id:
            for pep_car in Vehicle.objects.raw('SELECT * from business_register_vehicle WHERE declaration_id=%s',
                                               [declaration_id]):
                print(pep_car.valuation)
                if (pep_car.valuation is None) and (str(pep_car.created_at.date()) > '2014-12-31'):
                    return 0.4
                else:
                    pass
        return 0


class LiveNowhere(BaseScoringRule):  # 4_1 rule

    def calculate_wage(self):
        live_nowhere = True
        for declaration_id in self.pep_declarations_id:
            for declaration in Declaration.objects.raw('SELECT * FROM business_register_declaration WHERE id=%s',
                                                       [declaration_id]):
                pep_city_of_residence_id = declaration.city_of_residence_id
            for pep_property in Property.objects.raw('SELECT * from business_register_property WHERE declaration_id=%s'
                                                     ' AND type>0 AND type<5', [declaration_id]):
                if pep_property.city_id == pep_city_of_residence_id:
                    live_nowhere = False
                    continue
                else:
                    pass
            if live_nowhere:
                return 0.7

        return 0


class LiveNowhereRegion(BaseScoringRule):  # 4_2 rule

    def calculate_wage(self):
        live_nowhere = True
        for declaration_id in self.pep_declarations_id:
            for declaration in Declaration.objects.raw('SELECT * FROM business_register_declaration WHERE id=%s',
                                                       [declaration_id]):
                pep_city_of_residence_id = declaration.city_of_residence_id
            for pep_property in Property.objects.raw('SELECT * from business_register_property WHERE declaration_id=%s'
                                                     ' AND type>0 AND type<5', [declaration_id]):
                for pep_region_of_residence_id in RatuCity.objects.raw('SELECT * from location_register_ratucity WHERE'
                                                                       ' id=%s',[pep_city_of_residence_id]):
                    for pep_region_of_property_id in RatuCity.objects.raw(
                            'SELECT * from location_register_ratucity WHERE'
                            ' id=%s', [pep_property.city_id]):
                        if pep_region_of_residence_id == pep_region_of_property_id:
                            live_nowhere = False
                            continue
                        else:
                            pass
            if live_nowhere:
                return 0.7

        return 0


x = LiveNowhereRegion(1)
print(x.calculate_wage())
