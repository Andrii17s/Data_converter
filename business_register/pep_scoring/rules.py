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
from location_register.models.ratu_models import RatuCity, RatuRegion
from business_register.pep_scoring.constants import ScoringRuleEnum


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


class IsLiveNowhereCity(BaseScoringRule):
    """
    Rule 4.1 - PEP04_adr
    weight - 0.7
    There is no information on the real estate or apartment in the city, which indicated as PEP's place of residence
    """

    rule_id = ScoringRuleEnum.PEP04_adr

    class DataSerializer(serializers.Serializer):
        declaration_id = serializers.IntegerField(min_value=0, required=True)
        live_in_city = serializers.CharField(min_length=1, max_length=100, required=True)
        live_in_city_id = serializers.IntegerField(min_value=0, required=True)

    def calculate_weight(self) -> tuple[int or float, dict]:
        property_types = [Property.HOUSE, Property.SUMMER_HOUSE, Property.APARTMENT, Property.ROOM]
        city_id = Declaration.objects.filter(
            id=self.declaration.id,
        ).values_list('city_of_residence_id', flat=True)[::1][0]
        property_cities = Property.objects.filter(
            declaration=self.declaration.id,
            type__in=property_types,
        ).values_list('city_id', flat=True)[::1]
        if city_id not in property_cities:
            city_name = RatuCity.objects.filter(
                id=city_id
            ).values_list('name', flat=True)[::1][0]
            weight = 0.7
            data = {
                "declaration_id": self.declaration.id,
                "live_in_city": city_name,
                "live_in_city_id": city_id,
            }
            return weight, data
        return 0, {}


class IsLiveNowhereRegion(BaseScoringRule):
    """
    Rule 4.2 - PEP04_reg
    weight - 0.1
    There is no information on the real estate or apartment in the region, which indicated as PEP's place of residence
    """

    rule_id = ScoringRuleEnum.PEP04_reg


    class DataSerializer(serializers.Serializer):
        declaration_id = serializers.IntegerField(min_value=0, required=True)
        live_in_region = serializers.CharField(min_length=1, max_length=30, required=True)
        live_in_region_id = serializers.IntegerField(min_value=0, required=True)

    def calculate_weight(self) -> tuple[int or float, dict]:
        property_types = [Property.HOUSE, Property.SUMMER_HOUSE, Property.APARTMENT, Property.ROOM]
        city_id = Declaration.objects.filter(
            id=self.declaration.id,
        ).values_list('city_of_residence_id', flat=True)[::1][0]
        region_id = RatuCity.objects.filter(
            id=city_id,
        ).values_list('region_id', flat=True)[::1][0]
        property_cities = Property.objects.filter(
            declaration=self.declaration.id,
            type__in=property_types,
        ).values_list('city_id', flat=True)[::1]
        if not property_cities:
            weight = 0.1
            data = {
                "declaration_id": self.declaration.id,
            }
            return weight, data
        property_regions = RatuCity.objects.filter(
            id__in=property_cities,
        ).values_list('region_id', flat=True)[::1]
        if region_id not in property_regions:
            region_name = RatuRegion.objects.filter(
                id=city_id
            ).values_list('name', flat=True)[::1][0]
            weight = 0.1
            data = {
                "declaration_id": self.declaration.id,
                "live_in_region_id": region_id,
                "live_in_region": region_name,
            }
            return weight, data
        return 0, {}
