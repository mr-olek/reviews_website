"""Russian breed name translations for Russian review sites."""

# Maps English breed name → Russian search term
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
}


def to_russian(english_name: str) -> str:
    """Return Russian name for a breed, falling back to English if unknown."""
    return BREED_RU.get(english_name, english_name)
