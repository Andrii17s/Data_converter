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
from business_register.models.pep_models import (RelatedPersonsLink, Pep)
from location_register.models.ratu_models import (RatuCity,)


# docstring

class BaseScoringRule(ABC):
    def __init__(self, pep):
        self.pep = pep

    @abstractmethod
    def calculate_weight(self):
        pass


class IsRealEstateWithoutValue(BaseScoringRule):
    """
    Rule 3.1 - PEP03_home
    weight - 0.4
    There is no information on the value of the real estate owned by PEP or
    family members since 2015
    """

    def calculate_weight(self):
        family_ids = self.pep.related_persons.filter(
            to_person_links__category=RelatedPersonsLink.FAMILY,
        ).values_list('id', flat=True).all()[::1]
        family_ids.append(self.pep.id)
        have_weight = Property.objects.filter(
            declaration__pep_id__in=family_ids,
            valuation__isnull=True,
            type=Property.SUMMER_HOUSE,
            created_at__year__gte=2015,
        ).exists()
        if have_weight:
            return 0.4
        return 0


class IsLandWithoutValue(BaseScoringRule):  # 3_2 rule
    """
    Rule 3.2 - PEP03_land
    weight - 0.1
    There is no information on the value of the land owned by PEP or
    family members since 2015
    """

    def calculate_weight(self):
        family_ids = self.pep.related_persons.filter(
            to_person_links__category=RelatedPersonsLink.FAMILY,
        ).values_list('id', flat=True).all()[::1]
        family_ids.append(self.pep.id)
        have_weight = Property.objects.filter(
            declaration__pep_id__in=family_ids,
            valuation__isnull=True,
            type=Property.LAND,
            created_at__year__gte=2015,
        ).exists()
        if have_weight:
            return 0.1
        return 0


class IsAutoWithoutValue(BaseScoringRule):  # 3_3 rule
    """
    Rule 3.3 - PEP03_car
    weight - 0.4
    There is no information on the value of the vehicle owned by PEP or
    family members since 2015
    """
    def calculate_weight(self):
        family_ids = self.pep.related_persons.filter(
            to_person_links__category=RelatedPersonsLink.FAMILY,
        ).values_list('id', flat=True).all()[::1]
        family_ids.append(self.pep.id)
        have_weight = Vehicle.objects.filter(
            declaration__pep_id__in=family_ids,
            created_at__year__gte=2015,
        ).exists()
        if have_weight:
            return 0.4
        return 0


class LiveNowhere(BaseScoringRule):  # 4_1 rule
    """
    Rule 4.1 - PEP04_adr
    weight - 0.7
    There is no information on the real estate or apartment in the city, which indicated as PEP's place of residence
    """

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
    """
    Rule 4.2 - PEP04_reg
    weight - 0.1
    There is no information on the real estate or apartment in the region, which indicated as PEP's place of residence
    """

    def calculate_wage(self):
        live_nowhere = True
        for declaration_id in self.pep_declarations_id:
            for declaration in Declaration.objects.raw('SELECT * FROM business_register_declaration WHERE id=%s',
                                                       [declaration_id]):
                pep_city_of_residence_id = declaration.city_of_residence_id
            for pep_property in Property.objects.raw('SELECT * from business_register_property WHERE declaration_id=%s'
                                                     ' AND type>0 AND type<5', [declaration_id]):
                for pep_region_of_residence_id in RatuCity.objects.raw('SELECT * from location_register_ratucity WHERE'
                                                                       ' id=%s', [pep_city_of_residence_id]):
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


class LuxuaryCars(BaseScoringRule):  # 18 rule -
    """
    Rule 18 - PEP18
    weight - 0.4
    There is no information on the value of the realestate owned by PEP or
    family members since 2015
    """

    def calculate_wage(self):
        for declaration_id in self.pep_declarations_id:
            for pep_car in Vehicle.objects.raw('SELECT * from business_register_vehicle WHERE declaration_id=%s',
                                               [declaration_id]):
                print(pep_car.valuation)
                if (pep_car.valuation is None) and (str(pep_car.created_at.date()) > '2014-12-31'):
                    return 0.4
                else:
                    pass
        return 0


class CarsCount(BaseScoringRule):  # 19 rule -
    """
    Rule 19 - PEP19
    weight - 0.4
    There is no information on the value of the realestate owned by PEP or
    family members since 2015
    """

    def calculate_wage(self):
        for declaration_id in self.pep_declarations_id:
            for pep_car in Vehicle.objects.raw('SELECT * from business_register_vehicle WHERE declaration_id=%s',
                                               [declaration_id]):
                print(pep_car.valuation)
                if (pep_car.valuation is None) and (str(pep_car.created_at.date()) > '2014-12-31'):
                    return 0.4
                else:
                    pass
        return 0


class CashTotalAmount(BaseScoringRule):  # 20 rule -
    """
    Rule 20 - PEP20
    weight - 0.8
    There is no information on the value of the realestate owned by PEP or
    family members since 2015
    """

    def calculate_wage(self):
        for declaration_id in self.family_declarations_id:
            for pep_property in Money.objects.raw('SELECT * from business_register_money WHERE declaration_id=%s',
                                                  [declaration_id]):
                if (pep_property.valuation is None) and (pep_property.type == 2) and (
                        str(pep_property.created_at.date()) > '2014-12-31'):
                    return 0.8
                else:
                    pass
        return 0


x = IsAutoWithoutValue(Pep.objects.raw('SELECT * from business_register_pep WHERE id=1')[0])
print(x.calculate_weight())
