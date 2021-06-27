from abc import ABC, abstractmethod
from business_register.models.declaration_models import (Declaration,
                                                         Property,
                                                         Vehicle,
                                                         VehicleRight,
                                                         Income,
                                                         Money,
                                                         PropertyRight,
                                                         )
from business_register.models.pep_models import (RelatedPersonsLink, Pep)
from location_register.models.ratu_models import RatuCity


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
        ).values_list('id', flat=True)[::1]
        family_ids.append(self.pep.id)
        have_weight = PropertyRight.objects.filter(
            pep_id__in=family_ids,
            property__valuation__isnull=True,
            type=Property.SUMMER_HOUSE,
            acquisition_date__year__gte=2015,
        ).values_list('property_id', 'property__declaration_id')[::1]
        if have_weight:
            weight = 0.4
            data = {
                "property_id": have_weight[0][0],
                "declaration_id": have_weight[0][1],
            }
            return weight, data
        return 0, {}


class IsLandWithoutValue(BaseScoringRule):
    """
    Rule 3.2 - PEP03_land
    weight - 0.1
    There is no information on the value of the land owned by PEP or
    family members since 2015
    """

    def calculate_weight(self):
        family_ids = self.pep.related_persons.filter(
            to_person_links__category=RelatedPersonsLink.FAMILY,
        ).values_list('id', flat=True)[::1]
        family_ids.append(self.pep.id)
        have_weight = PropertyRight.objects.filter(
            pep_id__in=family_ids,
            property__valuation__isnull=True,
            type=Property.LAND,
            acquisition_date__year__gte=2015,
        ).values_list('property_id', 'property__declaration_id')[::1]
        if have_weight:
            weight = 0.1
            data = {
                "property_id": have_weight[0][0],
                "declaration_id": have_weight[0][1],
            }
            return weight, data
        return 0, {}


class IsAutoWithoutValue(BaseScoringRule):
    """
    Rule 3.3 - PEP03_car
    weight - 0.4
    There is no information on the value of the vehicle owned by PEP or
    family members since 2015
    """

    def calculate_weight(self):
        family_ids = self.pep.related_persons.filter(
            to_person_links__category=RelatedPersonsLink.FAMILY,
        ).values_list('id', flat=True)[::1]
        family_ids.append(self.pep.id)
        have_weight = VehicleRight.objects.filter(
            pep_id__in=family_ids,
            car__valuation__isnull=True,
            acquisition_date__year__gte=2015,
        ).values_list('car_id', 'car__declaration_id')[::1]
        if have_weight:
            weight = 0.4
            data = {
                "vehicle_id": have_weight[0][0],
                "declaration_id": have_weight[0][1],
            }
            return weight, data
        return 0, {}


class IsMultiplyingMoney(BaseScoringRule):
    """
    Rule 22 - PEP22
    weight - 0.8
    Hard cash declared in the very first electronic asset declaration available in
    the system  exceeds in 5 or more times income declared for the corresponding year
    """

    def calculate_weight(self):
        declarations = Declaration.objects.filter(
            pep_id=self.pep.id,
        ).values('id', 'year')[::1]
        declaration_ids = {}

        for declaration in declarations:
            year = declaration['year']
            if not declaration_ids.__contains__(year):
                declaration_ids[declaration['year']] = list()
                declaration_ids[declaration['year']].extend([declaration['id']])
            elif not declaration['id'] in declaration_ids[year]:
                declaration_ids[year].extend([declaration['id']])
        id_sort_by_year = sorted(declaration_ids.items(), key=lambda x: x[0])
        assets = Money.objects.filter(
            declaration_id=id_sort_by_year[0][1][0],
        ).values_list('amount', 'currency')[::1]
        incomes = Income.objects.filter(
            declaration_id=id_sort_by_year[0][1][0],
        ).values_list('amount', flat=True)[::1]
        total_income = 0
        for income in incomes:
            total_income += income
        assets_UAH = 0
        assets_USD = 0
        assets_EUR = 0
        assets_GBP = 0
        for asset in assets:
            if asset[1] == 'UAH':
                assets_UAH += asset[0]
            elif asset[1] == 'USD':
                assets_USD += asset[0]
            elif asset[1] == 'EUR':
                assets_EUR += asset[0]
            else:
                assets_GBP += asset[0]
        total_assets = assets_USD * 27 + assets_EUR * 32.7 + assets_GBP * 38 + assets_UAH #!
        if (total_assets / total_income) > 5:
            weight = 0.8
            data = {
                "total_assets": total_assets,
                "total_income": total_income,
                "year": id_sort_by_year[0][0]
            }
            return weight, data
        return 0, {}
