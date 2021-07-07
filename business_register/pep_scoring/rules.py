from abc import ABC, abstractmethod

from django.utils import timezone
from rest_framework import serializers
from typing import Tuple, Union
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
    Transaction,
)
from business_register.models.pep_models import (RelatedPersonsLink, Pep)
from business_register.pep_scoring.rules_registry import register_rule, ScoringRuleEnum
from location_register.models.ratu_models import RatuCity

SPOUSE_TYPES = ['дружина', 'чоловік']


class BaseScoringRule(ABC):
    rule_id = None
    message_uk = ''
    message_en = ''

    class DataSerializer(serializers.Serializer):
        """ Overwrite this class in child classes """

    def __init__(self, declaration: Declaration) -> None:
        assert type(self.rule_id) == ScoringRuleEnum
        # if not self.message_uk or not self.message_en:
        #     message = (
        #         f'{self.__class__.__name__} don`t have messages (en, uk), '
        #         'pls provide they. Messages use `data` dict and `.format()` function '
        #         'for render full message'
        #     )
        #     print(message)
        #     logger.warning(message)

        self.rule_id = self.rule_id.value
        self.declaration: Declaration = declaration
        self.pep: Pep = declaration.pep
        self.weight = None
        self.data = None

    def validate_data(self, data) -> None:
        self.DataSerializer(data=data).is_valid(raise_exception=True)
        try:
            self.message_uk.format(**data)
            self.message_en.format(**data)
        except KeyError:
            raise ValueError(f'{self.__class__.__name__}[{self.rule_id}]: `data` dont have keys for render messages')

    def validate_weight(self, weight) -> None:
        assert type(weight) in (int, float)

    def calculate_with_validation(self) -> Tuple[Union[int, float], dict]:
        weight, data = self.calculate_weight()
        if weight != 0:
            self.validate_data(data)
            self.validate_weight(weight)
        self.weight = weight
        self.data = data
        return weight, data

    def save_to_db(self):
        assert self.weight is not None and self.data is not None
        PepScoring.objects.update_or_create(
            declaration=self.declaration,
            pep=self.pep,
            rule_id=self.rule_id,
            defaults={
                'data': self.data,
                'score': self.weight,
                'calculation_datetime': timezone.now(),
            }
        )

    @abstractmethod
    def calculate_weight(self) -> Tuple[Union[int, float], dict]:
        pass


@register_rule
class IsSpouseDeclared(BaseScoringRule):
    """
    Rule 1 - PEP01
    weight - 0.1
    Asset declaration does not indicate PEP’s spouse, while pep.org.ua register has information on them
    """

    rule_id = ScoringRuleEnum.PEP01
    message_uk = (
        'У декларації про майно немає даних про члена родини, '
        'тоді як у реєстрі pep.org.ua є {relationship_type} {spouse_full_name}'
    )
    message_en = 'Asset declaration does not indicate PEP\'s spouse'

    class DataSerializer(serializers.Serializer):
        relationship_type = serializers.CharField(required=True)
        spouse_full_name = serializers.CharField(required=True)

    def calculate_weight(self) -> Tuple[Union[int, float], dict]:
        link_to_spouse_from_antac_db = RelatedPersonsLink.objects.filter(
            from_person=self.pep,
            to_person_relationship_type__in=SPOUSE_TYPES
        ).first()
        if link_to_spouse_from_antac_db:
            is_spouse_declared = self.declaration.spouse
            if not is_spouse_declared:
                weight = 0.1
                data = {
                    'relationship_type': link_to_spouse_from_antac_db.to_person_relationship_type,
                    "spouse_full_name": link_to_spouse_from_antac_db.to_person.fullname.title()
                }
                return weight, data
        return 0, {}


# @register_rule
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

    def calculate_weight(self) -> Tuple[Union[int, float], dict]:
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


# @register_rule
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

    def calculate_weight(self) -> Tuple[Union[int, float], dict]:
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


# @register_rule
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

    def calculate_weight(self) -> Tuple[Union[int, float], dict]:
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


@register_rule
class IsBigExpenditures(BaseScoringRule):
    """
    Rule 13 - PEP13
    weight - 0.7
    The overall amount of income and monetary assets indicated in the declaration
    is smaller or equal to the expenditures indicated in the declaration
    """

    rule_id = ScoringRuleEnum.PEP13

    class DataSerializer(serializers.Serializer):
        total_USD = serializers.FloatField(min_value=0, required=True)
        expenditures_USD = serializers.FloatField(min_value=0, required=True)

    def calculate_weight(self) -> Tuple[Union[int, float], dict]:
        year = self.declaration.year

        income_UAH = 0
        assets_USD = 0
        expenditures_UAH = 0
        expenditures_USD = 0
        incomes = Income.objects.filter(
            declaration_id=self.declaration.id,
        ).values_list('amount', 'type')[::1]
        for income in incomes:
            try:
                income_UAH += income[0]
            except:
                pass
        income_USD = convert_to_usd('UAH', float(income_UAH), year)
        assets = Money.objects.filter(
            declaration_id=self.declaration.id,
        ).values_list('amount', 'currency')[::1]
        for currency_pair in assets:
            try:
                assets_USD += convert_to_usd(currency_pair[1], float(currency_pair[0]), year)
            except:
                pass
        expenditures = Transaction.objects.filter(
            declaration_id=self.declaration.id,
        ).values_list('amount')[::1]
        for expenditure in expenditures:
            try:
                expenditures_UAH += expenditure
            except:
                pass
            expenditures_USD = convert_to_usd('UAH', float(expenditures_UAH), year)
        total_USD = assets_USD + income_USD
        if expenditures_USD > total_USD:
            weight = 0.7
            data = {
                "total_USD": total_USD,
                "expenditures_USD": expenditures_USD,
            }
            return weight, data
        return 0, {}


x = IsBigExpenditures(Declaration.objects.raw('SELECT * from business_register_declaration WHERE id=1')[0])
print(x.calculate_weight())

@register_rule
class IsCostlyPresents(BaseScoringRule):
    """
    Rule 15 - PEP15
    weight - 0.8
    Declared presents amounting to more than 100 000 UAH
    """
    rule_id = ScoringRuleEnum.PEP15

    class DataSerializer(serializers.Serializer):
        presents_price_UAH = serializers.IntegerField(min_value=0, required=True)

    def calculate_weight(self) -> Tuple[Union[int, float], dict]:
        presents_max_amount = 100000
        presents_price_UAH = 0
        incomes = Income.objects.filter(
            declaration_id=self.declaration.id,
            amount__isnull=False,
        ).values_list('amount', 'type')[::1]
        for income in incomes:
            if income[1] in (Income.GIFT_IN_CASH, Income.GIFT):
                presents_price_UAH += income[0]
        if presents_price_UAH > presents_max_amount:
            weight = 0.8
            data = {
                "presents_price_UAH": presents_price_UAH,
            }
            return weight, data
        return 0, {}
