"""
Add 40 new dog breeds and 30 new cat breeds to the database.
Safe to run multiple times — skips breeds that already exist.

Usage:
  python3 add_new_breeds.py
"""
from __future__ import annotations

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# New dog breeds: (name, slug, one-sentence description)
# ---------------------------------------------------------------------------
NEW_DOGS = [
    ('Akita', 'akita', 'Powerful, loyal Japanese breed known for its dignified presence and unwavering devotion to family.'),
    ('Alaskan Malamute', 'alaskan-malamute', 'Large, strong Arctic sled dog bred for endurance with a friendly and pack-oriented nature.'),
    ('Basset Hound', 'basset-hound', 'Low-slung, gentle scenthound with soulful eyes and a famously laid-back disposition.'),
    ('Belgian Malinois', 'belgian-malinois', 'Highly driven, athletic herding and working dog favoured by police and military worldwide.'),
    ('Bichon Frise', 'bichon-frise', 'Cheerful, fluffy, and affectionate small companion that thrives on human company.'),
    ('Bloodhound', 'bloodhound', 'Gentle giant with the world\'s most powerful nose, used for trailing and tracking.'),
    ('Boston Terrier', 'boston-terrier', 'Compact, tuxedo-coated American gentleman with a lively and friendly personality.'),
    ('Bull Terrier', 'bull-terrier', 'Distinctive egg-shaped head and muscular build, paired with a playful and clownish nature.'),
    ('Cane Corso', 'cane-corso', 'Majestic Italian mastiff breed that is deeply loyal and a natural guardian of family and property.'),
    ('Cocker Spaniel', 'cocker-spaniel', 'Sweet-natured, merry sporting spaniel with beautiful silky ears and an eager-to-please attitude.'),
    ('Dalmatian', 'dalmatian', 'Striking spotted coach dog with high energy, intelligence, and a love of active exercise.'),
    ('English Springer Spaniel', 'english-springer-spaniel', 'Enthusiastic, versatile hunting and family dog with a friendly and obedient temperament.'),
    ('Great Dane', 'great-dane', 'Gentle giant of the dog world, standing among the tallest breeds yet known for calm affection.'),
    ('Great Pyrenees', 'great-pyrenees', 'Majestic white mountain dog bred to guard livestock, calm and devoted at home.'),
    ('Greyhound', 'greyhound', 'The world\'s fastest dog breed — sleek, sensitive, and surprisingly gentle as a companion.'),
    ('Havanese', 'havanese', 'Cuba\'s national dog, a small, sociable, and silky-coated companion full of lively charm.'),
    ('Irish Setter', 'irish-setter', 'Strikingly beautiful red-coated sporting dog with boundless enthusiasm and a friendly spirit.'),
    ('Irish Wolfhound', 'irish-wolfhound', 'Tallest dog breed in the world, with a gentle giant temperament and ancient Celtic heritage.'),
    ('Jack Russell Terrier', 'jack-russell-terrier', 'Small but fearless working terrier packed with energy, intelligence, and tenacious drive.'),
    ('Maltese', 'maltese', 'Ancient toy breed from the Mediterranean, prized for its flowing white coat and gentle personality.'),
    ('Mastiff', 'mastiff', 'One of the heaviest dog breeds, the English Mastiff is docile, loyal, and a natural protector.'),
    ('Miniature Schnauzer', 'miniature-schnauzer', 'Spirited, intelligent terrier-type breed with a distinctive beard and friendly, adaptable character.'),
    ('Newfoundland', 'newfoundland', 'Enormous, gentle water rescue dog from Canada, famous for its sweet nature and love of swimming.'),
    ('Old English Sheepdog', 'old-english-sheepdog', 'Shaggy, boisterous herding dog with a bear-like appearance and an affectionate, playful soul.'),
    ('Papillon', 'papillon', 'Elegant toy spaniel named for its butterfly-like ears, exceptionally intelligent and agile.'),
    ('Pembroke Welsh Corgi', 'pembroke-welsh-corgi', 'Beloved herding breed favoured by British royalty, known for its big personality in a low-slung body.'),
    ('Pomeranian', 'pomeranian', 'Vivacious, fox-faced spitz toy breed with a luxurious double coat and bold confidence.'),
    ('Portuguese Water Dog', 'portuguese-water-dog', 'Athletic, curly-coated working dog bred to assist fishermen, loyal and low-shedding.'),
    ('Rhodesian Ridgeback', 'rhodesian-ridgeback', 'Athletic African breed with a distinctive back ridge, bred to hunt lions and guard homesteads.'),
    ('Saint Bernard', 'saint-bernard', 'Iconic Swiss rescue dog, enormous in size, gentle in spirit, and patient with family.'),
    ('Samoyed', 'samoyed', 'Cloud-like white spitz breed from Siberia, known for its permanent smile and friendly warmth.'),
    ('Scottish Terrier', 'scottish-terrier', 'Independent, dignified, and feisty Scottish terrier with a distinctive beard and bold character.'),
    ('Shetland Sheepdog', 'shetland-sheepdog', 'Intelligent, agile herding dog from the Shetland Islands, responsive and deeply loyal.'),
    ('Shiba Inu', 'shiba-inu', 'Japan\'s most popular native breed, spirited and fox-like with a fiercely independent personality.'),
    ('Soft Coated Wheaten Terrier', 'soft-coated-wheaten-terrier', 'Exuberant Irish farm dog with a soft, wavy wheat-coloured coat and an enthusiastic personality.'),
    ('Staffordshire Bull Terrier', 'staffordshire-bull-terrier', 'Muscular, courageous British terrier with a surprisingly gentle, child-loving temperament.'),
    ('Vizsla', 'vizsla', 'Elegant, rust-gold Hungarian pointer and retriever that forms intensely close bonds with its family.'),
    ('Weimaraner', 'weimaraner', 'Sleek silver-grey German hunting dog with piercing eyes and an energetic, affectionate nature.'),
    ('West Highland White Terrier', 'west-highland-white-terrier', 'Plucky, confident Scottish terrier with a bright white coat and an independent spirit.'),
    ('Whippet', 'whippet', 'Graceful sighthound of medium size, equally at home sprinting at full speed and curled on the sofa.'),
]

# ---------------------------------------------------------------------------
# New cat breeds: (name, slug, one-sentence description)
# ---------------------------------------------------------------------------
NEW_CATS = [
    ('American Bobtail', 'american-bobtail', 'Naturally short-tailed domestic cat with a wild appearance, playful nature, and dog-like loyalty.'),
    ('American Curl', 'american-curl', 'Distinctive breed with uniquely curled-back ears and a playful, affectionate, kitten-like personality.'),
    ('Bombay', 'bombay', 'Sleek, jet-black cat bred to resemble a miniature panther, with a warm and sociable character.'),
    ('British Longhair', 'british-longhair', 'Calm, plush-coated longer-haired relative of the British Shorthair with the same round, gentle face.'),
    ('Burmilla', 'burmilla', 'Accidental cross between Burmese and Chinchilla Persian, combining beauty with a playful disposition.'),
    ('Chausie', 'chausie', 'Tall, athletic hybrid breed with jungle cat ancestry, highly active and strikingly wild in appearance.'),
    ('Colorpoint Shorthair', 'colorpoint-shorthair', 'Siamese-type breed with extended point colours, equally vocal and sociable as its Siamese parent.'),
    ('Cymric', 'cymric', 'The long-haired version of the Manx, tailless and round-bodied with a gentle and playful temperament.'),
    ('European Shorthair', 'european-shorthair', 'Natural Scandinavian shorthair breed, hardy, balanced in temperament, and adaptable to family life.'),
    ('Havana Brown', 'havana-brown', 'Rare all-chocolate cat with a warm, curious nature and a distinctive whisker-rich muzzle.'),
    ('Japanese Bobtail', 'japanese-bobtail', 'Ancient Japanese breed with a distinctive pom-pom tail, considered a symbol of good luck.'),
    ('Khao Manee', 'khao-manee', 'Sacred white Thai cat with jewel-like eyes, historically kept only by Thai royalty.'),
    ('Korat', 'korat', 'One of the oldest natural breeds from Thailand, a silver-blue cat considered a symbol of good fortune.'),
    ('LaPerm', 'laperm', 'Soft curly-coated breed with a gentle, people-oriented personality and minimal shedding.'),
    ('Lykoi', 'lykoi', 'The "werewolf cat" with a uniquely patchy coat that moults and regrows, intelligent and affectionate.'),
    ('Nebelung', 'nebelung', 'Long-haired blue-grey cat similar to the Russian Blue, reserved with strangers but deeply loyal to family.'),
    ('Ocicat', 'ocicat', 'Spotted wild-looking cat that is entirely domestic in origin, confident, athletic, and highly social.'),
    ('Oriental Shorthair', 'oriental-shorthair', 'Svelte, large-eared Siamese relative available in over 300 colour combinations, vocal and affectionate.'),
    ('Peterbald', 'peterbald', 'Russian hairless breed similar to the Sphynx, graceful, vocal, and extremely people-oriented.'),
    ('Pixiebob', 'pixiebob', 'Wild-looking bobtailed American breed with polydactyl toes and a calm, dog-like temperament.'),
    ('Ragamuffin', 'ragamuffin', 'Large, plush, and intensely affectionate cat closely related to the Ragdoll, loves being held.'),
    ('Scottish Straight', 'scottish-straight', 'Straight-eared cousin of the Scottish Fold, sharing the same round features and calm personality.'),
    ('Serengeti', 'serengeti', 'Long-legged, spotted hybrid breed developed to resemble a serval without wild cat genetics.'),
    ('Singapura', 'singapura', 'The world\'s smallest cat breed, originating from Singapore, with large eyes and a lively curiosity.'),
    ('Snowshoe', 'snowshoe', 'Siamese-derived breed with distinctive white paws and a sociable, gentle personality.'),
    ('Sokoke', 'sokoke', 'Rare East African natural breed with a distinctive modified tabby coat and an active, confident nature.'),
    ('Toyger', 'toyger', 'Domestic cat bred to resemble a tiger in miniature, with bold striping and a relaxed, friendly nature.'),
    ('Tiffanie', 'tiffanie', 'Semi-longhaired Asian breed with Burmese origins, affectionate, intelligent, and strikingly beautiful.'),
    ('Ukrainian Levkoy', 'ukrainian-levkoy', 'Hairless, inward-folded-eared breed from Ukraine, sociable, playful, and affectionate with its family.'),
    ('York Chocolate', 'york-chocolate', 'Rare American breed with a rich chocolate semi-long coat, known for its curious and active nature.'),
]

# ---------------------------------------------------------------------------
# Wikipedia article titles for image fetching (handles disambiguation cases)
# ---------------------------------------------------------------------------
WIKI_TITLES = {
    # Dogs
    'Akita': 'Akita (dog)',
    'Alaskan Malamute': 'Alaskan Malamute',
    'Basset Hound': 'Basset Hound',
    'Belgian Malinois': 'Belgian Malinois',
    'Bichon Frise': 'Bichon Frise',
    'Bloodhound': 'Bloodhound',
    'Boston Terrier': 'Boston Terrier',
    'Bull Terrier': 'Bull Terrier',
    'Cane Corso': 'Cane Corso',
    'Cocker Spaniel': 'American Cocker Spaniel',
    'Dalmatian': 'Dalmatian (dog)',
    'English Springer Spaniel': 'English Springer Spaniel',
    'Great Dane': 'Great Dane',
    'Great Pyrenees': 'Great Pyrenees',
    'Greyhound': 'Greyhound',
    'Havanese': 'Havanese dog',
    'Irish Setter': 'Irish Setter',
    'Irish Wolfhound': 'Irish Wolfhound',
    'Jack Russell Terrier': 'Jack Russell Terrier',
    'Maltese': 'Maltese dog',
    'Mastiff': 'Mastiff',
    'Miniature Schnauzer': 'Miniature Schnauzer',
    'Newfoundland': 'Newfoundland dog',
    'Old English Sheepdog': 'Old English Sheepdog',
    'Papillon': 'Papillon (dog)',
    'Pembroke Welsh Corgi': 'Pembroke Welsh Corgi',
    'Pomeranian': 'Pomeranian (dog)',
    'Portuguese Water Dog': 'Portuguese Water Dog',
    'Rhodesian Ridgeback': 'Rhodesian Ridgeback',
    'Saint Bernard': 'Saint Bernard (dog)',
    'Samoyed': 'Samoyed (dog)',
    'Scottish Terrier': 'Scottish Terrier',
    'Shetland Sheepdog': 'Shetland Sheepdog',
    'Shiba Inu': 'Shiba Inu',
    'Soft Coated Wheaten Terrier': 'Soft-coated Wheaten Terrier',
    'Staffordshire Bull Terrier': 'Staffordshire Bull Terrier',
    'Vizsla': 'Vizsla',
    'Weimaraner': 'Weimaraner',
    'West Highland White Terrier': 'West Highland White Terrier',
    'Whippet': 'Whippet',
    # Cats
    'American Bobtail': 'American Bobtail',
    'American Curl': 'American Curl',
    'Bombay': 'Bombay cat',
    'British Longhair': 'British Longhair',
    'Burmilla': 'Burmilla',
    'Chausie': 'Chausie',
    'Colorpoint Shorthair': 'Colorpoint Shorthair',
    'Cymric': 'Cymric (cat)',
    'European Shorthair': 'European Shorthair',
    'Havana Brown': 'Havana Brown',
    'Japanese Bobtail': 'Japanese Bobtail',
    'Khao Manee': 'Khao Manee',
    'Korat': 'Korat',
    'LaPerm': 'LaPerm',
    'Lykoi': 'Lykoi',
    'Nebelung': 'Nebelung',
    'Ocicat': 'Ocicat',
    'Oriental Shorthair': 'Oriental Shorthair',
    'Peterbald': 'Peterbald',
    'Pixiebob': 'Pixiebob',
    'Ragamuffin': 'Ragamuffin cat',
    'Scottish Straight': 'Scottish Fold',
    'Serengeti': 'Serengeti cat',
    'Singapura': 'Singapura (cat)',
    'Snowshoe': 'Snowshoe cat',
    'Sokoke': 'Sokoke',
    'Toyger': 'Toyger',
    'Tiffanie': 'Asian Semi-longhair',
    'Ukrainian Levkoy': 'Ukrainian Levkoy',
    'York Chocolate': 'York Chocolate',
}


def main() -> None:
    from app import create_app, db
    from app.models import SubCategory, Subject

    app = create_app('development')

    with app.app_context():
        dogs_sub = SubCategory.query.filter_by(slug='dogs').first()
        cats_sub = SubCategory.query.filter_by(slug='cats').first()

        if not dogs_sub:
            logger.error("Dogs subcategory not found — run seed.py first.")
            return
        if not cats_sub:
            logger.error("Cats subcategory not found — run seed.py first.")
            return

        added_dogs = 0
        for name, slug, desc in NEW_DOGS:
            exists = Subject.query.filter_by(
                subcategory_id=dogs_sub.id, slug=slug
            ).first()
            if exists:
                logger.info(f"  skip (exists): {name}")
                continue
            subj = Subject(
                subcategory_id=dogs_sub.id,
                name=name,
                slug=slug,
                description=desc,
            )
            db.session.add(subj)
            added_dogs += 1
            logger.info(f"  + Dog: {name}")

        added_cats = 0
        for name, slug, desc in NEW_CATS:
            exists = Subject.query.filter_by(
                subcategory_id=cats_sub.id, slug=slug
            ).first()
            if exists:
                logger.info(f"  skip (exists): {name}")
                continue
            subj = Subject(
                subcategory_id=cats_sub.id,
                name=name,
                slug=slug,
                description=desc,
            )
            db.session.add(subj)
            added_cats += 1
            logger.info(f"  + Cat: {name}")

        db.session.commit()
        logger.info(
            f"\nDone. Added {added_dogs} new dog breeds and {added_cats} new cat breeds."
        )


if __name__ == '__main__':
    main()
