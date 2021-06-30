from abc import ABC, abstractmethod

from django.utils import timezone
from rest_framework import serializers

from business_register.models.declaration_models import (
    Declaration,
    Property,
    Vehicle,
    VehicleRight,
    Income,
    Money,
    PropertyRight,
    PepScoring,
)
from business_register.models.pep_models import (RelatedPersonsLink, Pep)
from business_register.pep_scoring.constants import ScoringRuleEnum
from location_register.models.ratu_models import RatuCity


class BaseScoringRule(ABC):
    rule_id = None

    class DataSerializer(serializers.Serializer, ABC):
        """ Overwrite this class in child classes """

    def __init__(self, declaration: Declaration) -> None:
        assert type(self.rule_id) == ScoringRuleEnum
        self.rule_id = self.rule_id.value
        self.declaration: Declaration = declaration
        self.pep: Pep = declaration.pep
        self.weight = None
        self.data = None

    def validate_data(self, data) -> None:
        self.DataSerializer(data=data).is_valid(raise_exception=True)

    def validate_weight(self, weight) -> None:
        assert type(weight) in (int, float)

    def calculate_with_validation(self) -> tuple[int or float, dict]:
        weight, data = self.calculate_weight()
        self.validate_data(data)
        self.validate_weight(weight)
        self.weight = weight
        self.data = data
        return weight, data

    def save_to_db(self):
        assert self.weight and self.data
        PepScoring.objects.create(
            declaration=self.declaration,
            pep=self.pep,
            rule_id=self.rule_id,
            calculation_date=timezone.localdate(),
            score=self.weight,
            data=self.data,
        )

    @abstractmethod
    def calculate_weight(self) -> tuple[int or float, dict]:
        pass


class IsSpendingMore(BaseScoringRule):
    """
    Rule 2 - PEP02
    weight - 0.4
    The overall value of the property and assets exceeds income 10 or more times for the current year
    """

    def calculate_weight(self):
        declarations = Declaration.objects.filter(
            pep_id=self.pep.id,
        ).values('id', 'year')[::1]
        declaration_ids = {}

        for declaration in declarations:
            year = declaration['year']
            if year not in declaration_ids:
                declaration_ids[declaration['year']] = []
                declaration_ids[declaration['year']].extend([declaration['id']])
            elif not declaration['id'] in declaration_ids[year]:
                declaration_ids[year].extend([declaration['id']])

        for declarations_by_year in declaration_ids.items():
            assets_UAH = 0
            income_UAH = 0
            for declaration_id in declarations_by_year[1]:
                incomes = Income.objects.filter(
                    declaration_id=declaration_id,
                ).values_list('amount', 'type')[::1]
                for income in incomes:
                    income_UAH += income[0]
                try:
                    assets = Money.objects.filter(
                        declaration_id=declaration_id,
                    ).values_list('amount', 'currency')[::1]
                    assets_UAH = 0
                    assets_USD = 0
                    assets_EUR = 0
                    assets_GBP = 0
                    for currency_pair in assets:
                        if currency_pair[1] == 'UAH':
                            assets_UAH += currency_pair[0]
                        elif currency_pair[1] == 'USD':
                            assets_USD += currency_pair[0]
                        elif currency_pair[1] == 'EUR':
                            assets_EUR += currency_pair[0]
                        else:
                            assets_GBP += currency_pair[0]
                        assets_UAH = assets_USD * 27 + assets_EUR * 32.7 + assets_GBP * 38 + assets_UAH  # !
                except:
                    pass
                if assets_UAH > income_UAH * 10:
                    weight = 0.4
                    data = {
                        "assets_UAH": assets_UAH,
                        "income_UAH": income_UAH,
                        "year": declarations_by_year[0],
                    }
                    return weight, data
        return 0, {}


class IsRealEstateWithoutValue(BaseScoringRule):
    """
    Rule 3.1 - PEP03_home
    weight - 0.4
    There is no information on the value of the real estate owned by PEP or
    family members since 2015
    """

    rule_id = ScoringRuleEnum.PEP03_home

    class DataSerializer(serializers.Serializer):
        property_id = serializers.IntegerField(min_value=0, required=True)
        declaration_id = serializers.IntegerField(min_value=0, required=True)

    def calculate_weight(self) -> tuple[int or float, dict]:
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

    rule_id = ScoringRuleEnum.PEP03_land

    class DataSerializer(serializers.Serializer):
        property_id = serializers.IntegerField(min_value=0, required=True)
        declaration_id = serializers.IntegerField(min_value=0, required=True)

    def calculate_weight(self) -> tuple[int or float, dict]:
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

    rule_id = ScoringRuleEnum.PEP03_car

    class DataSerializer(serializers.Serializer):
        vehicle_id = serializers.IntegerField(min_value=0, required=True)
        declaration_id = serializers.IntegerField(min_value=0, required=True)

    def calculate_weight(self) -> tuple[int or float, dict]:
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
