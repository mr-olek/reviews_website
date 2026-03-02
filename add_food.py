#!/usr/bin/env python3
"""Seed Food & Cuisines category with 62 country cuisines, dishes, and reviews."""
import os, sys, random, time, requests, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Category, SubCategory, Subject, Review

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
SESSION = requests.Session()
SESSION.headers['User-Agent'] = 'Mozilla/5.0 (compatible; VerdictlyBot/1.0)'

# ---------------------------------------------------------------------------
# 62 cuisines ordered: Ukraine first, then by global popularity
# Each entry: (Display Name, slug, [dishes], wiki_article_for_cuisine_image)
# ---------------------------------------------------------------------------
CUISINES = [
    ('Ukrainian Cuisine', 'ukrainian', [
        'Borscht', 'Varenyky', 'Holubtsi', 'Chicken Kyiv',
        'Deruny', 'Kapusniak', 'Syrniki', 'Pampushky',
    ], 'Ukrainian cuisine'),
    ('Italian Cuisine', 'italian', [
        'Pizza Margherita', 'Spaghetti Carbonara', 'Risotto', 'Lasagne',
        'Tiramisu', 'Bruschetta', 'Osso Buco', 'Gelato',
    ], 'Italian cuisine'),
    ('Japanese Cuisine', 'japanese', [
        'Sushi', 'Ramen', 'Tempura', 'Sashimi',
        'Tonkatsu', 'Udon', 'Miso Soup', 'Takoyaki',
    ], 'Japanese cuisine'),
    ('Chinese Cuisine', 'chinese', [
        'Dim Sum', 'Peking Duck', 'Kung Pao Chicken', 'Mapo Tofu',
        'Hot Pot', 'Dumplings', 'Sweet and Sour Pork', 'Fried Rice',
    ], 'Chinese cuisine'),
    ('Mexican Cuisine', 'mexican', [
        'Tacos', 'Guacamole', 'Enchiladas', 'Tamales',
        'Pozole', 'Mole', 'Quesadillas', 'Chiles Rellenos',
    ], 'Mexican cuisine'),
    ('Indian Cuisine', 'indian', [
        'Butter Chicken', 'Biryani', 'Samosa', 'Dal Makhani',
        'Palak Paneer', 'Naan', 'Tikka Masala', 'Tandoori Chicken',
    ], 'Indian cuisine'),
    ('French Cuisine', 'french', [
        'Croissant', 'Coq au Vin', 'Bouillabaisse', 'Ratatouille',
        'Crème Brûlée', 'Quiche Lorraine', 'French Onion Soup', 'Foie Gras',
    ], 'French cuisine'),
    ('American Cuisine', 'american', [
        'Cheeseburger', 'Mac and Cheese', 'BBQ Ribs', 'Clam Chowder',
        'Apple Pie', 'Fried Chicken', 'New York Cheesecake', 'Lobster Roll',
    ], 'American cuisine'),
    ('Thai Cuisine', 'thai', [
        'Pad Thai', 'Green Curry', 'Tom Yum Soup', 'Som Tum',
        'Massaman Curry', 'Mango Sticky Rice', 'Pad See Ew', 'Thai Spring Rolls',
    ], 'Thai cuisine'),
    ('Greek Cuisine', 'greek', [
        'Moussaka', 'Souvlaki', 'Spanakopita', 'Greek Salad',
        'Tzatziki', 'Baklava', 'Gyros', 'Dolmades',
    ], 'Greek cuisine'),
    ('Spanish Cuisine', 'spanish', [
        'Paella', 'Gazpacho', 'Tortilla Española', 'Jamón Ibérico',
        'Churros', 'Patatas Bravas', 'Croquetas', 'Crema Catalana',
    ], 'Spanish cuisine'),
    ('Turkish Cuisine', 'turkish', [
        'Kebab', 'Baklava', 'Dolma', 'Manti',
        'Lahmacun', 'Menemen', 'Börek', 'Turkish Delight',
    ], 'Turkish cuisine'),
    ('Lebanese Cuisine', 'lebanese', [
        'Hummus', 'Falafel', 'Tabbouleh', 'Shawarma',
        'Fattoush', 'Kibbeh', 'Manakish', 'Kafta',
    ], 'Lebanese cuisine'),
    ('Korean Cuisine', 'korean', [
        'Kimchi', 'Bibimbap', 'Bulgogi', 'Tteokbokki',
        'Korean Fried Chicken', 'Japchae', 'Sundubu Jjigae', 'Kimbap',
    ], 'Korean cuisine'),
    ('Vietnamese Cuisine', 'vietnamese', [
        'Pho', 'Banh Mi', 'Goi Cuon', 'Bun Bo Hue',
        'Com Tam', 'Banh Xeo', 'Cao Lau', 'Cha Gio',
    ], 'Vietnamese cuisine'),
    ('Moroccan Cuisine', 'moroccan', [
        'Tagine', 'Couscous', 'Pastilla', 'Harira',
        'Mechoui', 'Bastilla', 'Kefta', 'Moroccan Mint Tea',
    ], 'Moroccan cuisine'),
    ('Ethiopian Cuisine', 'ethiopian', [
        'Injera', 'Doro Wat', 'Tibs', 'Kitfo',
        'Shiro', 'Misir Wat', 'Gored Gored', 'Ayib',
    ], 'Ethiopian cuisine'),
    ('Brazilian Cuisine', 'brazilian', [
        'Feijoada', 'Churrasco', 'Pão de Queijo', 'Coxinha',
        'Moqueca', 'Brigadeiro', 'Acarajé', 'Caipirinha',
    ], 'Brazilian cuisine'),
    ('Peruvian Cuisine', 'peruvian', [
        'Ceviche', 'Lomo Saltado', 'Aji de Gallina', 'Causa Rellena',
        'Pollo a la Brasa', 'Anticuchos', 'Tiradito', 'Arroz con Leche',
    ], 'Peruvian cuisine'),
    ('German Cuisine', 'german', [
        'Bratwurst', 'Schnitzel', 'Sauerbraten', 'Pretzels',
        'Sauerkraut', 'Black Forest Cake', 'Kartoffelsalat', 'Currywurst',
    ], 'German cuisine'),
    ('British Cuisine', 'british', [
        'Fish and Chips', 'Full English Breakfast', 'Roast Beef', 'Shepherd\'s Pie',
        'Bangers and Mash', 'Sticky Toffee Pudding', 'Cornish Pasty', 'Scotch Egg',
    ], 'British cuisine'),
    ('Russian Cuisine', 'russian', [
        'Beef Stroganoff', 'Pelmeni', 'Borscht', 'Blini',
        'Olivier Salad', 'Okroshka', 'Shashlik', 'Solyanka',
    ], 'Russian cuisine'),
    ('Indonesian Cuisine', 'indonesian', [
        'Nasi Goreng', 'Rendang', 'Satay', 'Gado-Gado',
        'Soto Ayam', 'Bakso', 'Tempeh', 'Sate Lilit',
    ], 'Indonesian cuisine'),
    ('Malaysian Cuisine', 'malaysian', [
        'Nasi Lemak', 'Laksa', 'Char Kway Teow', 'Roti Canai',
        'Hainanese Chicken Rice', 'Beef Rendang', 'Satay', 'Cendol',
    ], 'Malaysian cuisine'),
    ('Filipino Cuisine', 'filipino', [
        'Adobo', 'Sinigang', 'Lechon', 'Kare-Kare',
        'Pancit', 'Lumpia', 'Halo-Halo', 'Sisig',
    ], 'Filipino cuisine'),
    ('Portuguese Cuisine', 'portuguese', [
        'Pastel de Nata', 'Bacalhau', 'Caldo Verde', 'Francesinha',
        'Sardinhas Assadas', 'Arroz de Pato', 'Bifanas', 'Piri Piri Chicken',
    ], 'Portuguese cuisine'),
    ('Argentinian Cuisine', 'argentinian', [
        'Asado', 'Empanadas', 'Milanesa', 'Chimichurri',
        'Medialunas', 'Locro', 'Dulce de Leche', 'Alfajores',
    ], 'Argentine cuisine'),
    ('Swedish Cuisine', 'swedish', [
        'Meatballs', 'Gravlax', 'Smörgåsbord', 'Janssons Frestelse',
        'Köttbullar', 'Räkmacka', 'Husmanskost', 'Semla',
    ], 'Swedish cuisine'),
    ('Polish Cuisine', 'polish', [
        'Pierogi', 'Bigos', 'Żurek', 'Kotlet Schabowy',
        'Gołąbki', 'Flaczki', 'Barszcz', 'Makowiec',
    ], 'Polish cuisine'),
    ('Hungarian Cuisine', 'hungarian', [
        'Goulash', 'Chicken Paprikash', 'Langos', 'Halászlé',
        'Töltött Káposzta', 'Kürtőskalács', 'Dobos Torte', 'Lecsó',
    ], 'Hungarian cuisine'),
    ('Georgian Cuisine', 'georgian', [
        'Khachapuri', 'Khinkali', 'Churchkhela', 'Lobiani',
        'Pkhali', 'Ojakhuri', 'Badrijani Nigvzit', 'Chakapuli',
    ], 'Georgian cuisine'),
    ('Iranian Cuisine', 'iranian', [
        'Ghormeh Sabzi', 'Chelo Kebab', 'Ash Reshteh', 'Fesenjan',
        'Tahdig', 'Khoresh Bademjan', 'Mirza Ghasemi', 'Baghali Polo',
    ], 'Iranian cuisine'),
    ('Israeli Cuisine', 'israeli', [
        'Shakshuka', 'Falafel', 'Sabich', 'Israeli Salad',
        'Burekas', 'Hummus', 'Jachnun', 'Malabi',
    ], 'Israeli cuisine'),
    ('Egyptian Cuisine', 'egyptian', [
        'Koshari', 'Ful Medames', 'Molokhia', 'Feteer Meshaltet',
        'Hawawshi', 'Om Ali', 'Basbousa', 'Aish Baladi',
    ], 'Egyptian cuisine'),
    ('Nigerian Cuisine', 'nigerian', [
        'Jollof Rice', 'Egusi Soup', 'Suya', 'Puff Puff',
        'Moi Moi', 'Pepper Soup', 'Akara', 'Ogbono Soup',
    ], 'Nigerian cuisine'),
    ('South African Cuisine', 'south-african', [
        'Braai', 'Bobotie', 'Bunny Chow', 'Biltong',
        'Boerewors', 'Melktert', 'Koeksisters', 'Chakalaka',
    ], 'South African cuisine'),
    ('Pakistani Cuisine', 'pakistani', [
        'Biryani', 'Nihari', 'Haleem', 'Seekh Kebab',
        'Chapli Kebab', 'Daal Chawal', 'Karahi', 'Kheer',
    ], 'Pakistani cuisine'),
    ('Sri Lankan Cuisine', 'sri-lankan', [
        'Rice and Curry', 'Kottu Roti', 'Hoppers', 'Fish Ambul Thiyal',
        'Lamprais', 'Pol Sambol', 'Watalappam', 'String Hoppers',
    ], 'Sri Lankan cuisine'),
    ('Cambodian Cuisine', 'cambodian', [
        'Amok', 'Lok Lak', 'Bai Sach Chrouk', 'Nom Banh Chok',
        'Kuy Teav', 'Samlor Korko', 'Pleah Sach Ko', 'Banh Chiao',
    ], 'Cambodian cuisine'),
    ('Singaporean Cuisine', 'singaporean', [
        'Chicken Rice', 'Chilli Crab', 'Laksa', 'Char Kway Teow',
        'Bak Kut Teh', 'Satay', 'Roti Prata', 'Nasi Lemak',
    ], 'Singaporean cuisine'),
    ('Taiwanese Cuisine', 'taiwanese', [
        'Beef Noodle Soup', 'Scallion Pancake', 'Oyster Omelette', 'Pork Chop Rice',
        'Stinky Tofu', 'Bubble Tea', 'Lu Rou Fan', 'Gua Bao',
    ], 'Taiwanese cuisine'),
    ('Australian Cuisine', 'australian', [
        'Vegemite Toast', 'Pavlova', 'Lamington', 'Tim Tam',
        'Barramundi', 'Meat Pie', 'ANZAC Biscuit', 'Fairy Bread',
    ], 'Australian cuisine'),
    ('Canadian Cuisine', 'canadian', [
        'Poutine', 'Butter Tart', 'BeaverTail', 'Tourtière',
        'Nanaimo Bar', 'Montreal Smoked Meat', 'Peameal Bacon', 'Split Pea Soup',
    ], 'Canadian cuisine'),
    ('Jamaican Cuisine', 'jamaican', [
        'Jerk Chicken', 'Ackee and Saltfish', 'Curry Goat', 'Oxtail Stew',
        'Rice and Peas', 'Patty', 'Escovitch Fish', 'Bammy',
    ], 'Jamaican cuisine'),
    ('Cuban Cuisine', 'cuban', [
        'Ropa Vieja', 'Cuban Sandwich', 'Moros y Cristianos', 'Lechón Asado',
        'Tostones', 'Picadillo', 'Vaca Frita', 'Flan',
    ], 'Cuban cuisine'),
    ('Colombian Cuisine', 'colombian', [
        'Bandeja Paisa', 'Ajiaco', 'Sancocho', 'Arepa',
        'Empanadas', 'Fritanga', 'Lechona', 'Changua',
    ], 'Colombian cuisine'),
    ('Bangladeshi Cuisine', 'bangladeshi', [
        'Hilsa Fish Curry', 'Biryani', 'Bhuna Khichuri', 'Shorshe Ilish',
        'Panta Bhat', 'Beef Kala Bhuna', 'Mishti Doi', 'Pitha',
    ], 'Bangladeshi cuisine'),
    ('Nepalese Cuisine', 'nepalese', [
        'Dal Bhat', 'Momo', 'Newari Khaja Set', 'Thukpa',
        'Sel Roti', 'Dhindo', 'Bara', 'Chhurpi',
    ], 'Nepalese cuisine'),
    ('Afghan Cuisine', 'afghan', [
        'Kabuli Pulao', 'Bolani', 'Mantu', 'Qorma',
        'Ashak', 'Shor Nakhod', 'Lawand', 'Firni',
    ], 'Afghan cuisine'),
    ('Uzbek Cuisine', 'uzbek', [
        'Plov', 'Samsa', 'Lagman', 'Shashlik',
        'Manti', 'Dimlama', 'Chuchvara', 'Naryn',
    ], 'Uzbek cuisine'),
    ('Armenian Cuisine', 'armenian', [
        'Khorovats', 'Dolma', 'Harissa', 'Lahmajoun',
        'Manti', 'Ghapama', 'Khash', 'Basturma',
    ], 'Armenian cuisine'),
    ('Azerbaijani Cuisine', 'azerbaijani', [
        'Plov', 'Dolma', 'Dushbara', 'Piti',
        'Qutab', 'Levengi', 'Dovga', 'Pakhlava',
    ], 'Azerbaijani cuisine'),
    ('Burmese Cuisine', 'burmese', [
        'Mohinga', 'Laphet Thohk', 'Shan Noodles', 'Ohno Khao Swè',
        'Mont Di', 'Balachaung', 'Danbauk', 'Khauk Swè Thohk',
    ], 'Burmese cuisine'),
    ('Norwegian Cuisine', 'norwegian', [
        'Rakfisk', 'Lutefisk', 'Fårikål', 'Rømmegrøt',
        'Smørbrød', 'Klippfisk', 'Kjøttkaker', 'Lefse',
    ], 'Norwegian cuisine'),
    ('Danish Cuisine', 'danish', [
        'Smørrebrød', 'Flæskesteg', 'Frikadeller', 'Æbleskiver',
        'Rugbrød', 'Stegt Flæsk', 'Koldskål', 'Wienerbrød',
    ], 'Danish cuisine'),
    ('Czech Cuisine', 'czech', [
        'Svíčková', 'Vepřo-knedlo-zelo', 'Goulash', 'Trdelník',
        'Bramboráky', 'Nakládaný Hermelin', 'Svíčková na Smetaně', 'Palačinky',
    ], 'Czech cuisine'),
    ('Tunisian Cuisine', 'tunisian', [
        'Brik', 'Couscous', 'Lablabi', 'Mechouia Salad',
        'Ojja', 'Chorba', 'Bambalouni', 'Assida',
    ], 'Tunisian cuisine'),
    ('Ghanaian Cuisine', 'ghanaian', [
        'Jollof Rice', 'Fufu', 'Kelewele', 'Groundnut Soup',
        'Waakye', 'Red Red', 'Banku', 'Light Soup',
    ], 'Ghanaian cuisine'),
    ('Venezuelan Cuisine', 'venezuelan', [
        'Arepa', 'Pabellón Criollo', 'Hallacas', 'Cachapas',
        'Tequeños', 'Mandocas', 'Chicha', 'Bienmesabe',
    ], 'Venezuelan cuisine'),
    ('Chilean Cuisine', 'chilean', [
        'Cazuela', 'Empanadas', 'Pastel de Choclo', 'Curanto',
        'Completo', 'Humitas', 'Pebre', 'Mote con Huesillo',
    ], 'Chilean cuisine'),
    ('Ecuadorian Cuisine', 'ecuadorian', [
        'Ceviche', 'Llapingachos', 'Seco de Pollo', 'Encebollado',
        'Locro de Papa', 'Fritada', 'Fanesca', 'Caldo de Patas',
    ], 'Ecuadorian cuisine'),
    ('Bolivian Cuisine', 'bolivian', [
        'Salteñas', 'Pique Macho', 'Fricasé', 'Sopa de Maní',
        'Silpancho', 'Api', 'Charquekan', 'Tucumanas',
    ], 'Bolivian cuisine'),
]

# ---------------------------------------------------------------------------
# Review templates (food-focused)
# ---------------------------------------------------------------------------
REVIEW_TEMPLATES = [
    {
        'title': 'Absolutely incredible — a must-try dish',
        'body': "I had {name} for the first time at a {cuisine} restaurant and was completely blown away. The flavors were {flavor_desc}. Every bite was a revelation. I've been going back weekly ever since.",
        'rating': 5,
    },
    {
        'title': 'Authentic and deeply satisfying',
        'body': "{name} is everything I hoped it would be. The {flavor_desc} flavors are so complex yet balanced. It reminded me why {cuisine} food has such a devoted following worldwide. Will absolutely order again.",
        'rating': 5,
    },
    {
        'title': 'Better than I expected',
        'body': "I was skeptical about {name} having never tried {cuisine} food before, but I'm now a total convert. The dish is {flavor_desc} with layers of flavor I didn't anticipate. Highly recommended as a starter dish for the cuisine.",
        'rating': 5,
    },
    {
        'title': 'A real crowd-pleaser',
        'body': "Ordered {name} for a group dinner and everyone loved it. The presentation was beautiful and the taste was {flavor_desc}. Even my picky eaters went back for seconds. One of the best {cuisine} dishes I've ever had.",
        'rating': 5,
    },
    {
        'title': 'Great dish, solidly executed',
        'body': "{name} at this {cuisine} restaurant was very good. The {flavor_desc} taste was authentic and the portion was generous. The only small complaint is that it came out a little {minor_issue}, but overall a great experience.",
        'rating': 4,
    },
    {
        'title': 'Very good, close to the real thing',
        'body': "Having eaten authentic {name} in {region} I was pleasantly surprised by how close this version came. The {flavor_desc} base is spot-on and the quality ingredients shine through. A solid 4 out of 5.",
        'rating': 4,
    },
    {
        'title': 'Delicious but rich — share with a friend',
        'body': "{name} is absolutely delicious but very {texture_desc}. I'd recommend sharing it. The {flavor_desc} flavors are excellent and the preparation clearly comes from a place of tradition. My new favourite {cuisine} dish.",
        'rating': 4,
    },
    {
        'title': 'Good introduction to the cuisine',
        'body': "Tried {name} as my first foray into {cuisine} food and really enjoyed it. It's {flavor_desc} without being too challenging for unfamiliar palates. Would recommend it as a starting point for exploring this cuisine.",
        'rating': 4,
    },
    {
        'title': 'Mixed feelings — good but not great',
        'body': "{name} was okay. The {flavor_desc} taste was there but something felt off — perhaps the {minor_issue}. It wasn't bad by any means but for the price I expected a bit more. Might try again at a different restaurant.",
        'rating': 3,
    },
    {
        'title': 'Decent but not memorable',
        'body': "I've had much better {name} elsewhere. This version was {flavor_desc} enough but lacked depth. The portion size was fine, but overall it felt like a watered-down attempt at {cuisine} cooking. Not bad, just unremarkable.",
        'rating': 3,
    },
    {
        'title': 'Interesting flavors, not for everyone',
        'body': "{name} is a polarising dish. I personally found it too {texture_desc} for my taste, though I can appreciate the skill involved. If you enjoy bold {cuisine} flavors you may love it — it just wasn't quite my thing.",
        'rating': 3,
    },
    {
        'title': 'Disappointing — expected much more',
        'body': "I was really looking forward to trying {name} after all the hype. Unfortunately it was underwhelming — the {flavor_desc} promise wasn't delivered and it arrived {minor_issue}. Maybe this restaurant isn't the best place to try it.",
        'rating': 2,
    },
    {
        'title': 'A comfort food classic done right',
        'body': "{name} is the ultimate comfort food and this version nailed it. {flavor_desc} and warming, it's exactly what you want on a cold day or when you need cheering up. Possibly the best version of this dish I've found locally.",
        'rating': 5,
    },
    {
        'title': 'Made it at home — absolute game changer',
        'body': "I tried making {name} myself following a traditional {cuisine} recipe and the results were phenomenal. The {flavor_desc} flavors filled the whole kitchen. It's more {texture_desc} than it looks and totally worth the effort.",
        'rating': 5,
    },
    {
        'title': 'Perfect balance of flavors',
        'body': "What makes {name} so special is the balance. The {flavor_desc} elements complement each other perfectly — nothing overpowers. It's clearly a dish that has been refined over generations. A true representation of {cuisine} cooking at its best.",
        'rating': 5,
    },
    {
        'title': 'Underrated gem of the cuisine',
        'body': "{name} doesn't always get the attention it deserves as a {cuisine} dish. It's {flavor_desc} and surprisingly complex. I always recommend it to people exploring the cuisine for the first time — it's accessible yet distinctive.",
        'rating': 4,
    },
    {
        'title': 'Would travel just to eat this again',
        'body': "I first tried {name} while visiting the country and have been searching for a version this good ever since. Finally found a restaurant that gets the {flavor_desc} flavors exactly right. Worth every penny and then some.",
        'rating': 5,
    },
    {
        'title': 'Great value and generous portions',
        'body': "{name} here comes in a huge portion at a very fair price. The taste is {flavor_desc} and genuinely satisfying. It's not the most refined version I've tried but for everyday {cuisine} food it's excellent value.",
        'rating': 4,
    },
    {
        'title': 'A bit too spicy for my taste',
        'body': "{name} was delicious but absolutely fiery. I underestimated the heat level. If you enjoy spicy food you'll love it — the {flavor_desc} base is incredible. I'll order it again but ask for a milder version next time.",
        'rating': 3,
    },
    {
        'title': 'Beautifully presented and delicious',
        'body': "The presentation of {name} was stunning — it almost felt wrong to eat it. But when I did, the {flavor_desc} taste matched the appearance perfectly. A dish that delivers on both aesthetics and flavour. Top-tier {cuisine} cooking.",
        'rating': 5,
    },
    {
        'title': 'A staple for good reason',
        'body': "{name} has been a staple of {cuisine} culture for generations and it's easy to see why. The {flavor_desc} simplicity of the dish is its strength. Nothing unnecessary, just clean, honest flavors done with care.",
        'rating': 4,
    },
    {
        'title': 'Perfect street food experience',
        'body': "Had {name} from a street stall and it was fantastic — {flavor_desc} and made fresh right in front of me. There's something about eating authentic {cuisine} food in the right setting that elevates the whole experience.",
        'rating': 5,
    },
    {
        'title': 'Rich, hearty and deeply flavourful',
        'body': "{name} is a proper hearty dish. It's {flavor_desc} and {texture_desc} in the best possible way. The kind of food that warms you from the inside out. An absolute staple in {cuisine} home cooking.",
        'rating': 4,
    },
    {
        'title': 'Not my usual order but now it is',
        'body': "A friend convinced me to try {name} and I'm grateful they did. What I thought would be too {texture_desc} for me turned out to be {flavor_desc} and completely addictive. It's now top of my order every time I visit.",
        'rating': 5,
    },
    {
        'title': 'The real thing — no shortcuts taken',
        'body': "You can tell {name} here is made the traditional way — no shortcuts. The {flavor_desc} depth of flavour you only get from proper technique and quality ingredients is fully present. A rare find outside of {region}.",
        'rating': 5,
    },
]

FLAVOR_DESCS = [
    'rich and deeply savory', 'bright and herbaceous', 'smoky and aromatic',
    'tangy and refreshing', 'sweet and umami', 'complex and warming',
    'bold and spiced', 'light yet intensely flavourful', 'creamy and indulgent',
    'earthy and robust', 'zesty and fragrant', 'delicate and nuanced',
]
TEXTURE_DESCS = [
    'tender', 'crispy', 'creamy', 'hearty', 'flaky', 'silky',
    'chewy', 'crunchy', 'melt-in-your-mouth', 'dense and satisfying',
]
MINOR_ISSUES = [
    'slightly cold', 'a touch underseasoned', 'a little smaller than expected',
    'slightly overcooked', 'a bit oily', 'not quite hot enough',
]
REGIONS = [
    'the capital', 'the countryside', 'a coastal city', 'a local market',
    'the region it originates from', 'a family-run restaurant abroad',
]

FIRST_NAMES = [
    'Emma', 'Liam', 'Olivia', 'Noah', 'Ava', 'Ethan', 'Sophia', 'Mason',
    'Isabella', 'James', 'Mia', 'Logan', 'Charlotte', 'Lucas', 'Amelia',
    'Jackson', 'Harper', 'Aiden', 'Evelyn', 'Sebastian', 'Abigail', 'Mateo',
    'Emily', 'Jack', 'Elizabeth', 'Owen', 'Sofia', 'Henry', 'Avery', 'Samuel',
    'Ella', 'Elijah', 'Madison', 'Daniel', 'Scarlett', 'Benjamin', 'Victoria',
    'Aria', 'Dylan', 'Grace', 'Michael', 'Chloe', 'Ryan', 'Penelope', 'Jayden',
    'Zoe', 'Luke', 'Nora', 'Anthony', 'Lily', 'Mark', 'Layla', 'David',
    'Eleanor', 'John', 'Stella', 'Julian', 'Hazel', 'Elias', 'Aurora',
]


def slugify(text):
    return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', text.lower())).strip('-')


def make_review(dish_name, cuisine_name, tmpl):
    body = tmpl['body'].format(
        name=dish_name,
        cuisine=cuisine_name.replace(' Cuisine', ''),
        flavor_desc=random.choice(FLAVOR_DESCS),
        texture_desc=random.choice(TEXTURE_DESCS),
        minor_issue=random.choice(MINOR_ISSUES),
        region=random.choice(REGIONS),
    )
    return tmpl['title'], body, tmpl['rating']


# ---------------------------------------------------------------------------
# Image helpers
# ---------------------------------------------------------------------------
def wiki_image(title, width=600):
    try:
        r = SESSION.get('https://en.wikipedia.org/w/api.php', params={
            'action': 'query', 'titles': title, 'prop': 'pageimages',
            'pithumbsize': width, 'format': 'json',
        }, timeout=12)
        page = next(iter(r.json()['query']['pages'].values()))
        return page.get('thumbnail', {}).get('source')
    except Exception:
        return None


def commons_search(query, width=500):
    try:
        r = SESSION.get('https://commons.wikimedia.org/w/api.php', params={
            'action': 'query', 'list': 'search',
            'srsearch': f'filetype:bitmap {query}',
            'srnamespace': 6, 'srlimit': 5, 'format': 'json',
        }, timeout=12)
        for result in r.json().get('query', {}).get('search', []):
            r2 = SESSION.get('https://commons.wikimedia.org/w/api.php', params={
                'action': 'query', 'titles': result['title'],
                'prop': 'imageinfo', 'iiprop': 'url',
                'iiurlwidth': width, 'format': 'json',
            }, timeout=10)
            page = next(iter(r2.json()['query']['pages'].values()))
            iis = page.get('imageinfo', [])
            if iis and iis[0].get('thumburl'):
                return iis[0]['thumburl']
    except Exception as e:
        print(f'    commons error: {e}')
    return None


def download(url, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    for attempt in range(3):
        try:
            r = SESSION.get(url, timeout=20)
            if r.status_code == 200:
                with open(dest, 'wb') as f:
                    f.write(r.content)
                return True
            elif r.status_code == 429:
                print('    rate limited, sleeping 30s...')
                time.sleep(30)
        except Exception as e:
            print(f'    download error: {e}')
            time.sleep(3)
    return False


def fetch_image(name, wiki_title=None):
    url = wiki_image(wiki_title or name)
    if not url:
        url = commons_search(name)
    return url


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    app = create_app()
    with app.app_context():
        cat = Category.query.filter_by(slug='food').first()
        if not cat:
            cat = Category(name='Food & Cuisines', slug='food', icon='🍽️',
                           description='Explore dishes and cuisines from around the world.')
            db.session.add(cat)
            db.session.commit()
            print(f'Created category: {cat.name}')
        else:
            print(f'Category exists: {cat.name}')

        total_subjects = 0
        total_reviews = 0

        for cuisine_name, cuisine_slug, dishes, wiki_article in CUISINES:
            sc = SubCategory.query.filter_by(category_id=cat.id, slug=cuisine_slug).first()
            if sc:
                print(f'  Skipping {cuisine_name} (exists)')
                continue

            sc = SubCategory(category_id=cat.id, name=cuisine_name, slug=cuisine_slug)
            db.session.add(sc)
            db.session.flush()
            print(f'\nCreated: {cuisine_name}')

            # Subcategory image
            img_url = fetch_image(cuisine_name, wiki_article)
            if img_url:
                ext = img_url.split('.')[-1].split('?')[0].lower()
                if ext not in ('jpg', 'jpeg', 'png', 'webp', 'gif'):
                    ext = 'jpg'
                fname = f'food-{cuisine_slug}.{ext}'
                dest = os.path.join(STATIC_DIR, 'images', 'uploads', 'subcategories', fname)
                if download(img_url, dest):
                    sc.image_path = f'images/uploads/subcategories/{fname}'
                    print(f'  subcategory image saved')
            time.sleep(1)

            for dish in dishes:
                dish_slug = f'{cuisine_slug}-{slugify(dish)}'
                subj = Subject.query.filter_by(subcategory_id=sc.id, slug=dish_slug).first()
                if subj:
                    continue

                subj = Subject(subcategory_id=sc.id, name=dish, slug=dish_slug)
                db.session.add(subj)
                db.session.flush()

                # Dish image
                img_url = fetch_image(dish)
                if img_url:
                    ext = img_url.split('.')[-1].split('?')[0].lower()
                    if ext not in ('jpg', 'jpeg', 'png', 'webp', 'gif'):
                        ext = 'jpg'
                    fname = f'food-{dish_slug}.{ext}'
                    dest = os.path.join(STATIC_DIR, 'images', 'uploads', 'subjects', fname)
                    if download(img_url, dest):
                        subj.image_path = f'images/uploads/subjects/{fname}'
                        print(f'    img: {dish}')
                    else:
                        print(f'    no img: {dish}')
                else:
                    print(f'    no img: {dish}')
                time.sleep(0.8)

                # Reviews
                target = random.randint(12, 40)
                used_titles = set()
                from datetime import datetime, timedelta
                reviews_added = 0
                shuffled = REVIEW_TEMPLATES[:]
                random.shuffle(shuffled)

                for tmpl in shuffled * 2:
                    if reviews_added >= target:
                        break
                    title, body, base_rating = make_review(dish, cuisine_name, tmpl)
                    if title in used_titles:
                        continue
                    used_titles.add(title)
                    rating = max(1, min(5, base_rating + random.choice([-1, 0, 0, 0, 1])))
                    days_ago = random.randint(1, 730)
                    rev = Review(
                        subject_id=subj.id,
                        title=title,
                        body=body,
                        rating=rating,
                        author_name=random.choice(FIRST_NAMES),
                        source_site='sample',
                        original_date=datetime.utcnow() - timedelta(days=days_ago),
                        is_published=True,
                    )
                    db.session.add(rev)
                    reviews_added += 1

                subj.update_stats()
                total_subjects += 1
                total_reviews += reviews_added

            db.session.commit()
            print(f'  committed {cuisine_name}')

        print(f'\nDone. {total_subjects} dishes, {total_reviews} reviews.')


if __name__ == '__main__':
    main()
