"""Populate description, pros, and cons for all 50 breeds."""
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

# name -> (description, [pros], [cons])
BREED_INFO = {
    # ── DOGS ──────────────────────────────────────────────────────────────────
    'Labrador Retriever': (
        "The Labrador Retriever has been the most popular dog breed in the world for decades — and for good reason. Originally bred as a fisherman's helper in Newfoundland, Labs combine athleticism, intelligence, and an almost supernaturally friendly temperament. They are equally at home as working service dogs, hunting companions, and family pets, adapting effortlessly to almost any lifestyle.",
        ["Extremely friendly and gentle with children and strangers", "Highly intelligent and easy to train", "Adaptable to family life, apartments, or active outdoor living", "Low aggression — rarely shows problematic behaviour", "Excellent with other dogs and pets"],
        ["Heavy shedder, especially in spring and autumn", "High energy when young — needs 1–2 hours of exercise daily", "Prone to overeating and obesity without portion control", "Can be destructive if bored or under-exercised"],
    ),
    'German Shepherd': (
        "The German Shepherd is one of the world's most versatile working dogs, excelling in police work, search and rescue, military service, and competitive dog sports. Bred in 19th-century Germany by Max von Stephanitz, the breed combines intelligence, loyalty, and physical capability in a package that is both elegant and powerful. A well-trained German Shepherd is an extraordinary companion.",
        ["Exceptionally intelligent — one of the easiest breeds to train", "Deeply loyal and protective of their family", "Versatile: excels in sports, work, and family life", "Confident and stable with proper socialisation", "Excellent health when sourced from tested breeding lines"],
        ["Requires significant daily exercise and mental stimulation", "Heavy shedder year-round — nicknamed 'German Shedder'", "Can develop anxiety or destructive behaviour if under-stimulated", "Hip and elbow dysplasia risk — choose breeders carefully"],
    ),
    'Golden Retriever': (
        "The Golden Retriever is beloved worldwide for its warm, tolerant temperament and eagerness to please. Developed in Scotland in the 19th century as a hunting dog, the Golden's intelligence, patience, and gentle nature have made it one of the most popular family dogs on earth. They are a top choice for therapy, assistance, and search-and-rescue work — and an unbeatable family companion.",
        ["Outstandingly gentle and patient, especially with children", "Highly trainable and eager to please", "Friendly with strangers, other dogs, and pets", "Excellent for first-time dog owners", "Long, loyal lifespan — typically 10–12 years"],
        ["Significant shedding, especially seasonally", "Needs at least 1–2 hours of exercise daily", "Can be overly exuberant and boisterous as a young dog", "Health risks include cancer and hip dysplasia — vet screening essential"],
    ),
    'French Bulldog': (
        "The French Bulldog has exploded in popularity over the last decade, and it's easy to see why. Compact, playful, and full of personality, Frenchies were bred as companion dogs and have never forgotten it. Their distinctive bat ears, wrinkled face, and stocky frame make them instantly recognisable, and their adaptable, low-exercise nature makes them ideal for city and apartment living.",
        ["Adaptable and perfectly suited to apartment life", "Low exercise requirements — ideal for less active owners", "Affectionate and entertaining personality", "Quiet — rarely excessive barkers", "Good with children and other pets"],
        ["Brachycephalic (flat-faced) — prone to breathing problems and overheating", "Can be expensive to breed and purchase due to health complications", "Stubborn streak can make training a challenge", "Significant health costs — avoid in very hot or humid climates"],
    ),
    'Bulldog': (
        "The English Bulldog has transformed from a bull-baiting dog of the 17th century into one of the world's most affectionate and laid-back companions. Their iconic wrinkled face, stocky body, and rolling gait have earned them fans worldwide. Modern Bulldogs are gentle, predictable, and surprisingly good with children — though their flat faces come with real health considerations that owners must understand.",
        ["Calm, stable temperament — rarely reactive or aggressive", "Excellent with children — famously patient", "Low exercise requirements suit less active households", "Charming, stubborn, and full of personality", "Devoted and loyal to their family"],
        ["Serious brachycephalic health issues — breathing, overheating, skin fold infections", "High veterinary costs compared to most breeds", "Can be very stubborn and resistant to training", "Snores loudly and may have flatulence issues"],
    ),
    'Poodle': (
        "Behind the elegant haircuts is one of the world's most intelligent and athletic dogs. Poodles — whether standard, miniature, or toy — were originally bred as water retrievers and retain the athletic ability and problem-solving intelligence of a proper working dog. The Standard Poodle in particular is a remarkable all-rounder: sporty, trainable, hypoallergenic-friendly, and deeply affectionate with family.",
        ["One of the most intelligent dog breeds — learns exceptionally fast", "Low-shedding coat, well-tolerated by many allergy sufferers", "Athletic and excels in dog sports and agility", "Friendly, social, and good with children", "Comes in three sizes — adaptable to different lifestyles"],
        ["Coat requires professional grooming every 6–8 weeks", "Can develop separation anxiety if left alone frequently", "High mental stimulation needs — boredom leads to mischief", "Some lines prone to hip issues and eye conditions"],
    ),
    'Beagle': (
        "The Beagle is one of the most recognisable dogs in the world — a sturdy, compact hound with an expression of perpetual curiosity. Originally bred for pack hunting by scent, Beagles are cheerful, energetic, and love company. Their moderate size, friendly nature, and relatively low maintenance make them a popular family choice, though their powerful nose and hound instincts require consistent management.",
        ["Happy, friendly, and wonderful with children", "Moderate exercise needs — manageable for most families", "Social with other dogs — thrives in multi-dog households", "Hardy and generally healthy breed", "Compact size, adaptable to various living situations"],
        ["Extremely scent-driven — recall can be unreliable near interesting smells", "Prone to howling and baying, particularly when bored or left alone", "Stubborn and can be difficult to train using conventional methods", "Needs secure fencing — will follow a scent regardless of danger"],
    ),
    'Rottweiler': (
        "The Rottweiler is a powerful, confident dog with a history stretching back to Roman times, when they were used to drive cattle and guard camps. Behind the imposing exterior is a calm, loyal, and surprisingly playful dog that is deeply devoted to its family. A well-bred and well-trained Rottweiler is an exceptional companion — but the breed demands a knowledgeable, consistent owner.",
        ["Deeply loyal and protective of family without aggression", "Highly intelligent and trainable in experienced hands", "Confident and stable when properly socialised", "Robust constitution and generally good health", "Natural guarding instinct provides genuine security"],
        ["Strong-willed — not suitable for inexperienced dog owners", "Requires extensive early socialisation to prevent reactivity", "Powerful build demands proper leash training from puppyhood", "Breed-specific restrictions exist in some countries and insurance policies"],
    ),
    'German Shorthaired Pointer': (
        "The German Shorthaired Pointer is the Swiss Army knife of the dog world — a versatile hunting dog that can point, retrieve on land and water, and track game, all in one package. Developed in 19th-century Germany, the GSP combines athletic ability, intelligence, and an affectionate temperament. For active owners who want a high-performance companion, few breeds come close.",
        ["Exceptionally athletic — ideal for runners and hikers", "Highly intelligent and responsive to training", "Affectionate and loyal family dog", "Versatile in sporting activities: tracking, agility, field work", "Short coat requires minimal grooming"],
        ["Very high exercise needs — needs 2+ hours of vigorous activity daily", "Not suited to apartments or sedentary lifestyles", "Strong prey drive requires careful management around small animals", "Can develop destructive behaviours quickly when under-exercised"],
    ),
    'Dachshund': (
        "The Dachshund — affectionately called the 'sausage dog' — was bred in Germany to hunt badgers in their dens. That heritage explains the long body, short legs, and fearless personality of a dog that thinks it's much bigger than it is. Available in miniature and standard sizes, and in smooth, wirehaired, and longhaired varieties, the Dachshund is adaptable, charming, and full of surprising spirit.",
        ["Big personality in a compact body — endlessly entertaining", "Adaptable to apartment living with proper exercise", "Deeply loyal and attached to their person", "Comes in many varieties to suit different preferences", "Good watchdog instincts despite small size"],
        ["Prone to intervertebral disc disease (IVDD) — back problems are a serious concern", "Stubborn hound mentality can make training frustrating", "May be reactive or snappy without proper socialisation", "Tendency to bark — can be an issue in shared accommodation"],
    ),
    'Siberian Husky': (
        "The Siberian Husky was developed by the Chukchi people of northeastern Siberia to pull sleds across vast frozen distances — and that heritage is written into every aspect of the breed. Athletic, energetic, and built for endurance, Huskies are among the most striking dogs in the world, with their dense double coats, piercing eyes, and wolf-like appearance. They are social, playful, and genuinely affectionate, but demand owners who match their energy.",
        ["Breathtakingly beautiful appearance, often with striking blue or multi-coloured eyes", "Friendly and outgoing with people and other dogs", "Exceptional athleticism — ideal companion for runners and hikers", "Pack-oriented — generally excellent in multi-dog households", "Playful and entertaining personality"],
        ["Extremely high exercise requirements — 2+ hours daily minimum", "Epic shedding, particularly during biannual coat blows", "Strong prey drive and escape-artist tendencies require secure containment", "Can be vocal — howls rather than barks, but loudly", "Independent thinking makes recall training challenging"],
    ),
    'Border Collie': (
        "The Border Collie is widely recognised as the most intelligent dog breed in the world. Developed on the Anglo-Scottish border for sheep herding, the Border Collie is defined by its intense focus, extraordinary trainability, and seemingly boundless energy. These dogs thrive with a job to do and an owner who matches their drive. In the right home, they are extraordinary — in the wrong one, they are a handful.",
        ["Unmatched intelligence — learns commands and complex tasks with remarkable speed", "Excels in dog sports: agility, obedience, flyball, frisbee", "Intensely loyal and bonds deeply with their handler", "Athletic and built for all-day endurance", "Highly responsive to training — the most trainable breed in the world"],
        ["Needs 2+ hours of vigorous exercise AND substantial mental stimulation daily", "Herding instinct can manifest as nipping or circling children and cyclists", "Prone to anxiety and neurotic behaviour if under-stimulated", "Collie Eye Anomaly and other genetic conditions — health testing essential"],
    ),
    'Australian Shepherd': (
        "Despite the name, the Australian Shepherd was developed in the American West as a versatile ranch and herding dog. The Aussie combines outstanding intelligence, athletic ability, and a striking appearance — often featuring the distinctive merle coat and heterochromia. They are devoted, energetic, and endlessly eager to work, making them a top choice for dog sports and active families.",
        ["Highly intelligent and exceptionally trainable", "Athletic and versatile — excellent for agility, herding, and frisbee", "Deeply loyal and devoted to their family", "Striking appearance — merle coats and striking eye colours", "Adaptable to various working and sporting roles"],
        ["Very high energy — needs 1.5–2 hours of vigorous exercise daily", "Strong velcro tendency — can develop separation anxiety", "Herding instinct may emerge with children or other animals", "Known genetic health conditions: MDR1 gene mutation, eye anomaly — test breeders"],
    ),
    'Boxer': (
        "The Boxer is a medium-to-large breed from Germany, developed in the 19th century from the now-extinct Bullenbeisser hunting dog. Modern Boxers are cheerful, energetic, and famously affectionate — their tendency to stand on hind legs and 'box' with their front paws gave the breed its name. They are loyal family dogs who combine playfulness and protectiveness in an endearing, if sometimes silly, package.",
        ["Joyful, playful personality that lasts well into adulthood", "Devoted and protective of their family", "Good with children — energetic enough to keep up, gentle enough to be safe", "Alert and makes a capable watchdog", "Short coat requires almost no grooming"],
        ["Brachycephalic — prone to overheating and breathing difficulties in heat", "High energy when young — needs daily vigorous exercise", "Shorter than average lifespan for the size (10–12 years)", "Can be stubborn and requires patient, consistent training"],
    ),
    'Yorkshire Terrier': (
        "The Yorkshire Terrier was developed in 19th-century northern England for catching rats in clothing mills, but has since become one of the world's most beloved toy breeds. Behind the silky coat and elegant appearance is a bold, energetic, and sometimes feisty terrier who has no idea of its small size. Yorkies are portable, adaptable, and full of personality — ideal companions for city dwellers who want a big character in a small package.",
        ["Compact size — ideal for apartments and city living", "Huge personality and fierce loyalty to their owner", "Low shedding coat, well-tolerated by mild allergy sufferers", "Portable and easy to travel with", "Surprisingly brave and alert — excellent watchdog for their size"],
        ["Coat requires daily brushing if kept long, or regular professional trims", "Prone to barking — early training is essential", "Dental disease is a serious and common health issue", "Fragile size — not suitable for very young or rough children"],
    ),
    'Shih Tzu': (
        "The Shih Tzu was bred as a royal companion in Imperial China, and the breed has maintained an air of dignified self-possession ever since. Despite their elegant appearance, Shih Tzus are sturdy, playful, and surprisingly adaptable. They are equally at home in a city apartment or a suburban house, and their low exercise needs and friendly temperament make them an excellent choice for older or less active owners.",
        ["Affectionate, gentle, and ideal companion for quieter households", "Low exercise requirements — suited to apartment life", "Friendly and sociable with adults, older children, and other pets", "Adaptable to various environments and routines", "Generally long-lived — often 10–16 years"],
        ["Requires daily facial cleaning and regular coat maintenance", "Flat face (brachycephalic) causes overheating and breathing issues in heat", "Can be difficult to housetrain", "Prone to eye problems due to large, prominent eyes"],
    ),
    'Doberman Pinscher': (
        "The Doberman Pinscher was created in late 19th-century Germany by a tax collector named Karl Friedrich Louis Dobermann — who wanted the ideal personal protection dog. The result is a sleek, athletic, highly intelligent breed that is equally capable as a guardian, a police dog, and a loyal family companion. A well-bred and properly socialised Doberman is a remarkable animal — sensitive, trainable, and deeply devoted.",
        ["Extremely intelligent — among the most trainable breeds in the world", "Athletic, elegant, and physically impressive", "Loyal and protective without unnecessary aggression", "Responds exceptionally well to positive reinforcement training", "Naturally alert — an effective deterrent and guardian"],
        ["Requires experienced, consistent ownership — not for first-time dog owners", "Needs substantial daily exercise and mental engagement", "Can develop separation anxiety if left alone frequently", "Cardiac issues (DCM) and hip problems are known health risks — health testing critical"],
    ),
    'Chihuahua': (
        "The Chihuahua is the world's smallest dog breed, with a history stretching back to ancient Mesoamerica. Despite their tiny stature, Chihuahuas are bold, tenacious, and absolutely brimming with personality. They form intense bonds with their owners and can be surprisingly good watchdogs. Their minimal exercise needs and small size make them exceptionally practical for city living and travel.",
        ["World's smallest breed — supremely portable and easy to house", "Intense loyalty and strong bond with their chosen person", "Minimal exercise requirements", "Long lifespan — often 14–16 years", "Low grooming needs, especially in the smooth-coat variety"],
        ["Prone to excessive barking if not trained early", "Fragile — easily injured, not suitable for rough handling or young children", "Can be temperamental and slow to accept strangers without socialisation", "Dental disease is a significant and common health concern"],
    ),
    'Cavalier King Charles Spaniel': (
        "The Cavalier King Charles Spaniel is a gentle, affectionate breed with a long history as a royal companion dog. Named after King Charles II of England, who was rarely seen without his Spaniels, the Cavalier combines a silky, elegant coat with the warmest temperament in the dog world. They are adaptable, easy to train, and genuinely happy in almost any home — making them one of the best all-round family dogs.",
        ["Exceptional temperament — gentle, patient, and universally friendly", "Adaptable to various lifestyles and living situations", "Good with children, elderly people, and other animals", "Easy to train and eager to please", "Moderate exercise needs — suitable for a range of owners"],
        ["Serious genetic health concerns: Mitral Valve Disease and Syringomyelia — health testing essential", "Floppy ears require regular cleaning to prevent infections", "Can develop separation anxiety", "Not ideal as a guard dog — too friendly with strangers"],
    ),
    'Bernese Mountain Dog': (
        "The Bernese Mountain Dog is a large, tri-coloured working breed from the Swiss Alps, used historically for drafting, droving, and farm guarding. Berners are famous for their gentle temperament, calm confidence, and affectionate nature. They are outstanding family dogs — patient with children, calm around other animals, and deeply devoted to their people. The main caveat of the breed is a relatively short lifespan compared to their size.",
        ["Gentle giant with an exceptionally calm and patient temperament", "Outstanding with children and multi-generational families", "Striking tri-colour coat is truly beautiful", "Calm indoors while still enjoying outdoor adventures", "Loyal and devoted without being clingy"],
        ["Shorter lifespan than many breeds — typically 7–10 years", "Heavy seasonal shedding — requires regular brushing", "Susceptible to certain cancers and joint problems", "Can overheat in warm weather due to thick double coat"],
    ),

    # ── CATS ──────────────────────────────────────────────────────────────────
    'Maine Coon': (
        "The Maine Coon is the largest domestic cat breed, and one of the oldest natural breeds in North America. With their tufted ears, bushy tails, and thick double coats, Maine Coons are built for the cold winters of New England. But it's their personality — dog-like in sociability and playfulness, yet independently feline — that has made them consistently one of the most popular breeds worldwide.",
        ["Dog-like personality: follows owners, comes when called, loves interaction", "Gentle giant — exceptionally good with children and other pets", "Playful and kitten-like energy that persists into adulthood", "Robust constitution and generally good health", "Distinctive, beautiful appearance with a wide range of colours and patterns"],
        ["Dense coat requires brushing 2–3 times per week to prevent matting", "Large size means larger food bills and bigger litter boxes", "Heavy shedding, particularly in spring", "Can be prone to hypertrophic cardiomyopathy (HCM) — health testing recommended"],
    ),
    'Persian': (
        "The Persian is one of the most ancient and recognisable cat breeds, with a history stretching back to 17th-century Persia. Known for their luxurious long coat, flat face, and serene temperament, Persians are quintessential lap cats — calm, quiet, and utterly devoted to a peaceful domestic life. They are affectionate without being demanding, and their dignified presence makes any room feel more elegant.",
        ["Extremely calm and gentle — ideal for quiet households", "Affectionate and devoted lap cat", "Generally quiet and undemanding", "Stunning appearance with lush, flowing coat", "Good with older children and other cats"],
        ["Daily grooming is absolutely non-negotiable — coat mats quickly without it", "Brachycephalic (flat face) causes breathing difficulties, eye tearing, and heat sensitivity", "Not suited to active or noisy households", "Prone to polycystic kidney disease (PKD) — always choose health-tested lines"],
    ),
    'Ragdoll': (
        "The Ragdoll is a large, semi-long-haired breed developed in California in the 1960s by breeder Ann Baker. Named for their tendency to go limp when held, Ragdolls are famously relaxed, affectionate, and gentle. They are among the most laid-back cats in the world — rarely showing aggression, following their owners around like gentle shadows, and tolerating handling that would distress most cats.",
        ["Exceptionally gentle and patient — superb with children and other pets", "Tends to go limp when held — uniquely easy to handle", "Quiet and relatively undemanding companion", "Beautiful blue eyes and colourpoint coat", "Adaptable to indoor life and various household types"],
        ["Coat requires regular brushing to prevent tangles", "Laid-back nature means they can be oblivious to threats — must be kept indoors", "Can be prone to hypertrophic cardiomyopathy — genetic testing recommended", "May gain weight easily if diet is not monitored"],
    ),
    'Siamese': (
        "The Siamese is one of the oldest and most distinctive cat breeds, originating in Thailand (formerly Siam) where they were kept as sacred temple cats. Known for their striking colourpoint markings, brilliant blue eyes, and remarkably vocal personality, Siamese are intensely social animals who form deep bonds with their owners. They are the most talkative cats in the world — and will make sure you know it.",
        ["Deeply social and forms strong bonds with their people", "Highly intelligent and interactive — like having a conversational companion", "Striking appearance: vivid blue eyes and colourpoint coat", "Playful and kitten-like throughout their life", "Long lifespan — often 15–20 years"],
        ["Very vocal — their yowl can be startling and persistent", "Needs constant company and interaction — not suited to long hours alone", "Can be jealous and demanding of attention", "Prone to certain health conditions including dental disease and respiratory issues"],
    ),
    'British Shorthair': (
        "The British Shorthair is one of the oldest and most beloved cat breeds in the UK, descended from domestic cats brought to Britain by the Romans. Known for their round face, dense plush coat, and calm, easygoing temperament, British Shorthairs are the definition of a stable, uncomplicated companion. They are affectionate without being demanding, and content to be near you without being underfoot.",
        ["Calm, stable temperament — rarely reactive or anxious", "Affectionate but not clingy — respects personal space", "Dense, plush coat that is surprisingly easy to maintain", "Good with children and other pets", "Long lifespan — typically 14–20 years"],
        ["Can become overweight without portion control", "Not a lap cat — may prefer sitting beside you rather than on you", "Less playful as they age — better suited to calmer households", "Blue British Shorthairs are particularly popular but can be very expensive"],
    ),
    'Abyssinian': (
        "The Abyssinian is one of the oldest known cat breeds, believed to have originated in ancient Egypt or Ethiopia. Slender, athletic, and covered in a distinctive ticked coat that shimmers in the light, Abyssinians are among the most active and curious domestic cats. They are endlessly interested in their environment and people, making them one of the most interactive and entertaining cats you can own.",
        ["Extraordinarily curious and playful — endlessly entertaining", "Athletic and acrobatic — loves to climb and explore", "Warm and interactive with their people", "Distinctive ticked coat is genuinely beautiful", "Intelligent and quick to learn tricks and solve puzzles"],
        ["Very high activity level — not suited to calm or sedentary households", "Doesn't thrive when left alone for long periods", "Short attention span during formal training", "Prone to hereditary diseases including progressive retinal atrophy — health testing essential"],
    ),
    'Scottish Fold': (
        "The Scottish Fold originated from a barn cat named Susie, discovered in Scotland in 1961, whose ear cartilage folded forward to give her an owl-like expression. That distinctive look — combined with a sweet, adaptable temperament — made the breed immediately popular worldwide. Scottish Folds are calm, playful, and tend to get along well with everyone. However, the gene responsible for the folded ears also raises significant welfare concerns that every prospective owner should understand.",
        ["Distinctive, immediately recognisable appearance", "Sweet, calm temperament — adaptable and gentle", "Good with children, other cats, and dogs", "Playful but not demanding — a balanced companion", "Available in both folded and straight-eared varieties"],
        ["The fold gene causes osteochondrodysplasia — a painful joint condition affecting ALL fold-eared cats", "Many cat welfare organisations recommend against breeding fold-eared cats", "Lifetime veterinary monitoring for joint pain may be required", "Breeding two Folds together is considered unethical by most registries"],
    ),
    'Sphynx': (
        "The Sphynx is the world's most famous hairless cat breed, developed in Canada in the 1960s from a natural genetic mutation. Despite the alien appearance, Sphynx cats are among the warmest and most affectionate breeds on earth — literally and figuratively. Their wrinkled, hairless skin radiates heat, and their personality is expansive: extroverted, playful, and genuinely devoted to human contact.",
        ["Extremely affectionate — true velcro cat that loves constant contact", "Hypoallergenic-friendly — no coat to shed (though not truly allergen-free)", "Social with strangers, other cats, and dogs", "Entertaining and extroverted personality", "Dog-like in their loyalty and people-orientation"],
        ["Requires weekly full-body wiping down to remove oil build-up on skin", "Cold-sensitive — needs warm environments and sometimes clothing in winter", "Ears accumulate wax quickly and need regular cleaning", "Can be prone to hypertrophic cardiomyopathy — cardiac monitoring recommended"],
    ),
    'Bengal': (
        "The Bengal was created by crossing domestic cats with the Asian Leopard Cat, producing a breed with genuinely wild markings — vivid rosettes and spots on a sleek, muscular body — and a high-energy, inquisitive personality to match. Bengals are stunning to look at and endlessly interesting to live with, but they are an active, demanding breed that requires owners who can match their intelligence and energy.",
        ["Spectacular wild appearance with vivid spots and rosettes", "Highly intelligent and curious — never boring to live with", "Athletic and playful throughout their life", "Many love water, making grooming easier", "Bond closely with their chosen person"],
        ["Very high energy — not suited to passive or busy owners who are rarely home", "Strong prey drive — supervision needed with small animals and birds", "Can become destructive if bored or under-stimulated", "Loud and communicative — not a quiet cat"],
    ),
    'Russian Blue': (
        "The Russian Blue is an elegant, reserved breed believed to have originated in the port city of Archangel in northern Russia. Their dense, plush blue-grey coat and vivid green eyes create a striking appearance, but it's their gentle, loyal personality that wins owners over. Russian Blues are devoted to their families while remaining naturally cautious with strangers — a combination that makes them quiet, steady, and deeply rewarding companions.",
        ["Gentle, quiet, and deeply loyal to their chosen family", "Low-shedding coat despite the plush appearance", "Low allergen production — often tolerated by mild allergy sufferers", "Calm and adaptable — suited to quieter households", "Intelligent and observant without being demanding"],
        ["Naturally shy with strangers — takes time to warm up to new people", "Can become anxious if their routine is frequently disrupted", "Not a lap cat on demand — affection is on their terms", "Needs mental stimulation or can become bored and withdrawn"],
    ),
    'Norwegian Forest Cat': (
        "The Norwegian Forest Cat — known in Norway as Skogkatt — is a large, semi-wild-looking breed that has lived in Scandinavian forests for centuries. Built for harsh climates with a thick water-repellent double coat, tufted ears, and large, tufted paws, the Wegie is as hardy as it looks. Despite the rugged exterior, they are affectionate, calm, and good-natured — the ideal companion for those who appreciate a more independent feline.",
        ["Hardy and exceptionally healthy — natural rather than selectively bred to extremes", "Calm and stable temperament — excellent with families", "Semi-long coat is less prone to matting than Persian or Ragdoll", "Good with children and other pets", "Adaptable and confident in new situations"],
        ["Dense coat sheds heavily, especially twice a year", "More independent than some breeds — may not seek constant affection", "Needs vertical space (cat trees, shelves) to feel content", "Large size requires more food and larger facilities than average cats"],
    ),
    'Burmese': (
        "The Burmese is one of the most social and affectionate cat breeds in the world, originating in Burma (now Myanmar) and formalised as a breed in the United States in the 1930s. Compact, muscular, and covered in a short satin coat, Burmese cats are warm, playful, and intensely devoted to their people. They are the quintessential companion cat — but their need for company means they should rarely be left alone for long.",
        ["Extraordinarily affectionate — one of the most people-oriented breeds", "Silky, low-maintenance short coat that sheds minimally", "Playful and kitten-like throughout life", "Adapts beautifully to family life with children and other pets", "Remarkably healthy breed with few genetic issues"],
        ["Needs constant company — can develop anxiety if frequently left alone", "Very social demand means single-cat owners need to be home often", "Vocal when unhappy or under-stimulated", "Some lines prone to craniofacial defect — choose breeders carefully"],
    ),
    'Devon Rex': (
        "The Devon Rex is one of the most distinctive cat breeds in the world, with its huge ears, prominent cheekbones, and short wavy coat giving it an unmistakably elfin, slightly alien appearance. Developed in Devon, England in the 1960s from a spontaneous mutation, the Devon Rex is an irresistibly mischievous, acrobatic, and affectionate cat that bonds closely with its family and treats every day as a performance opportunity.",
        ["Unique and striking appearance — bat-eared and wavy-coated", "Extremely affectionate and bonds intensely with family", "Low-shedding coat — well-tolerated by many allergy sufferers", "Highly playful and entertaining throughout life", "Social and confident with strangers"],
        ["Thin coat offers poor insulation — needs warm environments in colder climates", "Ears accumulate wax quickly and need regular cleaning", "Higher metabolic rate means they eat more than similarly-sized cats", "Can be mischievous and get into things if not given adequate enrichment"],
    ),
    'American Shorthair': (
        "The American Shorthair is one of the most popular pedigree breeds in the United States, descended from working cats brought to America by early European settlers. Valued for their mousing ability and adaptable temperament, American Shorthairs have been refined into a well-balanced, healthy, and agreeable companion cat. They are the embodiment of the all-round cat: hardy, friendly, and uncomplicated.",
        ["Exceptionally adaptable and easy to live with", "Hardy and robust — one of the healthiest pedigree breeds", "Friendly but not overly demanding", "Good with children, dogs, and other cats", "Long lifespan — frequently 15–20 years"],
        ["Less interactive than some breeds — won't always seek out cuddles", "Moderate shedding — coat needs occasional brushing", "Can become overweight without portion management", "Less visually distinctive than some other breeds — though that's also their charm"],
    ),
    'Exotic Shorthair': (
        "The Exotic Shorthair was developed in the 1950s by crossing Persians with American Shorthairs to create a Persian-type cat with a short, plush coat. The result is a cat that combines the gentle, serene temperament of the Persian with the practicality of a shorter, lower-maintenance coat. Often described as 'the lazy man's Persian,' the Exotic is one of the most relaxed and affectionate breeds available.",
        ["Calm, gentle, and deeply affectionate", "Short coat requires far less grooming than a Persian", "Quiet and peaceful — ideal for calm households", "Good with children, older people, and other pets", "Adaptable and content as an indoor-only cat"],
        ["Flat face causes the same brachycephalic health issues as Persians", "Prone to tear staining — daily eye cleaning required", "Less active than many breeds — not for owners who want an energetic cat", "Still requires regular brushing 1–2 times per week"],
    ),
    'Birman': (
        "The Birman — or Sacred Birman — is a silky, semi-long-haired breed with a gentle, inquisitive personality and distinctive white 'glove' markings on all four paws. According to legend, they were the sacred companions of Burmese temple priests. Modern Birmans are known for their beautiful blue eyes, affectionate nature, and calm adaptability — a breed that integrates gracefully into virtually any household.",
        ["Gentle, patient, and consistently sweet-natured", "Silky semi-long coat is less prone to matting than Persian or Ragdoll", "Beautiful blue eyes and distinctive white gloves", "Warm and affectionate without being clingy", "Good with children, elderly people, and other pets"],
        ["Semi-long coat still needs regular brushing, 2–3 times per week", "Can be prone to hypertrophic cardiomyopathy — choose health-tested lines", "Slower to warm up to strangers than some breeds", "Loves routine — can be unsettled by major changes"],
    ),
    'Tonkinese': (
        "The Tonkinese is a deliberate cross between the Siamese and the Burmese, combining the intelligence and sociability of both breeds. The result is a cat that is vocal and interactive like a Siamese, but with the warmer, less intense personality of the Burmese. Tonkinese cats are affectionate, playful, and endlessly engaging — the perfect choice for anyone who wants an active, communicative companion without the full Siamese intensity.",
        ["Highly social and people-oriented", "Intelligent and easy to engage with play and training", "Less intense than pure Siamese — slightly calmer and gentler", "Beautiful aquamarine eyes unique to the breed", "Playful and kitten-like throughout their life"],
        ["Needs regular company and stimulation — not suited to long periods alone", "Vocal and communicative — may not suit noise-sensitive households", "High energy requires appropriate enrichment and play", "Can be demanding of attention"],
    ),
    'Himalayan': (
        "The Himalayan is a pointed version of the Persian, produced by crossing Persians with Siamese to introduce the colourpoint coat pattern and blue eyes. The result is a cat that combines Persian calm and long coat with Siamese colouring — and a personality that sits between the two parent breeds. Himalayans are gentle, quiet, and beautiful, but their flat face and long coat come with real care responsibilities.",
        ["Strikingly beautiful — vivid blue eyes against a colourpoint coat", "Extremely calm and gentle temperament", "Deeply affectionate and devoted companion", "Quiet and well-suited to calm, peaceful households", "Good with older children and other gentle pets"],
        ["Daily grooming is absolutely essential — coat mats without it", "Brachycephalic face causes breathing issues, tear staining, and heat sensitivity", "Susceptible to polycystic kidney disease — genetic testing essential", "High maintenance overall — not for busy or low-commitment owners"],
    ),
    'Turkish Angora': (
        "The Turkish Angora is one of the oldest and most elegant natural cat breeds, originating in the Ankara region of Turkey. With its fine, silky single coat, athletic build, and distinctly confident personality, the Turkish Angora is unlike any other long-haired breed. They are active, curious, and sometimes bossy — they know they're beautiful, and they expect appropriate recognition.",
        ["Elegantly beautiful with a fine, single-layer silky coat", "Athletic, playful, and remains active well into adulthood", "Social and curious — loves to participate in everything", "Many love water — making grooming less of a struggle", "Long natural history — robust constitution and good health"],
        ["Assertive and sometimes demanding personality — knows what it wants", "Coat may need occasional brushing despite the single-layer structure", "Can be bossy with other cats if not properly introduced", "High activity level — not suited to passive or frequently absent owners"],
    ),
    'Chartreux': (
        "The Chartreux is a rare and ancient French breed, associated with the Carthusian monks who may have bred them at the Grande Chartreuse monastery near Grenoble. Known for their distinctive blue-grey coat with a slightly woolly texture, copper or amber eyes, and a gentle, observant personality, the Chartreux is a quietly exceptional cat. They are loyal, calm, and devoted — a breed that wears its affection quietly but consistently.",
        ["Exceptionally calm, quiet, and undemanding", "Deeply loyal — forms strong bonds with their family", "Dense, water-repellent blue coat is beautiful and relatively easy to maintain", "Good with children and other pets", "Robust and healthy — natural breed with few genetic issues"],
        ["Slow to warm up to strangers — reserved with new people", "Less demonstrative than some breeds — affection is quiet and subtle", "Can seem aloof to those expecting more expressive cats", "Relatively rare — finding a reputable breeder takes research"],
    ),
    'Munchkin': (
        "The Munchkin is a natural mutation cat breed characterised by very short legs caused by a genetic mutation affecting long bone growth — similar to achondroplasia in dogs. Discovered in the 1980s in Louisiana, Munchkins have since become popular for their distinctive appearance and playful, confident personality. Despite the short legs, they are surprisingly agile and mobile, though they cannot always access the heights a normal cat can.",
        ["Distinctive and immediately recognisable appearance", "Playful, curious, and confident personality", "Adaptable and generally sociable with people and other pets", "Compact size makes them practical for smaller homes", "Active and entertaining despite their unusual build"],
        ["The mutation causing short legs is controversial — ethical debate is ongoing", "Cannot jump to the same heights as standard cats — needs step access to furniture", "Some lines show spinal and hip issues related to the mutation", "Needs responsible breeding — some lines have additional health complications"],
    ),
    'Siberian': (
        "The Siberian is Russia's national cat — a large, powerful, naturally occurring breed that developed over centuries in the harsh Siberian climate. Their triple-layer, water-repellent coat and robust constitution reflect that heritage. What surprises most owners is the personality: warm, dog-like, and deeply affectionate. Siberians also produce lower levels of the Fel d 1 allergen than most breeds, making them one of the better options for allergy-sensitive households.",
        ["Often tolerated by allergy sufferers — lower Fel d 1 allergen levels", "Warm, loyal, and affectionate despite large imposing size", "Remarkably robust and healthy — a natural, unselected breed", "Dense triple coat is water-resistant and surprisingly manageable", "Good with children, dogs, and other cats"],
        ["Large size — needs space, bigger food portions, and larger facilities", "Triple coat sheds significantly, particularly twice a year", "Can be reserved with strangers until trust is established", "Relatively rare outside Russia — finding a breeder takes effort"],
    ),
    'Turkish Van': (
        "The Turkish Van is an ancient semi-longhaired breed from the Lake Van region of Turkey, distinguished by the 'Van pattern' — a predominantly white body with colour restricted to the head and tail. They are sometimes called 'the swimming cats' because they genuinely seem to enjoy water — unusual for domestic cats. Turkish Vans are active, assertive, and endlessly entertaining, but they are a breed with opinions and they will share them.",
        ["Fascinatingly distinctive Van colour pattern", "Known for their unique water fascination — many actively seek out water", "Athletic and playful — naturally very active", "Robust natural breed with generally good health", "Surprisingly affectionate despite independent personality"],
        ["Very active and needs significant daily enrichment and play", "Independent and assertive — not a lap cat on demand", "Can be bossy with other cats", "Semi-long coat needs regular brushing to prevent occasional tangles"],
    ),
    'Cornish Rex': (
        "The Cornish Rex is one of the most distinctive cats in the world, with its dramatically large ears, prominent cheekbones, and short, tightly waved coat caused by a mutation that first appeared in Cornwall, England in 1950. The Cornish Rex looks like something from another planet — and acts like it too. They are among the most active, acrobatic, and extroverted cats in existence, turning every room into a stage.",
        ["Truly unique appearance — unlike any other breed", "Very low shedding — coat produces minimal loose hair", "Extroverted and social — loves people and gets along with other pets", "Remains playful and kitten-like throughout life", "Often well-tolerated by allergy sufferers"],
        ["Thin coat provides minimal insulation — sensitive to cold", "Higher caloric needs due to elevated metabolism", "Needs significant daily enrichment and play to stay settled", "Ears require more frequent cleaning than most breeds"],
    ),
    'Balinese': (
        "The Balinese is essentially a long-haired Siamese — a naturally occurring mutation that produced a Siamese with a flowing silky coat and plumed tail. They share the Siamese's intelligence, sociability, and blue eyes, but with a slightly softer personality and a spectacularly beautiful coat that somehow requires less maintenance than it suggests. Balinese are devoted, vocal, and completely enchanting companions.",
        ["Stunning silky coat with Siamese colourpoint markings and blue eyes", "Intelligent, social, and deeply affectionate", "Somewhat less intense than pure Siamese — slightly calmer temperament", "Low-shedding single coat is easy to maintain despite its length", "Long lifespan — often 15–20 years"],
        ["Vocal and communicative — not for noise-sensitive owners", "Needs significant company and engagement — not suited to long hours alone", "Can be demanding of attention", "Prone to some Siamese-related health conditions"],
    ),
    'Somali': (
        "The Somali is a long-haired Abyssinian — the result of a recessive gene for long hair that occasionally appeared in Abyssinian litters and was eventually developed into its own breed. The Somali carries all of the Abyssinian's athleticism, curiosity, and intelligence, wrapped in a spectacular semi-long ticked coat and a dramatically bushy fox-like tail. They are extraordinarily beautiful and tirelessly active.",
        ["One of the most beautiful cats in the world — the 'fox cat'", "Highly intelligent, curious, and endlessly entertaining", "Athletic and remains playful throughout its life", "Interactive and warm with their chosen family", "Ticked coat is visually stunning and relatively easy to maintain"],
        ["Very high energy — demands active, engaged owners", "Doesn't thrive when left alone for long periods", "Needs significant environmental enrichment to stay settled", "Not suited to calm or passive households"],
    ),
    'Egyptian Mau': (
        "The Egyptian Mau is the only naturally spotted domestic cat breed — their spots are a genuine part of their genetic heritage, not the result of crossing with wild cats. Believed to be descended from cats depicted in ancient Egyptian art, Maus are athletic, loyal, and distinctly reserved with strangers. They are the fastest domestic cat breed, capable of running up to 48km/h, and their combination of wild beauty and loyal devotion is genuinely extraordinary.",
        ["The only naturally spotted domestic cat — unique and beautiful", "Deeply loyal and devoted to their chosen family", "Extraordinary athlete — fastest domestic cat breed", "Generally healthy as a natural breed", "Striking gooseberry-green eye colour unique to the breed"],
        ["Reserved and sometimes shy with strangers — needs patient socialisation", "Can be vocal when unhappy or under-stimulated", "High energy needs require daily active play", "Needs space to run and express their natural athleticism"],
    ),
    'Manx': (
        "The Manx is a naturally tailless (or short-tailed) cat breed originating on the Isle of Man, where the mutation became fixed in the island's isolated cat population. Beyond the distinctive taillessness, Manx cats are known for their rounded, compact body and a personality that is often described as dog-like — they fetch, follow their owners, and form unusually strong bonds with their people. They are loyal, playful, and enduringly charming.",
        ["Dog-like loyalty and personality — some learn to fetch", "Calm, stable, and highly adaptable temperament", "Good with children and other pets", "Available in varying tail lengths: rumpy, stumpy, and tailed", "Generally healthy when sourced from responsible breeders"],
        ["Manx syndrome: tailless genetics can cause serious spinal defects in some lines", "Health testing by breeders is essential — avoid buying from untested lines", "Compact build can lead to weight gain — portion control important", "May be reluctant to jump to great heights due to body structure"],
    ),
    'Selkirk Rex': (
        "The Selkirk Rex is the newest of the Rex cat breeds, discovered in Montana in 1987 when a shelter kitten was born with an unusually curly coat. Unlike Devon and Cornish Rex, the Selkirk Rex has a full, plush, sheep-like coat rather than a thin wavy one, giving them a teddy bear appearance that is immediately endearing. Their personality is equally cuddly — patient, affectionate, and wonderfully uncomplicated.",
        ["Unique plush curly coat with a wonderfully soft texture", "Extremely patient and gentle temperament", "Good with children, other cats, and dogs", "Adaptable and easy-going — one of the least demanding Rex breeds", "The curl gene is dominant — outcrossing maintains genetic diversity"],
        ["Coat can mat without regular brushing — needs 2–3 times per week", "Less energetic than some breeds — may not suit owners wanting an active cat", "Still relatively new breed — finding a reputable breeder requires research", "Can gain weight if diet is not managed carefully"],
    ),
    'Savannah': (
        "The Savannah cat is a hybrid between a domestic cat and an African Serval, first produced in 1986. The result is a tall, spotted, remarkably athletic cat that looks genuinely wild and has the personality to partially match. Earlier generation Savannahs (F1, F2) are very close to wild in temperament; later generations (F4, F5) are more reliably domestic. All generations share extraordinary beauty, high intelligence, and boundless energy.",
        ["The most spectacular-looking domestic cat — genuinely wild appearance", "Highly intelligent and bonds strongly with their family", "Dog-like in loyalty — many learn to walk on leash and play fetch", "Athletic and endlessly entertaining", "Strong presence and confident personality"],
        ["Legal restrictions in many countries, states, and cities — research essential before purchasing", "Very high energy — needs extensive enrichment and large living spaces", "Earlier generations can be unpredictable in temperament", "Expensive to purchase and can be costly to insure and house appropriately"],
    ),
}


def main():
    from app import create_app, db
    from app.models import Subject

    app = create_app('development')

    with app.app_context():
        updated = 0
        for subj in Subject.query.all():
            info = BREED_INFO.get(subj.name)
            if not info:
                continue
            description, pros, cons = info
            subj.description = description
            subj.pros = '\n'.join(pros)
            subj.cons = '\n'.join(cons)
            updated += 1

        db.session.commit()
        logger.info(f"Updated {updated} breeds with description, pros, and cons.")


if __name__ == '__main__':
    main()
