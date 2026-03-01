"""Russian breed name translations and irecommend.ru content slugs."""

# Maps English breed name → Russian search term (used by otzovik)
BREED_RU = {
    # Dogs
    'Labrador Retriever': 'лабрадор ретривер',
    'German Shepherd': 'немецкая овчарка',
    'Golden Retriever': 'золотистый ретривер',
    'French Bulldog': 'французский бульдог',
    'Bulldog': 'английский бульдог',
    'Poodle': 'пудель',
    'Beagle': 'бигль',
    'Rottweiler': 'ротвейлер',
    'German Shorthaired Pointer': 'курцхаар',
    'Dachshund': 'такса',
    # Cats
    'Maine Coon': 'мейн-кун',
    'Persian': 'персидская кошка',
    'Ragdoll': 'рэгдолл',
    'Siamese': 'сиамская кошка',
    'British Shorthair': 'британская короткошерстная',
    'Abyssinian': 'абиссинская кошка',
    'Scottish Fold': 'шотландская вислоухая',
    'Sphynx': 'сфинкс кошка',
    'Bengal': 'бенгальская кошка',
    'Russian Blue': 'русская голубая кошка',
    'Norwegian Forest Cat': 'норвежская лесная кошка',
    'Burmese': 'бурманская кошка',
    'Devon Rex': 'девон рекс',
    'American Shorthair': 'американская короткошерстная',
    'Exotic Shorthair': 'экзотическая короткошерстная',
    'Birman': 'священная бирма',
    'Tonkinese': 'тонкинская кошка',
    'Himalayan': 'гималайская кошка',
    'Turkish Angora': 'турецкая ангора',
    'Chartreux': 'картезианская кошка',
}

# Maps English breed name → irecommend.ru /content/<slug> for the breed landing page
IRECOMMEND_SLUG = {
    # Dogs
    'Labrador Retriever': 'labrador-retriver',
    'German Shepherd': 'nemetskaya-ovcharka',
    'Golden Retriever': 'golden-retriver',
    'French Bulldog': 'frantsuzskii-buldog',
    'Bulldog': 'angliiskii-buldogbuldog',
    'Poodle': 'pudel',
    'Beagle': 'bigl',
    'Rottweiler': 'rotveler',
    'German Shorthaired Pointer': 'nemetskii-kratkhaar-kurtskhaar',
    'Dachshund': 'taksa',
    # Cats
    'Maine Coon': 'mein-kun',
    'Persian': 'persidskii',
    'Ragdoll': 'regdoll',
    'Siamese': 'siamskaya-koshka',
    'British Shorthair': 'britanskaya-korotkosherstnaya',
    'Abyssinian': 'abissinskaya-koshka',
    'Scottish Fold': 'skottish-fold-shotlandskaya-visloukhaya-koshka',
    'Sphynx': 'kanadskii-sfinks',
    'Bengal': 'bengalskaya-koshka',
    'Russian Blue': 'russkaya-golubaya',
    'Norwegian Forest Cat': 'norvezhskaya-lesnaya-koshka',
    'Burmese': 'evropeiskaya-burmansksaya-koshka',
    'Devon Rex': 'devon-reks',
    'Exotic Shorthair': 'ekzoticheskaya-korotkosherstnaya',
    'Birman': 'birmanskayasvyashchennaya-birma',
    'Tonkinese': 'tonkinskaya-tonkinez-0',
    'Himalayan': 'gimalaiskaya-koshka',
    'Turkish Angora': 'turetskaya-angora',
    'Chartreux': 'shartrez',
}


def to_russian(english_name: str) -> str:
    """Return Russian name for a breed, falling back to English if unknown."""
    return BREED_RU.get(english_name, english_name)


def to_irecommend_slug(english_name: str):
    """Return irecommend.ru content slug, or None if unknown."""
    return IRECOMMEND_SLUG.get(english_name)
