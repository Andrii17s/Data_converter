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
from location_register.models.ratu_models import RatuCity, RatuRegion


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


class IsLiveNowhereCity(BaseScoringRule):
    """
    Rule 4.1 - PEP04_adr
    weight - 0.7
    There is no information on the real estate or apartment in the city, which indicated as PEP's place of residence
    """

    def calculate_weight(self):
        property_types = [Property.HOUSE, Property.SUMMER_HOUSE, Property.APARTMENT, Property.ROOM]
        declarations_id = Declaration.objects.filter(
            pep_id=self.pep.id,
        ).values_list('id', flat=True)[::1]
        for declaration_id in declarations_id:
            city_id = Declaration.objects.filter(
                id=declaration_id,
            ).values_list('city_of_residence_id', flat=True)[::1][0]
            property_cities = Property.objects.filter(
                declaration=declaration_id,
                type__in=property_types,
            ).values_list('city_id', flat=True)[::1]
            if city_id not in property_cities:
                city_name = RatuCity.objects.filter(
                    id=city_id
                ).values_list('name', flat=True)[::1][0]
                weight = 0.7
                data = {
                    "declaration_id": declaration_id,
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

    def calculate_weight(self):
        property_types = [Property.HOUSE, Property.SUMMER_HOUSE, Property.APARTMENT, Property.ROOM]
        declarations_id = Declaration.objects.filter(
            pep_id=self.pep.id,
        ).values_list('id', flat=True)[::1]
        for declaration_id in declarations_id:
            city_id = Declaration.objects.filter(
                id=declaration_id,
            ).values_list('city_of_residence_id', flat=True)[::1][0]
            region_id = RatuCity.objects.filter(
                id=city_id,
            ).values_list('region_id', flat=True)[::1][0]
            property_cities = Property.objects.filter(
                declaration=declaration_id,
                type__in=property_types,
            ).values_list('city_id', flat=True)[::1]
            if not property_cities:
                weight = 0.1
                data = {
                    "declaration_id": declaration_id,
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
                    "declaration_id": declaration_id,
                    "live_in_region_id": region_id,
                    "live_in_region": region_name,
                    "live_in_city_id": city_id,
                }
                return weight, data
        return 0, {}
