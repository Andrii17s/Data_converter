"""
Here we are collecting alf functions for cleaning xml records from whitespaces and /
abbreviations, splitting tag.texts and converting strings with date info to datetimes
"""
import binascii
import datetime
import os
import re
import sys

# changing to lowercase, deleting 'р.', 'м.', 'с.', 'смт.', 'смт', 'сщ.', 'с/рада.', 'сщ/рада.', /
# 'вул.' from a string
from django.utils import translation
from num2words import num2words

from business_register.models.company_models import Company, CompanyType
from location_register.models.address_models import Country


def clean_name(name):
    return re.sub(r'р\.|м\.|с\.|смт\.|сщ\.|с/рада\.|сщ/рада\.|вул\.', "", name.lower()).strip()


# a dictionary for storing all abbreviations and full forms
SHORT_TO_FULL_DICT = {
    'вул.': 'вулиця ',
    'бульв.': 'бульвар ',
    'просп.': 'проспект ',
    'пров.': 'провулок ',
    'пл.': 'площа ',
    'р-н': 'район',
    'р-ну': 'району',
    'обл.': 'область',
    'области': 'області'
}


# changing to lowercase and abbreviations to full forms like 'р-н' to 'район' /
# (see all cases in short_to_full_dict)
def change_to_full_name(name):
    name = name.lower()
    for abbr, full_form in SHORT_TO_FULL_DICT.items():
        name = name.replace(abbr, full_form)
    return name


# extracting the first word
def get_first_word(string):
    return string.split()[0]


# getting all words before slash and changing string to lowercase
def get_lowercase_substring_before_slash(string):
    return string.split('/')[0].lower()


# extracting all words except first
def cut_first_word(string):
    words_after_first = string.split()[1:]
    return " ".join(words_after_first)


# deleting ';' from a string, changing '/' to '.', then converting it to the datetime format 'Y-m-d'
def format_date_to_yymmdd(str_ddmmyy):
    if str_ddmmyy:
        if ';' in str_ddmmyy:
            str_ddmmyy = str_ddmmyy.replace(";", "")
        if '/' in str_ddmmyy:
            str_ddmmyy = str_ddmmyy.replace("/", ".")
        try:
            if sys.platform.startswith('linux'):
                date = datetime.datetime.strptime(str_ddmmyy, "%d.%m.%Y").strftime("%4Y-%m-%d")
            else:
                date = datetime.datetime.strptime(str_ddmmyy, "%d.%m.%Y").strftime("%Y-%m-%d")
        except ValueError:
            return None
        return date


#  converting datetime format from '%d.%m.%Y' to 'Y-m-d'
def simple_format_date_to_yymmdd(str_ddmmyy):
    try:
        date = datetime.datetime.strptime(str_ddmmyy, "%d.%m.%Y").strftime("%Y-%m-%d")
    except ValueError:
        return None
    return date


# checking if exists, then converting to string
def to_lower_string_if_exists(value):
    if value:
        return str(value).lower()
    return None


def generate_key():
    return binascii.hexlify(os.urandom(20)).decode()


def uah2words(value):
    lang = translation.get_language()
    if lang == 'uk':
        amount_words = num2words(
            float(value), lang=lang, to='currency',
            currency='UAH', separator=' ', cents=False,
        )
    else:
        uah, kop = divmod(value, 1)
        kop = round(kop * 100)
        amount_words = f'{num2words(uah, lang=lang, to="cardinal")} hryvnias {kop:02} kopiyok'
    return amount_words


class Timer():

    def __init__(self):
        self.previous = datetime.datetime.now()
        self.times_dict = {}
        self.times_dict['total\t\t\t'] = datetime.timedelta()

    def time_it(self, period_name: str):
        now = datetime.datetime.now()
        if period_name in self.times_dict:
            self.times_dict[period_name] += now - self.previous
        else:
            self.times_dict[period_name] = now - self.previous
        self.times_dict['total\t\t\t'] += now - self.previous
        self.previous = now

    def print_result(self):
        sorted_times_array = sorted(self.times_dict.items(), key=lambda item: item[1], reverse=True)
        self.times_dict = dict(sorted_times_array[1:] + sorted_times_array[:1])
        print('----------------------------------------------------------------------------------')
        for period_name, value in self.times_dict.items():
            print(period_name, '\t', str(value).split(".")[0], '\t',
                  round(value / self.times_dict['total\t\t\t'] * 100, 2), '%')
        print('----------------------------------------------------------------------------------')


def replace_incorrect_symbols(string):
    string = string \
        .strip() \
        .replace('\t', ' ') \
        .replace('\r', '') \
        .replace('\n', ' ') \
        .replace('’', "'") \
        .replace('—', '-') \
        .replace('–', '-') \
        .replace('−', '-') \
        .replace('\xa0', ' ') \
        .replace('«', '"') \
        .replace('»', '"') \
        .replace("''", '"')
    string = re.sub(r'\s+', ' ', string)
    return string


ukr_to_en_first_char = {
    'є': 'ye',
    'ї': 'yi',
    'й': 'y',
    'ю': 'yu',
    'я': 'ya',
    'Й': 'Y',
    'Ю': 'Yu',
    'Я': 'Ya',
    'Ї': 'Yi',
    'Є': 'Ye'
}
ukr_to_en = {
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'h',
    'ґ': 'g',
    'д': 'd',
    'е': 'e',
    'є': 'ie',
    'ё': 'jo',
    'ж': 'zh',
    'з': 'z',
    'и': 'y',
    'і': 'i',
    'ї': 'i',
    'й': 'i',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'kh',
    'ц': 'ts',
    'ч': 'ch',
    'ш': 'sh',
    'щ': 'shch',
    'ъ': '',
    'ы': 'y',
    'ь': '',
    'э': 'e',
    'ю': 'iu',
    'я': 'ia',
    'А': 'A',
    'Б': 'B',
    'В': 'V',
    'Г': 'H',
    'Ґ': 'G',
    'Д': 'D',
    'Е': 'E',
    'Ё': 'Jo',
    'Ж': 'Zh',
    'З': 'Z',
    'И': 'Y',
    'Й': 'I',
    'К': 'K',
    'Л': 'L',
    'М': 'M',
    'Н': 'N',
    'О': 'O',
    'П': 'P',
    'Р': 'R',
    'С': 'S',
    'Т': 'T',
    'У': 'U',
    'Ф': 'F',
    'Х': 'Kh',
    'Ц': 'Ts',
    'Ч': 'Ch',
    'Ш': 'Sh',
    'Щ': 'Shch',
    'Ъ': '',
    'Ы': 'Y',
    'Ь': '',
    'Э': 'E',
    'Ю': 'Iu',
    'Я': 'Ia',
    '’': '',
    'І': 'I',
    'Ї': 'I',
    'Є': 'Ie'
}


def transliterate(string):
    word_list = re.split('(\W|\d)', string)
    new_string = ''
    for word in word_list:
        new_word = ''
        for char in word:
            if word.index(char) == 0:
                new_word += ukr_to_en_first_char.get(char, ukr_to_en.get(char, char))
            else:
                new_word += ukr_to_en.get(char, char)
        new_word = new_word.title() if word.istitle() else new_word
        new_word = new_word.upper() if word.isupper() else new_word
        new_string += new_word
    return new_string


def transliterate_field(string, field_name=None):
    if not field_name:
        return transliterate(string)
    else:
        string_parts = re.split('("|«|\'\'|,)', string, 1)
        first_string_part = string_parts[0].strip().lower()
        if field_name == 'company_name':
            company_type = CompanyType.objects.filter(name=first_string_part).first()
            if company_type:
                new_first_string_part = company_type.name_eng + ' '
            else:
                new_first_string_part = transliterate(first_string_part)
        elif field_name == 'address':
            country = Country.objects.filter(name_uk=first_string_part).first()
            if country:
                new_first_string_part = country.name.title()
            else:
                new_first_string_part = transliterate(first_string_part)
        else:
            return transliterate(string)
        return new_first_string_part + transliterate(''.join(string_parts[1:]))
