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
from location_register.models.ratu_models import (RatuCity, )


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
        ).values_list('id', flat=True).all()[::1]
        family_ids.append(self.pep.id)
        have_weight = Vehicle.objects.filter(
            declaration__pep_id__in=family_ids,
            created_at__year__gte=2015,
        ).exists()
        if have_weight:
            return 0.4
        return 0


class IsLiveNowhere(BaseScoringRule):
    """
    Rule 4.1 - PEP04_adr
    weight - 0.7
    There is no information on the real estate or apartment in the city, which indicated as PEP's place of residence
    """

    def calculate_weight(self):
        property_types = [Property.HOUSE, Property.SUMMER_HOUSE, Property.APARTMENT, Property.ROOM]
        declarations_id = Declaration.objects.filter(
            pep_id=self.pep.id,
        ).values_list('id', flat=True).all()[::1]
        for declaration in declarations_id:
            city = Declaration.objects.filter(
                id=declaration,
            ).values_list('city_of_residence_id', flat=True).all()[::1][0]
            property_cities = Property.objects.filter(
                declaration=declaration,
                type__in=property_types,
            ).values_list('city_id', flat=True).all()[::1]
            if not (city in property_cities):
                return 0.4
        return 0


class LiveNowhereRegion(BaseScoringRule):
    """
    Rule 4.2 - PEP04_reg
    weight - 0.1
    There is no information on the real estate or apartment in the region, which indicated as PEP's place of residence
    """

    def calculate_weight(self):
        property_types = [Property.HOUSE, Property.SUMMER_HOUSE, Property.APARTMENT, Property.ROOM]
        declarations_id = Declaration.objects.filter(
            pep_id=self.pep.id,
        ).values_list('id', flat=True).all()[::1]
        for declaration in declarations_id:
            city = Declaration.objects.filter(
                id=declaration,
            ).values_list('city_of_residence_id', flat=True).all()[::1][0]
            region = RatuCity.objects.filter(
                id=city,
            ).values_list('region_id', flat=True).all()[::1][0]
            property_cities = Property.objects.filter(
                declaration=declaration,
                type__in=property_types,
            ).values_list('city_id', flat=True).all()[::1]
            if not property_cities:
                return 0.1
            property_regions = RatuCity.objects.filter(
                id__in=property_cities,
            ).values_list('region_id', flat=True).all()[::1]
            if not (region in property_regions):
                return 0.1
        return 0


class IsNewCars(BaseScoringRule):
    """
    Rule 17 - PEP17
    weight - 0.8
    Declared ownership of vehicle produced after 2013 with an indicated value less than 150000 UAH
    """

    def calculate_weight(self):
        year = 2013  # min production year
        price = 150000  # max vehicle price
        have_weight = Vehicle.objects.filter(
            declaration__pep_id=self.pep.id,
            created_at__year__gt=year,
            valuation__lt=price,
        ).exists()
        if have_weight:
            return 0.8
        return 0


class IsLuxuryCars(BaseScoringRule):
    """
    Rule 18 - PEP18
    weight - 0.4
    Declared ownership and/or right of use of a business class car, or car with a price exceeding
    800000 UAH or brand vehicle, which is considered to be a luxury car
    """

    def calculate_weight(self):
        max_price = 800000  # max price of non-luxury vehicle
        have_car = Vehicle.objects.filter(
            declaration__pep_id=self.pep.id,
            is_luxury=True,
            valuation__gt=max_price,
        ).exists()
        have_rights = VehicleRight.objects.filter(
            pep_id=self.pep.id,
            car__is_luxury=True,
            car__valuation__gt=max_price,
        ).exists()
        if have_car or have_rights:
            return 0.4
        return 0


class CarsCount(BaseScoringRule):
    """
    Rule 19 - PEP19
    weight - 0.4
    Declared ownership and/or right of use of more than 5 cars
    """

    def calculate_weight(self):
        max_count = 5  # max amount of cars
        declarations_id = Declaration.objects.filter(
            pep_id=self.pep.id,
        ).values_list('id', flat=True).all()[::1]
        for declaration in declarations_id:
            have_car = Vehicle.objects.filter(
                declaration=declaration,
            ).count()
            have_rights = VehicleRight.objects.filter(
                pep_id=self.pep.id,
            ).count()
            if have_car + have_rights > max_count:
                return 0.4
        return 0
