from abc import ABC, abstractmethod

from django.utils import timezone
from rest_framework import serializers
from data_ocean.utils import convert_to_usd

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

    class DataSerializer(serializers.Serializer):
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


class IsMoneyFromNowhere(BaseScoringRule):
    """
    Rule 21 - PEP21
    weight - 1.0
    Monetary assets declared this year exceed the sum of
    income and amount of monetary assets of the previous year
    """

    rule_id = ScoringRuleEnum.PEP21

    class DataSerializer(serializers.Serializer):
        new_year = serializers.IntegerField(min_value=0, required=True)
        old_sum_USD = serializers.IntegerField(min_value=0, required=True)
        new_sum_USD = serializers.IntegerField(min_value=0, required=True)
        declaration_id = serializers.IntegerField(min_value=0, required=True)

    def calculate_weight(self) -> tuple[int or float, dict]:
        year = self.declaration.year

        try:
            old_declaration = Declaration.objects.filter(
                pep_id=self.pep.id,
                year=year - 1
            ).values('id', 'year')[::1][0]
        except:
            return 0, {}
        new_declaration = {'id': self.declaration.id, 'year': year}
        declaration_sum = []
        for declaration in (old_declaration, new_declaration):
            declaration_id = declaration['id']
            assets_USD = 0.0
            income_UAH = 0.0
            try:
                assets = Money.objects.filter(
                    declaration_id=declaration_id,
                ).values_list('amount', 'currency')[::1]
                for currency_pair in assets:
                    assets_USD += convert_to_usd(currency_pair[1], float(currency_pair[0]), year)
                incomes = Income.objects.filter(
                    declaration_id=declaration_id,
                ).values_list('amount', 'type')[::1]
                for income in incomes:
                    income_UAH += income[0]
                income_USD = convert_to_usd('UAH', income_UAH, year)
                assets_USD += income_USD
            except:
                pass
            declaration_sum.append(assets_USD)
            declaration_sum.append(income_USD)
        if declaration_sum[0] + declaration_sum[1] < declaration_sum[2]:
            weight = 1.0
            data = {
                "new_year": year,
                "old_sum_USD": declaration_sum[0] + declaration_sum[1],
                "new_sum_USD": declaration_sum[2],
                "declaration_id": self.declaration.id,
            }
            return weight, data
        return 0, {}
