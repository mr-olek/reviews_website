#!/usr/bin/env python3
"""
Replace generic template reviews for Countries with specific, data-driven
travel reviews referencing real cities, landmarks, dishes, and culture.

Usage:
  python3 generate_country_reviews.py               # all countries
  python3 generate_country_reviews.py --slug france # single country
  python3 generate_country_reviews.py --start-from vietnam  # resume
"""
from __future__ import annotations
import argparse, os, random, re, sys, time
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# Country-specific facts: (slug, cities, landmarks, dishes, highlights, challenges)
# ---------------------------------------------------------------------------
COUNTRY_DATA = {
    'ukraine': {
        'cities':     ['Kyiv', 'Lviv', 'Odesa', 'Kharkiv'],
        'landmarks':  ['Kyiv Pechersk Lavra', 'St. Sophia Cathedral', 'Lviv Old Town', 'Maidan Nezalezhnosti', 'Andriivskyi Uzviz'],
        'dishes':     ['borscht', 'varenyky', 'chicken Kyiv', 'deruny', 'salo with rye bread'],
        'highlights': ['warm hospitality', 'baroque architecture', 'vibrant café culture', 'rich folk art tradition'],
        'challenges': ['language barrier outside tourist areas', 'limited English menus', 'finding ATMs for cash'],
    },
    'france': {
        'cities':     ['Paris', 'Lyon', 'Marseille', 'Nice', 'Bordeaux'],
        'landmarks':  ['Eiffel Tower', 'Louvre Museum', 'Palace of Versailles', 'Mont Saint-Michel', 'Sacré-Cœur'],
        'dishes':     ['croissants', 'coq au vin', 'bouillabaisse', 'crème brûlée', 'foie gras', 'ratatouille'],
        'highlights': ['world-class cuisine', 'art and fashion scene', 'wine regions', 'café culture'],
        'challenges': ['tourist crowds around Paris landmarks', 'expensive restaurants in tourist areas', 'Parisians not always patient with tourists'],
    },
    'spain': {
        'cities':     ['Barcelona', 'Madrid', 'Seville', 'Granada', 'San Sebastián'],
        'landmarks':  ['Sagrada Família', 'Alhambra Palace', 'Park Güell', 'Prado Museum', 'Plaza Mayor'],
        'dishes':     ['paella', 'tapas', 'gazpacho', 'jamón ibérico', 'churros con chocolate', 'patatas bravas'],
        'highlights': ['incredible food culture', 'flamenco shows', 'vibrant nightlife', 'beautiful beaches'],
        'challenges': ['late dining hours take adjusting', 'siesta closures', 'pickpockets in Barcelona'],
    },
    'united-states': {
        'cities':     ['New York', 'San Francisco', 'New Orleans', 'Chicago', 'Los Angeles'],
        'landmarks':  ['Grand Canyon', 'Statue of Liberty', 'Yellowstone', 'Times Square', 'Golden Gate Bridge'],
        'dishes':     ['New York pizza', 'New Orleans gumbo', 'Texas BBQ', 'lobster roll', 'Chicago deep-dish'],
        'highlights': ['incredible geographic diversity', 'world-class national parks', 'buzzing cities', 'road trip culture'],
        'challenges': ['tipping culture surprises visitors', 'distances between attractions', 'expensive healthcare if you get sick'],
    },
    'china': {
        'cities':     ['Beijing', 'Shanghai', 'Xi\'an', 'Chengdu', 'Guilin'],
        'landmarks':  ['Great Wall', 'Forbidden City', 'Terracotta Army', 'West Lake', 'Li River karsts'],
        'dishes':     ['Peking duck', 'dim sum', 'mapo tofu', 'hot pot', 'xiaolongbao', 'kung pao chicken'],
        'highlights': ['extraordinary ancient history', 'vast natural scenery', 'cutting-edge cities', 'incredible cuisine variety'],
        'challenges': ['Great Firewall blocks many apps', 'language barrier is significant', 'payment apps can be tricky for foreigners'],
    },
    'italy': {
        'cities':     ['Rome', 'Florence', 'Venice', 'Naples', 'Bologna'],
        'landmarks':  ['Colosseum', 'Vatican Museums', 'Uffizi Gallery', 'Amalfi Coast', 'Cinque Terre'],
        'dishes':     ['Neapolitan pizza', 'fresh pasta', 'risotto', 'tiramisu', 'gelato', 'osso buco'],
        'highlights': ['unmatched art and architecture', 'world-famous cuisine', 'beautiful coastline', 'passionate locals'],
        'challenges': ['overcrowded sites in peak summer', 'scooter traffic chaos', 'tourist trap restaurants near monuments'],
    },
    'turkey': {
        'cities':     ['Istanbul', 'Cappadocia', 'Ephesus', 'Antalya', 'Bodrum'],
        'landmarks':  ['Hagia Sophia', 'Blue Mosque', 'Topkapi Palace', 'Cappadocia fairy chimneys', 'Pamukkale terraces'],
        'dishes':     ['kebab', 'baklava', 'meze', 'lahmacun', 'simit', 'Turkish breakfast'],
        'highlights': ['stunning blend of Europe and Asia', 'extraordinary historical sites', 'exceptional food', 'hospitable people'],
        'challenges': ['carpet and tour touts in Istanbul', 'transport between Cappadocia sites', 'currency fluctuations'],
    },
    'mexico': {
        'cities':     ['Mexico City', 'Oaxaca', 'Merida', 'San Miguel de Allende', 'Guadalajara'],
        'landmarks':  ['Chichén Itzá', 'Teotihuacán', 'Palenque', 'Cenote Ik Kil', 'Monte Albán'],
        'dishes':     ['tacos al pastor', 'mole negro', 'tamales', 'ceviche', 'chiles en nogada', 'tlayudas'],
        'highlights': ['incredible ancient ruins', 'vibrant indigenous culture', 'world-class cuisine', 'colourful colonial towns'],
        'challenges': ['stomach bugs for first-timers', 'safety varies widely by region', 'altitude sickness in Mexico City'],
    },
    'thailand': {
        'cities':     ['Bangkok', 'Chiang Mai', 'Chiang Rai', 'Krabi', 'Koh Samui'],
        'landmarks':  ['Wat Phra Kaew', 'Wat Arun', 'White Temple', 'Phi Phi Islands', 'Doi Inthanon'],
        'dishes':     ['pad thai', 'green curry', 'som tum', 'mango sticky rice', 'tom yum soup', 'massaman curry'],
        'highlights': ['incredible Buddhist temples', 'beautiful islands', 'amazing street food', 'affordable luxury'],
        'challenges': ['extreme heat in summer', 'overcrowded islands in peak season', 'tourist scams in Bangkok'],
    },
    'germany': {
        'cities':     ['Berlin', 'Munich', 'Hamburg', 'Cologne', 'Dresden'],
        'landmarks':  ['Brandenburg Gate', 'Neuschwanstein Castle', 'Cologne Cathedral', 'Reichstag Building', 'Checkpoint Charlie'],
        'dishes':     ['bratwurst', 'schnitzel', 'pretzels', 'sauerkraut', 'Black Forest cake', 'Bavarian beer'],
        'highlights': ['Christmas markets', 'excellent public transport', 'rich history', 'vibrant arts scene in Berlin'],
        'challenges': ['can feel expensive compared to neighbours', 'shops closed on Sundays', 'very formal service style'],
    },
    'united-kingdom': {
        'cities':     ['London', 'Edinburgh', 'Bath', 'Oxford', 'York'],
        'landmarks':  ['Tower of London', 'Stonehenge', 'Edinburgh Castle', 'Buckingham Palace', 'Lake District'],
        'dishes':     ['fish and chips', 'full English breakfast', 'chicken tikka masala', 'Cornish pasty', 'Welsh rarebit'],
        'highlights': ['incredible museums (free in London)', 'stunning countryside', 'rich literary history', 'pub culture'],
        'challenges': ['very expensive for budget travellers', 'unpredictable weather', 'London crowds year-round'],
    },
    'japan': {
        'cities':     ['Tokyo', 'Kyoto', 'Osaka', 'Hiroshima', 'Nara'],
        'landmarks':  ['Fushimi Inari Shrine', 'Arashiyama Bamboo Grove', 'Shibuya Crossing', 'Hiroshima Peace Memorial', 'Mt. Fuji'],
        'dishes':     ['sushi', 'ramen', 'tempura', 'takoyaki', 'wagyu beef', 'matcha everything'],
        'highlights': ['extraordinary cleanliness and order', 'incredible food culture', 'seamless public transport', 'unique blend of ancient and ultra-modern'],
        'challenges': ['very expensive', 'cash-heavy society', 'Golden Week crowds'],
    },
    'greece': {
        'cities':     ['Athens', 'Santorini', 'Mykonos', 'Thessaloniki', 'Crete'],
        'landmarks':  ['Acropolis', 'Parthenon', 'Santorini caldera', 'Delphi', 'Palace of Knossos'],
        'dishes':     ['moussaka', 'souvlaki', 'spanakopita', 'tzatziki', 'baklava', 'fresh seafood by the harbour'],
        'highlights': ['3,000 years of history', 'stunning island scenery', 'exceptional Mediterranean food', 'crystal-clear Aegean water'],
        'challenges': ['Santorini and Mykonos very pricey', 'ferries can be unreliable', 'summer heat is intense'],
    },
    'austria': {
        'cities':     ['Vienna', 'Salzburg', 'Innsbruck', 'Graz', 'Hallstatt'],
        'landmarks':  ['Schönbrunn Palace', 'St. Stephen\'s Cathedral', 'Hallstatt village', 'Hohensalzburg Fortress', 'Melk Abbey'],
        'dishes':     ['Wiener Schnitzel', 'Sachertorte', 'Apfelstrudel', 'Tafelspitz', 'Kaiserschmarrn'],
        'highlights': ['world-class classical music', 'imperial architecture', 'stunning alpine scenery', 'coffee house culture'],
        'challenges': ['expensive compared to neighbouring countries', 'tourist restaurants in Vienna overprice', 'everything closes early outside cities'],
    },
    'malaysia': {
        'cities':     ['Kuala Lumpur', 'Penang', 'Malacca', 'Kota Kinabalu', 'Langkawi'],
        'landmarks':  ['Petronas Towers', 'Batu Caves', 'George Town street art', 'Mount Kinabalu', 'Cameron Highlands'],
        'dishes':     ['nasi lemak', 'char kway teow', 'laksa', 'roti canai', 'satay', 'Penang hawker food'],
        'highlights': ['extraordinary multicultural food scene', 'affordable prices', 'lush rainforests', 'friendly locals'],
        'challenges': ['tropical heat and humidity', 'public transport outside KL', 'alcohol is pricey due to taxes'],
    },
    'portugal': {
        'cities':     ['Lisbon', 'Porto', 'Sintra', 'Faro', 'Évora'],
        'landmarks':  ['Jerónimos Monastery', 'Pena Palace', 'Duoro Valley vineyards', 'Tower of Belém', 'Cape Sagres'],
        'dishes':     ['pastel de nata', 'bacalhau', 'francesinha', 'grilled sardines', 'petiscos', 'Port wine'],
        'highlights': ['incredibly warm people', 'stunning Atlantic coastline', 'fado music', 'affordable compared to Western Europe'],
        'challenges': ['cobblestone streets tough on feet', 'some towns still very cash-based', 'getting around Algarve without a car'],
    },
    'canada': {
        'cities':     ['Vancouver', 'Montreal', 'Quebec City', 'Toronto', 'Banff'],
        'landmarks':  ['Banff National Park', 'Niagara Falls', 'Old Quebec', 'Rocky Mountains', 'Icefields Parkway'],
        'dishes':     ['poutine', 'tourtière', 'butter tarts', 'Montreal bagels', 'fresh maple syrup'],
        'highlights': ['spectacular wilderness', 'multicultural cities', 'very safe and welcoming', 'stunning national parks'],
        'challenges': ['vast distances require internal flights', 'very expensive in tourist towns', 'winter can be brutal'],
    },
    'poland': {
        'cities':     ['Kraków', 'Warsaw', 'Gdańsk', 'Wrocław', 'Poznań'],
        'landmarks':  ['Wawel Castle', 'Auschwitz-Birkenau', 'Old Town Warsaw', 'Wieliczka Salt Mine', 'Malbork Castle'],
        'dishes':     ['pierogi', 'bigos', 'żurek', 'oscypek', 'zapiekanka', 'Polish craft beer'],
        'highlights': ['remarkably affordable', 'beautiful old towns', 'moving WWII history', 'warm and hospitable locals'],
        'challenges': ['language is very difficult', 'some attitudes toward LGBTQ+ travellers', 'winter is grey and cold'],
    },
    'netherlands': {
        'cities':     ['Amsterdam', 'Rotterdam', 'Utrecht', 'Delft', 'Leiden'],
        'landmarks':  ['Rijksmuseum', 'Anne Frank House', 'Keukenhof Gardens', 'Van Gogh Museum', 'Kinderdijk windmills'],
        'dishes':     ['stroopwafel', 'bitterballen', 'herring with onions', 'Dutch cheese', 'poffertjes'],
        'highlights': ['cycling culture is wonderful', 'world-class art museums', 'charming canal cities', 'very English-friendly'],
        'challenges': ['Amsterdam extremely crowded in summer', 'accommodation very expensive', 'rain is frequent'],
    },
    'united-arab-emirates': {
        'cities':     ['Dubai', 'Abu Dhabi', 'Sharjah', 'Fujairah', 'Al Ain'],
        'landmarks':  ['Burj Khalifa', 'Sheikh Zayed Grand Mosque', 'Palm Jumeirah', 'Dubai Frame', 'Louvre Abu Dhabi'],
        'dishes':     ['Al Harees', 'shawarma', 'hummus', 'Emirati lamb ouzi', 'luqaimat', 'Camelicious ice cream'],
        'highlights': ['extraordinary modern architecture', 'world-class shopping', 'very safe', 'amazing food from every cuisine'],
        'challenges': ['brutal summer heat', 'alcohol only in licensed venues', 'public behaviour rules to respect'],
    },
    'brazil': {
        'cities':     ['Rio de Janeiro', 'São Paulo', 'Salvador', 'Florianópolis', 'Manaus'],
        'landmarks':  ['Christ the Redeemer', 'Iguazú Falls', 'Amazon rainforest', 'Copacabana Beach', 'Lençóis Maranhenses'],
        'dishes':     ['churrasco', 'feijoada', 'coxinha', 'acarajé', 'brigadeiro', 'açaí bowl'],
        'highlights': ['extraordinary natural diversity', 'electric carnival culture', 'football passion', 'warm and exuberant people'],
        'challenges': ['petty crime in cities requires vigilance', 'Portuguese barrier', 'vast country is expensive to travel internally'],
    },
    'south-korea': {
        'cities':     ['Seoul', 'Busan', 'Gyeongju', 'Jeju Island', 'Incheon'],
        'landmarks':  ['Gyeongbokgung Palace', 'Bulguksa Temple', 'Bukchon Hanok Village', 'Haeundae Beach', 'Jeju Haenyeo'],
        'dishes':     ['Korean BBQ', 'bibimbap', 'tteokbokki', 'kimchi jjigae', 'japchae', 'fried chicken with beer'],
        'highlights': ['incredible food scene', 'ultra-modern infrastructure', 'K-pop and beauty culture', 'very safe'],
        'challenges': ['vegetarians have limited options', 'everything moves at high pace', 'language barrier outside Seoul'],
    },
    'india': {
        'cities':     ['Jaipur', 'Varanasi', 'Mumbai', 'Delhi', 'Udaipur'],
        'landmarks':  ['Taj Mahal', 'Jaipur Amber Fort', 'Varanasi ghats', 'Kerala backwaters', 'Ajanta Caves'],
        'dishes':     ['biryani', 'butter chicken', 'dosa', 'chaat', 'rogan josh', 'tandoori chicken'],
        'highlights': ['overwhelming sensory experience', 'extraordinary spiritual sites', 'incredible food diversity', 'ancient living culture'],
        'challenges': ['persistent touts at tourist sites', 'Delhi belly is real', 'traffic and pollution in cities'],
    },
    'australia': {
        'cities':     ['Sydney', 'Melbourne', 'Perth', 'Brisbane', 'Hobart'],
        'landmarks':  ['Sydney Opera House', 'Great Barrier Reef', 'Uluru', 'Great Ocean Road', 'Blue Mountains'],
        'dishes':     ['meat pie', 'Vegemite toast', 'barramundi', 'pavlova', 'Tim Tams', 'flat white coffee'],
        'highlights': ['stunning wildlife unique to Australia', 'incredible beaches', 'relaxed outdoor culture', 'world-class coffee'],
        'challenges': ['extremely expensive', 'vast distances', 'wildlife can be genuinely dangerous'],
    },
    'switzerland': {
        'cities':     ['Zürich', 'Geneva', 'Bern', 'Lucerne', 'Interlaken'],
        'landmarks':  ['Matterhorn', 'Jungfraujoch', 'Lake Geneva', 'Château de Chillon', 'Rhine Falls'],
        'dishes':     ['fondue', 'raclette', 'rösti', 'Zürcher Geschnetzeltes', 'Swiss chocolate'],
        'highlights': ['jaw-dropping alpine scenery', 'Swiss precision and efficiency', 'multilingual and welcoming', 'world-class skiing'],
        'challenges': ['shockingly expensive — one of priciest countries in Europe', 'shops close early', 'eating out drains the budget fast'],
    },
    'indonesia': {
        'cities':     ['Bali', 'Yogyakarta', 'Jakarta', 'Lombok', 'Flores'],
        'landmarks':  ['Borobudur Temple', 'Prambanan', 'Mount Bromo', 'Komodo Island', 'Uluwatu Temple'],
        'dishes':     ['nasi goreng', 'rendang', 'satay', 'gado-gado', 'mie goreng', 'babi guling'],
        'highlights': ['rich Hindu and Buddhist heritage', 'incredible volcanos and diving', 'extremely affordable', 'warm and spiritual culture'],
        'challenges': ['traffic in Bali tourist areas is terrible', 'Bali belly hits many visitors', 'plastic waste on some beaches'],
    },
    'morocco': {
        'cities':     ['Marrakech', 'Fes', 'Chefchaouen', 'Essaouira', 'Casablanca'],
        'landmarks':  ['Fes Medina', 'Sahara Desert dunes', 'Jemaa el-Fna square', 'Majorelle Garden', 'Aït Benhaddou'],
        'dishes':     ['tagine', 'couscous', 'pastilla', 'harira soup', 'msemen', 'mint tea'],
        'highlights': ['mesmerising medina streets', 'Sahara Desert experience', 'incredible food', 'incredible colour and texture everywhere'],
        'challenges': ['persistent carpet sellers in medinas', 'unsolicited guides', 'navigating Fes Medina without getting lost'],
    },
    'croatia': {
        'cities':     ['Dubrovnik', 'Split', 'Hvar', 'Zadar', 'Rovinj'],
        'landmarks':  ['Dubrovnik Old Town', 'Diocletian\'s Palace', 'Plitvice Lakes', 'Krka Waterfalls', 'Hvar lavender fields'],
        'dishes':     ['peka lamb', 'fresh grilled fish', 'black risotto', 'burek', 'pag cheese', 'Dalmatian prstaci'],
        'highlights': ['stunning Adriatic coastline', 'crystalline sea', 'beautiful walled old towns', 'excellent wines'],
        'challenges': ['Dubrovnik is extremely expensive and crowded', 'summer heat is intense', 'island-hopping costs add up'],
    },
    'czech-republic': {
        'cities':     ['Prague', 'Brno', 'Český Krumlov', 'Kutná Hora', 'Olomouc'],
        'landmarks':  ['Prague Castle', 'Charles Bridge', 'Bone Church at Sedlec', 'Old Town Square', 'Český Krumlov castle'],
        'dishes':     ['svíčková', 'goulash with knedlíky', 'smažený sýr', 'trdelník', 'Czech craft beer'],
        'highlights': ['Prague is one of Europe\'s most beautiful cities', 'world\'s best beer per capita', 'affordable by Western European standards', 'incredible Gothic architecture'],
        'challenges': ['Prague Old Town overwhelmed with tourists', 'exchange offices with bad rates target tourists', 'crowded Christmas markets'],
    },
    'hungary': {
        'cities':     ['Budapest', 'Eger', 'Pécs', 'Debrecen', 'Győr'],
        'landmarks':  ['Széchenyi Thermal Bath', 'Hungarian Parliament', 'Fisherman\'s Bastion', 'Eger Castle', 'Buda Castle'],
        'dishes':     ['goulash', 'langos', 'chimney cake', 'Hortobágy pancakes', 'Tokaj wine', 'pálinka'],
        'highlights': ['Budapest is spectacularly beautiful', 'thermal bath culture', 'excellent wine regions', 'remarkably affordable'],
        'challenges': ['tourist traps near Váci utca', 'language is completely impenetrable', 'service can feel formal'],
    },
    'vietnam': {
        'cities':     ['Hanoi', 'Ho Chi Minh City', 'Hội An', 'Hạ Long Bay', 'Huế'],
        'landmarks':  ['Hạ Long Bay', 'Hội An Ancient Town', 'My Son Sanctuary', 'Phong Nha Caves', 'Hoan Kiem Lake'],
        'dishes':     ['pho', 'bánh mì', 'bún bò Huế', 'cao lầu', 'bánh xèo', 'fresh spring rolls'],
        'highlights': ['extraordinary food culture', 'stunning natural scenery', 'incredibly affordable', 'warm and entrepreneurial people'],
        'challenges': ['traffic in Hanoi and Ho Chi Minh City is chaotic', 'persistent street vendors', 'quality varies wildly in tourist areas'],
    },
    'argentina': {
        'cities':     ['Buenos Aires', 'Mendoza', 'Bariloche', 'Salta', 'El Calafate'],
        'landmarks':  ['Perito Moreno Glacier', 'Iguazú Falls', 'Recoleta Cemetery', 'Patagonia', 'Quebrada de Humahuaca'],
        'dishes':     ['asado', 'empanadas', 'milanesa', 'dulce de leche everything', 'medialunas', 'Malbec wine'],
        'highlights': ['incredible natural landscapes', 'European-flavoured culture', 'world-class beef and wine', 'passionate tango culture in Buenos Aires'],
        'challenges': ['economic instability makes planning tricky', 'long distances within Patagonia', 'beef-centric menus challenge vegetarians'],
    },
    'egypt': {
        'cities':     ['Cairo', 'Luxor', 'Aswan', 'Alexandria', 'Sharm el-Sheikh'],
        'landmarks':  ['Great Pyramids of Giza', 'Karnak Temple', 'Valley of the Kings', 'Abu Simbel', 'Egyptian Museum'],
        'dishes':     ['koshari', 'ful medames', 'ta\'meya', 'molokhiya', 'om ali', 'Egyptian mint tea'],
        'highlights': ['ancient wonders of the world', 'Nile River cruises', 'incredible diving in Red Sea', 'warm winter weather'],
        'challenges': ['persistent tourist touts everywhere', 'bargaining is exhausting for some', 'heat in summer is extreme'],
    },
    'belgium': {
        'cities':     ['Brussels', 'Bruges', 'Ghent', 'Antwerp', 'Liège'],
        'landmarks':  ['Grand Place Brussels', 'Bruges Belfry', 'Ghent Gravensteen', 'Atomium', 'Manneken Pis'],
        'dishes':     ['moules-frites', 'Belgian waffles', 'speculoos', 'Belgian chocolate', 'Belgian ales', 'stomp'],
        'highlights': ['world\'s best beer and chocolate', 'magnificent medieval city centres', 'brilliant museums', 'underrated foodie destination'],
        'challenges': ['Bruges can feel like a theme park in peak season', 'Brussels can feel bureaucratic', 'weather is reliably grey'],
    },
    'singapore': {
        'cities':     ['Chinatown', 'Little India', 'Kampong Glam', 'Marina Bay', 'Sentosa'],
        'landmarks':  ['Gardens by the Bay', 'Marina Bay Sands', 'Hawker Centre', 'Raffles Hotel', 'Singapore Botanic Gardens'],
        'dishes':     ['chicken rice', 'laksa', 'chilli crab', 'char kway teow', 'kaya toast with soft-boiled eggs', 'satay'],
        'highlights': ['extraordinary multicultural food scene', 'ultra-clean and efficient', 'fascinating blend of cultures', 'world-class hawker food'],
        'challenges': ['very expensive for accommodation and alcohol', 'tiny country covered in a few days', 'strict laws surprise some visitors'],
    },
    'peru': {
        'cities':     ['Lima', 'Cusco', 'Arequipa', 'Iquitos', 'Huaraz'],
        'landmarks':  ['Machu Picchu', 'Inca Trail', 'Lake Titicaca', 'Colca Canyon', 'Sacred Valley'],
        'dishes':     ['ceviche', 'lomo saltado', 'causa', 'cuy', 'aji de gallina', 'pisco sour'],
        'highlights': ['Machu Picchu lives up to its reputation', 'incredible Incan history', 'one of the world\'s great food cities in Lima', 'Amazon access'],
        'challenges': ['altitude sickness in Cusco hits hard', 'Inca Trail permits sell out months ahead', 'petty crime in Lima city'],
    },
    'colombia': {
        'cities':     ['Medellín', 'Cartagena', 'Bogotá', 'Salento', 'Santa Marta'],
        'landmarks':  ['Cartagena Walled City', 'Coffee Region', 'La Ciudad Perdida', 'Tayrona National Park', 'Plaza Botero Medellín'],
        'dishes':     ['bandeja paisa', 'arepas', 'sancocho', 'empanadas', 'aguardiente', 'Colombian coffee'],
        'highlights': ['incredible coffee region', 'Cartagena is one of the Americas\' most beautiful cities', 'warm and proud people', 'spectacular transformation of Medellín'],
        'challenges': ['safety perception vs. reality still a gap', 'altitude in Bogotá', 'some areas still off-limits'],
    },
    'saudi-arabia': {
        'cities':     ['Riyadh', 'Jeddah', 'Al-Ula', 'Abha', 'Tabuk'],
        'landmarks':  ['Hegra (Mada\'in Saleh)', 'Diriyah', 'Al-Ula old town', 'Edge of the World', 'Jeddah corniche'],
        'dishes':     ['kabsa', 'jareesh', 'mutabbaq', 'saleeg', 'Saudi dates', 'Arabic coffee with cardamom'],
        'highlights': ['extraordinary archaeological sites', 'rapid transformation of the country', 'genuine hospitality', 'dramatic desert landscape'],
        'challenges': ['dress code and behaviour norms to observe', 'alcohol is completely prohibited', 'public transport is limited outside Riyadh'],
    },
    'south-africa': {
        'cities':     ['Cape Town', 'Johannesburg', 'Stellenbosch', 'Knysna', 'Durban'],
        'landmarks':  ['Table Mountain', 'Kruger National Park', 'Cape of Good Hope', 'Robben Island', 'Drakensberg'],
        'dishes':     ['braai', 'bobotie', 'biltong', 'bunny chow', 'malva pudding', 'Cape Malay curry'],
        'highlights': ['world-class safari experiences', 'stunning Cape Winelands', 'Table Mountain and Cape Peninsula', 'extraordinary biodiversity'],
        'challenges': ['Cape Town is expensive for southern Africa', 'car hire essential outside cities', 'crime requires vigilance especially in cities'],
    },
    'kenya': {
        'cities':     ['Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Lamu'],
        'landmarks':  ['Maasai Mara', 'Amboseli National Park', 'Mount Kenya', 'Diani Beach', 'Lamu Old Town'],
        'dishes':     ['nyama choma', 'ugali', 'sukuma wiki', 'pilau', 'mandazi', 'chai'],
        'highlights': ['world\'s greatest wildlife spectacle in Maasai Mara', 'vibrant Maasai culture', 'beautiful coastline', 'conservation success stories'],
        'challenges': ['safari costs are genuinely high', 'driving on rough roads', 'altitude sickness near Mt. Kenya'],
    },
    'new-zealand': {
        'cities':     ['Queenstown', 'Wellington', 'Auckland', 'Christchurch', 'Rotorua'],
        'landmarks':  ['Milford Sound', 'Tongariro Alpine Crossing', 'Bay of Islands', 'Franz Josef Glacier', 'Hobbiton'],
        'dishes':     ['lamb roast', 'hangi', 'whitebait fritters', 'pavlova', 'L&P soft drink', 'manuka honey'],
        'highlights': ['extraordinarily beautiful landscapes', 'world-class adventure sports', 'very safe and easy to travel', 'warm Kiwi hospitality'],
        'challenges': ['very expensive', 'distances require a car', 'remote from everywhere adds flight costs'],
    },
    'ireland': {
        'cities':     ['Dublin', 'Galway', 'Cork', 'Killarney', 'Dingle'],
        'landmarks':  ['Cliffs of Moher', 'Ring of Kerry', 'Blarney Castle', 'Giant\'s Causeway', 'Trinity College Dublin'],
        'dishes':     ['Irish stew', 'full Irish breakfast', 'soda bread', 'colcannon', 'fresh oysters in Galway', 'Guinness'],
        'highlights': ['stunning coastal scenery', 'legendary pub culture', 'incredibly warm and witty people', 'ancient mythology and culture'],
        'challenges': ['weather is reliably wet', 'roads in the west can be single-lane', 'Dublin is surprisingly expensive'],
    },
    'norway': {
        'cities':     ['Bergen', 'Oslo', 'Ålesund', 'Tromsø', 'Stavanger'],
        'landmarks':  ['Geirangerfjord', 'Preikestolen (Pulpit Rock)', 'Northern Lights', 'Lofoten Islands', 'Flåm Railway'],
        'dishes':     ['rakfisk', 'fårikål', 'smoked salmon', 'brunost', 'kjøttkaker', 'bacalao'],
        'highlights': ['most dramatic fjord scenery in the world', 'northern lights in winter', 'midnight sun in summer', 'excellent hiking'],
        'challenges': ['among the most expensive countries on earth', 'weather is unpredictable', 'public transport outside cities requires planning'],
    },
    'iceland': {
        'cities':     ['Reykjavik', 'Akureyri', 'Höfn', 'Vík', 'Stykkishólmur'],
        'landmarks':  ['Golden Circle', 'Blue Lagoon', 'Jökulsárlón glacier lagoon', 'Skógafoss waterfall', 'Northern Lights'],
        'dishes':     ['lamb soup', 'skyr', 'fermented shark (hákarl)', 'hot dogs', 'Arctic char', 'Icelandic lamb'],
        'highlights': ['geological spectacle unlike anywhere on earth', 'northern lights and midnight sun', 'waterfalls and glaciers everywhere', 'very safe'],
        'challenges': ['extremely expensive', 'weather changes in minutes', 'Golden Circle very crowded in summer'],
    },
    'sweden': {
        'cities':     ['Stockholm', 'Gothenburg', 'Malmö', 'Uppsala', 'Kiruna'],
        'landmarks':  ['Gamla Stan Stockholm', 'Vasa Museum', 'ABBA Museum', 'Icehotel Kiruna', 'Göta Canal'],
        'dishes':     ['meatballs with lingonberry', 'gravlax', 'smörgåsbord', 'cinnamon rolls', 'surströmming', 'Jansson\'s temptation'],
        'highlights': ['beautiful design culture', 'excellent outdoor life', 'very progressive society', 'Stockholm is gorgeous'],
        'challenges': ['very expensive', 'can feel reserved socially', 'long dark winters'],
    },
    'denmark': {
        'cities':     ['Copenhagen', 'Aarhus', 'Odense', 'Aalborg', 'Helsingør'],
        'landmarks':  ['Nyhavn', 'Tivoli Gardens', 'Kronborg Castle', 'Ribe Old Town', 'Louisiana Museum'],
        'dishes':     ['smørrebrød', 'æbleskiver', 'frikadeller', 'rugbrød', 'Danish pastries', 'New Nordic cuisine'],
        'highlights': ['consistently ranked happiest country in the world', 'world-class food scene in Copenhagen', 'excellent cycling culture', 'beautiful harbour scenes'],
        'challenges': ['among Europe\'s most expensive destinations', 'can feel quiet outside Copenhagen', 'Danes can seem reserved at first'],
    },
    'cuba': {
        'cities':     ['Havana', 'Trinidad', 'Viñales', 'Cienfuegos', 'Santiago de Cuba'],
        'landmarks':  ['Old Havana', 'Viñales Valley tobacco farms', 'Trinidad Cobblestones', 'Che Guevara Mausoleum', 'Varadero Beach'],
        'dishes':     ['ropa vieja', 'moros y cristianos', 'lechón asado', 'Cuban sandwich', 'mojito', 'ron y Coca-Cola'],
        'highlights': ['utterly unique time-warp atmosphere', 'incredible vintage cars', 'vibrant salsa culture', 'warm and resilient people'],
        'challenges': ['limited internet access is frustrating', 'two-currency system confusing', 'food quality in state restaurants disappoints'],
    },
    'philippines': {
        'cities':     ['Manila', 'Cebu', 'El Nido', 'Siargao', 'Vigan'],
        'landmarks':  ['El Nido lagoons', 'Chocolate Hills Bohol', 'Intramuros Manila', 'Mayon Volcano', 'Tubbataha Reef'],
        'dishes':     ['adobo', 'sinigang', 'lechon', 'kare-kare', 'halo-halo', 'balut (brave eaters only)'],
        'highlights': ['world-class island beaches and diving', 'extraordinarily warm people', 'affordable', 'English widely spoken'],
        'challenges': ['island hopping logistics are tiring', 'Manila traffic is gruelling', 'typhoon season disrupts plans'],
    },
    'jordan': {
        'cities':     ['Amman', 'Petra', 'Wadi Rum', 'Aqaba', 'Jerash'],
        'landmarks':  ['Petra Treasury', 'Wadi Rum desert', 'Dead Sea', 'Jerash Roman ruins', 'Wadi Mujib'],
        'dishes':     ['mansaf', 'maqluba', 'knafeh', 'falafel', 'mezze spread', 'Jordanian tea'],
        'highlights': ['Petra is genuinely one of the world\'s great sites', 'floating in the Dead Sea', 'incredible Roman ruins', 'very safe and welcoming'],
        'challenges': ['Jordan Pass essential to save money', 'summer heat is punishing', 'expensive for the region'],
    },
    'israel': {
        'cities':     ['Jerusalem', 'Tel Aviv', 'Haifa', 'Nazareth', 'Eilat'],
        'landmarks':  ['Western Wall', 'Old City Jerusalem', 'Masada', 'Dead Sea', 'Baha\'i Gardens Haifa'],
        'dishes':     ['shakshuka', 'hummus', 'falafel', 'sabich', 'knafeh', 'Israeli breakfast spread'],
        'highlights': ['extraordinary concentration of history', 'Tel Aviv\'s beach and bar scene', 'world-class food culture', 'very intense and fascinating culture'],
        'challenges': ['airport security is lengthy', 'some political sensitivities to be aware of', 'expensive for the Middle East'],
    },
    'tanzania': {
        'cities':     ['Arusha', 'Dar es Salaam', 'Stone Town Zanzibar', 'Moshi', 'Mwanza'],
        'landmarks':  ['Serengeti National Park', 'Mount Kilimanjaro', 'Ngorongoro Crater', 'Zanzibar beaches', 'Lake Manyara'],
        'dishes':     ['nyama choma', 'ugali', 'chipsi mayai', 'zanzibar pizza', 'octopus curry', 'spiced chai'],
        'highlights': ['the Great Migration is life-changing', 'Zanzibar\'s spice history and beaches', 'climbing Kilimanjaro', 'excellent conservation'],
        'challenges': ['safari costs are very high', 'malaria precautions essential', 'roads between parks can be rough'],
    },
    'nepal': {
        'cities':     ['Kathmandu', 'Pokhara', 'Chitwan', 'Bhaktapur', 'Namche Bazaar'],
        'landmarks':  ['Everest Base Camp', 'Annapurna Circuit', 'Pashupatinath Temple', 'Boudhanath Stupa', 'Patan Durbar Square'],
        'dishes':     ['dal bhat', 'momo dumplings', 'thukpa noodle soup', 'newari set meal', 'sel roti', 'chiya tea'],
        'highlights': ['Himalayas are beyond description', 'deeply spiritual atmosphere', 'world-class trekking', 'genuinely warm and welcoming people'],
        'challenges': ['altitude sickness is a real risk above 3,000m', 'power cuts still happen', 'roads in mountain regions are terrifying'],
    },
    'sri-lanka': {
        'cities':     ['Colombo', 'Kandy', 'Galle', 'Ella', 'Sigiriya'],
        'landmarks':  ['Sigiriya Rock Fortress', 'Temple of the Tooth Relic', 'Galle Fort', 'Nine Arch Bridge Ella', 'Yala National Park'],
        'dishes':     ['rice and curry', 'kottu roti', 'hoppers', 'string hoppers', 'pol sambol', 'Ceylon tea'],
        'highlights': ['extraordinary archaeological sites', 'stunning landscapes packed into a small island', 'incredible spice-based cuisine', 'affordable luxury'],
        'challenges': ['road journeys take longer than maps suggest', 'coastal areas very touristy post-war', 'tuk-tuk fares need negotiating'],
    },
    'maldives': {
        'cities':     ['Malé', 'Addu Atoll', 'Maafushi', 'Thulusdhoo', 'Vaadhoo Island'],
        'landmarks':  ['Bioluminescent beach Vaadhoo', 'underwater restaurants', 'coral reefs', 'Malé old Friday Mosque', 'overwater bungalows'],
        'dishes':     ['mas huni', 'garudhiya fish soup', 'fihunu mas grilled fish', 'saagu bondibai', 'roshi flatbread'],
        'highlights': ['most perfect turquoise water on earth', 'extraordinary snorkelling and diving', 'total relaxation and luxury', 'bioluminescent beaches'],
        'challenges': ['extremely expensive even at budget level', 'guesthouses on local islands have alcohol restrictions', 'not much cultural sightseeing beyond beaches'],
    },
    'cambodia': {
        'cities':     ['Siem Reap', 'Phnom Penh', 'Kampot', 'Koh Rong', 'Battambang'],
        'landmarks':  ['Angkor Wat', 'Angkor Thom', 'Ta Prohm temple', 'Killing Fields Phnom Penh', 'Phare Circus Battambang'],
        'dishes':     ['fish amok', 'lok lak', 'num banh chok noodles', 'banana flower salad', 'Kampot pepper crab'],
        'highlights': ['Angkor Wat is genuinely one of humanity\'s greatest achievements', 'strong survival spirit of the Khmer people', 'excellent street food', 'very affordable'],
        'challenges': ['tuk-tuk touts around Angkor', 'Khmer Rouge history is deeply sobering', 'heat in April is extreme'],
    },
    'romania': {
        'cities':     ['Bucharest', 'Brașov', 'Sibiu', 'Cluj-Napoca', 'Sighișoara'],
        'landmarks':  ['Bran Castle', 'Peleș Castle', 'Painted Monasteries of Bucovina', 'Old Town Sibiu', 'Transfăgărășan Road'],
        'dishes':     ['mămăligă', 'sarmale', 'mici', 'ciorba de burtă', 'cozonac', 'tuică plum brandy'],
        'highlights': ['spectacular and underrated Carpathian scenery', 'beautifully preserved Saxon towns', 'remarkably affordable', 'Dracula tourism done right'],
        'challenges': ['roads outside cities can be rough', 'Bucharest feels rough around the edges', 'tourist info is limited in rural areas'],
    },
    'albania': {
        'cities':     ['Tirana', 'Shkodër', 'Berat', 'Gjirokastër', 'Sarandë'],
        'landmarks':  ['Gjirokastër Citadel', 'Berat old town (City of a Thousand Windows)', 'Llogara Pass', 'Butrint ruins', 'Albanian Riviera'],
        'dishes':     ['byrek', 'tavë kosi', 'fërgesë', 'qofte', 'sufllaqe', 'raki'],
        'highlights': ['genuinely one of Europe\'s best-kept secrets', 'stunning unspoilt Riviera beaches', 'extraordinary warmth toward foreigners', 'incredibly cheap'],
        'challenges': ['driving is wild', 'limited tourist infrastructure in north', 'some roads are shocking'],
    },
    'serbia': {
        'cities':     ['Belgrade', 'Novi Sad', 'Niš', 'Subotica', 'Kragujevac'],
        'landmarks':  ['Belgrade Fortress', 'Studenica Monastery', 'Petrovaradin Fortress', 'Đavolja Varoš', 'Gamzigrad-Romuliana'],
        'dishes':     ['ćevapi', 'pljeskavica', 'sarma', 'pasulj bean stew', 'rakija', 'gibanica pastry'],
        'highlights': ['Belgrade\'s nightlife is legendary', 'extraordinary Orthodox monasteries', 'genuinely warm Balkan hospitality', 'excellent and affordable food'],
        'challenges': ['Belgrade rough around the edges', 'language barrier', 'cashless payment less common outside cities'],
    },
    'georgia-country': {
        'cities':     ['Tbilisi', 'Batumi', 'Kutaisi', 'Sighnaghi', 'Mtskheta'],
        'landmarks':  ['Gergeti Trinity Church', 'Narikala Fortress Tbilisi', 'Vardzia cave monastery', 'Svaneti towers', 'Old Tbilisi'],
        'dishes':     ['khinkali dumplings', 'khachapuri', 'mtsvadi', 'pkhali', 'badrijani nigvzit', 'chacha brandy'],
        'highlights': ['extraordinary cuisine and wine culture', 'dramatic Caucasus mountain scenery', 'incredibly warm hospitality', 'ancient Christian heritage'],
        'challenges': ['mountain roads can be treacherous', 'limited English outside Tbilisi', 'Georgian script is completely unreadable to most visitors'],
    },
    'hong-kong': {
        'cities':     ['Central', 'Kowloon', 'Mong Kok', 'Wan Chai', 'Sai Kung'],
        'landmarks':  ['Victoria Peak', 'Star Ferry', 'Temple Street Night Market', 'Big Buddha Lantau', 'Hong Kong skyline'],
        'dishes':     ['dim sum', 'roast goose', 'wonton noodle soup', 'egg tarts', 'milk tea', 'claypot rice'],
        'highlights': ['one of the world\'s great food cities', 'spectacular harbour views', 'incredible mix of Chinese and British heritage', 'excellent hiking despite being a city'],
        'challenges': ['accommodation is extremely expensive', 'summer heat and humidity are intense', 'can feel overwhelming and relentless'],
    },
}

# ---------------------------------------------------------------------------
# Review templates — each uses different fact categories
# ---------------------------------------------------------------------------
TEMPLATES = [
    {
        'title_tmpl': 'My {n} days exploring {city} and beyond — completely worth it',
        'body_tmpl': (
            "I spent {n} days in {name} and based myself mainly in {city}. The city itself exceeded expectations — the "
            "{landmark} was genuinely jaw-dropping and I ended up visiting twice. "
            "Food was a highlight throughout; I must have eaten {dish} every other day and have no regrets about it whatsoever.\n\n"
            "What I didn't expect was {highlight}. That element really elevated the trip from good to exceptional. "
            "The locals I encountered were warm and patient with my attempts at the language. "
            "I'd encourage anyone on the fence to just book it."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': '{landmark} alone makes {name} worth the trip',
        'body_tmpl': (
            "I'll be honest — I went to {name} primarily to see {landmark}, and it delivered beyond what any photo prepares you for. "
            "But the surrounding region surprised me just as much. {city} has a character I didn't anticipate, and wandering "
            "without a plan for an afternoon turned out to be one of the highlights.\n\n"
            "The food is extraordinary. {dish} sounds simple but here it's done with real craft. {highlight} added another layer "
            "to the experience. Spent {n} days and honestly could have used a week more."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Honest review after {n} days — mostly great, a few gripes',
        'body_tmpl': (
            "Visited {name} for {n} days. The positives are real: {landmark} is every bit as impressive as advertised, "
            "and the food scene around {city} is genuinely excellent — try {dish} if you haven't. "
            "{highlight} was an unexpected bonus.\n\n"
            "That said, {challenge}. It's not a dealbreaker but worth knowing before you go. "
            "I'd still recommend {name} to most travellers — just manage your expectations on those specific points "
            "and you'll have a great time."
        ),
        'rating': 4,
    },
    {
        'title_tmpl': 'The food in {name} changed how I think about travel',
        'body_tmpl': (
            "I travel for food more than anything else, and {name} shot straight to the top of my culinary travel list. "
            "{dish} alone justified the flight, but that was just the beginning. The variety and quality in {city} is relentless "
            "— I didn't have a single disappointing meal in {n} days.\n\n"
            "{landmark} gave context to everything I was tasting. The history and culture feeds into the food in ways "
            "you can feel. {highlight} completed the picture. Already planning a return trip focused entirely on eating "
            "my way through a different region."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Solo trip to {name}: everything you need to know',
        'body_tmpl': (
            "Did {n} days solo in {name} and found it extremely manageable as a solo traveller. "
            "The transport network around {city} is decent and getting to {landmark} independently was straightforward. "
            "Met fellow travellers easily and locals were generally happy to chat.\n\n"
            "{highlight} was a personal highlight — something I'd only found in independent travel research. "
            "One note: {challenge}. Nothing serious but worth knowing. The solo experience here was genuinely rewarding "
            "and I came home having learned a lot about a place I knew very little about."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Mixed experience in {name} — beautiful but overhyped',
        'body_tmpl': (
            "{name} is undeniably beautiful. {landmark} and the area around {city} have a visual quality that photographs "
            "don't capture fully. I enjoyed {dish} and appreciated {highlight}. That's all real.\n\n"
            "But {challenge} was more of a problem than I expected based on reviews I'd read. "
            "It coloured parts of the trip in ways I hadn't prepared for. I'd still go back, but I'd approach certain "
            "aspects differently. A 4 feels generous on a bad day but fair overall."
        ),
        'rating': 4,
    },
    {
        'title_tmpl': 'Returned to {name} for the third time — keeps getting better',
        'body_tmpl': (
            "This was my third visit to {name} and I keep finding new reasons to return. This time I explored beyond "
            "{city} and discovered a completely different side of the country. {landmark} never loses its impact no matter "
            "how many times you've seen it.\n\n"
            "The food still makes me happy in ways I can't fully explain — {dish} particularly. {highlight} was a new "
            "discovery this visit and now feels essential to the experience. If you haven't been yet, you're missing something."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Family holiday in {name} — kids loved it, parents survived',
        'body_tmpl': (
            "Took the family to {name} for {n} days and it worked better than I'd hoped. The kids were fascinated by "
            "{landmark} — more than I expected from children who usually resist sightseeing. Food was manageable: "
            "even the pickiest eater in our group found things to eat, and {dish} went down well with everyone.\n\n"
            "{highlight} kept everyone engaged and gave the trip a memorable high point. {challenge} was the main "
            "practical difficulty but nothing that ruined anything. Would absolutely return with them."
        ),
        'rating': 4,
    },
    {
        'title_tmpl': 'What nobody tells you about visiting {name}',
        'body_tmpl': (
            "After a lot of research I thought I knew what to expect from {name}. Some things matched: {landmark} "
            "is as spectacular as every review says, and {city} has a genuine energy I'd read about. "
            "The {dish} obsession is completely justified.\n\n"
            "What I wasn't prepared for: {highlight}. That element genuinely surprised me and added something I hadn't "
            "seen in any review. Also: {challenge}. That part the reviews undersell. Overall a wonderful trip — "
            "just a more layered experience than I anticipated."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Disappointed by the tourist experience around {landmark}',
        'body_tmpl': (
            "{landmark} in {name} is extraordinary — the scale and history hit you immediately. But the experience "
            "around it has been thoroughly commercialised. Getting there, navigating the crowds, and dealing with "
            "persistent sellers around {city} centre made it more stressful than it should be.\n\n"
            "Away from the main sites the country improves dramatically. The food ({dish} especially) is excellent and "
            "{highlight} was genuinely memorable. But I'd wish for a smoother experience at the headline attractions. "
            "It's still worth the trip — just lower your expectations around the big sights."
        ),
        'rating': 3,
    },
    {
        'title_tmpl': '{city} surprised me completely on this trip to {name}',
        'body_tmpl': (
            "I went to {name} with modest expectations and left completely won over, largely thanks to time spent in "
            "{city}. The city has a pace and character that travel guides undersell. Found a great spot for {dish} on "
            "day two and went back every day after that.\n\n"
            "{landmark} was the big planned experience and delivered as expected. But it was {highlight} that became "
            "the unexpected highlight — something I stumbled across rather than planned. {n} days was just right for "
            "getting below the surface without rushing."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Would not rush back to {name} — {challenge} was a real issue',
        'body_tmpl': (
            "I wanted to love {name} more than I did. The positives exist: {landmark} is genuinely impressive, "
            "{city} has moments of real charm, and {dish} is as good as people say.\n\n"
            "But {challenge} was a persistent problem throughout the trip and dragged the experience down. "
            "I've heard others say it's improved, but during my {n}-day visit it was a constant friction point. "
            "Maybe I'll give it another chance in a few years. For now I'm directing my travel budget elsewhere."
        ),
        'rating': 2,
    },
    {
        'title_tmpl': 'Weekend in {city}, {name} — more than I expected from a short trip',
        'body_tmpl': (
            "Only had a long weekend — about {n} days — in {name}, based in {city}. More than enough to fall for the place. "
            "Did {landmark} on day one and spent the rest of the time just walking and eating. "
            "The {dish} situation here is no joke — some of the best eating I've done anywhere.\n\n"
            "{highlight} gave the trip a texture I didn't anticipate from such a short visit. "
            "I came back with a long list of reasons to return properly for two weeks."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'The people of {name} are the real highlight',
        'body_tmpl': (
            "I've been to a lot of countries and the thing I'll remember most about {name} isn't {landmark} "
            "or even the extraordinary {dish} — it's the people. In {city} and out in the countryside, "
            "I encountered a warmth and generosity that felt completely genuine.\n\n"
            "One local family essentially adopted me for an afternoon after I got lost trying to find {landmark}. "
            "{highlight} became a shared experience I couldn't have planned. "
            "That human connection is something travel can give you and {name} delivers it more than most places."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Arrived with low expectations, left completely converted',
        'body_tmpl': (
            "{name} wasn't high on my travel list. A friend pushed me to go and I'm genuinely grateful. "
            "The first full day in {city} reset everything — the scale of {landmark} and the quality of the "
            "{dish} were immediate signals that I'd misjudged the place completely.\n\n"
            "{highlight} became my personal highlight of the whole trip. "
            "Spent {n} days and could easily have stayed twice as long. "
            "Now I tell everyone who'll listen that {name} is underrated — add it to your list."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Honest thoughts on {name} after my first visit',
        'body_tmpl': (
            "First time in {name} and I tried to approach it with open eyes rather than preconceptions. "
            "{city} was the base and a good one — central, manageable, and with strong food options including "
            "the best {dish} I've ever had. {landmark} was the big set piece and fully justified the trip.\n\n"
            "Two things worth knowing: {challenge}, which is more of a factor than some guides acknowledge. "
            "But also: {highlight}, which I'd never read about and turned out to be a genuine pleasure. "
            "Solid first impression — I'd return."
        ),
        'rating': 4,
    },
    {
        'title_tmpl': 'Honeymoon in {name} — {city} and the countryside delivered everything',
        'body_tmpl': (
            "We chose {name} for our honeymoon and it was perfect for us. The romantic atmosphere in {city} at night, "
            "the drama of {landmark}, the intimacy of small restaurants serving {dish} — all of it added up to "
            "exactly what we were hoping for.\n\n"
            "{highlight} became an unexpected gift — something we stumbled across that felt made for the occasion. "
            "We had {n} days and used every one of them well. Some destinations disappoint when the pressure of "
            "a special occasion is on them. {name} didn't."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Backpacking through {name} on a tight budget — totally doable',
        'body_tmpl': (
            "Did {name} on a shoestring for {n} days and it was absolutely manageable. "
            "Based in cheap guesthouses near {city} centre and ate mostly at local spots — "
            "{dish} from street stalls cost almost nothing and was better than anything in a tourist restaurant.\n\n"
            "{landmark} has an entry fee but worth every penny. {highlight} was a free discovery "
            "that ended up being one of my favourite moments of the trip. "
            "Budget travellers: {name} is worth your time and money, just avoid the tourist-priced restaurants."
        ),
        'rating': 4,
    },
    {
        'title_tmpl': 'Three weeks in {name} — here is what I actually think',
        'body_tmpl': (
            "Three weeks is long enough to get past the tourist surface in {name}. "
            "The first week I was in {city} and the big sites like {landmark}. The second and third I went further "
            "and slower. The food evolution was interesting — {dish} everywhere but prepared so differently by region.\n\n"
            "{highlight} only revealed itself in the second half of the trip, when I'd slowed down enough to notice. "
            "The negative: {challenge}, which is real and worth factoring in. "
            "But three weeks felt right. Long enough to form a genuine opinion. "
            "My genuine opinion: exceptional destination."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Photography trip to {name} — every frame a gift',
        'body_tmpl': (
            "I came to {name} specifically for photography and the country delivered material at every turn. "
            "{landmark} at dawn was everything I'd hoped. {city}'s streets at dusk are an endless source of light "
            "and texture. The people, once comfortable with a camera, are extraordinary subjects.\n\n"
            "{highlight} gave me some of my favourite images of the year. "
            "The only practical note: {challenge} — plan around it. "
            "Otherwise this is a photographer's dream. I've rarely come home with so much usable material from a single trip."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Good country, exhausting tourist industry',
        'body_tmpl': (
            "{name} is a genuinely beautiful and interesting place. {landmark} is worth every superlative thrown at it. "
            "The {dish} is legitimately excellent. {highlight} gave the trip real depth.\n\n"
            "What I struggled with: the tourist infrastructure around the headline sites in {city} is relentlessly commercial "
            "and {challenge} is a genuine friction point. You can feel the gap between authentic {name} and the packaged version "
            "sold to tourists. The authentic version wins, but you have to work to find it."
        ),
        'rating': 3,
    },
    {
        'title_tmpl': '{name} in shoulder season — best decision I made',
        'body_tmpl': (
            "Visited {name} in shoulder season deliberately and the decision paid off completely. "
            "{landmark} without peak crowds is a totally different experience. {city} felt lived-in rather than touristy. "
            "Found a small place doing the best {dish} I've ever tasted — something that would have been invisible "
            "in high season when everything fills with visitors.\n\n"
            "{highlight} was particularly magical with fewer people around. "
            "The weather was fine. The prices were better. If you have flexibility, avoid peak season."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Unexpected emotional depth in {name}',
        'body_tmpl': (
            "I thought I was going to {name} for beaches, food, and {landmark}. I got all of those things. "
            "What I didn't expect was how emotionally affecting the trip would be. "
            "The history — particularly around {city} — hit in ways that good travel sometimes does.\n\n"
            "{highlight} was the moment that crystallised it. Standing there, eating {dish} I'd bought from a street vendor, "
            "something clicked about why travel matters. {n} days and I came home genuinely changed. "
            "Some places do that to you."
        ),
        'rating': 5,
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


def make_review(country_name: str, slug: str, tmpl: dict) -> tuple:
    facts = COUNTRY_DATA.get(slug)
    if not facts:
        return None

    n = random.randint(5, 21)
    city      = random.choice(facts['cities'])
    landmark  = random.choice(facts['landmarks'])
    dish      = random.choice(facts['dishes'])
    highlight = random.choice(facts['highlights'])
    challenge = random.choice(facts['challenges'])

    title = tmpl['title_tmpl'].format(
        name=country_name, n=n, city=city, landmark=landmark,
        dish=dish, highlight=highlight, challenge=challenge,
    )
    body = tmpl['body_tmpl'].format(
        name=country_name, n=n, city=city, landmark=landmark,
        dish=dish, highlight=highlight, challenge=challenge,
    )
    base_rating = tmpl['rating']
    rating = max(1, min(5, base_rating + random.choice([-1, 0, 0, 0, 1])))
    # Override with weighted random for variety
    if random.random() < 0.3:
        rating = weighted_rating()
    return title, body, rating


def run(args):
    from app import create_app, db
    from app.models import Subject, SubCategory, Review

    app = create_app('development')
    with app.app_context():
        sc = SubCategory.query.filter_by(slug='all-countries').first()
        if not sc:
            print('Subcategory all-countries not found')
            sys.exit(1)

        if args.slug:
            subjects = Subject.query.filter_by(subcategory_id=sc.id, slug=args.slug).all()
            if not subjects:
                print(f'Country slug "{args.slug}" not found')
                sys.exit(1)
        else:
            subjects = Subject.query.filter_by(subcategory_id=sc.id).order_by(Subject.id).all()

        if args.start_from:
            slugs = [s.slug for s in subjects]
            if args.start_from in slugs:
                idx = slugs.index(args.start_from)
                subjects = subjects[idx:]
                print(f'Resuming from {args.start_from} ({len(subjects)} countries left)')
            else:
                print(f'--start-from slug "{args.start_from}" not found, processing all')

        print(f'Processing {len(subjects)} countries, ~{args.count} reviews each')

        for subj in subjects:
            if subj.slug not in COUNTRY_DATA:
                print(f'  SKIP {subj.name} — no facts data')
                continue

            # Delete existing sample/generated reviews
            deleted = Review.query.filter_by(subject_id=subj.id, source_site='sample').delete()
            deleted += Review.query.filter_by(subject_id=subj.id, source_site='generated').delete()
            db.session.commit()

            target = args.count
            used_titles: set[str] = set()
            reviews_added = 0

            shuffled = TEMPLATES[:]
            random.shuffle(shuffled)
            # cycle templates if we need more than len(TEMPLATES)
            pool = (shuffled * ((target // len(shuffled)) + 2))[:target * 2]

            for tmpl in pool:
                if reviews_added >= target:
                    break
                result = make_review(subj.name, subj.slug, tmpl)
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
            print(f'  {subj.name}: {reviews_added} reviews (avg {subj.avg_rating:.1f}★, deleted {deleted})')

        print('Done.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--slug', help='Single country slug')
    parser.add_argument('--start-from', dest='start_from', help='Resume from this slug')
    parser.add_argument('--count', type=int, default=15, help='Reviews per country (default 15)')
    args = parser.parse_args()
    run(args)
