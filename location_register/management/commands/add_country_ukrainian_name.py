from django.core.management import BaseCommand
from location_register.models.address_models import Country


class Command(BaseCommand):
    help = 'Add or update name and name_uk in Country model'

    def handle(self, *args, **options):
        countries = countries_dict()
        for country in countries:
            nacp_id = country
            country_uk = countries[country][0]
            country_en = countries[country][1]
            country, created = Country.objects.update_or_create(
                name=country_en, defaults={'nacp_id': nacp_id, 'name_uk': country_uk}
            )
            if created:
                self.stdout.write(f'New country {country_en}')
        self.stdout.write('Done!')


def countries_dict():
    return {
        '1': ['україна', 'ukraine'],
        '2': ['австралія', 'australia'],
        '3': ['австрія', 'austria'],
        '4': ['азербайджан', 'azerbaijan'],
        '5': ['аландські острови', 'aland islands'],
        '6': ['албанія', 'albania'],
        '7': ['алжир', 'algeria'],
        '8': ['американське самоа', 'american samoa'],
        '9': ['американські віргінські острови', 'virgin islands (u.s.)'],
        '10': ['ангілья', 'anguilla'],
        '11': ['ангола', 'angola'],
        '12': ['андорра', 'andorra'],
        '13': ['антарктида', 'antarctica'],
        '14': ['антигуа і барбуда', 'antigua and barbuda'],
        '15': ['аргентина', 'argentina'],
        '16': ['аруба', 'aruba'],
        '17': ['афганістан', 'afghanistan'],
        '18': ['багамські острови', 'bahamas'],
        '19': ['бангладеш', 'bangladesh'],
        '20': ['барбадос', 'barbados'],
        '21': ['бахрейн', 'bahrain'],
        '22': ['беліз', 'belize'],
        '23': ['бельгія', 'belgium'],
        '24': ['бенін', 'benin'],
        '25': ['бермудські острови', 'bermuda'],
        '26': ['білорусь', 'belarus'],
        '27': ['болгарія', 'bulgaria'],
        '28': ['болівія', 'bolivia'],
        '29': ['боснія і герцеговина', 'bosnia herzegovina'],
        '30': ['ботсвана', 'botswana'],
        '31': ['бразилія', 'brazil'],
        '32': ['британська територія в індійському океані', 'british territory in the indian ocean'],
        '33': ['британські віргінські острови', 'virgin islands (british)'],
        '34': ['бруней', 'brunei'],
        '35': ['буркіна-фасо', 'burkina faso'],
        '36': ['бурунді', 'burundi'],
        '37': ['бутан', 'bhutan'],
        '38': ['вануату', 'vanuatu'],
        '39': ['ватикан', 'vatican city state'],
        '40': ['велика британія', 'great britain'],
        '41': ['венесуела', 'venezuela'],
        '42': ['в\'єтнам', 'vietnam'],
        '43': ['вірменія', 'armenia'],
        '44': ['волліс і футуна', 'wallis and futuna'],
        '45': ['габон', 'gabon'],
        '46': ['гаїті', 'haiti'],
        '48': ['гамбія', 'gambia'],
        '49': ['гана', 'ghana'],
        '47': ['гаяна', 'guyana'],
        '50': ['гваделупа', 'guadeloupe'],
        '51': ['гватемала', 'guatemala'],
        '52': ['гвінея', 'guinea'],
        '53': ['гвінея-бісау', 'guinea-bissau'],
        '54': ['гернсі', 'guernsey'],
        '61': ['гібралтар', 'gibraltar'],
        '55': ['гондурас', 'honduras'],
        '56': ['гонконг', 'hong kong'],
        '57': ['гренада', 'grenada'],
        '62': ['ґренландія', 'greenland'],
        '58': ['греція', 'greece'],
        '59': ['грузія', 'georgia'],
        '60': ['гуам', 'guam'],
        '63': ['данія', 'denmark'],
        '65': ['джерсі', 'jersey'],
        '66': ['джибуті', 'djibouti'],
        '67': ['домініка', 'dominica'],
        '68': ['домініканська республіка', 'dominican republic'],
        '64': ['др конго', 'congo, (republic of)'],
        '70': ['еквадор', 'ecuador'],
        '71': ['екваторіальна гвінея', 'equatorial guinea'],
        '72': ['еритрея', 'eritrea'],
        '73': ['естонія', 'estonia'],
        '74': ['ефіопія', 'ethiopia'],
        '75': ['єгипет', 'egypt'],
        '76': ['ємен', 'yemen'],
        '77': ['замбія', 'zambia'],
        '78': ['західна сахара', 'western sahara'],
        '79': ['зімбабве', 'zimbabwe'],
        '69': ['зовнішні малі острови сша', 'united states minor outlying islands'],
        '80': ['ізраїль', 'israel'],
        '81': ['індія', 'india'],
        '82': ['індонезія', 'indonesia'],
        '83': ['ірак', 'iraq'],
        '84': ['іран', 'iran'],
        '85': ['ірландія', 'ireland'],
        '86': ['ісландія', 'iceland'],
        '87': ['іспанія', 'spain'],
        '88': ['італія', 'italy'],
        '89': ['йорданія', 'jordan'],
        '90': ['кабо-верде', 'cape verde'],
        '91': ['казахстан', 'kazakhstan'],
        '92': ['кайманові острови', 'cayman islands'],
        '93': ['камбоджа', 'cambodia'],
        '94': ['камерун', 'cameroon'],
        '95': ['канада', 'canada'],
        '96': ['катар', 'qatar'],
        '97': ['кенія', 'kenya'],
        '98': ['киргизстан', 'kyrgyzstan'],
        '101': ['кіпр', 'cyprus'],
        '102': ['кірибаті', 'kiribati'],
        '99': ['китай', 'china'],
        '103': ['кокосові острови (кілінг)', 'cocos (keeling) islands'],
        '104': ['колумбія', 'colombia'],
        '105': ['коморські острови', 'comoros'],
        '106': ['конго', 'congo'],
        '107': ['коста-рика', 'costa rica'],
        '108': ['кот-д\'івуар', 'cote d\'ivoire'],
        '109': ['куба', 'cuba'],
        '110': ['кувейт', 'kuwait'],
        '111': ['лаоська народно-демократична республіка', 'lao people\'s democratic republic'],
        '112': ['латвія', 'latvia'],
        '113': ['лесото', 'lesotho'],
        '114': ['литва', 'lithuania'],
        '115': ['ліберія', 'liberia'],
        '116': ['ліван', 'lebanon'],
        '117': ['лівія', 'livia'],
        '118': ['ліхтенштейн', 'liechtenstein'],
        '119': ['люксембург', 'luxembourg'],
        '120': ['маврикій', 'mauritius'],
        '121': ['мавританія', 'mauritania'],
        '122': ['мадагаскар', 'madagascar'],
        '123': ['майотта', 'mayotte'],
        '124': ['макао', 'macau'],
        '125': ['македонія', 'macedonia (the former yugoslav republic of)'],
        '126': ['малаві', 'malawi'],
        '127': ['малайзія', 'malaysia'],
        '128': ['малі', 'mali'],
        '129': ['мальдіви', 'maldives'],
        '130': ['мальта', 'malta'],
        '131': ['марокко', 'morocco'],
        '132': ['мартиніка', 'martinique'],
        '133': ['маршаллові острови', 'marshall islands'],
        '134': ['мексика', 'mexico'],
        '135': ['мозамбік', 'mozambique'],
        '136': ['молдова', 'moldova (republic of)'],
        '137': ['монако', 'monaco'],
        '138': ['монголія', 'mongolia'],
        '139': ['монтсеррат', 'montserrat'],
        '140': ['м\'янма', 'myanmar'],
        '141': ['намібія', 'namibia'],
        '142': ['науру', 'nauru'],
        '143': ['непал', 'nepal'],
        '144': ['нігер', 'niger (republic of)'],
        '145': ['нігерія', 'nigeria'],
        '146': ['нідерланди', 'netherlands'],
        '147': ['нідерландські антильські острови', 'netherlands antilles'],
        '148': ['нікарагуа', 'nicaragua'],
        '149': ['німеччина', 'germany'],
        '150': ['ніуе', 'niue'],
        '151': ['нова зеландія', 'new zealand'],
        '152': ['нова каледонія', 'new caledonia'],
        '153': ['норвегія', 'norway'],
        '154': ['об\'єднані арабські емірати', 'united arab emirates'],
        '155': ['оман', 'oman'],
        '156': ['острів буве', 'bouvet island'],
        '157': ['острів мен', 'isle of man'],
        '158': ['острів норфолк', 'norfolk island'],
        '159': ['острів різдва', 'christmas island'],
        '161': ['острови герд і макдональд', 'heard island and mcdonald islands'],
        '162': ['острови кука', 'cook islands'],
        '160': ['острови святої єлени, вознесіння і тристан-да-кунья',
                'saint helena, ascension and tristan da cunha'],
        '214': ['острови теркс і кайкос', 'turks & caicos islands'],
        '163': ['пакистан', 'pakistan'],
        '164': ['палау', 'palau'],
        '165': ['палестина', 'palestine'],
        '166': ['панама', 'panama'],
        '167': ['папуа - нова гвінея', 'papua new guinea'],
        '173': ['південно-африканська республіка', 'south african republic'],
        '168': ['парагвай', 'paraguay'],
        '169': ['перу', 'peru'],
        '170': ['південна джорджія та південні сандвічеві острови',
                'south georgia and the south sandwich islands'],
        '171': ['південна корея', 'south korea'],
        '172': ['південний судан', 'south sudan (republic of)'],
        '100': ['північна корея', 'korea (republic of)'],
        '174': ['північні маріанські острови',
                'northern mariana islands'],
        '175': ['піткерн', 'the pitcairn islands'],
        '176': ['польща', 'poland'],
        '177': ['португалія', 'portugal'],
        '178': ['пуерто-рико', 'puerto rico'],
        '179': ['реюньйон', 'reunion'],
        '180': ['росія', 'russia'],
        '181': ['руанда', 'rwanda'],
        '182': ['румунія', 'romania'],
        '183': ['сальвадор', 'el salvador'],
        '184': ['самоа', 'samoa'],
        '185': ['сан-марино', 'san marino'],
        '186': ['сан-томе і принсіпі', 'sao tome and principe'],
        '187': ['саудівська аравія', 'saudi arabia'],
        '188': ['свазіленд', 'swaziland'],
        '189': ['свальбард і ян-маєн', 'svalbard and yang-mayen'],
        '190': ['сейшельські острови', 'seychelles'],
        '191': ['сен-бартельмі', 'saint barthelemy'],
        '192': ['сенегал', 'senegal'],
        '193': ['сен-мартін', 'saint-martin'],
        '194': ['сен-п\'єр і мікелон', 'saint pierre and miquelon'],
        '195': ['сент-вінсент і гренадини', 'st vincent'],
        '196': ['сент-кіттс і невіс', 'saint kitts and nevis'],
        '197': ['сент-люсія', 'saint lucia'],
        '198': ['сербія', 'serbia (republic of)'],
        '199': ['сирія', 'syria'],
        '200': ['сінгапур', 'singapore'],
        '201': ['словаччина', 'slovakia'],
        '202': ['словенія', 'slovenia'],
        '203': ['соломонові острови', 'solomon islands'],
        '204': ['сомалі', 'somalia'],
        '206': ['судан', 'sudan'],
        '207': ['суринам', 'suriname'],
        '208': ['східний тимор', 'east timor'],
        '205': ['сполучені штати америки', 'united states of america'],
        '209': ['сьєрра-леоне', 'sierra leone'],
        '210': ['таджикистан', 'tajikistan'],
        '211': ['таїланд', 'thailand'],
        '212': ['тайвань', 'taiwan'],
        '213': ['танзанія', 'tanzania'],
        '215': ['того', 'togo'],
        '216': ['токелау', 'tokelau'],
        '217': ['тонга', 'tonga'],
        '218': ['тринідад і тобаго', 'trinidad and tobago'],
        '219': ['тувалу', 'tuvalu'],
        '220': ['туніс', 'tunisia'],
        '221': ['туреччина', 'turkey'],
        '222': ['туркменістан', 'turkmenistan'],
        '223': ['уганда', 'uganda'],
        '224': ['угорщина', 'hungary'],
        '225': ['узбекистан', 'uzbekistan'],
        '227': ['уругвай', 'uruguay'],
        '228': ['фарерські острови', 'faroe islands'],
        '229': ['федеративні штати мікронезії', 'micronesia, federated states of'],
        '230': ['фіджі', 'fiji'],
        '231': ['філіппіни', 'philippines'],
        '232': ['фінляндія', 'finland'],
        '233': ['фолклендські (мальвінські) острови', 'falkland islands'],
        '234': ['франція', 'france'],
        '235': ['французька гвіана', 'guyane (french)'],
        '236': ['французька полінезія', 'polynesia (french)'],
        '237': ['французькі південні території', 'french southern territories'],
        '238': ['хорватія', 'croatia'],
        '239': ['центральноафриканська республіка', 'central african republic'],
        '240': ['чад', 'chad'],
        '241': ['чехія', 'czech republic'],
        '242': ['чилі', 'chile'],
        '243': ['чорногорія', 'montenegro'],
        '244': ['швейцарія', 'switzerland'],
        '245': ['швеція', 'sweden'],
        '246': ['шрі-ланка', 'sri lanka'],
        '247': ['ямайка', 'jamaica'],
        '248': ['японія', 'japan'],
    }
