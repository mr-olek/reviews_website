#!/usr/bin/env python3
"""
Replace generic template reviews for Food & Cuisines with specific, data-driven
reviews referencing real ingredients, flavour profiles, dining contexts, cultural
notes, and drink pairings.

Usage:
  python3 generate_food_reviews.py                    # all cuisines
  python3 generate_food_reviews.py --slug thai        # single cuisine
  python3 generate_food_reviews.py --start-from greek # resume from cuisine
  python3 generate_food_reviews.py --count 15         # reviews per dish (default 15)
"""
from __future__ import annotations
import argparse, os, random, sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# Cuisine-specific facts, keyed by subcategory slug
# ---------------------------------------------------------------------------
CUISINE_DATA = {
    'ukrainian': {
        'ingredients':     ['beetroot', 'sour cream', 'dill', 'pork fat', 'buckwheat'],
        'flavors':         ['earthy and hearty', 'subtly sour', 'rich and warming', 'deeply comforting'],
        'dining_context':  ['a family Sunday lunch', 'a traditional Ukrainian home kitchen', 'a village-style restaurant'],
        'cultural_notes':  ['Ukrainian cuisine reflects centuries of agricultural abundance', 'many dishes are tied to Orthodox religious calendar'],
        'pairings':        ['horilka', 'kvass', 'dark rye bread', 'smetana'],
    },
    'french': {
        'ingredients':     ['butter', 'cream', 'shallots', 'thyme', 'Dijon mustard'],
        'flavors':         ['rich and refined', 'buttery and aromatic', 'deeply layered', 'elegantly balanced'],
        'dining_context':  ['a Parisian bistro', 'a formal dinner party', 'a countryside auberge', 'a brasserie lunch'],
        'cultural_notes':  ['French cuisine is a UNESCO Intangible Cultural Heritage', 'the terroir philosophy links food to its region of origin'],
        'pairings':        ['Burgundy red wine', 'Champagne', 'baguette', 'a digestif of Calvados'],
    },
    'italian': {
        'ingredients':     ['San Marzano tomatoes', 'fresh basil', 'Parmesan', 'olive oil', 'aged balsamic'],
        'flavors':         ['bright and tomatoey', 'rich and umami', 'fresh and herbal', 'deeply savory'],
        'dining_context':  ['a family trattoria in Rome', 'a Sunday ragu lunch', 'a Neapolitan pizzeria', 'a home kitchen'],
        'cultural_notes':  ['Italian cooking is intensely regional with little crossover between provinces', 'ingredient simplicity and quality are the guiding principles'],
        'pairings':        ['Chianti', 'Prosecco', 'sparkling mineral water', 'limoncello after the meal'],
    },
    'japanese': {
        'ingredients':     ['dashi stock', 'soy sauce', 'mirin', 'sake', 'fresh wasabi'],
        'flavors':         ['clean and umami-forward', 'delicate and precise', 'subtly sweet and salty', 'deeply savoury'],
        'dining_context':  ['an intimate Tokyo counter restaurant', 'a ramen shop at lunchtime', 'a high-end kaiseki setting', 'a conveyor belt sushi bar'],
        'cultural_notes':  ['Japanese cuisine philosophy of shokunin craftsmanship shapes how even simple dishes are prepared', 'seasonal ingredients guide the menu in traditional settings'],
        'pairings':        ['sake', 'green tea', 'cold Sapporo beer', 'barley tea'],
    },
    'chinese': {
        'ingredients':     ['Sichuan peppercorn', 'oyster sauce', 'five-spice', 'Shaoxing wine', 'fermented black bean'],
        'flavors':         ['bold and numbing', 'deeply savoury and sweet', 'aromatic and complex', 'rich with umami'],
        'dining_context':  ['a bustling dim sum hall', 'a family banquet table', 'a street stall in Chengdu', 'a regional specialty restaurant'],
        'cultural_notes':  ['Chinese cuisine encompasses eight major regional schools with distinct ingredients and techniques', 'communal sharing at the table is culturally central'],
        'pairings':        ['jasmine tea', 'Tsingtao beer', 'Shaoxing rice wine', 'chrysanthemum tea'],
    },
    'mexican': {
        'ingredients':     ['dried ancho chilli', 'epazote', 'tomatillo', 'Mexican chocolate', 'masa harina'],
        'flavors':         ['smoky and earthy', 'bright and citrusy', 'complex and layered with chilli', 'deeply aromatic'],
        'dining_context':  ['a street taco stand', 'a family mercado lunch', 'an Oaxacan restaurant', 'a home kitchen on a Sunday'],
        'cultural_notes':  ['Mexican cuisine is a UNESCO Intangible Cultural Heritage', 'pre-Columbian ingredients like corn, beans, and chilli form the foundation'],
        'pairings':        ['mezcal', 'horchata', 'Mexican lager with lime', 'agua fresca'],
    },
    'indian': {
        'ingredients':     ['ghee', 'whole spices', 'yogurt marinade', 'tamarind', 'fenugreek leaves'],
        'flavors':         ['warmly spiced and aromatic', 'rich and complex', 'tangy and vibrant', 'deeply layered'],
        'dining_context':  ['a family home kitchen on a weekend', 'a dhaba roadside restaurant', 'a north Indian restaurant abroad', 'a wedding feast setting'],
        'cultural_notes':  ['Indian cuisine varies enormously by state, religion, and climate', 'spices are used medicinally as well as for flavour in Ayurvedic tradition'],
        'pairings':        ['chai tea', 'lassi', 'Kingfisher beer', 'nimbu pani lemon water'],
    },
    'american': {
        'ingredients':     ['smoked brisket', 'sharp cheddar', 'maple syrup', 'hot sauce', 'sourdough bread'],
        'flavors':         ['bold and smoky', 'rich and indulgent', 'sweet and tangy', 'generously seasoned'],
        'dining_context':  ['a Southern BBQ joint', 'a New England seafood shack', 'a classic diner', 'a Fourth of July cookout'],
        'cultural_notes':  ['American cuisine is a mosaic of immigrant traditions adapted over generations', 'regional BBQ styles from Texas to Carolina are matters of fierce local pride'],
        'pairings':        ['craft IPA', 'sweet iced tea', 'bourbon on ice', 'root beer'],
    },
    'thai': {
        'ingredients':     ['galangal', 'kaffir lime leaves', 'Thai basil', 'fish sauce', 'palm sugar'],
        'flavors':         ['balanced between sweet, sour, salty, and spicy', 'fragrant and herbaceous', 'bright and lively', 'deeply aromatic'],
        'dining_context':  ['a Bangkok street stall', 'a family restaurant', 'a beachside seafood spot', 'a traditional home kitchen'],
        'cultural_notes':  ['Thai cooking philosophy balances four key flavour profiles in every dish', 'fresh herbs and aromatics are added at the last moment to preserve fragrance'],
        'pairings':        ['Thai iced tea', 'Singha beer', 'fresh coconut water', 'nam manao lime soda'],
    },
    'greek': {
        'ingredients':     ['Greek olive oil', 'feta cheese', 'dried oregano', 'lemon juice', 'Kalamata olives'],
        'flavors':         ['bright and lemony', 'rich with olive oil', 'herbal and aromatic', 'cleanly savoury'],
        'dining_context':  ['a taverna by the Aegean sea', 'a family Sunday meal', 'a meze sharing table', 'a village feast'],
        'cultural_notes':  ['Greek cuisine has influenced the entire Mediterranean culinary tradition for millennia', 'the sharing table or mezethes is central to Greek social eating'],
        'pairings':        ['ouzo', 'retsina', 'cold Fix lager', 'Greek coffee after the meal'],
    },
    'spanish': {
        'ingredients':     ['saffron', 'smoked paprika', 'Jamón Ibérico', 'Manchego cheese', 'Arborio-style Bomba rice'],
        'flavors':         ['smoky and savoury', 'rich with olive oil', 'briny and complex', 'deeply aromatic'],
        'dining_context':  ['a tapas bar in Barcelona', 'a Sunday family paella', 'a pintxos bar in San Sebastián', 'a siesta-hour lunch restaurant'],
        'cultural_notes':  ['Spanish eating culture centres on long social meals rather than quick eating', 'the tapas tradition developed as small accompaniments to drinks'],
        'pairings':        ['Rioja red wine', 'Cava sparkling wine', 'Estrella Damm beer', 'horchata'],
    },
    'turkish': {
        'ingredients':     ['sumac', 'pomegranate molasses', 'lamb mince', 'Turkish red pepper paste', 'bulgur wheat'],
        'flavors':         ['warmly spiced and complex', 'tangy with sumac and pomegranate', 'richly savory', 'subtly sweet and aromatic'],
        'dining_context':  ['an Istanbul meyhane tavern', 'a kebab restaurant at lunchtime', 'a traditional Ottoman-style restaurant', 'a home dinner table'],
        'cultural_notes':  ['Turkish cuisine bridges Central Asian, Middle Eastern, and Mediterranean influences', 'the meze tradition of small shared dishes predates the main course'],
        'pairings':        ['ayran yoghurt drink', 'çay black tea', 'raki anise spirit', 'pomegranate juice'],
    },
    'lebanese': {
        'ingredients':     ['tahini', 'za\'atar', 'sumac', 'pine nuts', 'seven-spice baharat blend'],
        'flavors':         ['fresh and citrusy', 'nutty and sesame-forward', 'aromatic with herbs and spice', 'bright and balanced'],
        'dining_context':  ['a mezze spread for a large gathering', 'a Beirut street stall', 'a family Sunday lunch', 'a Middle Eastern restaurant abroad'],
        'cultural_notes':  ['Lebanese hospitality is expressed through abundance on the table', 'the cuisine shares roots with the broader Levantine tradition'],
        'pairings':        ['arak', 'fresh mint lemonade', 'Lebanese wine', 'strong cardamom coffee'],
    },
    'korean': {
        'ingredients':     ['gochujang chilli paste', 'doenjang fermented soy', 'sesame oil', 'perilla leaves', 'kimchi brine'],
        'flavors':         ['fiery and fermented', 'deeply umami', 'complex and bold', 'sweet, spicy, and savoury at once'],
        'dining_context':  ['a Korean barbecue restaurant with table grills', 'a pojangmacha street tent', 'a home banchan spread', 'a late-night soju bar'],
        'cultural_notes':  ['Korean cuisine integrates fermented ingredients like kimchi as a health and preservation tradition', 'the communal banchan side dishes are as important as the main'],
        'pairings':        ['soju', 'makgeolli rice wine', 'barley tea', 'banana milk'],
    },
    'vietnamese': {
        'ingredients':     ['fish sauce', 'lemongrass', 'fresh mint and coriander', 'rice paper', 'star anise broth'],
        'flavors':         ['light and herbal', 'clean and deeply savoury', 'fresh with citrus and mint', 'subtly sweet and spiced'],
        'dining_context':  ['a Hanoi pho stall at breakfast', 'a street banh mi counter', 'a Hoi An restaurant', 'a home cooking class'],
        'cultural_notes':  ['Vietnamese cuisine shows French colonial influence alongside traditional Southeast Asian techniques', 'fresh herbs added at the table are a defining characteristic'],
        'pairings':        ['Vietnamese iced coffee', 'fresh sugarcane juice', 'bia hoi draught beer', 'lime soda'],
    },
    'moroccan': {
        'ingredients':     ['ras el hanout', 'preserved lemon', 'argan oil', 'harissa', 'medjool dates'],
        'flavors':         ['warmly spiced and aromatic', 'sweet and savoury together', 'richly perfumed', 'complex with dried fruit and spice'],
        'dining_context':  ['a riad rooftop dinner in Marrakech', 'a family couscous Friday', 'a medina restaurant', 'a desert camp dinner'],
        'cultural_notes':  ['Moroccan cuisine draws from Berber, Arab, Andalusian, and French influences', 'hospitality rituals including mint tea service are integral to the food experience'],
        'pairings':        ['Moroccan mint tea', 'almond milk', 'Casablanca beer', 'orange blossom water drink'],
    },
    'german': {
        'ingredients':     ['smoked pork', 'caraway seeds', 'sauerkraut', 'mustard', 'dark rye bread'],
        'flavors':         ['hearty and deeply savoury', 'smoky and satisfying', 'tangy from fermentation', 'robust and filling'],
        'dining_context':  ['a Bavarian beer hall', 'a winter Christmas market', 'a Sunday family roast lunch', 'a traditional Gasthaus'],
        'cultural_notes':  ['German bread culture is extraordinarily diverse with over 300 officially registered varieties', 'regional specialities vary dramatically between Bavaria, Saxony, and the Rhineland'],
        'pairings':        ['weissbier', 'Riesling', 'Radler shandy', 'schnapps after the meal'],
    },
    'british': {
        'ingredients':     ['mature Cheddar', 'Worcestershire sauce', 'HP sauce', 'malt vinegar', 'proper beef suet'],
        'flavors':         ['rich and savoury', 'comforting and hearty', 'subtly sweet with caramelised elements', 'deeply satisfying'],
        'dining_context':  ['a Sunday pub lunch', 'a traditional seaside chippy', 'a full English café breakfast', 'a country house hotel'],
        'cultural_notes':  ['British cuisine was shaped by the Empire, introducing curries and international ingredients into the national diet', 'pub food culture has undergone a renaissance in the gastropub era'],
        'pairings':        ['real ale', 'English Breakfast tea', 'dry cider', 'a glass of claret with Sunday roast'],
    },
    'portuguese': {
        'ingredients':     ['bacalhau salt cod', 'piri piri', 'chouriço', 'fresh sardines', 'egg yolks'],
        'flavors':         ['briny and savoury', 'smoky and robust', 'sweet and eggy in pastries', 'bright with olive oil and garlic'],
        'dining_context':  ['a Lisbon tasca restaurant', 'a coastal seafood restaurant', 'a tascas lunch counter', 'a pastelaria morning coffee'],
        'cultural_notes':  ['Portugal developed bacalhau salt cod cookery while exploring the Atlantic and has over 365 recipes for it', 'pastéis de nata originated in Belém monastery in the 18th century'],
        'pairings':        ['Vinho Verde', 'Port wine', 'Sagres beer', 'ginjinha cherry liqueur'],
    },
    'polish': {
        'ingredients':     ['sauerkraut', 'dried mushrooms', 'sour rye sourdough', 'fresh dill', 'smoked sausage'],
        'flavors':         ['tangy and hearty', 'deeply savoury with fermented notes', 'rich and comforting', 'earthy from mushrooms'],
        'dining_context':  ['a family Christmas Eve wigilia dinner', 'a Warsaw milk bar', 'a traditional Polish restaurant', 'a home kitchen in winter'],
        'cultural_notes':  ['Polish cuisine reflects Central European and Slavic agricultural traditions', 'the Christmas Eve wigilia meal has strict traditional rules including twelve meatless dishes'],
        'pairings':        ['Żubrówka bison grass vodka', 'kompot fruit drink', 'Polish beer', 'kwas chlebowy bread drink'],
    },
    'hungarian': {
        'ingredients':     ['sweet paprika', 'lard', 'sour cream', 'onion', 'Hungarian wax peppers'],
        'flavors':         ['richly paprika-spiced', 'hearty and warming', 'creamy and savoury', 'deeply flavourful'],
        'dining_context':  ['a Budapest csárda tavern', 'a family Sunday lunch', 'a lakeside restaurant on the Balaton', 'a traditional market stall'],
        'cultural_notes':  ['Hungarian cuisine was shaped by nomadic Magyar traditions mixed with Ottoman and Habsburg influences', 'paprika only entered Hungarian cooking in the 17th century but now defines the cuisine'],
        'pairings':        ['Tokaji wine', 'Pálinka fruit brandy', 'Dreher beer', 'soda water spritzer'],
    },
    'czech': {
        'ingredients':     ['caraway', 'Czech beer', 'pork knuckle', 'bread dumplings', 'pickled vegetables'],
        'flavors':         ['hearty and deeply savoury', 'malty from beer braises', 'subtly tangy from pickles', 'rich and filling'],
        'dining_context':  ['a Prague pub restaurant', 'a traditional Czech hospoda', 'a ski resort lunch', 'a market square lunch counter'],
        'cultural_notes':  ['Czech cuisine is inseparable from beer culture, one of the world\'s highest per-capita consumption nations', 'bread dumplings served alongside everything evolved as the perfect vehicle for rich sauces'],
        'pairings':        ['Czech Pilsner Urquell', 'Moravian wine', 'svíčková cream sauce', 'slivovitz plum brandy'],
    },
    'swedish': {
        'ingredients':     ['gravlax cured salmon', 'lingonberry', 'dill', 'cream', 'allspice'],
        'flavors':         ['clean and subtly sweet', 'delicately cured', 'cream-enriched and comforting', 'herbal with dill'],
        'dining_context':  ['a Swedish smörgåsbord table', 'a midsommar summer feast', 'a cosy fika café', 'a Noma-influenced Nordic restaurant'],
        'cultural_notes':  ['Swedish fika culture elevates the coffee break with pastries into a social institution', 'the smörgåsbord tradition of abundant cold dishes influenced buffet culture worldwide'],
        'pairings':        ['aquavit', 'Swedish punsch', 'lingonberry juice', 'light lager'],
    },
    'danish': {
        'ingredients':     ['rye bread rugbrød', 'pickled herring', 'fresh dill', 'brown butter', 'Nordic berries'],
        'flavors':         ['clean and fermented', 'buttery and rich', 'bright and pickled', 'subtly sweet with berries'],
        'dining_context':  ['a Copenhagen smørrebrød lunch bar', 'a traditional Sunday brunch', 'a Noma-inspired New Nordic restaurant', 'a Christmas julefrokost feast'],
        'cultural_notes':  ['Danish New Nordic cuisine movement redefined fine dining globally in the 2000s', 'the julefrokost Christmas lunch is a major social event with traditional dishes strictly observed'],
        'pairings':        ['aquavit', 'Danish lager', 'æblemost apple juice', 'cold buttermilk'],
    },
    'norwegian': {
        'ingredients':     ['fresh salmon', 'brown cheese', 'cloudberry', 'lamb', 'dried stockfish'],
        'flavors':         ['clean and oceanic', 'rich and slightly sweet', 'gamey and earthy', 'subtly smoky'],
        'dining_context':  ['a Bergen fish market lunch', 'a mountain hytte cabin dinner', 'a traditional Norwegian home', 'a seafood restaurant on the fjord'],
        'cultural_notes':  ['Norwegian coastal geography shaped a cuisine centred on preserved and fresh fish', 'rakfisk fermented trout is an ancient preservation method still enjoyed at Christmas'],
        'pairings':        ['aquavit', 'Norwegian lager', 'brunost brown cheese', 'cloudberry cream'],
    },
    'georgian': {
        'ingredients':     ['blue fenugreek', 'walnut paste', 'adjika pepper paste', 'tkemali plum sauce', 'sulguni cheese'],
        'flavors':         ['nutty and aromatic', 'tangy and herbal', 'rich with walnuts and spice', 'complex and distinctive'],
        'dining_context':  ['a traditional Georgian supra feast', 'a Tbilisi restaurant with a tamada toastmaster', 'a family Sunday table', 'a wine cellar dinner'],
        'cultural_notes':  ['the Georgian supra feast is a ritual occasion with formal toasts guided by a tamada toastmaster', 'Georgia claims one of the world\'s oldest continuous wine-making traditions dating back 8000 years'],
        'pairings':        ['Georgian amber wine', 'chacha grape pomace spirit', 'Borjomi mineral water', 'tkhemali sauce'],
    },
    'argentinian': {
        'ingredients':     ['beef asado cuts', 'chimichurri herbs', 'Malbec wine', 'dulce de leche', 'yerba mate'],
        'flavors':         ['intensely beefy and smoky', 'herbal and garlicky', 'richly caramelised', 'bold and satisfying'],
        'dining_context':  ['a parrilla grill restaurant', 'a Sunday asado in a friend\'s garden', 'a Buenos Aires steakhouse', 'a family quincho barbecue area'],
        'cultural_notes':  ['the asado is an Argentinian social institution as much as a cooking technique', 'Argentina consumes more beef per capita than almost any other country'],
        'pairings':        ['Malbec', 'Fernet and cola', 'yerba mate', 'Quilmes lager'],
    },
    'peruvian': {
        'ingredients':     ['aji amarillo pepper', 'huacatay black mint', 'leche de tigre lime marinade', 'purple corn', 'quinoa'],
        'flavors':         ['bright and citrusy', 'spicy and aromatic', 'fresh and marine', 'subtly sweet with chilli heat'],
        'dining_context':  ['a Lima cevichería', 'a Novoandino contemporary Peruvian restaurant', 'a market anticucho stall', 'a coastal chicharronería'],
        'cultural_notes':  ['Peruvian cuisine blends indigenous Andean traditions with Japanese, Chinese, African, and Spanish influences', 'Lima is considered one of the world\'s great culinary destinations'],
        'pairings':        ['Pisco Sour', 'chicha morada purple corn drink', 'Inca Kola', 'cold Cusqueña beer'],
    },
    'colombian': {
        'ingredients':     ['achiote annatto', 'Colombian hogao tomato sauce', 'fresh guanábana', 'plantain', 'chicharrón pork rinds'],
        'flavors':         ['hearty and comforting', 'subtly sweet with tropical fruit', 'savoury and satisfying', 'richly textured'],
        'dining_context':  ['a Bogotá corrientazo lunch counter', 'a coastal Caribbean seafood restaurant', 'a family Sunday sancocho', 'an Antioquia bandeja paisa restaurant'],
        'cultural_notes':  ['Colombian cuisine varies dramatically between the coastal Caribbean, Andean, and Amazonian regions', 'the bandeja paisa plate is a point of Antioquian cultural pride'],
        'pairings':        ['tinto black coffee', 'agua panela sugarcane drink', 'Águila beer', 'lulada lulo fruit drink'],
    },
    'brazilian': {
        'ingredients':     ['black beans', 'dende palm oil', 'dried shrimp', 'manioc flour farinha', 'fresh malagueta chilli'],
        'flavors':         ['rich and earthy', 'smoky and umami-deep', 'sweet from tropical fruits', 'robust and filling'],
        'dining_context':  ['a churrascaria rodizio steakhouse', 'a Rio de Janeiro boteco bar', 'a São Paulo padaria', 'a Bahian seafood restaurant'],
        'cultural_notes':  ['Brazilian cuisine reflects indigenous, Portuguese, and African culinary heritages in equal measure', 'feijoada black bean stew is a national dish with African and Portuguese roots'],
        'pairings':        ['caipirinha', 'guaraná Antarctica', 'Brahma lager', 'açaí bowl'],
    },
    'iranian': {
        'ingredients':     ['saffron', 'dried limes', 'pomegranate molasses', 'fenugreek', 'barberries'],
        'flavors':         ['fragrant and aromatic', 'sweet-sour with pomegranate', 'rich and saffron-gilded', 'subtly bitter and complex'],
        'dining_context':  ['a traditional Iranian home dinner', 'a Tehran restaurant', 'a Persian New Year nowruz celebration', 'a communal sofreh tablecloth feast'],
        'cultural_notes':  ['Iranian cuisine has a 3000-year recorded history with influences on Arab, Turkish, and Central Asian cooking', 'the sofreh spread on the floor is the traditional Iranian dining setting'],
        'pairings':        ['doogh yoghurt drink', 'rose water sharbat', 'hot black tea with sugar', 'fresh pomegranate juice'],
    },
    'israeli': {
        'ingredients':     ['tahini', 'za\'atar', 'Medjool dates', 'pomegranate seeds', 'silan date syrup'],
        'flavors':         ['sesame-rich and nutty', 'bright and fresh with herbs', 'warmly spiced', 'sweet and tangy'],
        'dining_context':  ['a Tel Aviv hummusiya', 'a Shabbat family dinner', 'a Carmel Market street stall', 'a fusion restaurant mixing Mediterranean traditions'],
        'cultural_notes':  ['Israeli cuisine is shaped by Jewish diaspora traditions from across the world fused with local Levantine ingredients', 'Shabbat and holiday meals follow religious traditions that shape the food served'],
        'pairings':        ['Israeli wine', 'mint lemonade', 'arak', 'fresh orange juice'],
    },
    'egyptian': {
        'ingredients':     ['fenugreek seeds', 'cumin', 'coriander seed', 'molokhia leaves', 'lentils'],
        'flavors':         ['earthy and warming', 'deeply savoury and spiced', 'hearty and filling', 'subtly herbal'],
        'dining_context':  ['a Cairo street stall at lunchtime', 'a Nile-side restaurant', 'a family home dinner', 'a traditional Egyptian koshari shop'],
        'cultural_notes':  ['Egyptian cuisine is one of the oldest recorded food cultures, with accounts dating to pharaonic times', 'koshari is considered the national dish representing the multicultural influence on Egyptian cooking'],
        'pairings':        ['karkadeh hibiscus tea', 'ayran', 'Egyptian Stella beer', 'mint tea'],
    },
    'singaporean': {
        'ingredients':     ['sambal belacan paste', 'pandan leaves', 'coconut milk', 'lemongrass', 'prawn paste hae ko'],
        'flavors':         ['complex and fiery', 'richly coconut-sweet', 'deeply umami from prawn paste', 'fragrant and layered'],
        'dining_context':  ['a hawker centre', 'a kopitiam coffee shop', 'a Michelin-starred hawker stall', 'a laksa restaurant'],
        'cultural_notes':  ['Singapore\'s hawker culture was inscribed as UNESCO Intangible Cultural Heritage in 2020', 'the cuisine blends Malay, Chinese, Indian, and Peranakan traditions in a unique fusion'],
        'pairings':        ['teh tarik pulled tea', 'Tiger beer', 'fresh coconut water', 'bandung rose milk drink'],
    },
    'malaysian': {
        'ingredients':     ['belacan shrimp paste', 'pandan', 'curry leaves', 'coconut cream', 'galangal'],
        'flavors':         ['richly spiced and coconut-sweet', 'fragrant and aromatic', 'bold and complex', 'sweet-savoury balance'],
        'dining_context':  ['a Penang hawker stall', 'a mamak 24-hour restaurant', 'a Kuala Lumpur kopitiam', 'a Baba Nyonya Peranakan restaurant'],
        'cultural_notes':  ['Malaysian cuisine reflects the Malay, Chinese, Indian, and indigenous Orang Asli traditions of a multicultural society', 'Penang is considered the food capital of Malaysia and rivals Singapore for hawker excellence'],
        'pairings':        ['teh tarik', 'Milo', 'Anchor beer', 'fresh sugarcane juice'],
    },
    'indonesian': {
        'ingredients':     ['tempeh', 'kecap manis sweet soy', 'coconut milk', 'candlenut', 'terasi shrimp paste'],
        'flavors':         ['rich and coconut-forward', 'deeply spiced with galangal and lemongrass', 'sweet-savoury', 'complex from slow-cooked rendang'],
        'dining_context':  ['a Padang restaurant with displayed dishes', 'a Bali warung', 'a Jakarta street food cart', 'a family feast table'],
        'cultural_notes':  ['Indonesian cuisine spans over 17,000 islands with dramatically different regional traditions', 'rendang from West Sumatra is consistently voted one of the world\'s most delicious dishes'],
        'pairings':        ['es teh manis iced sweet tea', 'kopi tubruk', 'Bintang beer', 'jamu herbal drink'],
    },
    'pakistani': {
        'ingredients':     ['whole garam masala', 'Kashmiri chilli', 'green cardamom', 'ghee', 'dried apricots'],
        'flavors':         ['boldly spiced and aromatic', 'rich with slow-cooked depth', 'warming and hearty', 'fragrant from whole spices'],
        'dining_context':  ['a Lahore dhaba', 'a Karachi biryani house', 'a family Eid feast', 'a BBQ nihari restaurant at midnight'],
        'cultural_notes':  ['Pakistani cuisine draws from Mughal court traditions combined with local Punjabi and Sindhi cooking', 'nihari was originally eaten after the fajr morning prayer as a slow-cooked overnight stew'],
        'pairings':        ['lassi', 'chai', 'rooh afza rose syrup drink', 'zeera cumin water'],
    },
    'bangladeshi': {
        'ingredients':     ['mustard oil', 'hilsa fish', 'posto poppy seeds', 'panch phoron five-spice', 'green chilli'],
        'flavors':         ['pungent from mustard oil', 'fresh and fishy', 'spicy and tangy', 'earthy from poppy seeds'],
        'dining_context':  ['a Dhaka riverside fish restaurant', 'a family Friday hilsa lunch', 'a Sylheti tea estate', 'a traditional Bengali home'],
        'cultural_notes':  ['hilsa fish is a cultural icon in Bangladesh — its seasonal availability is a national event', 'Bengali cuisine shares roots with West Bengal India but has distinct Muslim food traditions'],
        'pairings':        ['jhal muri puffed rice snack', 'aam panna green mango drink', 'lassi', 'hot sweet tea'],
    },
    'sri-lankan': {
        'ingredients':     ['Maldive fish chips', 'Ceylon cinnamon', 'pandan', 'coconut scraped fresh', 'goraka dried gamboge'],
        'flavors':         ['fiery and aromatic', 'deeply coconut-rich', 'tangy from goraka and tamarind', 'warming with cinnamon'],
        'dining_context':  ['a Colombo rice and curry lunch', 'a Jaffna Tamil restaurant', 'a hill country tea estate restaurant', 'a family hoppers breakfast'],
        'cultural_notes':  ['Sri Lankan cuisine differs markedly between Sinhalese, Tamil, and Burgher traditions on the same island', 'Maldive fish is a uniquely Sri Lankan ingredient with no close equivalent elsewhere'],
        'pairings':        ['Ceylon tea', 'king coconut water', 'arrack', 'ginger beer'],
    },
    'nepalese': {
        'ingredients':     ['timur Sichuan pepper', 'mustard oil', 'black lentils', 'buckwheat', 'dried yak cheese'],
        'flavors':         ['earthy and warming', 'subtly numbing from timur', 'hearty and filling', 'simply seasoned and clean'],
        'dining_context':  ['a Kathmandu teahouse', 'a trekking lodge dal bhat', 'a Newari restaurant', 'a Sherpa kitchen in the mountains'],
        'cultural_notes':  ['dal bhat power for 24 hours is a trekking mantra reflecting how central the dish is to Nepali daily life', 'Newari cuisine of the Kathmandu Valley is a distinct and sophisticated subcategory'],
        'pairings':        ['butter tea', 'tongba millet beer', 'nimbu pani', 'raksi grain spirit'],
    },
    'ethiopian': {
        'ingredients':     ['berbere spice blend', 'niter kibbeh spiced clarified butter', 'teff injera', 'mitmita bird\'s eye chilli', 'fenugreek'],
        'flavors':         ['intensely spiced and complex', 'tangy from fermented injera', 'richly buttery', 'deep and earthy'],
        'dining_context':  ['a communal injera sharing meal', 'an Addis Ababa restaurant', 'an Ethiopian diaspora restaurant abroad', 'a traditional coffee ceremony setting'],
        'cultural_notes':  ['Ethiopian communal eating with no utensils from a shared injera is a social and hygienic tradition', 'the Ethiopian coffee ceremony is a formalised ritual that can take hours'],
        'pairings':        ['tej honey wine', 'Ethiopian coffee ceremony', 'tej', 'fresh juice'],
    },
    'nigerian': {
        'ingredients':     ['palm oil', 'locust beans dawadawa', 'uziza leaves', 'crayfish powder', 'ogiri fermented seeds'],
        'flavors':         ['rich and earthy from palm oil', 'deeply umami from fermented ingredients', 'spicy and bold', 'complex and robust'],
        'dining_context':  ['a Lagos buka local restaurant', 'a family gathering', 'a Nigerian restaurant abroad', 'a roadside suya stall at night'],
        'cultural_notes':  ['Nigerian cuisine varies between the Yoruba, Igbo, Hausa, and other ethnic culinary traditions', 'suya spiced meat skewers are eaten across West Africa but claim deep Nigerian roots'],
        'pairings':        ['Chapman cocktail', 'Fanta orange', 'palm wine', 'zobo hibiscus drink'],
    },
    'ghanaian': {
        'ingredients':     ['palm nut', 'groundnuts', 'dried fish', 'kontomire cocoyam leaves', 'fermented dawadawa'],
        'flavors':         ['nutty and palm-rich', 'smoky and warming', 'hearty and earthy', 'subtly sweet from plantain'],
        'dining_context':  ['a Accra chop bar', 'a family Sunday fufu meal', 'a market jollof rice stall', 'a Ghanaian restaurant abroad'],
        'cultural_notes':  ['the debate over Ghanaian versus Nigerian jollof rice is a celebrated West African rivalry', 'fufu and soup eating requires communal sharing and is eaten with the hands'],
        'pairings':        ['Malt Guinness', 'sobolo sorrel drink', 'Club Beer', 'fresh palm wine'],
    },
    'south-african': {
        'ingredients':     ['braai wood and coals', 'boerewors spice mix', 'Mrs Ball\'s chutney', 'dried biltong', 'chakalaka relish'],
        'flavors':         ['smoky and braaied', 'spiced and savoury', 'sweet-tangy from chutney', 'robust and satisfying'],
        'dining_context':  ['a weekend braai', 'a Cape Malay restaurant in Cape Town', 'a shebeen township tavern', 'a game reserve bush dinner'],
        'cultural_notes':  ['the braai is a cross-cultural South African institution that transcends racial and social divides', 'Cape Malay cuisine reflects the heritage of enslaved people brought from Southeast Asia'],
        'pairings':        ['Castle Lager', 'Pinotage wine', 'rooibos tea', 'Amarula cream liqueur'],
    },
    'jamaican': {
        'ingredients':     ['scotch bonnet', 'allspice pimento', 'thyme', 'coconut milk', 'ackee fruit'],
        'flavors':         ['fiery and aromatic', 'smoky from the jerk pit', 'rich and coconut-sweet', 'boldly spiced'],
        'dining_context':  ['a Kingston jerk pit', 'a roadside rum bar', 'a beach seafood restaurant', 'a family Sunday dinner'],
        'cultural_notes':  ['Jamaican jerk cooking traces to the Maroon communities who preserved meat with allspice and chilli', 'ackee is legally restricted for export when unripe due to toxicity — an unusual national dish ingredient'],
        'pairings':        ['Red Stripe beer', 'rum punch', 'sorrel drink', 'ginger beer'],
    },
    'cuban': {
        'ingredients':     ['Mojo marinade', 'black beans', 'plantain', 'sofrito tomato base', 'slow-roasted pork'],
        'flavors':         ['citrusy from mojo', 'earthy and hearty', 'sweet from caramelised plantain', 'savoury and deeply satisfying'],
        'dining_context':  ['a Havana paladar restaurant', 'a family Sunday lechón', 'a roadside food stall', 'a Cuban café abroad'],
        'cultural_notes':  ['paladares are privately owned Cuban restaurants that developed as an alternative to state food service', 'Cuban cuisine reflects Spanish, African, and Caribbean indigenous influences'],
        'pairings':        ['mojito', 'Cuba Libre', 'Cristal beer', 'guarapo sugarcane juice'],
    },
    'canadian': {
        'ingredients':     ['Quebec cheese curds', 'maple syrup', 'wild blueberry', 'Arctic char', 'peameal bacon'],
        'flavors':         ['sweet and savoury from maple', 'rich and indulgent', 'fresh and clean', 'comforting and familiar'],
        'dining_context':  ['a Montreal poutinerie', 'a sugar shack cabane à sucre', 'a prairie farm breakfast', 'an east coast seafood shack'],
        'cultural_notes':  ['poutine emerged from Quebec rural diners in the 1950s and became Canada\'s most internationally recognised dish', 'maple syrup production is a seasonal Quebec ritual celebrated at family sugar shacks'],
        'pairings':        ['Canadian rye whisky', 'Molson Canadian', 'maple latte', 'Nanaimo bar dessert'],
    },
    'australian': {
        'ingredients':     ['Vegemite', 'macadamia nut', 'bush tucker wattle seed', 'barramundi', 'Anzac oats'],
        'flavors':         ['intensely savoury from Vegemite', 'fresh and light', 'subtly sweet with native fruits', 'clean and straightforward'],
        'dining_context':  ['a beachside café', 'a backyard barbie', 'an outback pub meal', 'a Melbourne brunch café'],
        'cultural_notes':  ['Australian cuisine has absorbed multicultural influences and developed a distinct contemporary style', 'bush tucker movement incorporates indigenous ingredients like wattleseed and lemon myrtle into modern cooking'],
        'pairings':        ['flat white coffee', 'Coopers Pale Ale', 'Sauvignon Blanc', 'Tim Tam with tea'],
    },
    'taiwanese': {
        'ingredients':     ['soy-braised pork', 'oyster sauce', 'basil', 'scallion', 'fermented tofu'],
        'flavors':         ['deeply savoury from braising', 'umami-rich', 'subtly sweet and aromatic', 'comforting and warming'],
        'dining_context':  ['a Taipei night market', 'a traditional beef noodle restaurant', 'a morning soy milk and scallion pancake shop', 'a family dumpling house'],
        'cultural_notes':  ['Taiwanese night markets are a pillar of social life and street food culture', 'bubble tea was invented in Taiwan and exported globally as one of the most influential food trends of recent decades'],
        'pairings':        ['bubble milk tea', 'Taiwanese lager', 'soy milk warm', 'Kavalan whisky'],
    },
    'filipino': {
        'ingredients':     ['cane vinegar', 'bagoong shrimp paste', 'calamansi lime', 'patis fish sauce', 'annatto seeds'],
        'flavors':         ['tangy and savoury from vinegar', 'rich and porky', 'subtly sweet and sour', 'deeply umami'],
        'dining_context':  ['a family birthday lechón', 'a turo-turo cafeteria', 'a beach seafood restaurant', 'a Manila restaurant abroad'],
        'cultural_notes':  ['Filipino adobo was the Spanish colonisers\' term for the indigenous vinegar and salt preservation technique', 'kamayan feasts eaten with hands from banana leaves are experiencing a cultural revival'],
        'pairings':        ['San Miguel beer', 'sago\'t gulaman drink', 'lambanog coconut spirit', 'fresh calamansi juice'],
    },
    'burmese': {
        'ingredients':     ['fermented tea leaves laphet', 'dried shrimp', 'fish paste ngapi', 'turmeric', 'lemongrass'],
        'flavors':         ['pungent and fermented', 'savoury and slightly sour', 'warming with turmeric', 'complex and earthy'],
        'dining_context':  ['a Yangon tea shop', 'a traditional Burmese home breakfast', 'a mohinga street stall at dawn', 'a Mandalay restaurant'],
        'cultural_notes':  ['laphet fermented tea leaf salad is a uniquely Burmese ingredient used in salads and as a stimulant snack', 'mohinga fish noodle soup is considered the national dish and eaten as breakfast across the country'],
        'pairings':        ['Myanmar Beer', 'lahpet yay tea leaf tea', 'toddy palm juice', 'fresh lime soda'],
    },
    'cambodian': {
        'ingredients':     ['prahok fermented fish paste', 'kroeung lemongrass paste', 'kaffir lime', 'banana blossom', 'fresh turmeric'],
        'flavors':         ['delicate and herbal', 'subtly fermented and umami', 'fresh with lemongrass', 'lightly sweet and fragrant'],
        'dining_context':  ['a Phnom Penh riverside restaurant', 'a Siem Reap market food stall', 'a traditional home kitchen', 'a village feast during festival season'],
        'cultural_notes':  ['Cambodian cuisine shares roots with Thai and Vietnamese cooking but has its own distinct identity shaped by Khmer culture', 'prahok is a uniquely Cambodian ingredient that foreigners find challenging but locals consider essential'],
        'pairings':        ['Angkor beer', 'sugarcane juice', 'fresh coconut water', 'palm wine'],
    },
    'uzbek': {
        'ingredients':     ['lamb tail fat kurdyuk', 'yellow carrots', 'cumin', 'Devzira rice', 'cottonseed oil'],
        'flavors':         ['richly meaty and caraway-forward', 'deeply savoury from lamb fat', 'subtly sweet from carrots', 'warming and hearty'],
        'dining_context':  ['a Samarkand chaikhana teahouse', 'a family plov ceremony', 'a Tashkent restaurant', 'a bazaar food stall'],
        'cultural_notes':  ['plov rice pilaf is considered the cornerstone of Uzbek hospitality and is cooked by men for important occasions', 'Uzbek cuisine sits at the crossroads of the ancient Silk Road trade routes'],
        'pairings':        ['black tea with sugar', 'ayran', 'Sarbast lager', 'non flatbread alongside'],
    },
    'azerbaijani': {
        'ingredients':     ['dried sour plums', 'saffron', 'quince', 'pomegranate', 'chess herbs (dill, parsley, tarragon, mint)'],
        'flavors':         ['fragrant and saffron-gilded', 'sweet-sour from fruit', 'aromatic with fresh herbs', 'richly layered'],
        'dining_context':  ['a Baku meykhana restaurant', 'a traditional Azerbaijani home dinner', 'a wedding feast', 'a Caspian seafood restaurant'],
        'cultural_notes':  ['Azerbaijani cuisine reflects Turkic, Persian, and Caucasian influences meeting at a historical crossroads', 'tea drinking is a ritual — black tea served in armudu pear-shaped glasses accompanies every social encounter'],
        'pairings':        ['armudu black tea', 'doshab grape molasses', 'Xirdalan beer', 'sherbet fruit drink'],
    },
    'armenian': {
        'ingredients':     ['dried apricots zardalu', 'pomegranate', 'lamb shoulder', 'tarragon', 'madzoon yoghurt'],
        'flavors':         ['sweet-sour from pomegranate and apricot', 'warmly herbal', 'rich from slow-cooked lamb', 'subtly tangy'],
        'dining_context':  ['a Yerevan restaurant', 'a family khorovats barbecue Sunday', 'a traditional home holiday table', 'an Armenian diaspora community event'],
        'cultural_notes':  ['Armenia claims the world\'s oldest winery dating to 4100 BC and has a deep wine-making heritage', 'the Armenian genocide shaped diaspora communities who carried the cuisine globally'],
        'pairings':        ['Armenian brandy', 'pomegranate wine', 'madzoon tan yoghurt drink', 'Armenian cognac'],
    },
    'afghan': {
        'ingredients':     ['qorma onion sauce', 'dried sour grapes kishmish', 'cardamom', 'saffron', 'bolani stuffing herbs'],
        'flavors':         ['fragrant and warming', 'subtly sweet from dried fruit', 'aromatic with cardamom and saffron', 'hearty and rice-forward'],
        'dining_context':  ['a traditional Afghan home dinner', 'an Eid celebration feast', 'an Afghan restaurant abroad', 'a teahouse on the Silk Road route'],
        'cultural_notes':  ['Afghan hospitality tradition demands feeding guests regardless of the host\'s circumstances', 'kabuli pallow rice is the national dish, traditionally cooked for the most important occasions'],
        'pairings':        ['qymaq cream tea', 'doogh', 'green cardamom tea', 'fresh pomegranate juice'],
    },
    'tunisian': {
        'ingredients':     ['harissa chilli paste', 'tabil coriander spice blend', 'preserved lemon', 'olive oil', 'dried rose petals'],
        'flavors':         ['fiery and aromatic', 'bright with preserved lemon', 'deeply savoury', 'boldly spiced and warming'],
        'dining_context':  ['a Tunis medina restaurant', 'a seaside fish restaurant', 'a family couscous Friday', 'a market food stall'],
        'cultural_notes':  ['Tunisian cuisine is the spiciest of the Maghreb cuisines thanks to the importance of harissa', 'Tunisia is the world\'s third largest olive oil producer and olive oil underpins the cuisine'],
        'pairings':        ['mint tea', 'Celtia beer', 'boukha fig spirit', 'fresh lemon juice'],
    },
    'bolivian': {
        'ingredients':     ['llajua chilli salsa', 'chuño freeze-dried potato', 'quinoa', 'ají amarillo', 'charque dried llama meat'],
        'flavors':         ['earthy from Andean ingredients', 'subtly spiced', 'hearty and filling', 'simple and honest'],
        'dining_context':  ['a La Paz salteñería morning', 'a market lunch counter', 'a traditional Andean home', 'an indigenous community festival feast'],
        'cultural_notes':  ['Bolivia preserves some of the most ancient Andean food traditions including chuño freeze-drying which dates to pre-Inca times', 'salteñas are distinct from Argentinian empanadas with a juicy broth filling'],
        'pairings':        ['api maize drink warm', 'singani grape spirit', 'cola morada', 'chicha de maíz'],
    },
    'ecuadorian': {
        'ingredients':     ['aji criollo', 'culantro', 'tomate de árbol tree tomato', 'choclo corn', 'mote hominy'],
        'flavors':         ['fresh and citrusy', 'subtly spiced and herbal', 'earthy from corn', 'bright and satisfying'],
        'dining_context':  ['a Quito mercado central', 'a Guayaquil ceviche bar', 'a traditional home lunch', 'an indigenous market food stall in the Andes'],
        'cultural_notes':  ['Ecuador\'s position on the equator gives it extraordinary biodiversity of ingredients from coast, highlands, and Amazon', 'llapingachos potato cakes are a highland staple tied to Andean agricultural tradition'],
        'pairings':        ['naranjilla juice', 'chicha de jora', 'Club beer', 'canelazo hot cinnamon drink'],
    },
    'chilean': {
        'ingredients':     ['merkén smoked chilli', 'pebre herb salsa', 'shellfish from Patagonia', 'Carménère wine', 'mote wheat'],
        'flavors':         ['smoky and herbal', 'fresh from the sea', 'simple and hearty', 'subtly sweet with mote'],
        'dining_context':  ['a Santiago picada local restaurant', 'a Valparaíso seafood market', 'a family asado', 'a Patagonian lamb restaurant'],
        'cultural_notes':  ['Chilean cuisine reflects the extraordinary length of the country with Pacific seafood, Andean ingredients, and Patagonian lamb all defining different regions', 'the completo hot dog with avocado is a peculiarly Chilean street food obsession'],
        'pairings':        ['Carménère', 'terremoto cocktail', 'Cristal lager', 'mote con huesillo peach drink'],
    },
    'venezuelan': {
        'ingredients':     ['precooked white cornmeal masarepa', 'guasacaca avocado sauce', 'papelón brown sugar', 'black beans caraotas', 'Queso de mano fresh cheese'],
        'flavors':         ['sweet-savoury from cornmeal base', 'fresh from avocado sauce', 'hearty and comforting', 'tropical and vibrant'],
        'dining_context':  ['a Caracas arepera', 'a family hallacas making session at Christmas', 'a Colombian-Venezuelan border town restaurant', 'a Venezuelan diaspora restaurant abroad'],
        'cultural_notes':  ['the arepa is Venezuela\'s daily bread — eaten at all meals in countless configurations', 'hallacas Christmas preparation is a multi-day family tradition where the whole extended family participates'],
        'pairings':        ['Malta dark malt drink', 'chicha de arroz', 'ron Santa Teresa rum', 'papelón con limón'],
    },
    'russian': {
        'ingredients':     ['sour cream smetana', 'dill', 'salted herring', 'buckwheat', 'pickled vegetables'],
        'flavors':         ['rich and dairy-forward', 'subtly sour from fermentation', 'hearty and warming', 'savoury and satisfying'],
        'dining_context':  ['a Moscow restaurant', 'a family New Year table', 'a dacha summer kitchen', 'a traditional Russian stolovaya canteen'],
        'cultural_notes':  ['Russian New Year table is the most important annual food event, laden with Olivier salad, herring under fur coat, and other Soviet-era staples', 'the Russian tea tradition using a samovar is centuries old and central to social hospitality'],
        'pairings':        ['vodka', 'kvas', 'black tea from a samovar', 'kefir'],
    },
}

# ---------------------------------------------------------------------------
# Review templates
# ---------------------------------------------------------------------------
TEMPLATES = [
    {
        'title_tmpl': 'First time trying {name} — completely converted',
        'body_tmpl': (
            "I had never tried {name} before this visit and I wasn't sure what to expect. "
            "The {flavor} taste hit immediately and made sense of the dish in a way descriptions never quite do. "
            "{ingredient} is an ingredient I'd not encountered used quite like this before.\n\n"
            "The {dining_context} setting added something to the experience — this kind of food makes sense in that environment. "
            "{cultural_note}. My server recommended {pairing} alongside and it was exactly right. "
            "I've been telling everyone to try {name}. Outstanding first encounter."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Best {name} I\'ve had — and I\'ve tried a few',
        'body_tmpl': (
            "Having eaten {name} at several restaurants over the past year, I can say this version is the best. "
            "The {flavor} quality is more pronounced here than anywhere else I've tried. "
            "{ingredient} is handled with real knowledge — you can taste the difference.\n\n"
            "This is proper {dining_context} cooking, not an adaptation for foreign tastes. "
            "{pairing} was the obvious choice and the combination was perfect. "
            "{cultural_note}. Would return for this dish alone."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Restaurant review — {name} that actually delivered',
        'body_tmpl': (
            "I'm sceptical of any restaurant claiming to do {name} well, having been disappointed often enough. "
            "This one delivered. The {flavor} base was authentic and the use of {ingredient} showed real knowledge.\n\n"
            "{cultural_note}. The atmosphere was genuinely {dining_context}, which the food matched. "
            "{pairing} came with the meal as it should. "
            "The portions were generous and the price was fair. A reliable place for this dish."
        ),
        'rating': 4,
    },
    {
        'title_tmpl': 'Home cooking attempt — {name} from scratch',
        'body_tmpl': (
            "I spent an afternoon making {name} from scratch following a traditional recipe. "
            "Getting {ingredient} right was the main challenge — it's not as straightforward as it looks. "
            "The {flavor} result was rewarding once I got it right.\n\n"
            "{cultural_note}. I served it with {pairing} as the recipe suggested and the pairing made sense. "
            "It took longer than I expected but the outcome was genuinely satisfying. "
            "Making {name} yourself gives you a new appreciation for what goes into it at a restaurant."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Comparing {name} across three restaurants — an honest verdict',
        'body_tmpl': (
            "I ate {name} at three different restaurants in the same week to compare. The results were illuminating. "
            "The use of {ingredient} varied significantly — only one got it right. "
            "The {flavor} profile should be consistent but interpretation differs widely.\n\n"
            "{cultural_note}. The best version came from {dining_context}, which felt authentic. "
            "{pairing} was offered at all three but only one knew how to serve it properly. "
            "The gap between mediocre and excellent {name} is larger than you'd think."
        ),
        'rating': 4,
    },
    {
        'title_tmpl': 'Cultural discovery through {name}',
        'body_tmpl': (
            "{name} opened a door into a cuisine I'd previously known almost nothing about. "
            "The {flavor} flavours are unlike anything in my usual rotation and I mean that positively. "
            "{cultural_note}. Understanding that context made the dish taste different — richer with meaning.\n\n"
            "I learned that {ingredient} is central to this cuisine's character, not just a seasoning. "
            "The {dining_context} setting was authentic and helpful for understanding what I was eating. "
            "{pairing} completed the picture. A genuinely educational meal."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Ingredient appreciation — what makes {name} special',
        'body_tmpl': (
            "What sets {name} apart is the handling of {ingredient}. "
            "In lesser versions this is treated as a background note. Here it's central and the {flavor} result shows it. "
            "I've started buying it to cook with at home after this experience.\n\n"
            "{cultural_note}. The {dining_context} atmosphere was right for this kind of food. "
            "I had {pairing} as recommended and it matched well. "
            "If you want to understand what makes this cuisine distinctive, {name} is the place to start."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': '{name} as comfort food — exactly what I needed',
        'body_tmpl': (
            "Some dishes exist to comfort and {name} is absolutely in that category. "
            "The {flavor} quality works on something almost primal — "
            "you feel the warmth of it immediately. {ingredient} does work that no substitute can replicate.\n\n"
            "{cultural_note}. There's something about the {dining_context} context that reinforces the comfort effect. "
            "{pairing} alongside is the traditional way and it makes complete sense. "
            "I come back to this dish when I need something dependable and restorative."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Cooking class experience — learning {name} properly',
        'body_tmpl': (
            "I took a cooking class specifically to learn how to make {name} correctly. "
            "The instructor explained why {ingredient} is used the way it is — "
            "something I'd never understood from just eating it. The {flavor} result when you make it yourself is different.\n\n"
            "{cultural_note}. We learned how {dining_context} shapes the way this dish is eaten. "
            "The class ended with the meal and a glass of {pairing}. "
            "I've made it three times since and each time it improves. Highly recommend the cooking class approach."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Street food {name} — the authentic version',
        'body_tmpl': (
            "The best {name} I've ever had came from a street stall, not a restaurant. "
            "The {flavor} intensity was completely different — more direct and uncompromised. "
            "{ingredient} was used without hesitation, the way it should be.\n\n"
            "{cultural_note}. The {dining_context} setting meant eating standing up or on a low stool, "
            "which is how this food is supposed to be encountered. {pairing} was sold right next to it. "
            "Don't wait to find the 'right' restaurant. Find the street version first."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Holiday memory — {name} that transported me back',
        'body_tmpl': (
            "I first ate {name} on a trip five years ago and have been searching for a version this good ever since. "
            "This restaurant finally delivered the {flavor} quality I remembered. "
            "{ingredient} was handled correctly — something most restaurants here get slightly wrong.\n\n"
            "{cultural_note}. It was the {dining_context} memory that I was really chasing and this recreated it. "
            "{pairing} was offered and brought the whole experience together. "
            "Some dishes are attached to a time and place. This one finally restored that attachment."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Underwhelming {name} — expected more',
        'body_tmpl': (
            "I was looking forward to {name} here based on the reputation. The reality was disappointing. "
            "The {flavor} character that makes this dish special was muted — either from shortcuts with {ingredient} "
            "or from scaling up production at the expense of quality.\n\n"
            "{cultural_note}. The {dining_context} setting I was hoping for wasn't quite there either. "
            "{pairing} was available but not suggested appropriately. "
            "I've had much better versions elsewhere. Two stars because the dish concept is sound; the execution let it down."
        ),
        'rating': 2,
    },
    {
        'title_tmpl': 'Honest verdict on {name} — good but not exceptional',
        'body_tmpl': (
            "{name} here was solidly made — {flavor} without anything to complain about. "
            "{ingredient} was present and handled reasonably. "
            "But something was missing from the depth that this dish should have.\n\n"
            "{cultural_note}. The {dining_context} atmosphere was pleasant enough. "
            "{pairing} was available and a good suggestion. "
            "For a reliable version of {name} this works. For an exceptional one, I'd keep looking. Three stars."
        ),
        'rating': 3,
    },
    {
        'title_tmpl': '{name} for a dinner party — went down extremely well',
        'body_tmpl': (
            "I made {name} for eight guests who had varying familiarity with the cuisine. "
            "Every single person asked for the recipe. The {flavor} profile was the main talking point — "
            "no one had quite experienced {ingredient} used that way before.\n\n"
            "{cultural_note}. I explained the {dining_context} context as I served it which helped people appreciate it fully. "
            "{pairing} was what I offered alongside and it worked perfectly. "
            "Excellent dinner party dish — impressive without being inaccessible."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Finding the best {name} in the city — a personal search',
        'body_tmpl': (
            "I spent three months trying every version of {name} I could find locally. "
            "The variation in quality is extraordinary. The best version handled {ingredient} with genuine knowledge "
            "and the {flavor} result was noticeably superior.\n\n"
            "{cultural_note}. The winning restaurant had the right {dining_context} feel — "
            "unpretentious and focused on the food. {pairing} was suggested correctly. "
            "Worth the search. When {name} is made properly it's a completely different experience."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Why {name} deserves more attention',
        'body_tmpl': (
            "{name} rarely gets the international recognition it deserves. The {flavor} complexity is genuine, "
            "not simple, and the technique involved in using {ingredient} correctly takes real skill.\n\n"
            "{cultural_note}. I encountered it first in {dining_context} and that context helped me understand it properly. "
            "{pairing} is the natural accompaniment and the combination makes the case for the dish. "
            "If you haven't explored this cuisine seriously, {name} is the dish to start with."
        ),
        'rating': 4,
    },
    {
        'title_tmpl': 'Traditional versus modern {name} — which wins?',
        'body_tmpl': (
            "I've now had {name} prepared traditionally and in a modern interpretation. Both are interesting. "
            "The traditional version emphasises {ingredient} in the way {cultural_note}. "
            "The {flavor} character is more pronounced and direct.\n\n"
            "The modern interpretation is technically impressive but loses something. "
            "The {dining_context} context for the traditional version adds meaning that plating alone can't provide. "
            "{pairing} with the traditional version made more sense than with the modern. "
            "Traditional wins, but the modern is worth trying once."
        ),
        'rating': 4,
    },
    {
        'title_tmpl': '{name} exceeded every expectation',
        'body_tmpl': (
            "I went in with low expectations — I'd had mediocre versions before. "
            "What I found was {name} made with real commitment to {ingredient} and technique. "
            "The {flavor} result was more complex and satisfying than anything I'd had before.\n\n"
            "{cultural_note}. The {dining_context} was exactly right for this kind of eating. "
            "{pairing} was offered as the natural choice and it elevated everything. "
            "When a dish you thought you knew surprises you completely, that's worth celebrating. "
            "Five stars without hesitation."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Decent {name} — nothing more, nothing less',
        'body_tmpl': (
            "{name} at this place was fine. The {flavor} flavour was there but not distinguished. "
            "{ingredient} was present in the right quantities but without the care that makes the difference. "
            "You can taste when something is being made to a formula.\n\n"
            "{cultural_note}. The {dining_context} setting was generic rather than immersive. "
            "{pairing} was offered but not explained. "
            "If you're in the area and want {name} it'll do. If you're going out of your way, look elsewhere."
        ),
        'rating': 3,
    },
    {
        'title_tmpl': 'The {name} I grew up eating — memory as a review',
        'body_tmpl': (
            "I grew up eating {name} and have strong opinions shaped by memory. "
            "The version here triggered that recognition in the first bite — the {flavor} was right, "
            "{ingredient} was handled the way it should be.\n\n"
            "{cultural_note}. Growing up it was always {dining_context}, which shaped my reference point entirely. "
            "{pairing} alongside it is the only way it makes sense to me. "
            "It's hard to be objective about food you have emotional history with, but objectively: this is very good."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Pairing {name} correctly — a note on {pairing}',
        'body_tmpl': (
            "Most people overlook how much the right drink changes {name}. I ordered it with {pairing} "
            "and the {flavor} elements of the dish sharpened considerably against the pairing. "
            "{ingredient} in particular became more prominent in a good way.\n\n"
            "{cultural_note}. The {dining_context} is where you learn these pairings — they evolved together. "
            "If you've been having {name} with the wrong drink, try it correctly once. "
            "It's a genuinely different experience. The restaurant deserves credit for getting this right."
        ),
        'rating': 4,
    },
    {
        'title_tmpl': 'A dish that tells its story — {name} reviewed',
        'body_tmpl': (
            "You can taste history in {name} if you know what to look for. "
            "{cultural_note}. The {flavor} character reflects those layers — "
            "{ingredient} doesn't appear by accident; it came from a specific tradition.\n\n"
            "The {dining_context} setting made sense of it. You understand the food differently when the context is right. "
            "{pairing} alongside is part of that story. "
            "Some food is just fuel. {name}, properly made, is something more. "
            "This version told the story well."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Spice level warning — {name} is not what I expected',
        'body_tmpl': (
            "I underestimated {name}. The {flavor} description didn't prepare me for the reality. "
            "{ingredient} brings a heat or pungency that builds steadily rather than hitting upfront. "
            "By halfway through I was sweating but couldn't stop eating.\n\n"
            "{cultural_note}. The {dining_context} setting means locals eat this with ease while visitors like me reach for water. "
            "{pairing} cut through it better than water would have. "
            "Don't order the mild version out of caution — the full version is the point. "
            "I'd go back. Three stars only because I wasn't warned."
        ),
        'rating': 3,
    },
]

FIRST_NAMES = [
    'Sarah', 'James', 'Olivia', 'Liam', 'Emma', 'Noah', 'Ava', 'Ethan',
    'Sophia', 'Mason', 'Isabella', 'Logan', 'Charlotte', 'Lucas', 'Amelia',
    'Jackson', 'Mia', 'Aiden', 'Harper', 'Sebastian', 'Emily', 'Jack',
    'Elizabeth', 'Owen', 'Sofia', 'Henry', 'Avery', 'Samuel', 'Ella',
    'Daniel', 'Scarlett', 'Benjamin', 'Victoria', 'Aria', 'Dylan', 'Grace',
    'Michael', 'Chloe', 'Ryan', 'Marcus', 'Diana', 'Priya', 'Kenji',
    'Fatima', 'Carlos', 'Ingrid', 'Takashi', 'Miriam', 'Stefan', 'Leila',
]

RATING_WEIGHTS = {5: 38, 4: 30, 3: 18, 2: 9, 1: 5}


def weighted_rating():
    pool = []
    for r, w in RATING_WEIGHTS.items():
        pool.extend([r] * w)
    return random.choice(pool)


def make_review(dish_name: str, cuisine_slug: str, tmpl: dict) -> tuple | None:
    facts = CUISINE_DATA.get(cuisine_slug)
    if not facts:
        return None

    ingredient    = random.choice(facts['ingredients'])
    flavor        = random.choice(facts['flavors'])
    dining_context = random.choice(facts['dining_context'])
    cultural_note = random.choice(facts['cultural_notes'])
    pairing       = random.choice(facts['pairings'])

    title = tmpl['title_tmpl'].format(
        name=dish_name, ingredient=ingredient, flavor=flavor,
        dining_context=dining_context, cultural_note=cultural_note, pairing=pairing,
    )
    body = tmpl['body_tmpl'].format(
        name=dish_name, ingredient=ingredient, flavor=flavor,
        dining_context=dining_context, cultural_note=cultural_note, pairing=pairing,
    )
    base_rating = tmpl['rating']
    rating = max(1, min(5, base_rating + random.choice([-1, 0, 0, 0, 1])))
    if random.random() < 0.25:
        rating = weighted_rating()
    return title, body, rating


def run(args):
    from app import create_app, db
    from app.models import Subject, SubCategory, Review, Category

    app = create_app('development')
    with app.app_context():
        cat = Category.query.filter_by(slug='food').first()
        if not cat:
            print('Category "food" not found')
            import sys; sys.exit(1)

        if args.slug:
            sc = SubCategory.query.filter_by(category_id=cat.id, slug=args.slug).first()
            if not sc:
                print(f'Cuisine slug "{args.slug}" not found under food')
                import sys; sys.exit(1)
            subcategories = [sc]
        else:
            subcategories = SubCategory.query.filter_by(category_id=cat.id).order_by(SubCategory.id).all()

        # Collect all subjects across selected subcategories
        all_subjects = []
        for sc in subcategories:
            subjects = Subject.query.filter_by(subcategory_id=sc.id).order_by(Subject.id).all()
            all_subjects.extend(subjects)

        if args.start_from and not args.slug:
            # start_from targets a cuisine subcategory slug: skip cuisines before it
            sc_slugs = [sc.slug for sc in subcategories]
            if args.start_from in sc_slugs:
                idx = sc_slugs.index(args.start_from)
                remaining_scs = subcategories[idx:]
                all_subjects = []
                for sc in remaining_scs:
                    subjects = Subject.query.filter_by(subcategory_id=sc.id).order_by(Subject.id).all()
                    all_subjects.extend(subjects)
                print(f'Resuming from cuisine "{args.start_from}" ({len(all_subjects)} dishes left)')
            else:
                print(f'--start-from slug "{args.start_from}" not found in cuisines, processing all')

        print(f'Processing {len(all_subjects)} dishes, ~{args.count} reviews each')

        for subj in all_subjects:
            cuisine_slug = subj.subcategory.slug
            if cuisine_slug not in CUISINE_DATA:
                print(f'  SKIP {subj.name} — no facts data for cuisine "{cuisine_slug}"')
                continue

            deleted = Review.query.filter_by(subject_id=subj.id, source_site='sample').delete()
            deleted += Review.query.filter_by(subject_id=subj.id, source_site='generated').delete()
            db.session.commit()

            target = random.randint(12, 25)
            used_titles: set[str] = set()
            reviews_added = 0

            shuffled = TEMPLATES[:]
            random.shuffle(shuffled)
            pool = (shuffled * ((target // len(shuffled)) + 2))[:target * 2]

            for tmpl in pool:
                if reviews_added >= target:
                    break
                result = make_review(subj.name, cuisine_slug, tmpl)
                if result is None:
                    continue
                title, body, rating = result
                if title in used_titles:
                    continue
                used_titles.add(title)

                days_ago = random.randint(30, 365 * 3)
                rev = Review(
                    subject_id=subj.id,
                    title=title,
                    body=body,
                    rating=rating,
                    author_name=random.choice(FIRST_NAMES),
                    source_site='generated',
                    original_date=datetime.utcnow() - timedelta(days=days_ago),
                    is_published=True,
                )
                db.session.add(rev)
                reviews_added += 1

            db.session.commit()
            subj.update_stats()
            db.session.commit()
            print(f'  {subj.name} [{cuisine_slug}]: {reviews_added} reviews (avg {subj.avg_rating:.1f}★, deleted {deleted})')

        print('Done.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--slug', help='Single cuisine slug (e.g. thai)')
    parser.add_argument('--start-from', dest='start_from', help='Resume from this cuisine slug')
    parser.add_argument('--count', type=int, default=15, help='Reviews per dish (default 15)')
    args = parser.parse_args()
    run(args)
