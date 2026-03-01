from __future__ import annotations

import hashlib
import logging
import os
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

_ADJECTIVES = [
    "Happy", "Fluffy", "Brave", "Gentle", "Swift", "Loyal", "Clever", "Bold",
    "Calm", "Eager", "Fierce", "Golden", "Jolly", "Kind", "Lively", "Merry",
    "Noble", "Peppy", "Quiet", "Rusty", "Sunny", "Tender", "Vivid", "Witty",
    "Zesty", "Amber", "Breezy", "Crisp", "Dandy", "Earthy",
]

_ANIMALS = [
    "Paw", "Tail", "Snout", "Fang", "Claw", "Muzzle", "Whisker", "Fetch",
    "Bark", "Purr", "Howl", "Wag", "Nuzzle", "Romp", "Leap", "Trot",
    "Gallop", "Bound", "Prowl", "Pounce",
]


def _rnd_name(rng: random.Random) -> str:
    adj = rng.choice(_ADJECTIVES)
    animal = rng.choice(_ANIMALS)
    num = rng.randint(10, 99)
    return f"{adj}{animal}{num}"


BREED_DATA: dict = {
    # ------------------------------------------------------------------ DOGS
    "Akita": {
        "description": (
            "The Akita is a large, powerful Japanese breed originally used for hunting bear and guarding royalty. "
            "Known for their dignified and reserved nature, Akitas are deeply loyal to their families while being naturally aloof with strangers. "
            "They require experienced handling and consistent training to channel their strong-willed personality."
        ),
        "pros": [
            "Fiercely loyal and devoted to their family",
            "Naturally clean and easy to housebreak",
            "Excellent guard dog instincts",
            "Calm and quiet indoors",
        ],
        "cons": [
            "Can be aggressive toward other dogs",
            "Not suitable for first-time owners",
            "Heavy seasonal shedding",
            "Strong prey drive requires secure fencing",
        ],
        "reviews": [
            (5, "My shadow for eleven years", "I got my Akita when he was eight weeks old and he has never left my side since. He is not a cuddly dog in the traditional sense but he follows me everywhere and watches over me with those serious amber eyes. When strangers come to the door he stands between me and them without making a sound, which honestly is more intimidating than barking. He needs a firm hand during training but once he respects you the bond is unbreakable. Grooming twice a week keeps the shedding manageable. Best dog I have ever owned."),
            (4, "Magnificent but demanding breed", "My Akita is stunning to look at and has a presence that commands a room. She learned basic commands quickly but she decides when she wants to obey, which requires patience. She is fantastic with my kids but I never leave her alone with unfamiliar dogs because she has a short fuse with them. The double coat blows out twice a year and I could stuff a mattress with the fur. Worth every extra effort for the right experienced owner."),
            (5, "Ultimate one-person dog", "She chose me from day one and that was that. My Akita has no interest in anyone else in the household, which sounds extreme but she is perfectly polite with my family, just indifferent. With me she is tender and attentive. She alerted me to a gas leak at 3am by pawing at my face. I owe her my life. Training took about a year of daily work but she is now impeccably behaved in public."),
            (3, "Beautiful breed but not for everyone", "I researched Akitas for two years before getting one and I still underestimated the challenge. Mine is fantastic at home but every walk requires full attention because he wants to start something with every dog we pass. We have done extensive socialization work and professional training and he is better but never fully relaxed around other dogs. If you live in a rural area with space and no other pets this breed is incredible."),
            (5, "Regal and quietly affectionate", "People assume Akitas are cold but mine is the opposite, she just expresses love differently. She leans against my legs, rests her head on my lap in the evenings, and checks on me whenever I am in a different room. She does not bark excessively, she does not destroy furniture, and she is fastidiously clean. The shedding is real but so is the reward of living with this magnificent animal."),
            (4, "Great with proper socialization", "Started socializing my Akita from eight weeks old and the difference is noticeable compared to other Akitas I have met. He is calm around dogs he knows and tolerates well-mannered strangers. He has a strong independent streak that makes training an ongoing negotiation rather than a one-time lesson but he is responsive when motivated. The loyalty and protection he provides are second to none."),
            (2, "More than I could handle", "I love this breed but I have to be honest about my experience. My Akita developed dog aggression at around eighteen months despite all my socialization efforts. Two dog fights with neighbours later I had to rehome him to a single-dog household with an experienced owner. He thrives there now. This is not a breed for an apartment or a multi-dog home unless you know exactly what you are doing."),
            (5, "Ten out of ten for the right home", "My Akita is nine now and I cannot imagine life without her. She has never been destructive, never barks unnecessarily, and has perfect house manners. She is reserved with guests initially but warms up once she has assessed them as safe. The grooming and the dog-selective nature are real considerations but they are manageable. She is healthy, vital, and still acts like a puppy on walks."),
            (4, "Impressive intelligence and presence", "Training my Akita required me to be smarter than him, which was a challenge. He figured out how to open the refrigerator within the first month. He is not food motivated for training which made early lessons hard but he is praise-motivated so we found our rhythm. He is calm, quiet, and astonishingly perceptive about my moods. When I am stressed he presses himself against me without being asked."),
        ],
    },
    "Alaskan Malamute": {
        "description": (
            "The Alaskan Malamute is one of the oldest Arctic sled dogs, bred for hauling heavy freight across frozen terrain. "
            "These powerful and athletic dogs have a friendly, outgoing personality but retain strong pack instincts and a need for vigorous daily exercise. "
            "They thrive in active households that can provide outlets for their considerable energy and intelligence."
        ),
        "pros": [
            "Friendly and sociable with people",
            "Incredibly strong and athletic working companion",
            "Surprisingly gentle and patient with children",
            "Adaptable to cold climates",
        ],
        "cons": [
            "Needs massive amounts of daily exercise",
            "Prone to digging and howling",
            "Heavy shedder year-round with dramatic blow-outs",
            "Can be difficult to recall off-leash",
        ],
        "reviews": [
            (5, "A force of nature in the best way", "Owning a Malamute is like owning a beautiful, chaotic force of nature. Koda needs two hours of hard exercise every single day or he reorganises my garden for me. On days when we hike or go running he is absolutely perfect at home, calm and gentle with my kids. His howl sounds like a wolf and the neighbours initially complained but they have since adopted him as the unofficial neighbourhood mascot. There is truly no other breed like this one."),
            (4, "Amazing dog, demanding lifestyle", "My Malamute is the most beautiful dog I have ever seen and also the most exhausting. We do canicross three times a week and long hikes on weekends. When she is well exercised she is the gentlest creature alive with my toddler. When she is under-exercised she dismantles furniture. The shedding is extraordinary. I go through two vacuum bags a week but I would not trade her for anything."),
            (5, "Best trail partner imaginable", "I adopted my Malamute at two years old and she has transformed my fitness. I had to get fit to keep up with her. She pulls strongly on the leash which we have worked on but she is excellent in harness for bikejoring. She is sweet with everyone she meets, dogs included, and has never shown aggression. She does talk back with dramatic howls when she disagrees with a decision but I find it hilarious."),
            (3, "Beautiful breed but be prepared", "I love my Malamute deeply but the reality of ownership hit me hard. The shedding is not just heavy it is relentless. The exercise requirement is not a suggestion it is a mandate. He dug up my entire back garden in one afternoon when I was sick and could not walk him. He is wonderful with my family and incredibly affectionate. Just make sure your lifestyle genuinely matches this breed before committing."),
            (5, "Gentle giant with my family", "My Malamute has been extraordinary with my three children, ages four through ten. He lets the youngest crawl on him and never reacts negatively. He is enormous and powerful but seems to understand he needs to be gentle with small humans. He greets every visitor like a long-lost friend. His only downside is the hair. I could build a second dog from what he sheds in a week."),
            (4, "Incredible working dog, not a pet for the lazy", "I use my Malamute for weight pulling competitions and she absolutely excels. The strength in this breed is remarkable. She trains enthusiastically and has an excellent work ethic when the task involves physical effort. Obedience commands are a different story since she finds them boring. She is selective about which instructions she follows but physical working tasks she performs with full commitment and joy."),
            (5, "Changed my life for the better", "Getting my Malamute forced me to overhaul my entire lifestyle. I now hike every morning, run three evenings a week, and spend my weekends outdoors. He dragged me out of a sedentary rut and I have lost thirty pounds in the process. He is affectionate, funny, communicative, and has the best temperament of any dog I have met. The house is covered in fur and I could not care less."),
            (4, "Loves everyone, respects no fences", "My Malamute loves every human and dog she has ever met but she views fencing as a suggestion rather than a boundary. We have reinforced our fence three times. She is not trying to escape out of anxiety, she just genuinely wants to go on an adventure. We have reliable recall in open fields but near exciting smells all training goes out the window. Extraordinary breed, needs extraordinary containment."),
            (3, "Not suitable for my climate", "I made the mistake of getting a Malamute in a subtropical climate. He struggles terribly in summer heat despite our air-conditioned home. We can only walk early morning and late evening from May through September. He is wonderful in winter and spring but the summer restrictions on exercise are genuinely challenging for a breed that needs this much activity. If you live somewhere warm, research this seriously before committing."),
        ],
    },
    "Basset Hound": {
        "description": (
            "The Basset Hound is a short-legged scent hound of French origin, bred to trail rabbits and hare through dense undergrowth. "
            "With their mournful expression, floppy ears, and melodious bay, Bassets are charming and low-key companions who are devoted to their families. "
            "They can be stubborn on the leash when a scent catches their attention, but at home they are reliably calm and affectionate."
        ),
        "pros": [
            "Gentle and patient temperament with children",
            "Low energy indoors, happy to nap",
            "Friendly with other dogs and pets",
            "Rarely aggressive",
        ],
        "cons": [
            "Stubbornly follows nose regardless of commands",
            "Loud, persistent baying when bored or excited",
            "Prone to obesity without diet management",
            "Ears require regular cleaning to prevent infection",
        ],
        "reviews": [
            (5, "The perfect lazy day companion", "My Basset Hound Humphrey is the most laid-back dog I have ever met. He spends about twenty hours a day sleeping and the remaining four hours eating, sniffing the garden, and demanding belly rubs. He is endlessly patient with my kids, never snaps, and greets every visitor like they are the most important person in the world. He does bay loudly when the postman arrives but a treat stops him immediately. Truly a wonderful breed for a calmer household."),
            (4, "Sweet and stubborn in equal measure", "My Basset is absolutely adorable and completely infuriating on walks. The moment she catches an interesting scent she becomes deaf to all commands and nothing in the world exists except that smell. I have learned to let her sniff to her heart's content and she eventually comes back to me. At home she is the most gentle, loving dog. Her long ears need cleaning twice a week but otherwise she is low maintenance."),
            (5, "Best dog for apartment living", "I was worried a dog this size might struggle in my flat but my Basset has adapted perfectly. He gets two walks a day and is completely content to rest otherwise. He is quiet indoors, gentle with my elderly mother who visits often, and loves cuddles on the sofa. He has never been destructive. The only expense is food because he will eat absolutely anything and everything without stopping."),
            (3, "Lovable but the baying is intense", "I adore my Basset but nobody warned me about the volume and persistence of a Basset bay. When she is left alone for more than an hour she bays until I return and my neighbours have complained twice. We are working with a trainer on separation anxiety but it is a slow process. When I am home she is the most peaceful, affectionate dog imaginable. Just be prepared for the noise if you have close neighbours."),
            (5, "Gentle giant for families", "Three kids under eight and a Basset Hound is a match made in heaven. He lets my youngest dress him up in doll clothes without complaint. He is never rough, never jumps, and seems to genuinely enjoy the chaos of a busy family home. He does need to be watched around food because he will steal anything within reach. His droopy eyes and sad expression are completely misleading. He is the happiest dog alive."),
            (4, "Surprisingly athletic when motivated", "People think Bassets are couch potatoes and mine mostly is, but when he catches a scent trail in the woods he transforms into a determined athlete. He can cover miles on a good scent and his nose is extraordinary. I do field trailing with him as a hobby and he takes to it naturally. The challenge is the baying during training but fellow enthusiasts understand. A great breed for someone who wants a slow-paced companion with hidden depth."),
            (4, "Great temperament, high maintenance ears", "My Basset has the best temperament of any dog I have owned. She is calm, patient, and endlessly affectionate. The downside is her ears. They need cleaning twice a week and she has had three ear infections in two years despite my efforts. The vet says it is just the anatomy of the breed. It is not a dealbreaker but it is an ongoing time and financial commitment that surprised me."),
            (5, "My son's best friend", "My twelve-year-old son was going through a tough time at school and our Basset Hound became his therapy. They spend hours together, the dog following him everywhere with those mournful eyes, listening without judgment. The breed is genuinely empathetic and seems to sense when someone needs comfort. Our Basset is healthy at seven years old and we are hoping for many more years with this wonderful, soulful breed."),
        ],
    },
    "Belgian Malinois": {
        "description": (
            "The Belgian Malinois is a highly driven, intelligent herding breed now widely used by military and police forces worldwide. "
            "Intense, athletic, and tireless, Malinois thrive when given demanding work and consistent training from experienced handlers. "
            "In the right hands they are exceptional partners, but they are not recommended for novice owners or low-activity households."
        ),
        "pros": [
            "Exceptional intelligence and trainability",
            "Outstanding working and sport dog capabilities",
            "Loyal and deeply bonded to their handler",
            "Highly alert and protective",
        ],
        "cons": [
            "Requires hours of intense daily exercise and mental stimulation",
            "Not suitable for inexperienced dog owners",
            "Can develop destructive behaviours when under-stimulated",
            "High prey drive requires careful management",
        ],
        "reviews": [
            (5, "The ultimate working partner", "I have had dogs all my life but nothing prepared me for a Malinois. She learned sit, down, stay, heel, and a dozen sport commands in her first three months. She runs agility courses faster than dogs twice her age, works IPO protection with precision, and is a flawless tracking dog. She is also exhausting. She needs four hours of structured activity every single day or she will find her own entertainment. For an active, experienced handler this breed is extraordinary."),
            (4, "Brilliant but not for beginners", "My Mal is the smartest dog I have ever owned and also the most demanding. He figured out how to open every door in my house within a month. He needs a job. We do agility, nosework, and obedience trials. When he is well stimulated he is calm, affectionate, and a joy to live with. When something is off in his schedule he becomes restless and mouthy. Incredibly rewarding for the right person."),
            (5, "Life-changing breed", "I got my Malinois after years with Border Collies so I thought I understood high-drive dogs. The Mal operates at another level entirely. She is relentless in her focus, athletic beyond belief, and bonds with a depth I have not experienced before. She watches me constantly, anticipates my next move, and seems genuinely offended when I do not challenge her enough. I do two hours of structured training daily plus off-leash running. She is everything I wanted."),
            (3, "Amazing dog in the wrong home", "I got a Malinois because I thought they were like German Shepherds. They are not. My boy was destructive, anxious, and unmanageable until I hired a specialist trainer and completely restructured my life around his needs. He is now a working sport dog and thriving, but the first year was genuinely difficult. If you are thinking about this breed, research intensively and be honest about your activity level and experience."),
            (5, "Best decision of my life", "My Malinois goes everywhere with me. We do bikejoring, agility, hiking, and Schutzhund. She has made me fitter, more disciplined, and more patient. Her training has been the most rewarding challenge I have ever taken on. She is sharp as a tack and reads me better than any human. In eight years she has never been destructive, never shown inappropriate aggression, and has been a perfectly well-mannered companion because I put in the necessary work."),
            (4, "Incredible sport dog, complex pet", "I use my Mal for French Ring sport and he is extraordinary at it. His focus, drive, and athleticism are unmatched. As a pet in a normal sense he is more complex. He is not a dog you can ignore for a weekend. He needs engagement every day without exception. My relationship with him is more like a training partnership than traditional pet ownership, and I would not have it any other way."),
            (2, "Rehomed after six months", "I have to be completely honest. I got a Malinois thinking my active lifestyle would be enough. It was not. This breed needs not just physical exercise but intense mental engagement that I was not equipped to provide. My boy became destructive and began nipping out of frustration. A professional trainer assessed him and confirmed he needed an experienced working-dog handler. He was rehomed to a police dog trainer and is thriving. Do your research before this breed."),
            (5, "The athlete of the dog world", "She can jump a six-foot fence from standing, run all day without tiring, and solve problems that would stump most breeds. My Malinois is extraordinary in every sense. We do nosework competitions and she has won at national level. She is focused, driven, and absolutely tireless. At home with me and my partner she is calm and affectionate. The key is she never has an idle day. Not one."),
        ],
    },
    "Bichon Frise": {
        "description": (
            "The Bichon Frise is a cheerful, small companion breed with a distinctive fluffy white coat and a naturally gentle disposition. "
            "Bred as a lap dog and performer, Bichons are sociable, playful, and remarkably adaptable to different living situations. "
            "They are a popular choice for allergy sufferers due to their low-shedding coat, though regular professional grooming is essential."
        ),
        "pros": [
            "Low-shedding coat, suitable for mild allergy sufferers",
            "Friendly and sociable with people and other pets",
            "Adaptable to apartment living",
            "Playful and easy to train",
        ],
        "cons": [
            "Requires frequent professional grooming",
            "Can be prone to separation anxiety",
            "May be difficult to housetrain",
            "Prone to certain health issues including allergies",
        ],
        "reviews": [
            (5, "The happiest little dog", "My Bichon Frise is the embodiment of joy. She wakes up every single morning as if it is the best day of her life. She greets every person she meets with genuine delight and has never met a stranger. She adapts perfectly to our apartment and gets all the exercise she needs from walks and indoor play. Her grooming appointments are every six weeks and she sits perfectly still for the groomer. A truly special little dog."),
            (4, "Perfect for allergy households", "My husband is allergic to most dogs but our Bichon barely triggers him. She does not shed visibly and we vacuum much less than friends with other breeds. The grooming costs add up, around sixty dollars every six weeks, but it is worth it for a dog that fits our household so perfectly. She is affectionate, smart, and entertaining. House training took three months with a crate but she is now reliable."),
            (5, "My mother's perfect companion", "We got a Bichon Frise for my elderly mother who lives alone and the results have been transformative. The dog gives her a reason to get up, go outside, and engage with the neighbourhood. Neighbours stop to chat during walks and she has made more friends in six months than in the previous year. The breed is gentle enough for an older person to handle and affectionate enough to provide real companionship."),
            (3, "Lovely dog but separation anxiety is real", "My Bichon is wonderful when I am home but she struggles significantly when I leave. We have worked with a behaviourist and done extensive crate training but she still howls for the first hour after I go to work. My downstairs neighbour has mentioned it. She is making progress but it is slow. If you work full time without a dog walker or sitter, factor this into your decision about the breed."),
            (5, "Joyful apartment dog", "I was nervous about getting a dog in my small city flat but my Bichon has been perfect. She plays energetically for twenty minutes then naps contentedly for hours. Two decent walks a day and she is fully satisfied. She is quiet, clean, and charming with visitors. Her bouncy white coat does require professional grooming every six weeks but the rest of her care is minimal. She has enriched my life enormously."),
            (4, "Clever and entertaining", "My Bichon has learned about thirty tricks and counts, picks out named toys, and understands a remarkable vocabulary. She is genuinely clever and loves having her mind engaged. Training sessions are her favourite part of the day. She can be stubborn about housetraining and regresses occasionally especially in winter when she dislikes the wet grass. Patience and consistency solved it eventually. A truly delightful little dog."),
            (5, "Best breed for our family", "We have two young children, a cat, and a Bichon Frise and the combination is perfect. She plays gently with the kids, ignores the cat completely, and adapts her energy level to whoever she is with at any given moment. She has never snapped or growled in three years. Her grooming is an additional expense but she brings so much happiness to our home that it barely registers."),
            (4, "Charming but needs company", "My Bichon absolutely must have company. She does poorly alone for more than a few hours and tells me about it loudly. We enrolled her in doggy daycare three days a week and the difference is remarkable. On daycare days she comes home tired and content. She is a sociable creature who genuinely needs interaction. Wonderful breed if your lifestyle accommodates that need."),
        ],
    },
    "Bloodhound": {
        "description": (
            "The Bloodhound is the quintessential scent hound, possessing the most acute sense of smell of any dog breed. "
            "Originally bred for tracking deer and boar, today Bloodhounds are famous for man-trailing work with law enforcement. "
            "Despite their serious working abilities, they are gentle, affectionate, and famously stubborn companions at home."
        ),
        "pros": [
            "Gentle, patient, and affectionate with family",
            "Extraordinary scenting ability and stamina on trail",
            "Good with children due to tolerant nature",
            "Rarely aggressive",
        ],
        "cons": [
            "Extremely stubborn and single-minded when on a scent",
            "Heavy drooling and ear odour require regular maintenance",
            "Loud, deep baying carries far",
            "Prone to bloat and joint issues",
        ],
        "reviews": [
            (5, "The most lovable wrinkled mess", "My Bloodhound is one hundred and ten pounds of wrinkled, drooling, baying love. He is the gentlest creature I have ever shared my life with. He has never once shown aggression to anyone or anything. He lies on the floor taking up the entire hallway and everyone has to step over him. His ears need cleaning twice a week and the drool is everywhere but in return I get the most affectionate, soulful companion imaginable."),
            (4, "Incredible nose, selective hearing", "I do volunteer search and rescue work with my Bloodhound and she is phenomenal at it. She has successfully trailed cold scents over twenty-four hours old across miles of varied terrain. At home she is completely different, slow, lazy, and absolutely obsessed with sleeping on the sofa. Her nose does not turn off though. She will follow a scent trail on walks regardless of what I want. You learn to build extra time into every outing."),
            (3, "Wonderful dog, significant maintenance", "My Bloodhound is a sweetheart but nobody warned me about the drool. It is everywhere. My walls, my ceiling, my guests. The ear smell requires diligent weekly cleaning or it becomes overwhelming. He bays loudly and my neighbours are not always charmed. He is wonderful with my family and endlessly patient with my kids. I love him completely but the upkeep is genuinely significant and worth knowing about upfront."),
            (5, "Gentle giant for our family", "We have three children and our Bloodhound has been absolutely perfect with all of them. She lets the youngest drag her around by the ears without complaint. She moves slowly, sniffs constantly, and occasionally launches into a bay that rattles the windows, but she is so fundamentally gentle and loving that every inconvenience is forgiven. She has a loose-jowled, mournful expression that makes everyone she meets smile."),
            (4, "Best nose in the business", "I got into tracking as a hobby specifically because of Bloodhounds and my experience has not disappointed. My boy has a nose that seems almost supernatural. He can pick up a footstep trail from hours earlier and follow it with unwavering certainty. Training him was mostly about keeping up with him rather than teaching him to track. His natural instinct is extraordinary. The challenge is everything else about owning a large, stubborn, drooly hound."),
            (5, "Changed how I think about dogs", "My Bloodhound is the most profoundly dog-like dog I have ever owned. He smells everything, follows every scent, bays at interesting discoveries, and sleeps deeply between adventures. He does not play fetch or do tricks or care about obedience for its own sake. He is purely himself and utterly authentic in everything he does. Living with him has made me appreciate the true nature of a working hound in a way no other breed has."),
            (4, "Lovable but needs a big yard", "My Bloodhound needs space to sniff and roam. We have half an acre and she uses every inch of it daily, nose to the ground in slow meditative circuits. She is calm and quiet inside but needs outdoor time to decompress and sniff. In our apartment during the first year she was restless and vocal. Since moving to our house she has been much more settled. A great breed for rural or suburban owners with space."),
            (3, "More challenging than expected", "The stubbornness of this breed cannot be overstated. My Bloodhound is not trainable in the traditional sense. He will sit and stay when he feels like it and ignore me completely when he does not. I have made peace with this because his personality is so wonderful that I do not really mind. But if you want a responsive, biddable companion you may want to look at another breed. If you want a lovable, funny, soulful character you will love a Bloodhound."),
        ],
    },
    "Boston Terrier": {
        "description": (
            "The Boston Terrier is a compact, well-mannered American breed with a tuxedo-like coat and an expressive, round-eyed face. "
            "Known as the American Gentleman, Bostons are friendly, intelligent, and enthusiastically playful while adapting well to both city apartments and family homes. "
            "They are sensitive to their owners' emotions and respond well to positive reinforcement training."
        ),
        "pros": [
            "Compact and well-suited to apartment living",
            "Friendly and gentle with children and seniors",
            "Low grooming maintenance",
            "Intelligent and responsive to training",
        ],
        "cons": [
            "Brachycephalic, prone to breathing issues in heat",
            "Can be gassy and snore loudly",
            "Eye injuries possible due to prominent eyes",
            "Some individuals can be stubborn",
        ],
        "reviews": [
            (5, "The American Gentleman lives up to his name", "My Boston Terrier is quite simply the most charming dog I have ever owned. He is perfectly sized for my apartment, is friendly to everyone without being overwhelming, and has manners that put many humans to shame. He learned his training commands quickly and performs them reliably. His snoring is Olympic-level and sometimes wakes me up, but I have come to find it oddly comforting. An excellent breed for city living."),
            (4, "Perfect city dog with minor caveats", "My Boston is my ideal companion for urban life. She is small enough to take everywhere, sociable enough that she makes friends on every outing, and calm enough that she is welcome in coffee shops and friends' homes. The breathing issues in summer heat are real and we have to limit midday exercise from June through August. She pants heavily and overheats quickly. With climate management she is perfectly healthy and happy."),
            (5, "Best dog for my lifestyle", "I work from home and my Boston Terrier has been the perfect companion for my routine. He stays near me while I work, goes on two walks a day enthusiastically, and spends evenings on my lap. He is not demanding or anxious, just content to be near me. His coat requires almost no brushing and he baths easily. The only sound he makes is snoring and occasional excited yodelling when I get his lead out."),
            (3, "Lovable but health issues are real", "My Boston has had two cherry eye surgeries and ongoing skin fold issues around her face. The vet bills have been significant. She is a lovely, affectionate dog with a wonderful personality but the brachycephalic health concerns are not trivial. Before getting this breed I would strongly recommend researching the specific health issues and budgeting accordingly. She is worth it for us but the costs surprised us."),
            (5, "Joyful and entertaining", "My Boston Terrier is genuinely the funniest dog I have ever known. He has elaborate ways of communicating what he wants, dramatic reactions to everything, and a sense of humour that seems almost deliberate. He makes everyone in the family laugh every single day. He is gentle with my elderly mother, playful with my kids, and calm with me when I need quiet. He somehow calibrates himself to whoever he is with."),
            (4, "Great with seniors and kids alike", "My seventy-year-old mother visits every week and my Boston is the highlight of her visit. He sits next to her on the sofa, lets her pet him for hours, and seems to sense her need for gentle company. With my eight-year-old son he is completely different, bouncy and playful and ready to run around the garden. His adaptability to different people and contexts is remarkable for such a small dog."),
            (4, "Smart and trainable", "My Boston learned forty commands in his first year and remembers every single one. He is sharp, attentive, and genuinely enjoys training sessions. The only challenge is he can be stubborn about things he finds unpleasant, like having his nails trimmed or going out in the rain. Once he decides he does not want to do something, the negotiation is real. But for everything he is willing to do, he is brilliant."),
            (5, "My heart dog", "I have owned many breeds over the years and my Boston Terrier has claimed a place in my heart that none of the others quite managed. He is present with me in a way that is hard to describe. He watches my face constantly, responds to my tone of voice, and seems genuinely invested in my wellbeing. When I am sad he climbs into my lap and stays there. When I am happy he dances. He is my favourite dog I have ever had."),
        ],
    },
    "Bull Terrier": {
        "description": (
            "The Bull Terrier is a distinctive breed known for its unique egg-shaped head and muscular, athletic body. "
            "Originally bred for fighting, modern Bull Terriers are comical, mischievous, and intensely devoted to their families. "
            "They have a clownish personality and need firm, consistent training to channel their considerable energy and stubbornness."
        ),
        "pros": [
            "Deeply devoted and entertaining family companion",
            "Short, easy-care coat",
            "Tough and robust, rarely suffers minor ailments",
            "Playful and entertaining personality",
        ],
        "cons": [
            "Can be stubborn and difficult to train",
            "Dog aggression possible without careful socialisation",
            "High energy requires regular exercise",
            "Breed-specific legislation in some areas",
        ],
        "reviews": [
            (5, "The clown prince of dogs", "My Bull Terrier is the most entertaining animal I have ever shared a home with. He spins in circles when excited, carries his toy everywhere as a greeting gift, and has worked out how to open the treat cupboard. He is muscular and powerful but uses all that mass for cuddles rather than intimidation. He is not the easiest dog to train because he finds rules amusing rather than binding, but he is completely devoted to me and the family."),
            (4, "Loyal and funny, needs firm handling", "My Bully is stubborn as a rock when she has decided something. Training sessions are a negotiation and patience is essential. But she is so fundamentally devoted and funny that I find it hard to stay frustrated. She has never been aggressive to people but she has a short fuse with other dogs and needs careful management on walks. With a patient owner who finds her personality entertaining rather than frustrating she is wonderful."),
            (5, "Best dog for an active single person", "I run every morning and my Bull Terrier keeps pace with me for the first three miles before he starts looking at me reproachfully. He is compact, muscular, and incredibly energetic. At home he cycles between intense play and deep sleep with very little in between. He does not cuddle conventionally but he must always be touching me, pressing against my legs or sleeping across my feet. A unique and wonderful breed."),
            (3, "Challenging first year", "I underestimated how much work a Bull Terrier puppy would be. He was mouthy, destructive, and seemingly impossible to tire out. We went through a professional trainer and it helped enormously. By eighteen months he had settled significantly. He is now a manageable, affectionate adult. But the puppy phase was genuinely one of the hardest things I have done. If you are considering this breed, be prepared for an intense first year."),
            (5, "My daughter's best friend", "Our Bull Terrier is ten years old now and has been my daughter's companion since she was born. He tolerates everything a child can throw at a dog with patience and good humour. He has never snapped at her even once. He is robust enough to handle rough play and gentle enough to sense when she is upset. His energy has slowed with age but his devotion has never wavered. We could not have chosen a better family dog."),
            (4, "Unique and unforgettable", "There is no other breed like a Bull Terrier. The triangular eyes, the egg head, the rolling bulldozing walk. My girl turns heads everywhere we go. She is tough and comical and absolutely sure she is in charge. She is not in charge but I allow her the illusion to keep the peace. She is excellent with my kids, so-so with other dogs, and completely unreasonable about the cat. A big personality in a medium-sized package."),
            (4, "Athletic and powerful", "My Bull Terrier excels at weight pulling and dock diving. He is powerful, athletic, and has enormous drive when engaged in something physical. His obedience is fair at best but his enthusiasm for physical challenges is extraordinary. He needs significant daily exercise or he becomes restless and destructive. For an active owner who enjoys physical activities with their dog he is a fantastic companion."),
            (3, "Breed not for everyone", "I love my Bull Terrier but I want to be honest for potential owners. He has been involved in two incidents with other dogs in three years despite my best socialization efforts. He is wonderful with people including children but his dog tolerance is genuinely limited. We manage it carefully and he is now on a protocol that keeps everyone safe. If you have other dogs or frequent dog-park visits this breed may not be the best fit."),
        ],
    },
    "Cane Corso": {
        "description": (
            "The Cane Corso is a large Italian mastiff with a noble and imposing presence, historically used as a guardian of property and livestock. "
            "Deeply loyal and protective of family, they are intelligent and trainable with experienced owners who provide firm, consistent leadership. "
            "They are not recommended for inexperienced owners and require early, thorough socialisation from puppyhood."
        ),
        "pros": [
            "Outstanding natural guardian instincts",
            "Deeply loyal and devoted to family",
            "Intelligent and trainable for experienced owners",
            "Calm and majestic indoors",
        ],
        "cons": [
            "Requires an experienced, confident owner",
            "Powerful enough to cause serious harm without proper control",
            "Not suitable for small living spaces",
            "Significant drooling from some lines",
        ],
        "reviews": [
            (5, "The ultimate family guardian", "My Cane Corso is the most impressive dog I have ever owned. He is one hundred and thirty pounds of calm, measured power. He does not bark unnecessarily, does not react impulsively, and never does anything without purpose. With my family he is soft and gentle, following the children around and lying near them while they sleep. When a stranger behaves oddly near us on a walk he simply moves between us and them without a sound. Truly extraordinary."),
            (4, "Magnificent breed, massive responsibility", "I want to be honest with anyone considering a Corso. This is not a dog for the faint-hearted. My girl is wonderful in the right hands but the wrong hands would be dangerous with a dog this powerful. I did two years of obedience work, socialization classes, and worked with a specialist trainer before I felt confident managing her in all situations. The investment was worth it but it was significant. She is now my most reliable, obedient dog."),
            (5, "Noble and loyal beyond compare", "My Cane Corso watches over my family with a quiet intensity that I find deeply comforting. He has never been aggressive inappropriately but there is no mistaking his protective intent. He is intelligent enough to distinguish genuine threats from normal visitors and responds accordingly. He is affectionate with family in a reserved, dignified way, not a lap dog but always present and attentive. An exceptional breed for the right owner."),
            (3, "Beautiful but overwhelming", "I got my Cane Corso thinking my previous dog experience with large breeds would translate. It did not fully. He tested my authority constantly for the first eighteen months and a professional trainer was essential. He is now reliable but it required more work than I anticipated. He is a wonderful dog but the combination of size, power, and dominant temperament means this breed demands genuine expertise. Be honest with yourself about your experience level."),
            (5, "Best decision for our acreage", "We have five acres and my Cane Corso has taken ownership of every square inch of it. He patrols regularly, investigates disturbances, and has deterred multiple would-be trespassers just by appearing at the fence. He is completely calm and friendly once we introduce someone as a welcome guest. With our family he is a devoted, gentle companion. His size and presence are everything we needed for our rural property."),
            (4, "Intelligent and obedient with proper training", "My Corso took to training faster than any dog I have previously owned. He is sharp, focused, and genuinely wants to please once he respects you. Earning that respect takes time and consistency but once established the bond is remarkable. He performs all commands reliably in distracting environments. The challenge is his sheer physical power. He needs to be trained to walk politely because if he decides to pull you are going with him."),
            (5, "Gentle giant with my family", "My children were eight and five when we got our Cane Corso puppy. Watching them grow up together has been one of the great joys of my life. He is enormous and my kids are still small but he calibrates his movements perfectly around them, moves slowly, and lies down to be at their level. He is protective without being aggressive and shows tremendous patience. He is three now and about one hundred and twenty pounds of gentle devotion."),
            (4, "Serious breed for serious owners", "I have owned Rottweilers and Dobermans previously and the Cane Corso is in a different league of commitment required. He needs daily training maintenance, not just as a puppy but always. He needs significant socialization. He needs an owner who projects calm confidence. When all of that comes together, he is a breathtaking animal to live with. Majestic, loyal, intelligent, and deeply bonded. Worth every ounce of effort for the right person."),
        ],
    },
    "Cocker Spaniel": {
        "description": (
            "The Cocker Spaniel is a beautiful and merry sporting breed known for its luxurious, silky coat and expressive dark eyes. "
            "Originally bred to hunt woodcock, today Cockers are cherished family companions who are equally at home in the field or on the sofa. "
            "They are gentle, eager to please, and respond beautifully to kind, positive training methods."
        ),
        "pros": [
            "Gentle, affectionate, and excellent with children",
            "Eager to please and highly trainable",
            "Adaptable to various living situations",
            "Enthusiastic and fun-loving personality",
        ],
        "cons": [
            "Coat requires frequent brushing and regular grooming",
            "Ears prone to infections requiring routine cleaning",
            "Can be sensitive and does not respond well to harsh handling",
            "Some lines prone to rage syndrome (rare but documented)",
        ],
        "reviews": [
            (5, "The most loving dog imaginable", "My Cocker Spaniel is the gentlest, most loving creature I have ever known. She is soft in every sense of the word, physically with her silky fur, and emotionally with her sensitivity to my moods. She senses when I am sad before I even know it myself and climbs into my lap immediately. She is patient with children, friendly with every dog she meets, and enthusiastic about everything from walks to cuddles. An absolutely wonderful breed."),
            (4, "Beautiful dog, significant grooming", "My Cocker is stunning but maintaining his coat is a serious commitment. He needs brushing every day to prevent matting and professional grooming every six to eight weeks. His ears need cleaning twice a week. He has had two ear infections despite my diligence. The grooming costs and time are real considerations. That said, his personality is so wonderful that I cannot imagine being without him. Just budget the grooming costs before you commit."),
            (5, "Perfect family dog", "We have three children and our Cocker Spaniel is the heart of our family. She plays tirelessly with the kids in the garden, comes on hiking trips with us, and spends evenings curled between whoever needs company most. She has never once shown anything other than gentleness and patience. She learned commands quickly and performs them reliably. The only real work is her coat. Well worth the grooming appointments."),
            (3, "Beautiful but anxiety-prone", "My Cocker is lovely but she struggles with anxiety that we have been working on for two years. She hates being alone for more than a couple of hours and can become destructive. We have used a behaviourist, anti-anxiety supplements, and careful management and she is much better now. I think she would have benefited from a more experienced owner from the start. For a patient, home-based owner she is wonderful. Less so for someone who is out a lot."),
            (5, "My son's devoted companion", "My son has autism and our Cocker Spaniel has been transformative for him. She is patient, soft, and seems to intuitively understand his needs. She sits with him during difficult moments and her presence calms him more effectively than any intervention we have tried. She is gentle enough that he can approach her on his own terms and affectionate enough to always meet him halfway. She has changed our family's life."),
            (4, "Sporty and energetic", "Most people think of Cockers as lap dogs but mine is an athlete. He runs, swims, and retrieves with total enthusiasm. We do gundog training together and his natural instincts are excellent. He has more stamina than I expected and loves being outdoors. At home he is calm and cuddly, which is the ideal combination. His coat takes effort but a professional trim keeps it manageable between sessions."),
            (5, "The perfect companion for a quiet life", "My children have grown up and I live alone with my Cocker Spaniel. She is the ideal companion for my quieter lifestyle. She is content with two moderate walks a day, loves sitting in the garden with me, and spends evenings at my feet. She is easy to take to cafes, friends' houses, and on weekends away. Her temperament is perfectly calibrated for a calmer household. I am completely devoted to her."),
            (4, "Highly trainable and responsive", "My Cocker Spaniel competed in obedience trials and achieved excellent scores. She is attentive, responsive, and genuinely loves the engagement of training. She learned complex sequences quickly and performs them with enthusiasm. Her sensitivity means she needs positive methods exclusively, raise your voice and she shuts down completely. With patience and positive reinforcement she is one of the most trainable dogs I have ever worked with."),
        ],
    },
    "Dalmatian": {
        "description": (
            "The Dalmatian is an instantly recognisable spotted breed with a history as a carriage dog, firehouse mascot, and circus performer. "
            "Athletic, energetic, and intelligent, Dalmatians thrive with active owners who can provide substantial daily exercise and consistent training. "
            "They are dignified and reserved with strangers but intensely devoted and playful with their own families."
        ),
        "pros": [
            "Athletic and tireless exercise companion",
            "Striking appearance with unique spotted coat",
            "Devoted and loyal to family",
            "Low-odour, relatively clean coat",
        ],
        "cons": [
            "High energy requires significant daily exercise",
            "Can be stubborn and independent",
            "Predisposition to deafness and urinary stones",
            "Shedding of white hairs is constant and sticks to fabric",
        ],
        "reviews": [
            (5, "The most athletic dog I have ever owned", "My Dalmatian runs alongside my bicycle for fifteen miles without showing fatigue. He is extraordinary physically, lean, fast, and seemingly inexhaustible. He is devoted to me and to my family, reserved at first with strangers but warm once he has assessed them. His shedding is impressive and constant. White hairs get into everything. But his personality and athleticism more than justify the extra vacuuming. A wonderful breed for active people."),
            (4, "Beautiful and energetic", "My Dal is stunning to look at and exhausting to own in the best possible way. She needs at least ninety minutes of vigorous exercise every day. When she gets it she is calm, affectionate, and well-behaved at home. When she does not she finds her own entertainment which is rarely appreciated. She is smart and learned commands quickly but she has an independent streak that keeps training interesting. Brilliant breed for an active lifestyle."),
            (3, "Underestimated the exercise requirement", "My Dalmatian is wonderful but I did not fully appreciate how much exercise this breed truly needs. I am relatively active but she needs more than I can consistently provide. On high-exercise days she is perfect. On lower-exercise days she is restless and destructive. We now have a dog walker three days a week which helps. If you work full time and are moderately active rather than highly active, be honest about whether you can meet this breed's needs."),
            (5, "My running partner for six years", "I have trained for three marathons with my Dalmatian running beside me. He has been the most extraordinary training partner, consistent, enthusiastic, and apparently never tired. He has made me a better runner. Off the trail he is dignified and calm, a completely different dog from the athlete on the road. He is devoted to my family and has been gentle and patient with my children. A truly magnificent breed."),
            (4, "Unique and captivating", "Everyone stops to admire my Dalmatian everywhere we go. Her spots are not evenly distributed and she has a large patch over one eye that gives her a piratical look. She is smart, independent, and can be a bit of a diva about things she dislikes. She flatly refuses to go out in heavy rain. But she is deeply affectionate with her family and makes every walk an event. The white fur on my furniture is eternal but so is my love for this breed."),
            (5, "Devoted family companion", "My Dalmatian has grown up with my three children and has been everything I could have wanted in a family dog. He is patient, playful, and enormously loyal. He sleeps outside my children's rooms at night, positioned like a guardian. He is reserved with people he does not know but never aggressive, just watchful. Once someone is welcomed into our home he accepts them completely. A noble and wonderful breed."),
            (4, "Health check essential before buying", "My Dalmatian is wonderful but I want to mention the health considerations. He has had two urinary stone incidents requiring dietary management, and one of his littermates was deaf from birth. These are documented breed issues and any reputable breeder will test for them. With appropriate care my boy is healthy and vital at six years old. Just do your homework and buy from a health-tested line."),
            (3, "Beautiful but not for first-timers", "My Dalmatian tested me more than any previous dog. She is intelligent enough to find every loophole in my rules and physical enough to get into any trouble she finds. Training required professional help and two years of daily work. She is now reliably obedient but it was a real commitment. She is a wonderful dog but in the wrong hands she could be chaos. First-time owners should consider a more forgiving breed."),
        ],
    },
}

_BREED_DATA_DOGS2: dict = {
    "English Springer Spaniel": {
        "description": (
            "The English Springer Spaniel is a medium-sized sporting breed celebrated for its boundless enthusiasm and versatility in the field. "
            "Springers are affectionate, eager to please, and thrive on both physical activity and close human companionship. "
            "They make excellent family dogs and are among the most responsive and trainable of all the spaniel breeds."
        ),
        "pros": [
            "Enthusiastic, affectionate, and great with children",
            "Highly trainable and eager to please",
            "Excellent sporting and working dog",
            "Adaptable to various living situations",
        ],
        "cons": [
            "High energy requires significant daily exercise",
            "Coat needs regular brushing and periodic professional grooming",
            "Can be over-excitable without proper training",
            "Ears prone to infection",
        ],
        "reviews": [
            (5, "The perfect active family dog", "My Springer has been with us for seven years and I genuinely cannot imagine our family without him. He runs with the children in the garden, comes on long hikes, and plays fetch until I give up before he does. Indoors he is calm and affectionate, curled up near whoever is in the room. He learned all his commands quickly and has never been aggressive. His tail seems to be in permanent motion. An absolute joy of a dog."),
            (4, "Brilliant gundog, enthusiastic pet", "I use my Springer for pheasant shooting in the season and she is extraordinary at it. Her nose, her style in cover, and her marking ability are all exceptional. Off-season she is a family pet who runs with my kids and sleeps at my feet. The transition between working dog and family companion is seamless. Her coat needs brushing every other day and a trim every couple of months but she is otherwise low maintenance."),
            (5, "Most loyal dog I have ever owned", "My Springer follows me everywhere in the house. He watches me while I work, waits outside the bathroom, and is at the door the moment I leave a room. He is not anxious about it, just genuinely devoted. He is soft with my elderly mother and gentle with the toddler next door who visits. His enthusiasm is sometimes overwhelming for smaller children but he tones it down quickly when corrected."),
            (3, "Needs much more exercise than I expected", "I knew Springers were active but mine exceeds all my expectations. He needs at least two hours of proper exercise every day or he is difficult indoors. On adequate-exercise days he is a perfect gentleman. On busy days when I cannot give him enough he chews, restless, and barks. I have had to completely restructure my day around his needs. Worth it but be honest with yourself about your lifestyle before choosing this breed."),
            (4, "Wonderful sport dog", "My Springer competes in agility and flyball and has excelled at both. He is fast, focused, and responds to training with infectious enthusiasm. His natural athleticism means he picks up physical tasks quickly and performs them with style. He can be a bit frenetic in new environments but settles fast once he has done a circuit and assessed the situation. A remarkable sporting dog and a warm companion."),
            (5, "Best breed for outdoor families", "We are a walking and camping family and our Springer is the perfect companion for our lifestyle. He has hiked mountains, swum in every river we have found, and crashed contentedly in tents and caravans without complaint. He adapts to any environment as long as we are with him. His joy at being outdoors is contagious and he has added an extra dimension of fun to every trip. Completely devoted and endlessly enthusiastic."),
            (4, "Smart and sensitive", "My Springer is perceptive in a way that surprised me. He reads my emotions accurately and adjusts accordingly. When I am stressed he comes and lies at my feet without being asked. When I am playful he matches my energy immediately. He is sensitive to tone and does not respond well to raised voices during training. Positive reinforcement gets incredible results with this breed. One of the most emotionally intelligent dogs I have had."),
            (3, "Ear maintenance is constant", "My Springer is wonderful but his ears have been a persistent challenge. He has had four ear infections in three years despite bi-weekly cleaning. The vet says his ear conformation makes him prone to it. We are managing it but the cost and effort are real. He is a fantastic dog in every other way and I love him completely. Just know that the ear care commitment is genuine for this breed."),
            (5, "Our family's heart", "My Springer came to us eight years ago as a rescue and transformed our family. He is gentle with my children, patient with my elderly father, and endlessly fun for everyone in between. He has been the subject of every family photo for eight years. He is greying around his muzzle now and slowing slightly but his tail still wags. He is the heart of our home and we are dreading the day we will have to say goodbye."),
        ],
    },
    "Great Dane": {
        "description": (
            "The Great Dane is the tallest of all dog breeds, known as the Apollo of Dogs for its majestic, elegant appearance. "
            "Despite their imposing size, Great Danes are gentle, friendly, and affectionate companions who are devoted to their families. "
            "They are calm indoors and require moderate exercise, making them surprisingly manageable for their size."
        ),
        "pros": [
            "Gentle, friendly giant with an affectionate nature",
            "Calm and quiet indoors",
            "Excellent with children despite size",
            "Moderate exercise requirements for their size",
        ],
        "cons": [
            "Short lifespan of 7-10 years typical for the breed",
            "Prone to bloat, a life-threatening condition",
            "Very large and can be clumsy indoors",
            "High food and veterinary costs due to size",
        ],
        "reviews": [
            (5, "The gentlest giant imaginable", "My Great Dane weighs one hundred and sixty pounds and believes he is a lap dog. He routinely attempts to sit on me on the sofa with apparent surprise when this creates difficulties. He is the softest, most gentle creature I have ever known. He has never knocked over my four-year-old despite being twice her height. He is calm, quiet, and deeply affectionate. The size costs are real but he is worth every penny."),
            (4, "Apollo of dogs deserves the title", "My Great Dane turns heads everywhere we go. She is breathtaking to look at, tall and elegant with a fluid gait. She is sweet-natured and friendly with everyone. The practical challenges of her size are real. Every hotel needs confirmation she is welcome, vet visits are expensive, and she knocked a lamp off a table by turning around. But she is so magnificent and gentle that the inconveniences are easily forgiven."),
            (5, "Best dog for a calm household", "People assume Great Danes need enormous amounts of exercise. Mine is perfectly satisfied with two moderate walks a day. He is calm, dignified, and surprisingly quiet in the house. He follows me from room to room, parks himself with a thud on the floor near me, and sighs contentedly. He greets visitors with a friendly wag of his enormous tail. He is the most low-key dog I have owned despite being the largest."),
            (3, "Heartbreaking lifespan", "I have to mention this honestly. My Great Dane was the most wonderful dog I have ever loved and we lost him at eight years old. He was relatively young but the breed simply does not live as long as smaller dogs. The love is immense but so is the grief that comes sooner than you expect. If you can accept the shorter partnership, the years you have with a Dane are extraordinary. Just go in with eyes open about this reality."),
            (5, "Perfect gentle giant for families", "We have two young children and a Great Dane and the combination is wonderful. She moves carefully around them despite her size and has never once knocked them over. She lets them use her as a pillow and accepts their attentions with patient grace. She is a remarkable animal and our children are learning a great deal about responsibility and kindness by caring for her. She has made our family life richer in every way."),
            (4, "Impressive and calm apartment dog", "I live in a large apartment and my Great Dane is honestly better suited to it than many smaller, more energetic breeds I have seen. She is quiet, does not bark excessively, and after two good walks she is content to rest. She takes up approximately half the sofa but that is a sacrifice I make willingly. My neighbours love her. She has been a remarkable ambassador for her breed in an urban setting."),
            (5, "Noble and devoted companion", "My Dane follows me everywhere with quiet dignity. He is not boisterous or demanding, just quietly present and deeply loyal. He notices when I am unwell and lies closer than usual. He greets my children when they come home from school with enormous wagging enthusiasm that threatens to clear the coffee table. He is the most charismatic dog I have ever owned and the house feels different when he is not in it."),
            (4, "Worth the extra investment", "Everything about a Great Dane costs more. Food, vet visits, beds, leads, collars, boarding. The costs are genuinely significant. I budget about twice what I would for a medium dog. But my Dane gives me something no other dog has. A presence that is both comforting and impressive. She is magnificent and I am so glad I did not let the costs deter me. Just plan for them honestly before you bring one home."),
        ],
    },
    "Great Pyrenees": {
        "description": (
            "The Great Pyrenees is a majestic, white mountain dog originally bred to guard livestock from wolves and bears in the Pyrenean mountains. "
            "Calm and patient with family, they are independent thinkers who take their guarding role seriously, often patrolling and barking at night. "
            "They are devoted companions but require patient, experienced owners who understand the breed's independent nature."
        ),
        "pros": [
            "Calm and patient with children and family",
            "Natural guardian instincts for home and livestock",
            "Tolerant of cold weather",
            "Gentle and nurturing nature",
        ],
        "cons": [
            "Tends to bark, especially at night",
            "Independent and can be difficult to train",
            "Heavy shedding twice a year",
            "Needs space and secure fencing due to roaming instinct",
        ],
        "reviews": [
            (5, "The most majestic dog I have ever owned", "My Great Pyrenees is like living with a magnificent white bear. She is enormous, calm, and deeply gentle with my family. She has bonded with our sheep and guards them with quiet vigilance. She rarely barks inappropriately but when she does it resonates. She is patient and loving with my children, seeming to understand they are part of her flock. The shedding is epic but brushing her is almost meditative. Truly a special breed."),
            (4, "Night barking requires management", "My Pyr is wonderful in almost every way but the barking is a real consideration. He patrols at night and barks at things that I cannot identify. We live in a rural area so the neighbours are distant but in a suburban setting this would be a serious problem. He is an independent thinker who does not take orders so much as consider them. With a flock to guard he is purposeful and brilliant. As a pure pet he needs a patient owner."),
            (5, "Ideal livestock guardian dog", "I have thirty sheep and my Great Pyrenees has bonded with them completely. She sleeps with the flock, patrols the perimeter, and has deterred at least one fox attack that I saw evidence of without loss of animals. She is calm and confident, never frantic, and the sheep seem to find her presence reassuring. She is also wonderful with my children who grew up alongside her. A working breed in the best possible sense."),
            (3, "Beautiful but not a companion dog", "I got my Pyr hoping for a large, affectionate companion. He is affectionate but on his terms and schedule. He is not interested in training, not interested in fetching, and not particularly interested in pleasing me. He does what he wants when he wants and views my directions as input rather than instruction. He is gentle and calm but he is fundamentally a working dog without a job and I think he would be much happier guarding livestock than living as my pet."),
            (5, "Gentle and nurturing with everyone", "My Great Pyrenees seems to view every living thing as under her protection. She is patient with cats, gentle with children, and even tolerant with the elderly rescue dog we adopted. She has never shown aggression to anything. She is calm, slow-moving, and infinitely patient. She is the most serene animal I have ever shared a home with. Her shedding fills a bag a week and she is entirely worth every hair."),
            (4, "Magnificent but needs a job", "My Pyr settled significantly once we got goats for him to guard. Before the goats he was restless and vocal and I felt he was frustrated without purpose. Now he is calm, focused, and deeply fulfilled. If you are considering this breed without livestock I would suggest thinking carefully about what role he will play. Give him a flock or a purpose and he is magnificent. Without that he may struggle."),
            (4, "Great for cold climates", "I live in a northern climate with harsh winters and my Great Pyrenees thrives in conditions that kept my previous dog indoors. She rolls in snow with visible joy and seems impervious to cold. She is calmer in cool weather than in heat and her coat is perfectly designed for outdoor life. She requires brushing and matting prevention in summer when she blows coat but otherwise her coat maintenance is straightforward."),
            (5, "The most devoted guardian", "My Pyrenees has become the unofficial guardian of our entire street. He knows every resident, acknowledges the regulars, and monitors strangers with quiet attention. He has never bitten or threatened anyone but his size and presence alone are enough to give any would-be troublemaker pause. He is soft and loving with those he knows. I have never felt safer in my home than with him."),
        ],
    },
    "Greyhound": {
        "description": (
            "The Greyhound is the fastest dog breed on earth, capable of reaching speeds of up to 45 miles per hour. "
            "Despite their athletic reputation, retired racing Greyhounds make surprisingly calm and affectionate house pets, often called the 40-mph couch potato. "
            "They are gentle, quiet, and low-maintenance companions who typically adapt very well to family life after the racing track."
        ),
        "pros": [
            "Calm and gentle indoor companion",
            "Low grooming requirements",
            "Quiet and rarely barks",
            "Affectionate and sensitive",
        ],
        "cons": [
            "High prey drive, unreliable off-leash near small animals",
            "Sensitive to cold due to low body fat",
            "Short bursts of speed require space to run safely",
            "Can develop separation anxiety",
        ],
        "reviews": [
            (5, "The forty-mph couch potato is real", "My retired Greyhound sleeps eighteen hours a day and runs like the wind for the other six. He is the most serene and gentle dog I have ever shared a home with. He never barks, rarely causes trouble, and requires minimal grooming. He adapted to home life within a week of leaving the track. He is sensitive and affectionate, resting his long head on my lap in the evenings. An extraordinary surprise of a breed for home life."),
            (4, "Best kept secret of the dog world", "I adopted my Greyhound on a whim and it changed my view of dog ownership. She is calm, quiet, and completely undemanding. She gets a forty-five minute walk in the morning and a shorter one in the evening and then she sleeps for the rest of the day. She is affectionate without being clingy. Her prey drive is very high and I cannot trust her off-leash near cats but in every other respect she is the ideal low-maintenance pet."),
            (5, "Gentle and noble", "There is a dignity about Greyhounds that sets them apart. My girl carries herself with quiet grace and seems to observe the world with serene detachment. She is gentle with my elderly father and patient with children. She occasionally does a zoomie in the garden at breathtaking speed and then returns to the sofa as if nothing happened. She has enriched my life with very little demand in return. Truly a remarkable breed."),
            (3, "Cold weather challenges", "My Greyhound struggles terribly in autumn and winter. He shivers on walks, refuses to go out in rain, and has developed a strategy of standing at the back door and staring at me accusatorially until I carry him back inside. He needs a coat for temperatures below about ten degrees. If you live somewhere with mild winters this is a non-issue. In a colder climate budget for several good quality coats and manage your expectations about outdoor time."),
            (5, "Easiest dog I have ever owned", "My Greyhound is my fourth dog and by far the easiest. He does not chew, does not bark, does not require extensive grooming, and is happy with two walks a day. He is clean, quiet, and gentle. He has had zero accidents in the house from the first week. The prey drive around cats requires management but apart from that he requires very little. For a busy person who still wants canine companionship he is perfect."),
            (4, "Surprisingly affectionate", "People think Greyhounds are aloof athletes. Mine is the most openly affectionate dog I have owned. He leans against me constantly, requests neck scratches by nudging my hand, and expresses clear displeasure when I stop. He is sensitive to my moods and responds to them. His athleticism is real and breathtaking when he sprints but it is his gentleness and warmth that define daily life with him. An underrated breed as a companion."),
            (4, "Great for apartment living", "My Greyhound lives in a city apartment with me and is perfectly content. She gets a good run in the park twice a week and walks daily. On exercise days she sleeps even more deeply. The breed's calm indoor temperament makes them genuinely suitable for urban living despite their size. The one limitation is I cannot live in my building's communal garden because she has spotted and chased a cat through it once. Management, not elimination, of the issue."),
            (5, "Rescued a racer and gained a best friend", "I adopted my Greyhound from a racing rescue three years ago and he has been one of the great joys of my life. He arrived cautious and slightly bewildered by domestic life. Within a month he was sprawled on the sofa demanding belly rubs. He is a completely different animal from what people expect and I now champion this breed actively to everyone who asks. Adopt a retired racer. You will not regret it."),
        ],
    },
    "Havanese": {
        "description": (
            "The Havanese is the national dog of Cuba, a small companion breed with a silky, long coat and an irrepressibly cheerful personality. "
            "Sociable, intelligent, and easy to train, Havanese adapt readily to apartment living and are known for their ability to bond closely with people of all ages. "
            "They are sometimes described as velcro dogs due to their desire to be close to their humans at all times."
        ),
        "pros": [
            "Sociable and friendly with everyone",
            "Intelligent and easy to train",
            "Low-shedding, suitable for mild allergy households",
            "Adaptable to small living spaces",
        ],
        "cons": [
            "Separation anxiety common, needs company",
            "Long coat requires daily brushing or professional grooming",
            "Can be prone to anxiety if under-socialised",
            "Small and delicate, can be injured by rough handling",
        ],
        "reviews": [
            (5, "The happiest little dog alive", "My Havanese greets every morning like it is the best day of his life. He bounces into each room ahead of me, checks everything is in order, and then returns to report back with a wagging tail. He is friendly with every human and dog he has ever encountered. He sits through grooming appointments with patience, learns new tricks in minutes, and spends evenings doing his best to occupy as much of my lap as possible for a seven-pound dog."),
            (4, "Perfect city companion", "I live alone in a city flat and my Havanese is my ideal companion. She is small enough to take anywhere, sociable enough to make every outing social, and calm enough to be welcome wherever we go. She needs a professional groom every eight weeks and daily brushing but the coat is beautiful. She is my constant companion and the flat feels genuinely empty when she is at the groomer. A wonderful breed for solo city dwellers."),
            (5, "Brilliant therapy dog temperament", "My Havanese visits my mother's care home twice a week and her effect on the residents is remarkable. She approaches everyone with gentle friendliness, allows herself to be petted and fussed over for hours, and seems to genuinely enjoy the attention. She never reacts negatively to unfamiliar handling. The breed's sociability and small size make her ideal for this work. She has brought real joy to people who need it."),
            (3, "Velcro dog is a real phenomenon", "My Havanese cannot be alone. Not just struggles, genuinely cannot be alone for more than two hours without distress. We have worked with a behaviourist and she is better but it is ongoing work. When I am home she is the most delightful companion. The problem is I do sometimes need to leave. If you work from home or have a family member home most of the time this breed is perfect. For someone who is out daily it is genuinely challenging."),
            (5, "My daughter's devoted companion", "My teenage daughter has anxiety and her Havanese has been a genuine therapeutic benefit. He senses her anxiety, moves to her side, and sits quietly with her during difficult moments. He is calm when she needs calm, playful when she needs distraction. He has an emotional intelligence that surprises me daily. He has made her life measurably better and our whole family has fallen in love with him."),
            (4, "Easy to train and eager to please", "My Havanese has learned more tricks than any dog I have previously owned. She picks up new commands in two or three sessions and retains them perfectly. She is enthusiastically motivated by treats and praise. She can perform sequences of ten behaviours in order without error. Training her is a genuine pleasure because she is so engaged and enthusiastic. She makes me look like a better trainer than I am."),
            (5, "Best breed for a quiet home", "I retired last year and my Havanese has made the transition to a quieter pace of life wonderful. He adapts his energy to mine, is content with leisurely walks, and spends long afternoons with me in the garden without needing to be entertained. He is small enough to manage easily and gentle enough that my grandchildren can interact with him safely. He is the ideal companion for a calmer chapter of life."),
            (4, "Charming and sociable", "My Havanese is the social secretary of our building. She has introduced me to every neighbour we have. People stop us constantly on walks to meet her. She is patient and charming with everyone and seems to genuinely enjoy being the centre of attention. Her coat is high maintenance but she carries it beautifully. A wonderful, joyful little dog that brings real warmth to every interaction."),
        ],
    },
    "Irish Setter": {
        "description": (
            "The Irish Setter is a striking, mahogany-coated sporting breed known for its exuberant energy and playful, rollicking personality. "
            "Bred for hunting upland birds, Setters are athletic, joyful, and deeply affectionate with their families, though they retain a mischievous streak well into adulthood. "
            "They thrive with active owners who can channel their enthusiasm into sport, exercise, and training."
        ),
        "pros": [
            "Exuberant, affectionate, and full of joy",
            "Excellent sporting and hunting dog",
            "Sociable with people and other dogs",
            "Stunning mahogany coat",
        ],
        "cons": [
            "Extremely high energy, needs hours of exercise daily",
            "Can be slow to mature, acting like a puppy for years",
            "Coat requires regular brushing and occasional trimming",
            "Easily distracted, recall can be unreliable",
        ],
        "reviews": [
            (5, "Living with a four-legged firework", "My Irish Setter is two years old and still very much a puppy in spirit. She gallops everywhere, greets everyone with overwhelming enthusiasm, and has a laugh-out-loud quality that makes every day amusing. She has knocked over everything in my house at least once but does it with such obvious joy that staying cross is impossible. On long trail runs she is in her element. A gorgeous, ridiculous, absolutely wonderful dog."),
            (4, "Beautiful athlete, late bloomer", "My Setter did not properly settle until he was three. The first two and a half years were genuinely challenging. He was exuberant to the point of chaos, easily distracted, and impossible to tire out. Now at four he is still energetic but focused, responsive, and a truly wonderful companion. He is breathtaking to watch run across a field. His coat takes twenty minutes of brushing three times a week. Completely worth the effort."),
            (5, "The most joyful dog on earth", "I defy anyone to spend time with an Irish Setter and not smile. Mine approaches every moment of her life with pure, undiluted joy. She wakes up happy, goes to sleep happy, and everything in between is an adventure. She has an infectious quality that has actually improved my outlook on life. She needs a lot of exercise and patience during her long puppyhood but the reward is a companion of extraordinary warmth and spirit."),
            (3, "Too much dog for my lifestyle", "I made a mistake getting an Irish Setter. I am moderately active but not highly active and this breed needs a genuinely high-activity lifestyle. He is wonderful on the days I can give him what he needs. On normal days he is restless, vocal, and determined to find his own entertainment. He is not destructive in a malicious way, more exuberantly exploratory. For an ultra-active person he would be perfect. For me he was too much."),
            (5, "My hunting partner for eight years", "My Irish Setter has been hunting with me since his first season at eighteen months and his natural ability is extraordinary. He finds birds like a machine, holds his point steadily, and retrieves with a soft mouth. Between seasons he is a devoted family companion who runs with my kids and sleeps at the foot of my bed. He is eight now and showing no signs of slowing down. An absolutely magnificent dog."),
            (4, "Sociable and friendly with everyone", "My Setter has never met a person or dog she did not immediately love. She makes friends everywhere she goes and has the social energy of a well-liked party host. She is not the most obedient dog I have owned but her warmth and enthusiasm make her a joy to be around. She has brought several new friends into my life because people stop to chat and exchange numbers when they meet her. A genuine social asset."),
            (5, "Stunning and spirited", "Living with an Irish Setter is like living with a beautiful, friendly tornado. My girl is four now and the tornado has downgraded to a spirited breeze. She is obedient, affectionate, and a remarkable walking partner. Her coat catches sunlight in the most beautiful way when she runs through fields. I spend time on grooming but she is so gorgeous that I do not mind. She is the most beautiful dog I have ever owned and her personality matches her looks."),
            (4, "Wonderful once mature", "The key to enjoying an Irish Setter is patience during the long puppyhood. Mine was testing until age three. From three onward he has been an absolutely brilliant dog. He is responsive, affectionate, playful without being destructive, and a wonderful sporting companion. People who give up on the breed before maturity miss out on something special. The investment of the early years is rewarded richly by the dog that emerges."),
        ],
    },
    "Irish Wolfhound": {
        "description": (
            "The Irish Wolfhound is the tallest dog breed in the world, originally bred to hunt wolves and elk in ancient Ireland. "
            "Despite their formidable size and history, Wolfhounds are famously gentle, dignified, and sensitive companions. "
            "They are devoted to their families and surprisingly calm indoors, making them manageable despite their enormous stature."
        ),
        "pros": [
            "Gentle, patient, and sweet-natured with family",
            "Calm and dignified indoors",
            "Rarely aggressive",
            "Majestic presence and striking appearance",
        ],
        "cons": [
            "Short lifespan, typically 6-8 years",
            "Very high food and veterinary costs",
            "Prone to heart disease and bone cancer",
            "Needs space due to sheer physical size",
        ],
        "reviews": [
            (5, "Gentle giant beyond comparison", "My Irish Wolfhound is the most gentle, dignified animal I have ever had the privilege of living with. He stands taller than my kitchen counter and is so soft in temperament that the contrast is almost comical. He moves slowly and deliberately around the house, seems always aware of his size, and has never once knocked over a child or caused accidental damage. He is quiet, calm, and deeply loving. A true giant of a companion."),
            (4, "Extraordinary breed, heartbreaking brevity", "My Wolfhound lived to eight and those eight years were among the best of my life. He was magnificent, gentle, and deeply bonded to me. The brevity of the time we had together was genuinely painful. I would do it again without hesitation but I want anyone considering the breed to understand that the lifespan is genuinely short. You are entering a shorter contract than with most breeds. Make every year count."),
            (5, "My children's best friend", "My three children grew up with our Wolfhound and the experience has been beautiful. He was patient and gentle with them from puppyhood, letting them lean on him, sleep against him, and treat him like a large stuffed toy. He tolerated everything with serene good nature. He is seven now and my youngest, who is nine, has grown up knowing no different reality. He is a profound part of our family."),
            (3, "Not practical for everyone", "I love my Wolfhound but the practicalities of this breed are genuinely significant. He eats as much as a small pony. His vet visits cost substantially more. He needs a large vehicle. He cannot fit in most dog beds and has commandeered my sofa permanently. He is wonderful but I want potential owners to genuinely assess their living situation, vehicle size, and budget before committing to this breed."),
            (5, "The most noble companion", "There is a quality to an Irish Wolfhound that I can only describe as noble. My girl carries herself with a quiet dignity that commands attention without demanding it. She is present without being demanding, affectionate without being clingy, and protective without being aggressive. She watches over my home and family with ancient, unhurried intelligence. She is the most impressive animal I have ever shared my life with."),
            (4, "Calm and manageable despite the size", "People ask how I manage a dog this large in my house. The truth is he is easier than many smaller, more energetic breeds I have owned. He is calm, quiet, and not destructive. He sleeps a lot and is happy with two moderate walks a day. He does eat a lot and takes up significant space but his temperament is so easy that the practical challenges feel manageable. He is a wonderful gentle giant."),
            (5, "Every year with him is precious", "Knowing the lifespan of this breed made me more intentional about our time together than I might otherwise have been. My Wolfhound is five now and I am acutely aware of the years ahead. This awareness has made me a more present owner, more grateful for each walk and each evening together. He has taught me something about enjoying what you have. He is remarkable in every way."),
            (4, "Worth every practical challenge", "My Wolfhound is ten months old now and already the size of a small horse. He has been wonderfully easy to train, is gentle with my cats, and has integrated into our family effortlessly. The food cost is significant and I needed to upgrade my car. But looking at him now I cannot imagine our home without him. He is magnificent and the practical adjustments were completely worth making."),
        ],
    },
    "Jack Russell Terrier": {
        "description": (
            "The Jack Russell Terrier is a small but fearless working terrier originally developed for fox hunting in England. "
            "Tenacious, energetic, and full of personality, Jack Russells are intelligent and entertaining companions who think themselves considerably larger than they actually are. "
            "They need firm, consistent handling and plenty of mental and physical stimulation to prevent boredom-related mischief."
        ),
        "pros": [
            "Lively, entertaining, and full of character",
            "Intelligent and quick to learn",
            "Low grooming maintenance",
            "Robust health and long lifespan",
        ],
        "cons": [
            "Very high energy for their size",
            "Strong prey drive, unreliable off-leash",
            "Can be stubborn and opinionated",
            "Prone to excessive barking",
        ],
        "reviews": [
            (5, "Twelve pounds of pure chaos and joy", "My Jack Russell Terrier is the most entertaining animal I have ever owned. He has the energy of a dog five times his size, the confidence of a dog ten times his size, and the stubbornness of a dog that does not care about sizes at all. He has learned every command I have taught him and chooses to follow them selectively. He makes me laugh every single day. He is my little legend."),
            (4, "Tiny but magnificent", "My JRT is nine years old and still acts like a puppy. She runs, leaps, investigates, and demands engagement with an energy that puts younger dogs to shame. She is smart as a whip and has figured out how to open kitchen cabinets. She learned her commands quickly but applies them only when it suits her. She is a handful but she is also the funniest, most characterful companion I have ever had."),
            (5, "Best farm dog for small game", "I have a smallholding and my Jack Russell is indispensable. He has cleared my outbuildings of rats completely and does a daily patrol that keeps the mice population minimal. He works independently and effectively, exactly as the breed was designed. He comes inside in the evenings and is a calm, affectionate companion. The working dog and the house dog coexist seamlessly. A brilliant little terrier."),
            (3, "Needs more than I could give", "My Jack Russell was the most demanding dog I have owned despite being the smallest. His energy and need for stimulation exceeded what I could consistently provide. He became destructive when bored and loud when frustrated. We rehomed him to a family with children and land and he is thriving there. If you are a low-energy person in a small flat, please consider a calmer breed. The JRT needs space, stimulation, and an active lifestyle."),
            (5, "Fearless and funny", "There is no more entertaining dog on earth than a Jack Russell Terrier. Mine is convinced he can intimidate my neighbour's Rottweiler and I have to respectfully disagree each time they meet. He is bold, opinionated, and hilariously confident in himself. He is also surprisingly affectionate, curling up on my pillow at night and huffing indignantly if I disturb him. He has more personality than most people I know."),
            (4, "Long-lived and healthy", "My Jack Russell is fourteen years old and still going strong. He has slowed somewhat but he still wants a walk every day, still bosses the cat around, and still has opinions about everything. The longevity of this breed is remarkable. He has been my companion for fourteen years and I am hoping for a few more yet. Healthy, resilient, and characterful to the end."),
            (5, "The perfect character dog", "I have owned labs, retrievers, and spaniels and my Jack Russell has more personality than all of them combined. She is determined, clever, and completely unimpressed by commands she finds inconvenient. She has a way of looking at me when I ask her to do something she disagrees with that communicates volumes. She is also fiercely loyal, sleeps on my pillow, and treats my lap as her personal property. An absolute character."),
            (4, "Great with kids who match his energy", "My Jack Russell and my eight-year-old son are perfectly matched energy-wise. They run each other ragged in the garden for hours and both come inside equally exhausted. He is patient with my son within the context of play but he does not like being disturbed when he is napping and will growl a warning. We have taught my son to respect that boundary. For an active family with older children he is brilliant."),
        ],
    },
    "Maltese": {
        "description": (
            "The Maltese is an ancient toy breed with a flowing white coat and a lively, affectionate personality. "
            "One of the oldest companion dogs in history, Maltese have been bred exclusively for human companionship for millennia. "
            "They are playful, charming, and spirited despite their small size, and form intense bonds with their owners."
        ),
        "pros": [
            "Gentle, affectionate companion",
            "Low-shedding coat suitable for mild allergy sufferers",
            "Playful and entertaining",
            "Long lifespan for a small breed",
        ],
        "cons": [
            "Coat requires daily brushing or regular professional grooming",
            "Can be prone to separation anxiety",
            "May be difficult to housetrain",
            "Fragile, can be injured by rough play",
        ],
        "reviews": [
            (5, "Cloud of white fluff and pure love", "My Maltese is six years old and I am still completely besotted with her. She is a cloud of white fluff who demands love on her schedule and gives it back multiplied. She has a tiny body but an enormous personality and firm opinions about everything. She knows what time dinner should be, what time walks happen, and what time she should be in bed, and she will remind me loudly if the schedule is not maintained."),
            (4, "Beautiful breed, significant grooming", "My Maltese is stunning when properly groomed and requires regular professional attention to stay that way. We have him in a shorter puppy cut which is more practical than the full show coat. Even with the shorter style he needs brushing every other day. The grooming cost is real and ongoing. He is absolutely worth it for his personality and companionship but go in with eyes open about the commitment."),
            (5, "Perfect companion for my mother", "My seventy-eight-year-old mother has had my Maltese for two years and the transformation in her happiness has been remarkable. He is small enough for her to manage easily, gentle enough that she is comfortable with him, and affectionate enough to give her the daily joy of being truly needed. He gets her up every morning and out for a short walk. He has added measurably to her quality of life."),
            (3, "Separation anxiety is significant", "My Maltese cannot be alone without distress. She vocalises, she refuses to eat, and her anxiety is genuine and real. We have worked with a veterinary behaviourist and tried multiple medications and behaviour modification programmes. She is much improved but it has been an extended project. If you intend to be away from home regularly you need to plan very carefully for this breed's companionship needs."),
            (5, "Playful and feisty", "People think Maltese are delicate lap dogs. Mine is a feisty, playful, ridiculous little dog who runs rings around my larger dogs and bosses them comprehensively. She is fearless, confident, and knows exactly what she wants. She plays hard and then naps hard. She is affectionate on her terms and those terms are frequently. A wonderful little dog who refuses to behave in a stereotypically fragile manner."),
            (4, "Lively and intelligent", "My Maltese has learned more tricks than I expected from a breed with a reputation for stubbornness. With treats she is attentive and responsive. She has mastered about twenty commands and can perform them in sequence. She can also identify her toys by name and retrieve the correct one. She is smarter than she lets on most of the time. A genuinely clever companion who hides her intelligence behind a pretty face."),
            (5, "Long-lived and healthy", "My Maltese is thirteen years old and still bright-eyed and active. She has slowed down and sleeps more than she did at three but she is still engaged with life and with me. The longevity of this breed is one of its great gifts. We have had thirteen wonderful years together and I hope for more. She has been my companion through many life changes and I genuinely cannot imagine my daily life without her."),
            (4, "Great apartment dog", "My Maltese is perfectly suited to urban apartment living. She gets a good walk twice a day and is completely content otherwise. She does not bark excessively, is welcomed everywhere small dogs are permitted, and adapts to travel well. I have taken her on trains, to hotels, and to friends' homes without incident. She is a wonderfully portable companion who fits seamlessly into a busy city lifestyle."),
        ],
    },
    "Mastiff": {
        "description": (
            "The Mastiff is one of the heaviest dog breeds in the world, with males regularly exceeding two hundred pounds. "
            "Despite their formidable size, Mastiffs are gentle, good-natured, and dignified companions who are devoted to their families. "
            "They require relatively moderate exercise for their size but need early socialization to manage their natural protective instincts."
        ),
        "pros": [
            "Gentle, patient, and devoted to family",
            "Naturally protective without excessive aggression",
            "Calm and relatively low energy indoors",
            "Loyal and deeply bonded to their people",
        ],
        "cons": [
            "Heavy drooling from most individuals",
            "Short lifespan of 6-10 years",
            "Expensive to feed, house, and treat medically",
            "Prone to bloat, joint problems, and heart conditions",
        ],
        "reviews": [
            (5, "Two hundred pounds of pure love", "My Mastiff weighs two hundred and fifteen pounds and his only ambition is to sleep as close to me as physically possible. He somehow fits himself entirely onto the sofa and stares reproachfully when I suggest he move. He is gentle with my children, tolerant of the cat, and completely devoted to our family. The drool is legendary but so is his love. He is the most affectionate dog I have ever had the privilege of owning."),
            (4, "Noble guardian and family dog", "My Mastiff is both the most imposing and the most gentle dog I have ever owned. He is calm and quiet in the house, excellent with my children, and completely unflappable in any situation. His size alone deters any unwanted attention and he has never needed to be more than present to communicate his protective intent. He drools extensively and eats as much as a teenager. He is completely worth every cent."),
            (5, "Best family protector", "We live rurally and my Mastiff has been the most reassuring presence our family could have. He patrols the property each evening, acknowledges familiar faces, and treats unknown visitors to a measured but unmistakable inspection. He has never been aggressive but no one who meets him has any doubt about what would happen if our family were threatened. With us he is completely soft and loving."),
            (3, "Beautiful breed, difficult practicalities", "I love my Mastiff profoundly but I want honest information available. He eats twelve cups of food a day. His vet visits are expensive because everything is dosed by weight. He drools on my ceiling somehow. He needs a large vehicle and special pet insurance. He is not suitable for a small home. If you can genuinely accommodate all of this, the dog you get is extraordinary. But these are not trivial considerations."),
            (5, "Gentle giant with my children", "My children were four and six when we got our Mastiff puppy. He is now three and bigger than both of them. He has been gentle, patient, and protective of them from the beginning. He lies down when they approach to bring himself to their level. He lets them climb on him. He watches over them in the garden. He is the most devoted guardian I could have asked for and the gentlest companion my children have ever had."),
            (4, "Surprisingly trainable", "My Mastiff took to training faster than I expected. He is motivated by praise and a calm, consistent approach gets excellent results. His size means teaching loose-leash walking was a genuine priority and he responded well to it. He now walks beautifully beside me which is essential when you are managing two hundred pounds of dog. He is obedient and manageable with proper foundational training. Do not skip this step with this breed."),
            (5, "Every year is precious", "Knowing that large breeds live shorter lives made me intentional about my time with my Mastiff from day one. He is six now and healthy but I am aware the clock moves differently for big dogs. We have adventures, slow mornings, long cuddles, and I photograph him constantly. He has been the most magnificent companion. Whatever years we have left will be celebrated and savoured."),
            (4, "Calm and compatible with other pets", "My Mastiff lives with two cats and an elderly small dog and the coexistence is peaceful. He approaches the cats with slow, careful movements and they have gradually accepted him. He is gentle with the small dog and seems to understand the size difference. He has never showed predatory behaviour toward any of them. His calm temperament makes multi-pet living surprisingly workable with this giant breed."),
        ],
    },
    "Miniature Schnauzer": {
        "description": (
            "The Miniature Schnauzer is a sturdy, spirited terrier-type breed with a distinctive bearded face and a bold, curious personality. "
            "Originally a ratting dog on German farms, today Miniature Schnauzers are popular companions known for being affectionate, highly adaptable, and remarkably long-lived. "
            "They are loyal to their families, intelligent, and thrive with regular mental stimulation and exercise."
        ),
        "pros": [
            "Low-shedding, good for mild allergy households",
            "Intelligent, trainable, and eager to please",
            "Long-lived, typically 12-15 years",
            "Adaptable to various lifestyles and living situations",
        ],
        "cons": [
            "Can be prone to barking",
            "Requires regular professional grooming or hand-stripping",
            "Can be stubborn about training specifics",
            "Some individuals prone to pancreatitis",
        ],
        "reviews": [
            (5, "Perfect all-round companion", "My Miniature Schnauzer is now eleven and I cannot imagine a better companion. He adapted to our flat perfectly when we downsized, he is low-shedding which suits my allergies, and he has been healthy and robust throughout his life. He learned a huge vocabulary of commands and toys by name. He is opinionated and tells me when he disagrees with something via a particular pointed stare. Brilliant, long-lived, and wonderful."),
            (4, "Spirited and smart", "My Mini Schnauzer is the nosiest dog I have ever owned. She must investigate everything, greet everyone, and be involved in every activity. She has a confident, forward personality that is entertaining if occasionally exhausting. She learned her training commands quickly but adds her own editorial to them. She is affectionate, lively, and makes every day more interesting. Her beard needs regular attention and she gets professional grooming every eight weeks."),
            (5, "Ideal for allergic households", "My son is allergic to most dogs. My Miniature Schnauzer is the only dog that does not trigger his allergies. We tested carefully before committing and he has been fine for three years. She is also the most adaptable dog I have owned, happy in the car, at hotels, at friends' houses, and in our flat. She is confident without being aggressive and affectionate without being clingy. A genuinely brilliant breed."),
            (3, "Barking needs management", "My Schnauzer is wonderful in most respects but the barking required significant work. He barks at the door, at the television, at unusual sounds, and at things only he can perceive. We did a full training programme focused on bark control and he is much better now but it was a real project. If you live in an apartment with close neighbours this is an important consideration before choosing this breed."),
            (5, "Loyal beyond measure", "My Schnauzer has been my companion through a divorce, a house move, and two job changes. She has been a consistent, grounding presence through significant upheaval. She watches me constantly, responds to my moods, and presses close when she senses I need it. She is healthy at nine, still bright and energetic, and the thought of life without her is genuinely sad. She has been one of the great constants of my adult life."),
            (4, "Excellent watchdog without being excessive", "My Schnauzer alerts me to anything unusual at the perimeter with two sharp barks and then waits for my response. If I go to investigate and find it benign he stops. He does not bark endlessly like some small dogs. He has a purpose to his alerting that seems intelligent and measured. He has deterred one attempted break-in and alerted me to a pipe leak. His watchdog instincts are genuinely useful."),
            (5, "Most trainable small breed I have owned", "I have had terriers before and the Miniature Schnauzer is by far the most responsive I have encountered. My girl picks up new commands quickly, retains them reliably, and performs them with enthusiasm. She completed advanced obedience training with excellent scores. She loves the engagement of training sessions and clearly finds them stimulating. An excellent little dog for someone who enjoys working with a responsive, intelligent companion."),
            (4, "Long-lived and healthy", "My Miniature Schnauzer is thirteen years old and still insists on his walks, still wants his training sessions, and still argues with me about bedtime. The longevity of this breed is genuinely remarkable. He has slowed down but his mind is sharp and his personality unchanged. He has been my companion through thirteen years and I am hoping for more. A robust, long-lived breed that gives you exceptional value in years of companionship."),
        ],
    },
    "Newfoundland": {
        "description": (
            "The Newfoundland is a giant, bear-like dog originally bred by Canadian fishermen for water rescue and hauling nets. "
            "Famous for their sweet temperament, exceptional swimming ability, and gentle nature with children, Newfoundlands are known as nanny dogs. "
            "They are devoted, patient, and calm, though their size, coat, and drooling tendencies require significant management."
        ),
        "pros": [
            "Extraordinarily gentle and patient with children",
            "Naturally gifted swimmer and water rescuer",
            "Calm, sweet-tempered companion",
            "Deeply devoted to family",
        ],
        "cons": [
            "Very heavy shedding and significant drooling",
            "Prone to joint issues and heart conditions",
            "High food, grooming, and veterinary costs",
            "Prone to overheating in warm climates",
        ],
        "reviews": [
            (5, "The nanny dog earns its title", "My Newfoundland is one hundred and fifty pounds of devoted, patient, gentle love. My three children treat him like a piece of furniture, climbing on him, using him as a pillow, and dressing him in hats, and he accepts it all with serene good nature. He has never once shown even mild irritation with them. He is the most fundamentally good-natured dog I have ever owned. The drool is real and so is the hair but it is worth every bit of it."),
            (4, "Giant teddy bear in the best way", "My Newf is everything I hoped for. He is calm indoors, gentle with visitors, and patient to a degree that puts humans to shame. He does drool extensively and I keep drool cloths in every room. His coat requires brushing four times a week to prevent matting. He is expensive to feed and the vet bills are sized accordingly. But his temperament is extraordinary. I have never met a more fundamentally sweet dog."),
            (5, "Born to swim and save", "My Newfoundland discovered water at eight months old and has never looked back. He swims every chance he gets and his technique is natural and powerful. We have done water rescue training and his instinct to support a struggling person in water is remarkable. He circles swimmers, positions himself for them to hold, and pulls toward shore. It is an ancient instinct working beautifully. An extraordinary working ability in a wonderful companion."),
            (3, "Not suitable for warm climates", "I love my Newfoundland but I made a mistake buying him before I moved from Scotland to the south of France. He struggles terribly in the heat. We have air conditioning and limit outdoor time during summer but he is visibly uncomfortable from May to September. He thrives in winter. If you live somewhere warm I would seriously reconsider this breed. His welfare in hot weather is a real concern I did not anticipate."),
            (5, "Most patient dog I have ever known", "My Newfoundland is six years old and has never once in his life reacted badly to anything. My children's friends are occasionally rough with him when they visit without adequate parental supervision and he simply moves away slowly and quietly. He has endless patience for human shortcomings. He is the most steady, reliable, and fundamentally kind animal I have ever lived with. He has made my belief in the goodness of dogs absolute."),
            (4, "Perfect for active water families", "We spend summers near a lake and my Newf has been the family dog we always dreamed of for that lifestyle. He swims with the children, accompanies the canoes, and generally supervises all water activities with obvious pleasure. On land he is slower and prefers a calmer pace but the water brings out his best self. A great breed for families whose lifestyle includes water activities."),
            (5, "Gentle with my vulnerable family members", "We have an elderly grandmother with dementia and my Newfoundland interacts with her with a gentleness that seems almost deliberate. He does not jump, does not rush, and moves slowly when she is nearby. He seems to sense her vulnerability. He has been a therapeutic presence for her and brings her moments of calm recognition. He is a remarkable animal and I feel he was the right dog for our complicated family situation."),
            (4, "Worth every practical challenge", "The practical realities of a Newfoundland are significant. Hair everywhere, drool on walls and ceilings somehow, enormous food quantities, large vet bills. None of it matters when you look at that massive, fluffy face and those gentle eyes. He is the most wonderful dog. We have made all the practical accommodations without regret. For the right family with the right space and resources, there is no better companion."),
        ],
    },
    "Old English Sheepdog": {
        "description": (
            "The Old English Sheepdog is a large, shaggy herding breed with a distinctive rolling gait and a bear-like appearance. "
            "Playful, adaptable, and gentle, the OES is a devoted family dog known for its intelligence and comical personality. "
            "Their profuse double coat requires substantial grooming commitment, but their warm temperament makes them beloved companions."
        ),
        "pros": [
            "Gentle, playful, and good with children",
            "Adaptable and easy-going temperament",
            "Intelligent and trainable",
            "Devoted family companion",
        ],
        "cons": [
            "Extremely high grooming requirements",
            "Can be boisterous, especially as a puppy",
            "Prone to joint and eye issues",
            "Coat mats quickly without regular attention",
        ],
        "reviews": [
            (5, "A living teddy bear", "My Old English Sheepdog is the most exuberantly affectionate dog imaginable. He greets everyone who enters our home like a long-lost family member, bouncing and spinning and generally creating a furry storm of joy. He is wonderful with my children and genuinely funny in his interactions with everyone. The grooming is a major commitment. I spend an hour brushing him twice a week and he has a professional groom every eight weeks. Worth every minute."),
            (4, "Lovable and gentle, demanding coat", "My OES is everything I wanted in a family dog. She is gentle, playful, and patient with my three young children. She is smart and responsive to training. The coat is the single biggest challenge and it is significant. She mats quickly if I miss brushing sessions and the grooming cost over a year is substantial. I have considered a shorter cut for practicality but the full coat is so magnificent that I keep persevering."),
            (5, "The gentle giant clown", "My Old English Sheepdog combines the size of a bear, the grace of an enthusiastic toddler, and the humour of a natural comedian. He runs into things, trips over his own feet, and peers at me from behind his fringe with profound earnestness. He is completely devoted to my family and completely unaware of his own size. We have had to re-home several coffee table ornaments for their own safety. Best dog we have ever owned."),
            (3, "Beautiful breed but the grooming almost broke me", "I knew the OES needed grooming but nothing prepared me for the reality. My boy mats within three days of brushing if I am not diligent. I went through three brushes in the first year. He now has a shorter pet clip which is much more manageable but he still needs attention every week. His personality is wonderful and his temperament is everything you could want. Just go in fully prepared for the grooming commitment."),
            (5, "Perfect family dog", "Our Old English Sheepdog has grown up with our children from the time they were toddlers. He has been patient, gentle, and playful through every phase of their growing up. He is twelve now and the grey around his muzzle matches his coat and makes him even more distinguished. He has slowed down but his tail still wags when the children come home from school. A deeply beloved family member."),
            (4, "Smart and biddable", "My OES picked up his training commands quickly and performs them reliably. He is motivated by both treats and praise and genuinely seems to enjoy the engagement of working with me. He has participated in obedience classes, rally, and herding trials. His herding instinct is real and strong. He is not the easiest to train because he has opinions but he is fundamentally biddable and genuinely wants to work with you."),
            (5, "Joyful and warm-hearted", "There is no dog I have ever owned who expressed joy more fully than my Old English Sheepdog. She runs with her whole body, greets with her whole heart, and loves with her whole soul. She makes every person she meets feel special. She is warm and funny and endlessly entertaining. The grooming is real but it is also bonding time and I have come to value it. A magnificent companion for the right committed owner."),
            (4, "Great in rural settings", "My OES has found her ideal environment on our smallholding. She has space to run, things to investigate, and my children to supervise. She has a gentle herding instinct she applies to the children when they venture too far and it is endearing. She adapts her energy to the environment and is perfectly calm inside in the evenings. A great dog for a rural or suburban lifestyle with space."),
        ],
    },
    "Papillon": {
        "description": (
            "The Papillon is a small, elegant spaniel-type breed named for its distinctive butterfly-shaped ears. "
            "Despite their dainty appearance, Papillons are athletic, highly intelligent, and among the best performers in canine agility and obedience sports. "
            "They are affectionate and adaptable, equally at home as lap dogs or competitive sport dogs."
        ),
        "pros": [
            "Exceptionally intelligent and trainable",
            "Athletic and excels at dog sports",
            "Adaptable to apartment or house living",
            "Long-lived, typically 13-16 years",
        ],
        "cons": [
            "Can be prone to excessive barking",
            "High energy despite small size",
            "Can be prone to patellar luxation",
            "Coat requires regular brushing",
        ],
        "reviews": [
            (5, "Tiny athlete, enormous intelligence", "My Papillon is the smartest dog I have ever owned in any size category. She learns new commands in one or two sessions, remembers them indefinitely, and performs sequences of twenty behaviours without a mistake. We compete in agility and she wins against dogs three times her size. She is small enough to take everywhere and smart enough to be genuinely stimulating to train. The perfect companion for an engaged, active owner."),
            (4, "Most trainable small breed", "I have owned multiple small breeds and my Papillon is far and away the most responsive and trainable of all of them. He picks up training rapidly, performs reliably under distraction, and genuinely loves the mental engagement of working with me. He has competed successfully in obedience, rally, and nosework. His energy level is higher than I expected from a small dog but he is manageable with sufficient daily exercise and training."),
            (5, "Elegant and athletic", "My Papillon combines the elegance of a show dog with the drive of a working sport dog. She is beautiful, well-proportioned, and carries herself with natural grace. On the agility course she transforms into a focused athlete who flows over equipment with stunning precision. At home she is a lap dog who enjoys quiet evenings and calm company. She is the perfect balance of beauty and athletic ability."),
            (3, "The barking was a problem", "My Papillon is wonderful in many ways but she barks at everything. Sounds outside, movement, birds in the garden, things only she can detect. We live in an apartment and my neighbours eventually complained. We worked with a trainer and it improved but never fully resolved. If you live in close proximity to other people this is a genuine consideration before choosing this breed."),
            (5, "Fifteen years of wonderful companionship", "My Papillon lived to fifteen and was active and engaged until his final year. The longevity of this breed is one of its greatest gifts. I had fifteen wonderful years with the most intelligent, charming, and characterful dog I have ever known. He competed in agility until eleven, learned new tricks until thirteen, and was my devoted companion until the very end. A remarkable breed for a long-term investment in companionship."),
            (4, "Perfect for agility enthusiasts", "I got into dog agility specifically to have an activity to share with my Papillon. She has been the ideal partner for it. She is fast, precise, and reads my handling cues beautifully. We have competed at regional level and she has won consistently against all sizes. The sport has been incredible fun for both of us and has deepened our bond significantly. An exceptional breed for anyone interested in canine sport."),
            (5, "Charming and affectionate", "My Papillon is the most charming little dog. She greets everyone with butterfly-winged ears erect, tail fanning, and an expression of pure delight at meeting a new friend. She charms everyone she encounters. She is soft and affectionate with me in the evenings, curled in my lap or pressed against my leg. Her personality is as beautiful as her appearance."),
            (4, "Great for city living", "My Papillon is perfectly suited to my city lifestyle. She is small enough to take everywhere dogs are permitted, calm enough for restaurants and coffee shops, and athletic enough to enjoy the parks and paths in our area. She does need a reasonable amount of exercise for a small dog but it is easily managed with an active urban lifestyle. A wonderful city companion for an engaged owner."),
        ],
    },
    "Pembroke Welsh Corgi": {
        "description": (
            "The Pembroke Welsh Corgi is a low-set, sturdy herding breed from Wales with a foxy face and a characteristically bobbed tail. "
            "Intelligent, outgoing, and athletic, Corgis have become iconic companions known for their enthusiastic personalities and surprising agility despite their short legs. "
            "They are devoted to their families and excel in a range of canine sports and activities."
        ),
        "pros": [
            "Intelligent, trainable, and eager to please",
            "Athletic and versatile in dog sports",
            "Affectionate and devoted to family",
            "Adaptable to various living situations",
        ],
        "cons": [
            "Heavy shedder, year-round with seasonal blow-outs",
            "Strong herding instinct, may nip heels",
            "Can be vocal and prone to barking",
            "Prone to certain spinal and eye conditions",
        ],
        "reviews": [
            (5, "The perfect active family dog", "My Pembroke Welsh Corgi is the ideal balance of manageable size and genuine working dog capability. She is fast, athletic, and learns commands almost faster than I can teach them. She has completed obedience, rally, and herding trial titles. She is also the most devoted, affectionate companion who follows me everywhere and sleeps pressed against my legs every night. She is the dog I have always wanted."),
            (4, "Big dog personality in a compact package", "My Corgi refuses to accept that he is not a large dog. He herds my children, bosses the cat, and issues opinions on every household decision. He is confident, determined, and endlessly entertaining. He learned his commands quickly but he negotiates them regularly. His shedding is significant and constant. The hair is everywhere but so is his joy. Worth every golden-furred inconvenience."),
            (5, "Most intelligent dog I have owned", "My Corgi has solved problems that have stumped previous dogs of all sizes. She figured out how to open the treat cabinet, how to alert me to the kettle boiling, and how to count out her daily treats to ensure accuracy. She is perceptive, quick, and seems to understand extended sentences. Training her is genuinely challenging because she knows when I have made a mistake before I do. An extraordinary, sharp, wonderful dog."),
            (3, "The herding instinct and the children", "My Corgi is wonderful with my children but the herding instinct is real and we have had to train against heel nipping. He does it gently and playfully but it was concerning when my children were small. We worked with a trainer and it is much better now. If you have young children and a Corgi, address this behaviour early with professional guidance. Beyond that challenge he is a magnificent family dog."),
            (5, "Devoted and joyful", "My Corgi is six years old and still greets every walk, every meal, and every return home as if it is the greatest moment of his life. He is joyful in a way that is infectious. He makes everyone in our house smile every day. He has been consistently healthy, responsive to training, and deeply bonded to our family. The shedding is a fact of life and we manage it. He is entirely worth it."),
            (4, "Excellent sport dog", "My Corgi competes in agility and has surprised everyone who expected a comical breed to be comically slow. She moves with precision and speed that belies her build. She has a competitive drive and a focus in the ring that is impressive. She has podium finishes against all breeds at regional level. Her herding instinct and drive make her a natural for working activities. A wonderful and underestimated sport dog."),
            (5, "Best choice for our family", "We did extensive research before getting a dog and the Corgi came up in every category we cared about. Intelligent, trainable, good with kids, manageable size. He has exceeded all our expectations. He is everything the research suggested and more. He is funny, clever, devoted, and endlessly engaging. He has been the best addition to our family we have ever made. The shedding is real but a robot vacuum handles most of it."),
            (4, "Vocal but manageable", "My Corgi barks at things outside, barks when bored, and barks to communicate general opinions. We have done extensive training to put the barking on command and reduce unsolicited expression. He is much better now and I can interrupt him reliably. His voice carries and without training it would be a problem. With training he is a wonderful, communicative companion whose barking serves a useful purpose."),
        ],
    },
    "Pomeranian": {
        "description": (
            "The Pomeranian is a small Spitz-type breed with a distinctive fluffy double coat and a foxy, alert expression. "
            "Descended from large sled dogs, modern Pomeranians are lively, confident, and spirited companions who carry themselves with self-important charm. "
            "They are intelligent and trainable but have a bold personality that can surprise owners expecting a purely docile lap dog."
        ),
        "pros": [
            "Lively, curious, and entertaining personality",
            "Intelligent and responsive to training",
            "Adaptable to apartment living",
            "Devoted and affectionate with their family",
        ],
        "cons": [
            "Prone to excessive barking",
            "Coat requires regular brushing to prevent matting",
            "Fragile, can be injured in rough play",
            "Can develop small dog syndrome without firm training",
        ],
        "reviews": [
            (5, "A cloud of fur and pure personality", "My Pomeranian is four pounds of concentrated personality. She is confident, entertaining, and absolutely certain she is in charge of the entire household. She has trained me more effectively than I have trained her. She is affectionate on her terms, which are frequent, and vocal about her preferences, which are many. She has more personality than most dogs ten times her size. I adore her completely."),
            (4, "Perfect apartment dog", "My Pom is ideal for my city flat. He is small enough to take everywhere, lively enough for entertaining walks, and calm enough indoors once his exercise needs are met. He does bark at sounds in the corridor but we have worked on this and he is manageable. His coat needs daily brushing to keep it beautiful and he gets a professional groom every eight weeks. A wonderful urban companion for someone who appreciates his spirited personality."),
            (5, "Most entertaining little dog", "My Pomeranian provides more entertainment per pound than any dog I have known. She has a spinning trick, a singing trick, and an impressively large vocabulary of commands. She learned each one in two or three sessions. She performs them with theatrical flair and seems to enjoy an audience. She is affectionate in the evenings and bouncy and curious during the day. A delightful, clever, and beautiful little companion."),
            (3, "The barking was a real challenge", "My Pomeranian barked at everything for the first two years. The postman, the wind, birds outside, the television. My neighbours in my building were patient but it was a genuine problem. We have worked extensively with a trainer and he is now manageable but without that investment the barking would have been insurmountable in our living situation. Anyone in a flat with close neighbours should plan for bark training from day one."),
            (5, "Devoted and perceptive companion", "My Pom is ten years old and has been my most devoted companion through the ups and downs of the last decade. She senses my mood with uncanny accuracy and adjusts accordingly. On hard days she is quietly present and close. On good days she spins and bounces and is ridiculous. She has been a genuine emotional support and I am grateful for every year we have had together. She shows no signs of slowing down."),
            (4, "Surprisingly trainable", "Despite having a reputation for being stubborn, my Pomeranian is one of the most responsive dogs I have trained. With positive reinforcement and short, engaging sessions she picks up new behaviours rapidly. She has titles in trick dog competitions and performed a ten-trick sequence at a charity event to great applause. The key is keeping training fun and rewarding. Make it boring and she will make other plans."),
            (5, "Great companion for seniors", "My father is seventy-two and his Pomeranian has transformed his daily life. The dog gets him up, takes him for walks, gives him purpose, and provides daily companionship. The Pom is small enough to be manageable for an older person and affectionate enough to give genuine emotional support. He has made new friends through her on walks and is more socially active than he has been in years. She has been genuinely beneficial for his health and happiness."),
            (4, "Bold and confident", "My Pomeranian has never read the memo about being a small dog. He confidently approaches dogs many times his size, issues instructions to my neighbour's Labrador, and shows absolutely no recognition of his physical limitations. This boldness is charming and occasionally alarming. He has needed careful management around larger dogs because his confidence exceeds their patience. But within safe parameters his personality is a wonderful thing to witness."),
        ],
    },
}

BREED_DATA.update(_BREED_DATA_DOGS2)

_BREED_DATA_DOGS3: dict = {
    "Portuguese Water Dog": {
        "description": (
            "The Portuguese Water Dog is an athletic, medium-sized working breed developed by Portuguese fishermen to herd fish, retrieve gear, and serve as a messenger between ships. "
            "They are energetic, intelligent, and deeply loyal to their families, with a love of water that is deeply ingrained. "
            "Their low-shedding, wavy or curly coat makes them popular with allergy-sensitive households."
        ),
        "pros": [
            "Low-shedding coat good for mild allergy sufferers",
            "Intelligent, eager to please, and highly trainable",
            "Loves water and outdoor activities",
            "Affectionate and devoted to family",
        ],
        "cons": [
            "High energy requires significant daily exercise",
            "Coat requires regular grooming",
            "Can be mischievous when under-stimulated",
            "Prone to hip dysplasia and progressive retinal atrophy",
        ],
        "reviews": [
            (5, "The perfect active family dog", "My Portuguese Water Dog is exactly what we needed for our outdoor-focused family. She swims, hikes, runs, and retrieves with equal enthusiasm. She is deeply affectionate at home and my children adore her. Her low-shedding coat has been a genuine bonus for my husband who is mildly allergic. She needed consistent training in her first year but is now a reliably well-mannered companion who enhances every activity we do."),
            (4, "Water dog lives up to its name", "My PWD discovered water at four months old and has not been fully dry since. He leaps into any body of water with joyful abandon and swims with powerful natural ability. He has been wonderful for our beach holidays. At home he needs a good hour of exercise every day to be calm. He is smart and can be mischievous if bored. With enough stimulation he is a wonderful, devoted companion."),
            (5, "Best breed for allergic households", "My daughter has dog allergies and my PWD is the only breed she can tolerate. We tested carefully before committing and she has had no allergic reaction in four years. Beyond the allergy benefit he is a wonderful dog. He is athletic, responsive to training, and endlessly affectionate with our family. He has been the family dog we thought we could never have due to allergies."),
            (4, "Energetic and engaging", "My PWD is the most engaged dog I have owned. She watches me constantly, anticipates my next move, and is always ready for whatever comes next. She completed agility training at top of her class and performs complex sequences reliably. Her energy level is high and she needs structured exercise and training every day without exception. When that need is met she is calm and delightful at home."),
            (5, "Devoted and joyful", "My Portuguese Water Dog has been my constant companion for eight years. She goes everywhere with me, from work to holidays to everyday errands. She is adaptable, sociable, and deeply devoted. She has been healthy throughout, which I attribute partly to careful breeding and partly to her active lifestyle. She is one of the best decisions I have ever made and I cannot imagine my life without her."),
            (3, "More energy than I anticipated", "I knew PWDs were active but mine exceeded my expectations. He needs real exercise, not just a walk around the block. We swim twice a week, run daily, and do agility training. On adequate exercise days he is wonderful. On low-exercise days he is a benign but persistent disruption. He is a great dog but the energy commitment is genuine. Be honest about your activity level before choosing this breed."),
            (4, "Excellent family companion", "My PWD has grown up with my three children and been an ideal family companion. She plays with them outdoors, is gentle with them indoors, and has been patient through every phase of their growing up. She is now nine and slowing slightly but her tail still wags at every family member's arrival. A wonderful, long-term companion for an active family."),
            (5, "Wonderful and versatile", "My PWD competes in agility, does therapy work in schools, and accompanies me paddleboarding on weekends. He is versatile in a way that few breeds are. He transitions between these roles easily and performs each one with enthusiasm. He is intelligent, adaptable, and genuinely joyful in everything he does. An extraordinary companion for an active, engaged owner."),
        ],
    },
    "Rhodesian Ridgeback": {
        "description": (
            "The Rhodesian Ridgeback is a powerful, athletic breed from southern Africa originally developed to hunt lions alongside their owners. "
            "Distinctive for the ridge of reversed fur along their spine, Ridgebacks are loyal, dignified, and affectionate with family while being reserved with strangers. "
            "They require confident, experienced handling and significant daily exercise to channel their considerable energy and independence."
        ),
        "pros": [
            "Loyal, devoted, and affectionate with family",
            "Exceptional athleticism and stamina",
            "Dignified and controlled temperament",
            "Low grooming maintenance",
        ],
        "cons": [
            "Strong-willed and requires experienced owner",
            "Can be aloof or reserved with strangers",
            "High exercise requirements",
            "Prey drive can be intense",
        ],
        "reviews": [
            (5, "The lion hunter lives up to the legend", "My Rhodesian Ridgeback is the most impressive dog I have ever owned. She is lean, powerful, and moves with a fluid athletic grace that turns heads everywhere we go. She is deeply devoted to my family and protective without being aggressive. She is reserved with strangers initially and warms gradually once she has assessed them. She is easy to maintain and has been consistently healthy. A magnificent, noble companion."),
            (4, "Athletic and loyal", "My Ridgeback runs with me every morning and could easily go further than I do. His stamina is extraordinary. He is calm and dignified indoors, never destructive, and reserved with strangers in a measured, intelligent way. He is not a breed for inexperienced owners because his independence requires confident handling. With the right person he is an exceptional companion. He has been the best running partner imaginable."),
            (5, "Dignified family guardian", "My Ridgeback watches over my family with quiet intelligence. He observes visitors carefully, accepts those we welcome, and positions himself between our family and anything he finds concerning. He has never been inappropriate but his presence alone communicates serious intent. With my children he is tender and patient. He is one of the most balanced dogs I have ever owned."),
            (3, "Independence requires patience", "My Ridgeback is wonderful but the independent streak is real. She decides which commands are worth following and when. Training required two years of consistent daily work and professional guidance. She is now reliable but it was a genuine investment. She is not a dog you can train once and consider done. She needs ongoing engagement. For an experienced owner with time she is excellent. For a first-time owner she would be challenging."),
            (5, "Best trail companion", "I do trail running and my Ridgeback has been my ideal partner for eight years. He runs trails beside me with power and sure-footedness, can go for hours without tiring, and seems happiest when covering ground at pace. He has been to mountain ranges across three countries with me and his adaptability in different environments is remarkable. Off trail he is a calm, devoted companion. On trail he is transcendent."),
            (4, "Low maintenance coat, big personality", "My Ridgeback's coat is effortless. A wipe with a damp cloth keeps him gleaming. He does not drool, rarely smells, and his short coat sheds minimally. He is clean and tidy in a way that bigger working breeds often are not. His personality is big however. He is opinionated, confident, and requires a firm but respectful approach. A wonderful dog for someone who appreciates a strong character."),
            (4, "Remarkable breed", "Living with a Ridgeback has changed how I think about dogs. He is not demonstrative in the way Labs and Retrievers are. He shows affection in subtle, meaningful ways. He rests his chin on my knee. He follows at a measured distance. He chooses to be near me rather than demanding interaction. His love is quiet and certain. Learning to read him has been one of the great rewards of dog ownership for me."),
            (5, "Healthy and long-lived", "My Ridgeback is eleven years old and still running trails with me, albeit shorter ones. She has had no significant health issues in her life, which I attribute to a reputable breeder, excellent nutrition, and an active lifestyle. The breed is generally healthy and her longevity is a genuine gift. She has been my companion through a decade of significant life events and her steady, loyal presence has been invaluable."),
        ],
    },
    "Saint Bernard": {
        "description": (
            "The Saint Bernard is a giant Swiss rescue dog famous for its work finding lost travellers in the Alps. "
            "Despite their enormous size, Saints are famously gentle, patient, and calm with families and children. "
            "They are devoted companions who need space, moderate exercise, and owners prepared for their considerable size and grooming requirements."
        ),
        "pros": [
            "Gentle, patient, and devoted family companion",
            "Excellent with children due to tolerant nature",
            "Calm and relatively low energy indoors",
            "Historically used for mountain rescue work",
        ],
        "cons": [
            "Heavy drooling especially after drinking",
            "Heavy seasonal shedding",
            "Short lifespan typical of giant breeds",
            "High food, space, and veterinary costs",
        ],
        "reviews": [
            (5, "The gentlest giant in existence", "My Saint Bernard weighs one hundred and eighty pounds and is the most gentle, patient animal I have ever shared my life with. My children have grown up climbing on him, sleeping against him, and treating him as a large, furry piece of furniture. He accepts everything with serene good nature. The drool is a fact of life and we have drool towels in every room. He is completely worth every inconvenience of his size."),
            (4, "Magnificent family dog", "My Saint is wonderful with my family and completely devoted to our household. He is calm indoors, friendly with visitors, and gentle with children. The practical challenges are real. He eats a great deal, requires a large vehicle, and drools on the ceiling somehow. His coat needs brushing three times a week and professional grooming quarterly. The costs are significant. The dog himself is magnificent and I would do it all again without hesitation."),
            (5, "The perfect nanny dog", "We have four children ages three through twelve and our Saint Bernard has been their gentle guardian through every phase. He moves carefully around the smallest ones, positions himself between them and anything he finds concerning, and accepts their affections with endless patience. He has never shown irritation. He is the most fundamentally kind and patient dog I have ever known. Our family is better for having him."),
            (3, "Too much dog for our home", "I love my Saint Bernard but I underestimated what living with a dog this size in a three-bedroom house would mean. He takes up the entire hallway. He drools on walls. He leaves muddy paw prints on ceilings somehow. He needs a large car. He costs significantly more than I budgeted. He is wonderful and I love him but if I were making the decision again I would be more honest about whether my home and budget were genuinely ready for this breed."),
            (5, "Calm and devoted in every season", "My Saint Bernard thrives in cold weather, loves snow with unalloyed joy, and is equally calm in moderate weather. His instinct for finding distressed people seems real. He once located my daughter who had gone further into the woods than intended and guided me to her. Whether that was instinct or luck I cannot say but it felt significant. He is eight years old, healthy, and as devoted as he was on the first day."),
            (4, "Surprisingly manageable daily", "Day-to-day living with a Saint is more manageable than people expect if you have the right setup. He is not highly energetic. Two good walks a day satisfy him. He is quiet in the house and not destructive. The practical issues are the drool and the size of everything associated with him. But his temperament is so easy that I often forget I own what is effectively a small bear."),
            (5, "Most patient dog alive", "I have owned many breeds and my Saint Bernard is the most fundamentally patient. Nothing seems to disturb or upset him. Children can be rough, visitors can be loud, and the house can be chaotic and he observes it all with calm, benevolent attention. He is the anchor of our household. When things get stressful I find myself seeking him out and his solid, warm presence is genuinely calming."),
            (4, "Worth every challenge", "The list of practical challenges with a Saint Bernard is real and long. Size, drool, shedding, cost. But when he rests his enormous head on my knee and looks at me with those warm, deep eyes I cannot remember why any of it mattered. He is a remarkable animal and the years we have had together have been among the best of my life. I urge anyone with the right situation to experience this breed."),
        ],
    },
    "Samoyed": {
        "description": (
            "The Samoyed is a beautiful, white-coated Arctic breed originally bred by the Samoyedic peoples of Siberia for herding reindeer and pulling sleds. "
            "Known for the characteristic Samoyed smile, these dogs are friendly, gentle, and sociable with an adaptable, family-oriented nature. "
            "Their dense double coat requires significant grooming, especially during seasonal shedding periods."
        ),
        "pros": [
            "Friendly and gentle with everyone including children",
            "Playful and sociable, gets on well with other dogs",
            "Adaptable and happy disposition",
            "Beautiful, distinctive appearance",
        ],
        "cons": [
            "Extremely heavy shedder, especially twice yearly",
            "Can be prone to howling and barking",
            "Needs significant daily exercise",
            "Coat requires extensive brushing and grooming",
        ],
        "reviews": [
            (5, "Living with a smiling snowflake", "My Samoyed smiles. It sounds anthropomorphic but she genuinely has an upturned mouth and bright, happy eyes that make her look perpetually delighted with life. She is friendly to every person and dog she has ever met. She is enthusiastic, warm, and endlessly fluffy. The shedding is extraordinary. During blow-outs I could stuff a duvet with her fur. She is completely worth every hair."),
            (4, "Gorgeous dog, significant coat", "My Samoyed is the most beautiful dog I have ever owned. His white coat is stunning and he carries it beautifully. The maintenance is real. He needs brushing every two days minimum and during seasonal blow-outs daily. We also do professional grooming quarterly. He is friendly, playful, and wonderful with my children. The shedding permeates every aspect of our home but we have accepted it as the price of his company."),
            (5, "Sociable and joyful", "My Samoyed approaches every day with visible joy. She greets everyone she meets, whether person or dog, with genuine warmth and enthusiasm. She has never shown a trace of aggression. She is playful with my children and gentle with elderly visitors. She is one of the most socially gifted dogs I have encountered. She needs exercise and grooming commitment but her personality makes both tasks a pleasure."),
            (3, "The howling was not in the description", "My Samoyed is wonderful in many ways but the howling surprised me. He howls when he is excited, when he hears certain music, when he disagrees with a decision, and sometimes for reasons I cannot identify. We live in a semi-detached house and my neighbours have mentioned it. We are working on it with a trainer and making progress. If you have close neighbours this is worth researching carefully before choosing this breed."),
            (5, "Best cold-weather companion", "My Samoyed is in her element in winter. She plays in snow with pure joy, tolerates temperatures that keep other breeds indoors, and seems genuinely energised by cold weather. She is less enthusiastic in summer heat and we have to manage outdoor time carefully. For our Nordic climate she is perfectly designed and endlessly happy. An extraordinary breed for cold-weather environments."),
            (4, "Friendly to a fault", "My Samoyed would let any burglar in and show them where the valuables are, then follow them around hoping for attention. She is friendly to literally everyone without distinction. She is a terrible guard dog but a wonderful companion. Her warmth and sociability make her a joy to take anywhere and my social life has improved considerably since I got her because people cannot resist stopping to meet her."),
            (5, "Gentle with my vulnerable dog", "I adopted an elderly, traumatised rescue dog last year and my Samoyed has been the most gentle, patient companion to her. He reads her signals accurately, never pushes her comfort limits, and has clearly contributed to her confidence and relaxation. Watching him interact carefully with a fearful dog has been one of the most moving things I have witnessed. He is a remarkably empathetic animal."),
            (4, "Worth the grooming commitment", "The first spring blow-out nearly defeated me. The amount of fur was genuinely extraordinary. I now have a professional blowout session at the groomer each spring and autumn which removes the majority of it efficiently. Between those sessions I brush every other day. The commitment is real but my Samoyed is so fundamentally lovely in every other way that I have made peace with it completely. He enriches my life daily."),
        ],
    },
    "Scottish Terrier": {
        "description": (
            "The Scottish Terrier is a compact, dignified, and spirited terrier breed with a distinctive beard and eyebrow profile. "
            "Feisty and independent, Scotties are devoted to their families but typically reserved with strangers, with a terrier's characteristic stubbornness and self-assurance. "
            "They are bold, alert, and surprisingly powerful for their compact size."
        ),
        "pros": [
            "Loyal and devoted to their own family",
            "Low-shedding, reasonable for mild allergy sufferers",
            "Bold and confident personality",
            "Compact size, adaptable to various homes",
        ],
        "cons": [
            "Stubborn and independent, challenging to train",
            "Reserved with strangers, can be territorial",
            "Strong prey drive, not reliable off-leash",
            "Can be prone to Scottie cramp and other breed-specific conditions",
        ],
        "reviews": [
            (5, "The most dignified small dog", "My Scottish Terrier carries himself with a dignity that is completely at odds with his size. He is eight inches tall and behaves as though the world was created for his convenience. He is devoted to me in a reserved, dignified way that is nothing like the exuberant love of a Labrador but is no less real. He is my quiet shadow, always near, always watching, always certain he knows best. A remarkable little character."),
            (4, "Loyal and stubborn in equal measure", "My Scottie will come when called approximately sixty percent of the time. The other forty percent she has reasons I am not privy to. She learned her commands early but applies them at her own discretion. She is devoted to my family in a particular Scottish Terrier way, which means she keeps an eye on us from a comfortable distance rather than crowding our space. She is funny, dignified, and completely unique."),
            (5, "Perfect companion for independent people", "My Scottie suits my lifestyle perfectly. I am an independent person who finds overly demanding, clingy dogs exhausting. He is devoted but self-sufficient. He does not need constant attention, does not suffer separation anxiety, and is perfectly content in his own company for reasonable periods. He checks in with me regularly and accepts affection warmly but does not demand it. We understand each other perfectly."),
            (3, "More independent than I wanted", "I wanted an affectionate, responsive companion dog. My Scottie is affectionate on her terms, which are less frequent than I prefer, and responsive to commands when it suits her, which is less frequent than I require. She is a wonderful personality but my ideal dog is more demonstratively loving and more reliably obedient. She would be perfect for someone who appreciates a more self-contained, independent companion."),
            (4, "Good watchdog in a small package", "My Scottie is the best early warning system I have owned. He alerts to anyone at the perimeter with two sharp barks, then waits. He does not bark endlessly and he does not react to every sound. He is selective and accurate. His bark is surprisingly deep for his size. He is reserved with strangers but warms appropriately once introduced. He has been an asset in our neighbourhood where we have had some security concerns."),
            (5, "Long-lived and healthy", "My Scottie is thirteen years old and still walking briskly, still interested in everything, still insisting on her opinions about household matters. The longevity of this breed is a genuine gift. She has slowed and her grey muzzle is more pronounced but her personality is completely unchanged. She is as opinionated and dignified at thirteen as she was at three. I am hoping for several more years with this remarkable little dog."),
            (4, "Character in a compact package", "My Scottie has more character than dogs three times his size. He has definite opinions, clear preferences, and is entirely unbothered by the views of others. He is a small dog who has never read a word about being small and therefore does not know it applies to him. He is brave, bold, and occasionally foolhardy but always entertaining. A wonderful companion for someone who appreciates a strong individual personality."),
            (5, "Best kept secret of the terrier world", "People walk past my Scottie on the street and underestimate him completely. He is calm, self-contained, and moves with unhurried dignity. But spend time with him and you discover a remarkably deep personality, genuine devotion expressed quietly, and a sharp intelligence applied selectively. He is the most underrated breed I have encountered. A truly special dog for a patient owner who can appreciate subtlety."),
        ],
    },
    "Shetland Sheepdog": {
        "description": (
            "The Shetland Sheepdog is a small, graceful herding breed from Scotland's Shetland Islands with a beautiful, flowing coat and a foxy face. "
            "Intelligent, responsive, and deeply sensitive, Shelties are among the most trainable of all breeds and excel at canine sports. "
            "They are devoted and affectionate with their families but can be reserved or wary with strangers."
        ),
        "pros": [
            "Exceptionally intelligent and highly trainable",
            "Devoted and affectionate with family",
            "Excels at agility, herding, and obedience sports",
            "Alert and attentive",
        ],
        "cons": [
            "Prone to excessive barking",
            "Coat requires regular brushing",
            "Can be reserved or timid with strangers",
            "Herding instinct may cause chasing of children or other pets",
        ],
        "reviews": [
            (5, "The most trainable dog I have ever owned", "My Sheltie is extraordinary. She learns new commands in one session, remembers them indefinitely, and performs them with precision and enthusiasm. We compete in agility and obedience and she has won at national level. She is also the most devoted companion, watching me constantly and responding to my mood with accurate sensitivity. She is the ideal dog for someone who wants to work closely with their animal."),
            (4, "Brilliant sport dog, big voice", "My Sheltie is an agility champion and he earns every ribbon. His focus, speed, and responsiveness are remarkable. The challenge in daily life is the barking. He alerts to everything and his bark is sharp and carries. We have done extensive training and he is much better but cannot be considered quiet. In a rural setting this would be a non-issue. In our semi-detached house it required real work to manage."),
            (5, "Most sensitive and responsive breed", "My Sheltie reads me with a sensitivity that still surprises me after six years. She knows when I am unwell before I do. She adjusts her behaviour to my emotional state without being asked. She is soft and gentle on difficult days, playful and energetic on good ones. She has been a profound companion through significant life events and her sensitivity has made her an inadvertent emotional support animal."),
            (3, "Timid with strangers was a challenge", "My Sheltie was quite fearful of strangers initially and we had to invest significantly in socialization and confidence-building. He is much better now but he will never be a confident, outgoing dog with unfamiliar people. He is happy and confident with his family and trusted friends. For someone who wants a social, outgoing dog he would be the wrong choice. For a family-focused companion he is wonderful."),
            (5, "Devoted and joyful", "My Sheltie has been my companion for ten years and the devotion she shows me has not diminished by a fraction. She is as attentive and responsive at ten as she was at one. She is bright-eyed, engaged with the world, and still enthusiastic about training and agility. The breed ages gracefully and maintains its vitality well. She has been the most consistently wonderful dog I have ever owned."),
            (4, "Wonderful with gentle children", "My Sheltie is excellent with my children once she knows them well. With unfamiliar children she is cautious and we always supervise initial meetings carefully. With my own children she is patient, gentle, and very occasionally gives a quiet herding nudge when they stray too far apart. Her herding instinct is gentle and can be redirected with training. A wonderful family dog for the right family."),
            (5, "Best breed for an active life", "My Sheltie accompanies me everywhere, from morning runs to weekend hikes. She has the endurance of a much larger dog and the adaptability to be calm when needed and energetic when the moment calls for it. She is the ideal size for travel and the ideal temperament for varied activities. She has made my active lifestyle richer and more connected to the natural world."),
            (4, "Gorgeous and elegant", "My Sheltie is beautiful. Her coat is a rich sable and white and she carries it magnificently. Grooming takes twenty minutes twice a week and she is patient and cooperative about it. She sheds seasonally and requires more attention during blow-out periods. Her beauty is part of her charm and the grooming investment, while real, produces a dog who is genuinely stunning to look at."),
        ],
    },
    "Shiba Inu": {
        "description": (
            "The Shiba Inu is Japan's most popular native breed, an ancient Spitz-type dog with a bold, fiery personality and fox-like good looks. "
            "Independent, fastidious, and deeply spirited, Shiba Inus have a cat-like quality to their self-sufficiency that makes them unique among dog breeds. "
            "They require experienced, patient owners who can appreciate and work with their strong-willed nature."
        ),
        "pros": [
            "Clean, self-grooming dog with minimal odour",
            "Loyal and devoted to their own family",
            "Spirited, entertaining, and unique personality",
            "Compact and adaptable to various living situations",
        ],
        "cons": [
            "Highly independent and difficult to train",
            "Screams dramatically when displeased",
            "Strong prey drive and unreliable off-leash",
            "Can be dog-selective or aggressive",
        ],
        "reviews": [
            (5, "The most unique dog I have ever owned", "My Shiba Inu is like no other dog I have experienced. She is clean, cat-like in her self-maintenance, and fastidious about her personal space. She is loyal to me in a deep, quiet way that is nothing like the eager devotion of a retriever. She observes the world with intelligent, measured eyes and does whatever she decides to do. Training her required me to become more creative than I have ever been as a dog owner. Absolutely unique."),
            (4, "Funny and spirited", "My Shiba is the most entertaining dog I have owned. He has strong opinions about everything and expresses them dramatically. He performs the Shiba scream in protest at bath time, nail trims, and vetted appointments. He is a gifted escape artist who views containment as a puzzle to solve. He is devoted to my family in a reserved, dignified way and genuinely funny in his reactions to the world."),
            (5, "Perfect for an experienced patient owner", "I have owned dogs for twenty years and my Shiba is the most interesting challenge I have had. Traditional training methods barely touch her. I had to learn new approaches, understand her motivation, and negotiate rather than dictate. When I adjusted my approach she responded. She is not obedient in the conventional sense but she is reliably cooperative with someone she respects. A remarkable, complex companion."),
            (3, "Not for first-time owners", "I got my Shiba thinking his independence would be refreshing. It was more than I bargained for. He is difficult to train, uninterested in pleasing me, and selective about when recall applies. He has escaped twice and caused two incidents with other dogs. He is not aggressive toward people and is actually affectionate with my family. But managing his independence and prey drive requires experience I did not have. He would be perfect with the right owner."),
            (4, "Clean and low maintenance physically", "My Shiba grooms herself like a cat, rarely smells, and her coat stays remarkably clean between the twice-yearly blow-outs. The coat care during shedding season is intense but otherwise she is the lowest maintenance dog I have owned physically. Behaviourally she requires significant management and ongoing training work. The balance is unusual but workable."),
            (5, "The Shiba scream made me laugh", "The first Shiba scream nearly gave me a heart attack. Now I find it completely hilarious. My Shiba expresses displeasure with a drama that is disproportionate to every situation. He screams at the sight of the nail clippers, at having his paw wiped, at being asked to come inside. He is theatrical and funny and I love him completely. He is devoted to me in his reserved Shiba way and our life together is never dull."),
            (4, "Gorgeous and self-possessed", "My Shiba Inu is one of the most beautiful dogs I have ever seen. His red and white coat is immaculate, his expression is perpetually alert and intelligent, and his compact, muscular build is perfect. He carries himself with an aristocratic confidence that draws attention wherever we go. He is not the most biddable dog I have encountered but he is absolutely the most impressive looking."),
            (5, "Once bonded, forever loyal", "My Shiba took six months to fully trust me and accept me as her person. The process was gradual and required patience and respect for her boundaries. But once that bond formed it was deep and solid. She is devoted to me in a way that is different from other breeds but no less real. She sleeps at my feet, follows at a measured distance, and greets my return with a joy that she usually keeps more composed. Worth every patient month."),
        ],
    },
    "Soft Coated Wheaten Terrier": {
        "description": (
            "The Soft Coated Wheaten Terrier is an Irish farm dog with a distinctive silky, wavy wheaten-coloured coat and an exuberant, puppyish personality that persists well into adulthood. "
            "Affectionate, energetic, and playful, Wheatens are enthusiastic companions who are good with children and adaptable to active family life. "
            "Their low-shedding coat is a bonus for mild allergy sufferers, though it requires regular professional grooming."
        ),
        "pros": [
            "Affectionate, playful, and fun-loving",
            "Low-shedding coat good for mild allergies",
            "Good with children and family life",
            "Adaptable and robust constitution",
        ],
        "cons": [
            "High energy requires consistent daily exercise",
            "Enthusiastic jumper, needs training to manage",
            "Coat requires regular professional grooming",
            "Can be stubborn with training",
        ],
        "reviews": [
            (5, "Joy on four legs", "My Wheaten greets every person who enters my home by jumping up to make full eye contact and then spinning in circles of pure delight. We have trained the jumping down considerably but the enthusiasm never dims. He is warm, playful, and endlessly affectionate. He has been gentle with my children from the start and adapts his energy to whoever he is with. A wonderful, joyful breed."),
            (4, "Energetic and entertaining", "My Wheaten is two years old and still has puppy energy. She runs, plays, zooms around the garden, and investigates everything with inexhaustible curiosity. She is wonderful on long hikes and equally happy playing fetch in the garden. Her coat needs professional grooming every eight weeks but it is silky and beautiful and does not shed visibly. A great active family dog with a joyful personality."),
            (5, "Best breed for allergy-sensitive families", "My son has dog allergies and we tested carefully before getting our Wheaten. He has no reaction to her in three years of close living. She is also a wonderful family dog, affectionate with my children, playful and energetic, and gentle enough for everyday family life. The allergy benefit combined with the wonderful temperament makes her the ideal dog for our household."),
            (3, "The Wheaten greeting needs work", "My Wheaten greets every arrival by launching herself at chest height with enthusiasm that has left bruises. She is not aggressive, she is delighted, but the jumping was a serious problem with elderly visitors. We have done extensive training and she is much better but the default enthusiastic greeting required real work to modify. New owners should prioritize this training from week one."),
            (5, "Loyal and devoted companion", "My Wheaten is seven years old and has been my most devoted companion through a difficult few years. He senses when I am struggling and moves close without being asked. He has a warmth and emotional perceptiveness that I find genuinely comforting. He is playful when I need distraction and calm when I need quiet. He adapts to my emotional needs with a sensitivity I have not seen in many breeds."),
            (4, "Great with other dogs", "My Wheaten is the most dog-friendly breed I have owned. She approaches every dog she meets with open, friendly energy and has never been involved in a conflict. She plays well with dogs of all sizes and adjusts her intensity appropriately. She is genuinely sociable and seems happiest in multi-dog environments. She is an excellent companion for households with other dogs."),
            (5, "Wonderful if you embrace the energy", "My Wheaten is not a calm dog and probably never will be. But I have come to love his exuberance as an expression of how fully he engages with life. Everything is wonderful to him. Every walk is an adventure, every person a new friend, every moment an opportunity for joy. Living with that energy is contagious. I am more optimistic and more present as a person for having him in my life."),
            (4, "Silky coat worth the grooming", "The Wheaten coat is beautiful and silky and does not shed onto furniture in the way so many breeds do. The cost is professional grooming every eight weeks, which is real. But the result is a dog that looks and feels wonderful and does not leave fur on everything I own. A good trade-off for a mild allergy household that wants a characterful, affectionate terrier."),
        ],
    },
    "Staffordshire Bull Terrier": {
        "description": (
            "The Staffordshire Bull Terrier is a medium-sized, muscular British breed known for its courage, tenacity, and deep affection for humans, particularly children. "
            "Often called the nanny dog for their devotion and gentleness with children, Staffies are among the most people-friendly breeds despite their tough appearance. "
            "They require confident, consistent training and careful socialisation with other dogs."
        ),
        "pros": [
            "Extremely affectionate and devoted to family",
            "Excellent with children, known as the nanny dog",
            "Playful and enthusiastic companion",
            "Short, low-maintenance coat",
        ],
        "cons": [
            "Can be dog-aggressive without careful socialisation",
            "Subject to breed-specific legislation in some areas",
            "High energy needs regular exercise",
            "Can be stubborn during training",
        ],
        "reviews": [
            (5, "The nanny dog title is fully earned", "My Staffie is the most devoted, affectionate dog I have ever owned and her relationship with my children is extraordinary. She sleeps outside their rooms, checks on them during the night, and positions herself between them and anything she perceives as a threat. She is endlessly patient with their antics and has never shown anything but love toward them. She is everything the nanny dog reputation promises and more."),
            (4, "Wonderful family dog, needs dog socialisation", "My Staffy is brilliant with people and absolutely devoted to my family. She is less reliable with unfamiliar dogs and we manage this carefully. Early socialisation helped significantly and she is fine with dogs she knows well. We walk her away from dog-heavy areas and she is otherwise a perfect companion. Her people skills are extraordinary and her devotion to my children is touching."),
            (5, "Most loving dog I have owned", "My Staffie is physically incapable of being near a human without expressing love. He leans, wriggles, licks, and must have physical contact at all times. When he is on the sofa with me he finds some way to ensure at least one paw or his head is touching me. He is the warmest, most affectionate dog I have met in any breed. His enthusiasm is sometimes overwhelming but it comes from a place of pure love."),
            (3, "Dog aggression required management", "My Staffie is wonderful with people but we have had three incidents with other dogs in four years despite careful socialisation from puppyhood. Each was provoked by the other dog but my Staffie's response was disproportionate. We work with a specialist trainer and have improved significantly. He is now reliable in managed situations. But if you have multiple dogs or frequent dog parks this is a real consideration."),
            (5, "Robust and healthy", "My Staffie is nine years old and has been remarkably healthy throughout her life. She had one ear infection at three and that is the extent of her medical history. She is robust, energetic, and vital in a way that defies her age. She still plays like a much younger dog. The breed is known for hardiness and my experience confirms it. She has been the easiest dog to maintain health-wise that I have ever owned."),
            (4, "Playful and joyful", "My Staffie approaches life as one long opportunity for play. He greets every walk with theatrical excitement, every toy with total commitment, and every person with irrepressible enthusiasm. He has made my life more joyful simply by demonstrating how much there is to be enthusiastic about. He is easy to exercise because he wants to be exercised. He is easy to train when properly motivated. He is a genuinely wonderful companion."),
            (5, "Changed how I think about the breed", "I had misconceptions about Staffies before I got mine. A rescue volunteer suggested her as a good fit for my family and I was hesitant. She has been the most wonderful dog. She is gentle, loving, funny, and completely devoted. She has challenged all my assumptions about the breed and I now champion Staffies actively to anyone who will listen. The reputation does not match the reality of a well-socialised, loved Staffie."),
            (4, "Ideal for active families", "My Staffie runs with me, plays with my kids, and comes on family hikes. He adapts his energy to any activity we offer him. He needs regular exercise to be calm indoors but is not excessively demanding. Two good walks and some play every day keeps him settled and content. He is the ideal balance of active companion and settled family dog."),
        ],
    },
    "Vizsla": {
        "description": (
            "The Vizsla is an elegant Hungarian pointer-retriever known for its distinctive golden-rust coat and its intense devotion to its owners. "
            "Sometimes called the velcro dog for their need to be close to their people, Vizslas are sensitive, athletic, and highly trainable sporting dogs. "
            "They thrive in active families and are genuinely unhappy when left alone for extended periods."
        ),
        "pros": [
            "Deeply affectionate and loyal to family",
            "Exceptional hunting and sporting dog ability",
            "Intelligent and highly trainable",
            "Short coat, minimal grooming required",
        ],
        "cons": [
            "Very high energy, needs hours of exercise daily",
            "Can develop separation anxiety",
            "Sensitive to harsh training methods",
            "Not suitable for sedentary lifestyles",
        ],
        "reviews": [
            (5, "The velcro dog name is no exaggeration", "My Vizsla has not left my side in three years. She follows me from room to room, lies at my feet while I work, and presses against me at every opportunity. Some people find this overwhelming but I find it deeply comforting. She is the most devoted animal I have ever known. She is also extraordinarily athletic and runs with me for an hour every morning without flagging. A remarkable companion for an active person."),
            (4, "Brilliant hunting dog, devoted companion", "My Vizsla performs in the field with elegance and precision. His pointing is natural and confident, his retrieve is soft-mouthed and reliable. Between seasons he is my devoted family companion, running with my children and sleeping pressed against them. He needs a great deal of exercise every day without exception. With that need met he is the most manageable, affectionate dog I have owned."),
            (5, "Sensitive and responsive", "My Vizsla responds to the most subtle cues. She reads my body language before I have spoken and adjusts her behaviour accordingly. Training her was a pleasure because she is so attuned to communication. She does not tolerate harsh handling and shuts down completely if I am too stern. With positive, gentle training she is exceptional. One of the most intelligent, responsive dogs I have worked with."),
            (3, "Separation anxiety was significant", "My Vizsla struggled terribly when left alone. She destroyed furniture in the first month, howled for hours according to my neighbour, and showed genuine distress. We worked with a behaviourist for six months and she is significantly better. She needs a dog walker on days I am in the office. The commitment required to manage her separation anxiety was more than I anticipated. A wonderful dog for someone who is home most of the time."),
            (5, "Best running partner of my life", "I have run marathons and my Vizsla has been my training partner for two of them. She runs distances that exhaust me without apparent effort and arrives home still ready to play. Her natural athleticism is extraordinary. When I am not running she needs other outlets and we do agility and nosework. She is the most perfectly designed athletic companion and I love her completely."),
            (4, "Beautiful and elegant", "My Vizsla is one of the most beautiful dogs I have ever seen. Her golden-rust coat gleams in sunlight and her movement is fluid and athletic. She is elegant in everything she does. The coat requires minimal care, a wipe with a damp cloth keeps her gleaming. She is not the easiest dog to own due to her energy and attachment needs but she is the most beautiful."),
            (5, "Perfect for the right lifestyle", "My Vizsla has been the ideal dog for my lifestyle, which involves running, hiking, and spending significant time outdoors. She is my constant companion on every adventure. She adapts beautifully to new environments and is sociable with people and dogs alike. She has high needs but for the right active person she is a near-perfect companion. I would choose her again without a moment's hesitation."),
            (4, "Affectionate with the whole family", "My Vizsla has chosen each member of my family as her person at different times of day. She is with me in the morning, with my wife in the afternoon, and with my children in the evening. She manages the attachments simultaneously and ensures everyone receives sufficient attention. She is a social, inclusive dog who bonds deeply with everyone in her household. A truly wonderful family companion."),
        ],
    },
    "Weimaraner": {
        "description": (
            "The Weimaraner is a striking German gun dog with a distinctive silver-grey coat and pale amber or blue eyes. "
            "Nicknamed the Grey Ghost, Weimaraners are powerful, athletic, and highly intelligent sporting dogs with strong personalities. "
            "They are devoted to their owners but require experienced handling and substantial daily exercise to prevent problem behaviours."
        ),
        "pros": [
            "Distinctive, beautiful appearance",
            "Loyal and deeply devoted to family",
            "Versatile hunting and sporting dog",
            "Short, low-maintenance coat",
        ],
        "cons": [
            "Extremely high energy and exercise requirements",
            "Strong-willed, requires experienced handling",
            "Prone to separation anxiety",
            "Can be destructive when under-stimulated",
        ],
        "reviews": [
            (5, "The grey ghost of the dog world", "My Weimaraner is the most strikingly beautiful dog I have ever owned. His silver coat and pale amber eyes turn heads everywhere we go. He is also the most devoted dog I have had, following me everywhere with quiet intensity. He needs a huge amount of exercise but when that need is met he is calm, obedient, and a remarkable companion. He has been worth every challenging moment of the first year."),
            (4, "Powerful and devoted", "My Weimaraner is an athlete. She runs for two hours and barely stops. She is sleek, powerful, and fast. She is also deeply attached to me and struggles when I am away. We have a dog walker on work days and she copes, but the attachment is real. With adequate exercise and company she is wonderful. She has been the most challenging and most rewarding dog I have ever owned simultaneously."),
            (5, "Best hunting dog I have used", "I hunt pheasant and my Weimaraner has been my most effective hunting companion by a significant margin. Her nose, her range, and her retrieve are outstanding. She works a field with confidence and style. Off season she is my devoted family companion who shares the sofa and follows my children around the garden. The transition between working dog and family pet is seamless. A truly versatile and extraordinary animal."),
            (3, "Too much dog for my lifestyle", "I thought I was active enough for a Weimaraner. I was not. He needs more than two hours of vigorous exercise daily. On the days I provide it he is manageable. On the days I cannot he becomes a grey ghost of destruction, methodically dismantling everything he can reach. He is a brilliant dog but the exercise commitment is non-negotiable for this breed. Be completely honest with yourself before committing."),
            (5, "Intelligent and responsive", "My Weimaraner picks up training commands faster than any dog I have worked with. She learned a complex tracking sequence in two sessions that took my previous dog two months. She is motivated, responsive, and genuinely engaged in working with me. The challenge is directing all that intelligence productively. Without a job she finds her own, which is rarely appreciated. With structured work she is extraordinary."),
            (4, "Beautiful and manageable with commitment", "My Weimaraner requires significant daily commitment in terms of exercise and engagement. With that commitment she is calm, affectionate, and easy to live with. She is obedient, well-mannered, and a wonderful companion. The grey coat is beautiful and requires minimal grooming. She has been the most rewarding dog I have owned in proportion to the investment I have made in her."),
            (5, "Devoted to my family", "My Weimaraner considers all four members of my family to be her people and distributes her devotion equally and generously. She greets each of us with the same whole-body joy every time we enter. She sleeps nearest whoever came home last. She is completely integrated into our family life and I cannot imagine the house without her distinctive grey presence. A truly wonderful breed for the right committed family."),
            (4, "Great second dog for experienced owners", "I got my Weimaraner as my second dog after a decade with Labradors. I thought my experience would prepare me. I was mostly right but the energy level is genuinely different. She is manageable but requires more daily investment than my Labs. She is more sensitive, more athletic, and more attached. With my experience she has been a wonderful challenge and a deeply rewarding companion. Not for first-time owners though."),
        ],
    },
    "West Highland White Terrier": {
        "description": (
            "The West Highland White Terrier is a small, sturdy Scottish terrier with a bright white double coat and a lively, confident personality. "
            "Westies are feisty, entertaining, and adaptable, equally at home in a city apartment or a country house. "
            "Despite their small size they have the bold, determined character typical of working terriers."
        ),
        "pros": [
            "Lively, confident, and entertaining personality",
            "Adaptable to various living situations",
            "Low-shedding coat",
            "Robust constitution and generally good health",
        ],
        "cons": [
            "Can be stubborn and difficult to train",
            "Strong prey drive",
            "Can be prone to skin allergies",
            "Coat requires regular professional grooming",
        ],
        "reviews": [
            (5, "Big personality in a small package", "My Westie is the most characterful small dog I have ever owned. She has opinions about everything, demands to be involved in every household activity, and is entirely unbothered by the views of anyone who disagrees with her plans. She is affectionate, funny, and endlessly entertaining. Her white coat is beautiful and her regular grooming appointments keep her looking immaculate. A truly wonderful little dog."),
            (4, "Charming and robust", "My Westie is nine years old and still acts like a puppy. He investigates everything, runs and plays with enthusiasm, and shows no signs of slowing down. He is remarkably robust and has had very few health issues. His coat needs professional grooming every eight weeks and daily brushing. He is stubborn about some commands but fundamentally affectionate and wonderful to live with. A characterful, long-lived little companion."),
            (5, "Perfect city companion", "My Westie is my ideal city dog. He is small enough to take everywhere, confident enough to handle busy environments without anxiety, and adaptable enough for train travel and hotel stays. He gets good exercise from our urban walks and is content in my flat. He is alert and interested in everything around him. A wonderful companion for an active city dweller who wants a dog with real character."),
            (3, "The prey drive was a surprise", "My Westie is wonderful in most respects but her prey drive for small animals is very high. She has escaped the garden twice in pursuit of squirrels and cannot be trusted off-leash anywhere near wildlife. We have reinforced all fencing and she is safely contained but the instinct is real and strong. Her prey drive does not extend to the cats she has grown up with but anything new and small is in potential danger."),
            (4, "Stubborn but lovable", "My Westie will come when called when he decides the time is right. He performs commands when they align with his current intentions. He has the terrier's characteristic self-determination and I have made peace with it. Within his terms he is an affectionate, entertaining companion who makes me laugh every day. His stubbornness is part of his character and I appreciate it even when it is inconvenient."),
            (5, "Long-lived and healthy", "My Westie is fourteen years old and still bright-eyed and engaged with life. She has slowed considerably and her hearing is less sharp but her personality is unchanged. She sits in the garden in the sunshine, investigates interesting smells slowly, and still demands her evening cuddle. The longevity of this breed is extraordinary. Fourteen years of wonderful, characterful companionship and I am hoping for more."),
            (4, "Adaptable and confident", "My Westie adapts to everything without apparent stress. He has travelled by train, plane, and ferry. He has stayed in hotels, caravans, and friends' houses. He settles within minutes in any new environment and explores with confident curiosity. His adaptability makes him an excellent travel companion. He is small enough to manage everywhere and confident enough to handle any situation."),
            (5, "Best decision for our family", "We needed a dog that would work in our semi-detached house with a medium garden, cope with our two children, and fit our moderately active lifestyle. The Westie checked every box. He is the right size, the right energy level, and has the right temperament for our family. He has been the best companion we could have chosen and we would get another Westie without hesitation."),
        ],
    },
    "Whippet": {
        "description": (
            "The Whippet is a medium-sized sighthound of English origin, bred for racing and hunting by sight. "
            "Elegant, gentle, and affectionate, Whippets combine impressive athletic speed with a calm, sensitive indoor temperament. "
            "They are often described as the ideal dog for those who want a graceful, gentle companion with the capacity for remarkable short-burst speed."
        ),
        "pros": [
            "Gentle, calm, and affectionate with family",
            "Low grooming requirements",
            "Quiet indoors, rarely barks",
            "Adaptable to apartment living",
        ],
        "cons": [
            "High prey drive, unreliable off-leash near small animals",
            "Sensitive to cold, needs a coat in cool weather",
            "Prone to running at dangerous speeds and possible injury",
            "Can develop separation anxiety",
        ],
        "reviews": [
            (5, "The perfect gentle companion", "My Whippet is everything I could have wanted. She is quiet, gentle, affectionate, and low-maintenance. She gets a good run twice a day and then spends the rest of her time on the sofa under a blanket. She is sensitive to my moods and adjusts her energy accordingly. She is graceful in everything she does and makes every room she is in look more elegant. An extraordinary breed for someone who wants gentle, uncomplicated companionship."),
            (4, "Elegant athlete", "My Whippet runs at speeds that are genuinely startling. In the park when he gets going he is a streak of muscle and motion that stops everyone nearby. Then he comes home and sleeps on the sofa for six hours. The contrast is extraordinary. He is gentle, quiet, and beautifully behaved indoors. His prey drive is very high and I cannot trust him off-leash near anything small, but otherwise he is a superb companion."),
            (5, "Best kept secret of the dog world", "More people should know about Whippets. They are the ideal medium-sized companion. They do not bark, do not smell, require minimal grooming, and are gentle with everyone they meet. They need good exercise but are genuinely calm between outings. My Whippet is the easiest dog I have ever owned and by far one of the most rewarding. Quiet, graceful, and deeply affectionate. Completely underrated."),
            (3, "Cold weather was harder than expected", "My Whippet finds cold genuinely uncomfortable. He shivers below ten degrees, refuses heavy rain, and has developed an elaborate protest routine for winter mornings. He needs a coat from October through March. He is a wonderful dog in every other respect but the cold sensitivity is real and requires management in a northern climate. Budget for good quality coats and manage your expectations about winter outdoor time."),
            (4, "Sensitive and emotionally aware", "My Whippet reads emotions with a sensitivity that consistently surprises me. She knew I was pregnant before I told anyone, following me more closely and being gentler in her movements around me. She adjusts her behaviour to the emotional climate of the household with accuracy. She is a gentle, aware companion who seems genuinely invested in the wellbeing of her people."),
            (5, "Gentle with my anxious rescue cat", "My anxious rescue cat has lived with my Whippet for three years and they now share the sofa comfortably. My Whippet learned quickly that the cat was not prey and has been respectful ever since. They groom each other occasionally. The prey drive is present on walks but at home with known animals my Whippet is gentle and respectful. Careful introduction and management made co-existence possible."),
            (4, "Ideal for apartment life", "My Whippet lives in a city apartment and is one of the most content urban dogs I have encountered. Two runs in the park every day and she is completely satisfied. She is quiet, does not bark, and is welcomed everywhere because she is gentle and unobtrusive. Her slim frame means she takes up surprisingly little space for a medium dog. A wonderful urban companion."),
            (5, "Devoted and graceful", "Living with a Whippet has been one of the great pleasures of my dog-owning life. She is elegant in movement, gentle in nature, and deeply devoted in her quiet way. She expresses love through proximity and touch rather than exuberance and it is profoundly comforting. She has been the most consistently wonderful companion I have ever had. I will always have a Whippet in my life."),
        ],
    },
}

BREED_DATA.update(_BREED_DATA_DOGS3)

_BREED_DATA_CATS1: dict = {
    # ------------------------------------------------------------------ CATS
    "American Bobtail": {
        "description": (
            "The American Bobtail is a naturally occurring bobtailed cat breed known for its wild, bobcat-like appearance and surprisingly friendly, dog-like temperament. "
            "Intelligent, interactive, and adaptable, American Bobtails are often described as the golden retrievers of the cat world for their playful and sociable nature. "
            "They form strong bonds with their families and are known to travel well, making them popular companion cats."
        ),
        "pros": [
            "Friendly and sociable, often described as dog-like",
            "Adapts well to travel and new environments",
            "Playful and interactive without being hyperactive",
            "Good with children and other pets",
        ],
        "cons": [
            "Longhaired variety needs regular brushing",
            "Can be attention-seeking and demand interaction",
            "Relatively rare, can be expensive",
            "Some lines prone to spinal issues related to the bobbed tail",
        ],
        "reviews": [
            (5, "The cat that acts like a dog", "My American Bobtail greets me at the door like a dog, plays fetch reliably, and comes when called by name. He also travels in the car without complaint and has stayed in four different hotels without apparent stress. He is unlike any cat I have previously owned. He is confident, interactive, and deeply affectionate. His stubby tail wags when he is happy. He is absolutely wonderful and I could not imagine going back to a conventional cat."),
            (4, "Wild looking but gentle natured", "My Bobtail has the appearance of a small wildcat with her tufted ears and muscular build. Her personality is entirely domestic and sweet. She is playful and interactive without being demanding. She joins family activities but does not insist on attention. She is wonderfully low-stress to live with while still being genuinely companionable. Her semi-long coat needs brushing twice a week to stay looking its best."),
            (5, "Ideal family cat", "My American Bobtail has been the perfect family cat from day one. She is patient with my children, sociable with visitors, and adaptable to the general chaos of family life. She initiates play with the children and signals clearly when she has had enough without resorting to scratching. She has never once been aggressive despite a great deal of provocation from energetic children. An ideal family companion."),
            (4, "Great traveller", "I travel frequently for work and my Bobtail accompanies me on road trips without stress. She adapted to her travel carrier quickly, accepts the car without complaint, and settles into new accommodation within an hour. Her adaptability is remarkable compared to previous cats I have owned. She is genuinely content as long as I am present. An ideal companion for someone who moves around a lot."),
            (5, "Interactive and engaging", "My Bobtail plays fetch reliably, walks on a lead without complaint, and has learned several simple commands. He is more interactive than any cat I have previously known. He follows me around the house like a shadow and involves himself in everything I do. He is affectionate without being clingy and engaging without being demanding. A truly wonderful, unique companion."),
            (3, "Attention needs more than expected", "My Bobtail is wonderful but she needs more interaction than I anticipated. She becomes bored and vocal when left to her own devices for too long. She is not destructive but she is persistent in demanding company. If you work from home or have family around most of the time she is perfect. For someone who is out full time she needs a feline companion to prevent boredom."),
            (4, "Confident and sociable", "My American Bobtail approaches every person and animal he meets with confident curiosity rather than fear. He has integrated perfectly with our dog and our two existing cats. He accepts visitors with friendly interest. He is self-assured in a way that I associate with well-socialised dogs more than cats. His confidence makes him easy to live with and a pleasure in any social situation."),
            (5, "Best cat I have ever owned", "I have had cats for thirty years and my American Bobtail is the most engaging, interactive, and companionable of them all. He is genuinely present in my life in a way that many cats are not. He greets me, plays with me, travels with me, and spends evenings in physical contact with me. His wild appearance and gentle nature are a wonderful contradiction. I am completely devoted to him."),
        ],
    },
    "American Curl": {
        "description": (
            "The American Curl is a distinctive breed whose defining characteristic is ears that curl backward from the face, creating an alert and surprised expression. "
            "Developing this curl within days of birth, Curls are sociable, playful, and retain kitten-like energy well into adulthood. "
            "They are adaptable and family-friendly, known for their gentle nature and strong bonds with their people."
        ),
        "pros": [
            "Gentle, sociable, and good with children and other pets",
            "Retains playful kitten energy throughout life",
            "Both shorthair and longhair varieties available",
            "Distinctive, attractive appearance",
        ],
        "cons": [
            "Ears require regular gentle cleaning",
            "Relatively rare, can be difficult to find reputable breeders",
            "Some cats may have ear cartilage issues if overbred",
            "Not as independent as some breeds, prefers company",
        ],
        "reviews": [
            (5, "The ears are even better in person", "My American Curl's ears are magnificent, curving backward like little horns and giving her a permanently quizzical expression. Her personality matches the look. She is curious, playful, and endlessly interested in everything around her. She still races around the house at six years old like a kitten. She is affectionate and sociable and has been wonderful with my family. A truly beautiful and engaging breed."),
            (4, "Kitten personality forever", "My Curl is seven years old and still plays with the same enthusiasm as when I brought him home as a kitten. He chases toy mice, leaps for feather wands, and invents games with household objects. He is never destructive but always busy. He is affectionate and seeks me out regularly for contact. His permanent kittenhood is one of the great pleasures of owning this breed."),
            (5, "Gentle and sociable", "My American Curl is the most socially gifted cat I have ever owned. She approaches visitors with friendly curiosity, integrates with dogs and other cats without drama, and adapts to new situations with equanimity. She is gentle with my children and tolerant of handling. She seems genuinely to enjoy human company and seeks it out rather than merely tolerating it. A wonderful companion."),
            (3, "Ear cleaning is non-negotiable", "My Curl has beautiful ears but they trap debris and need cleaning twice a week. I initially underestimated this and he developed an ear infection in his first year. Since I have been diligent with cleaning he has been problem-free. The ear maintenance is manageable but requires consistency. Beyond the ears he is a lovely, easy cat to care for."),
            (4, "Distinctive and beautiful", "People who visit my home always comment on my Curl's ears before anything else. They are genuinely striking and the expression they create is utterly unique. She has a permanently surprised look that matches her curious personality. She is playful, affectionate, and easy to live with. Her longhaired coat needs twice-weekly brushing but it is silky and easy to manage."),
            (5, "Perfect for a family home", "My American Curl has integrated seamlessly into our household with three children and a dog. She plays with the children, ignores the dog after an initial assessment period, and has never been aggressive. She is curious and playful without being demanding. She is present without being underfoot. She has been the ideal family cat and we are devoted to her."),
            (4, "Engaging and interactive", "My Curl plays fetch reliably, comes when called, and has learned that certain sounds predict interesting things happening. He is interactive in a way that feels genuinely reciprocal rather than purely self-interested. He brings me toys and waits expectantly. He is a genuinely engaging companion who makes solo living feel less solitary. His distinctive ears are a constant source of delight."),
            (5, "Healthy and robust", "My American Curl is ten years old and has had no significant health issues. He is bright, playful, and vital. The breed is generally healthy because the curl mutation affects only cartilage and does not involve significant structural problems when bred responsibly. I chose a reputable breeder who health-tests and the results speak for themselves. A robust, long-lived companion."),
        ],
    },
    "Bombay": {
        "description": (
            "The Bombay is a sleek, jet-black cat breed created in the 1950s to resemble a miniature black panther. "
            "Affectionate, curious, and highly social, Bombays crave human attention and form intense bonds with their families. "
            "They have a playful, dog-like personality and are known for following their owners around the house and enjoying being held and cuddled."
        ),
        "pros": [
            "Highly affectionate and devoted to family",
            "Sociable and good with children and other pets",
            "Playful and entertaining personality",
            "Short, sleek, low-maintenance coat",
        ],
        "cons": [
            "Needs significant human interaction, not suited to long solo periods",
            "Can be vocal when attention needs are not met",
            "Prone to obesity without diet management",
            "May try to dominate other cats in the household",
        ],
        "reviews": [
            (5, "My panther-sized companion", "My Bombay is the most sleek, elegant creature I have ever shared my home with. She moves like a tiny panther and has eyes like burnished copper coins. She is also the most affectionate, demanding, wonderful cat I have owned. She needs to be near me at all times. She follows me from room to room, sleeps pressed against me, and protests loudly if I close a door between us. She is exhausting and completely wonderful."),
            (4, "Dog-cat personality is real", "My Bombay comes when called, plays fetch with small toys, and greets me at the door every single evening. He is more interactive than any cat I have previously known. He is affectionate without being anxiety-ridden, sociable without being demanding. He is a genuinely enjoyable companion who enriches my solo living in a way I did not expect from a cat. His sleek black coat is beautiful and requires minimal care."),
            (5, "Best cat for a social household", "My Bombay is at his happiest when my house is full of people. He approaches every visitor with friendly confidence and collects attention from all of them. He is a social event in himself. He is perfect for my household where people come and go regularly. He is adaptable, confident, and loves company. He is the perfect cat for a social, active household."),
            (3, "Needs more company than I can provide", "My Bombay is wonderful when I am home but she struggles when I am at work. She vocalises when I leave and has been destructive on particularly long days away. I have addressed this partly by getting a second cat as company but she still clearly prefers human company to feline. If you work full time away from home, think carefully about whether you can meet this breed's companionship needs."),
            (4, "Playful and curious", "My Bombay investigates every corner of every room with methodical curiosity. She has developed complex games with household objects and initiates play regularly. She is never boring to live with. Her coat is immaculate and low maintenance. She is healthy and robust. She needs attention and interaction but for someone who wants an engaged, interactive cat she is wonderful."),
            (5, "My shadow and my comfort", "My Bombay has been my companion through a difficult couple of years. He is physically present whenever I need him, sleeps against me when I am unwell, and sits next to my chair when I am working. His warm, purring presence is genuinely comforting. He is not a cat you share space with. He is a cat who truly lives alongside you. I am profoundly grateful for him."),
            (4, "Easy to care for", "My Bombay's coat is effortless. A weekly brush keeps it gleaming and she rarely smells or needs bathing. She is an indoor cat and keeps herself remarkably clean. Her health has been excellent in six years. The primary care need is her emotional need for company and interaction, which is real and ongoing. As long as that need is met she is a low-maintenance, wonderful companion."),
            (5, "Stunning and charming", "My Bombay is the most commented-on cat I have ever owned. His jet-black coat, copper eyes, and panther-like movement make him genuinely striking. He accepts the attention he receives with gracious confidence. He is also the warmest, most engaging companion. Beautiful and wonderful in equal measure."),
        ],
    },
    "British Longhair": {
        "description": (
            "The British Longhair is the semi-longhaired version of the British Shorthair, sharing the same calm, easygoing temperament with a plush, flowing coat. "
            "Sturdy, round-faced, and serene, British Longhairs are gentle, undemanding cats who are content to be near their people without being overtly demanding. "
            "They are adaptable and suitable for quieter households where they can offer calm, dignified companionship."
        ),
        "pros": [
            "Calm, gentle, and undemanding temperament",
            "Adaptable to quieter households",
            "Beautiful plush coat",
            "Generally robust and healthy",
        ],
        "cons": [
            "Semi-long coat requires regular brushing",
            "Can be reserved with strangers",
            "Less interactive than some breeds",
            "Can be prone to weight gain",
        ],
        "reviews": [
            (5, "The most serene companion", "My British Longhair is the most peaceful creature I have ever shared my home with. She sits in the window in the sunshine, regards the world with calm amber eyes, and purrs when stroked without moving a muscle otherwise. She is not demanding, not destructive, and not vocal. She is simply present and warm and content. For someone who wants a calm, beautiful companion she is absolutely perfect."),
            (4, "Beautiful and easygoing", "My British Longhair has a coat that is genuinely luxurious. It is dense, plush, and beautiful but it needs brushing three times a week to prevent matting. He is a calm, round-faced, gentle cat who is happy in the company of family but does not demand attention. He is a wonderful quiet companion for a calmer lifestyle. His blue coat and copper eyes are a genuinely stunning combination."),
            (5, "Perfect for a quieter household", "I live alone and work from home and my British Longhair is the ideal companion for my lifestyle. She is present without being demanding. She sits near me while I work, moves to the sofa when I take breaks, and comes for a cuddle in the evenings on her terms. She is never disruptive. She is the most perfectly calibrated companion for a solo home worker I could have chosen."),
            (4, "Calm with children", "My British Longhair is patient and gentle with my children. She is not a playful, interactive cat but she tolerates their attention with dignified calm and seeks them out occasionally for gentle contact. She has never scratched or bitten despite some handling that pushed her patience. She signals clearly when she has had enough and retreats. Teaching my children to respect those signals has been a valuable lesson."),
            (5, "Elegant and beautiful", "My British Longhair is simply beautiful. She is round and fluffy and dignified and she knows it. She moves through the house with a self-possession that is genuinely impressive. She is not aloof in an unfriendly way, more self-contained and serene. She is affectionate with people she trusts and politely reserved with those she does not know. A wonderful, gracious companion."),
            (3, "Less interactive than I hoped", "I wanted a relatively low-maintenance cat that would still engage with me. My British Longhair is perhaps more reserved than I needed. She is beautiful and calm and pleasant company but she does not initiate interaction often and is content to be in the same room without making contact. She is not unfriendly but she is quite self-sufficient. A better fit for someone who enjoys a more independent companion."),
            (4, "Robust and healthy", "My British Longhair is eight years old and has had two minor health issues in that time. The breed is generally robust and my experience confirms it. He is vital, engaged with life, and shows no signs of age-related decline. His coat takes ongoing care but his health is excellent. He is a reliable, long-term companion who gives me confidence in his continued presence."),
            (5, "My grandchildren love her", "My elderly cat passed away two years ago and my grandchildren persuaded me to get another. My British Longhair is perfect for my situation. She is calm and gentle, manageable for me to care for, and patient and beautiful for my grandchildren to visit. She has brought warmth and life back to my home without the demands I was worried about managing at my age. She is a real treasure."),
        ],
    },
    "Burmilla": {
        "description": (
            "The Burmilla is an accidental creation from a 1981 cross between a Chinchilla Persian and a Burmese cat in the UK. "
            "Combining the best of both parent breeds, Burmillas are playful and sociable like Burmese but slightly calmer and more independent. "
            "Their distinctive silver-tipped coat and large green eyes make them strikingly beautiful cats with an equally attractive temperament."
        ),
        "pros": [
            "Playful but not as demanding as pure Burmese",
            "Sociable and affectionate with family",
            "Strikingly beautiful silver coat",
            "Good temperament with children and other pets",
        ],
        "cons": [
            "Coat needs regular grooming",
            "Less independent than some cats",
            "Relatively rare, limited breeder availability",
            "Can be vocal when wanting attention",
        ],
        "reviews": [
            (5, "The most beautiful cat I have ever owned", "My Burmilla's silver-tipped coat catches the light and she appears to shimmer when she moves. Her large green eyes are extraordinary. She is also wonderful to live with. She is playful without being exhausting, affectionate without being demanding, and sociable without being inappropriately forward with strangers. She is perfectly calibrated as a companion. I could not be more pleased with her."),
            (4, "Perfect balance of Burmese and Persian", "Having owned both Burmese and Persians, my Burmilla seems to have inherited the best of each. She has the Burmese sociability and playfulness without the intensity, and the Persian's calmer nature without the aloofness. She is the ideal middle ground between those two extremes. She is lovely to live with and has been healthy and robust in four years."),
            (5, "Great family cat", "My Burmilla has settled beautifully into our busy family home. She plays with the children, seeks out adults for quieter contact, and has integrated with our older cat without drama. She is sociable and adaptable and finds her own level of engagement with each family member. She is affectionate without being demanding and playful without being destructive. An ideal family cat."),
            (3, "Quite vocal at times", "My Burmilla is lovely but she is more vocal than I expected. She announces herself when entering rooms, comments on meals, and tells me clearly when her attention needs are not being met. She is not excessively demanding but she communicates assertively. I have come to enjoy the communication but it surprised me initially. Worth being aware of if you prefer a quieter cat."),
            (4, "Striking and sociable", "My Burmilla is the cat people always ask about. Her silver coat and green eyes are genuinely unusual and beautiful. She presents herself well and is sociable with visitors in a friendly, confident way that most cats are not. She is a wonderful representative of the breed and a pleasure to live with. Her coat needs brushing twice a week to maintain its beautiful condition."),
            (5, "My most harmonious cat", "I have had many cats over the years and my Burmilla is the most naturally harmonious to live with. She fits into routines without drama, does not disrupt sleep, and manages her own entertainment without destroying anything. She is warm and present without being demanding. She has the quality of being genuinely easy to share a home with while still being a fully engaging companion."),
            (4, "Intelligent and engaging", "My Burmilla figured out food puzzle toys faster than any cat I have owned. She is sharp and engaged and clearly enjoys mental stimulation. She invents her own games and has developed complex routines that she performs with obvious satisfaction. She is curious and interactive without the intensity of a fully Burmese cat. A wonderful, intelligent companion."),
            (5, "Best introduction to cat ownership", "My Burmilla was my first cat and she has been the perfect introduction to cat ownership. She is not too demanding or too independent. She is affectionate enough to make the relationship rewarding and self-sufficient enough not to be stressful. She has shown me the best aspects of cat companionship. I am completely converted to this breed and will always have a Burmilla."),
        ],
    },
    "Chausie": {
        "description": (
            "The Chausie is a large, athletic hybrid cat breed developed from crosses between domestic cats and the jungle cat of South Asia. "
            "Highly active, intelligent, and dog-like in their need for activity and human interaction, Chausies require experienced owners who can meet their significant mental and physical stimulation needs. "
            "They are stunning, wild-looking cats with friendly, loyal personalities toward their chosen family."
        ),
        "pros": [
            "Extraordinary athleticism and intelligence",
            "Loyal and deeply bonded to their family",
            "Striking, exotic appearance",
            "Interactive and engaging companion",
        ],
        "cons": [
            "Extremely high activity level requires constant stimulation",
            "Not suitable for inexperienced cat owners",
            "Can be destructive when under-stimulated",
            "Requires a raw or high-quality meat diet due to shortened intestines",
        ],
        "reviews": [
            (5, "Unlike any cat I have owned", "My Chausie is extraordinary. He is the size of a large domestic cat with the presence of something wild. He leaps to the top of seven-foot bookshelves from standing, runs circuits of the house at speed, and demands interactive play for hours every day. He is loyal to me in a way that feels more canine than feline. He waits for me, greets me at the door, and follows me everywhere. A remarkable, demanding, wonderful companion."),
            (4, "Demanding but incredible", "My Chausie requires more from me than any cat I have previously owned. Interactive play, puzzle feeders, environmental enrichment. Without these she is a creative problem-solver who applies her intelligence to dismantling my home. With them she is calm, satisfied, and the most engaging companion I have had. She is not a cat for a busy, low-energy household. For the right committed owner she is extraordinary."),
            (5, "Loyal beyond expectations", "My Chausie has bonded to me with an intensity I associate more with dogs than cats. She follows me from room to room, watches me with focused attention, and greets my return with vocal, physical enthusiasm. She is not unfriendly with others but she is fundamentally my cat. The bond we have developed is one of the most rewarding aspects of cat ownership I have experienced."),
            (3, "More wild than domestic", "I was drawn to the Chausie by its exotic appearance but I underestimated how much the wild ancestry affects its needs. My boy requires constant activity and stimulation that borders on exhausting to provide. He is not aggressive but he is genuinely difficult to manage without extensive environmental enrichment. He would be perfect for a committed enthusiast who understands hybrid cat needs. He was more than I bargained for."),
            (4, "Athletic beyond belief", "My Chausie moves in ways that seem physically improbable. She leaps, bounds, and navigates vertical spaces with fluid precision. Watching her move around my home is genuinely spectacular. She requires cat trees, running wheels, and interactive sessions to channel all that athleticism appropriately. For someone who finds the athletic capabilities of cats genuinely fascinating she is an extraordinary companion."),
            (5, "Wild beauty with loyal heart", "My Chausie looks like he escaped from a wildlife documentary and acts like my devoted shadow. The contrast between his wild appearance and his loyal, affectionate nature is one of the great delights of owning this breed. He is active and demanding but his loyalty and affection are real and deep. Living with him is like having a small, very athletic, very demanding wild thing that loves you unconditionally."),
            (4, "Needs specialist diet", "The dietary requirements of a Chausie are real and significant. She cannot tolerate grains or plant matter and requires a primarily raw or high-quality meat diet. This is a genuine ongoing cost and commitment. Her diet is now managed correctly and she is healthy and vital. But new owners should research this before committing. The dietary needs are not optional with this breed."),
            (5, "Changed my view of what a cat can be", "I thought I understood cats after twenty years of cat ownership. My Chausie changed that assumption completely. He is interactive, loyal, athletic, and present in a way no previous cat has been. He has expanded what I thought possible in the human-cat relationship. He is demanding and challenging and completely extraordinary. I would not have it any other way."),
        ],
    },
    "Colorpoint Shorthair": {
        "description": (
            "The Colorpoint Shorthair is a Siamese relative with colourpoint patterns in non-traditional colours including red, cream, tortoiseshell, and tabby points. "
            "Like their Siamese cousins, Colorpoints are vocal, opinionated, and intensely social cats who demand to be involved in their owners' lives. "
            "They are intelligent and affectionate but not suited to quiet households where they might not receive the interaction they need."
        ),
        "pros": [
            "Highly affectionate and bonded to their person",
            "Intelligent and interactive",
            "Striking colourpoint appearance in unusual colours",
            "Energetic and playful",
        ],
        "cons": [
            "Very vocal, can be demanding",
            "Needs significant human interaction",
            "Not suited to households where they will be alone frequently",
            "Can be prone to anxiety",
        ],
        "reviews": [
            (5, "The most communicative cat alive", "My Colorpoint Shorthair has opinions about everything and communicates them clearly and at length. She tells me about her day, complains about late meals, comments on visitors, and narrates her activities. Her voice is loud and she uses it constantly. I find it wonderful. She is deeply affectionate and follows me everywhere. For someone who wants a truly interactive cat she is extraordinary."),
            (4, "Siamese personality, unique colouring", "My Colorpoint has all the personality I love from Siamese cats in a beautiful red point package. He is vocal, clever, demanding, and deeply loving. He insists on being involved in everything I do. He is not a cat for a quiet household but for someone who enjoys an engaged, interactive companion he is everything you could want. His colouring is genuinely beautiful and unusual."),
            (5, "Bonded to me completely", "My Colorpoint Shorthair has chosen me as her person and the bond is extraordinary. She sleeps against me, follows me everywhere, greets me loudly when I return, and protests clearly when I leave. She is not anxious, just deeply attached. She gives me more active love than most dogs I have known. She has made living alone feel less solitary and more like a genuine partnership."),
            (3, "Too vocal for my apartment", "My Colorpoint is wonderful in many ways but the vocality has been a genuine challenge in my city apartment. She announces everything, every hunger, every preference, every arrival and departure. My neighbours have mentioned the volume twice. We are working on it but the Siamese vocal inheritance is strong. If you have close neighbours or prefer a quiet household this breed needs careful consideration."),
            (4, "Intelligent and trainable", "My Colorpoint has learned to come when called, sit on command, and retrieve small toys. He is sharper than any cat I have previously owned and engages with training games readily. He has learned that certain sounds predict food, play, or attention with impressive speed. His intelligence makes him an engaging, interactive companion who is never boring to live with."),
            (5, "Most affectionate cat I have had", "My Colorpoint sits on my chest in the evenings and purrs against my face. She pats my cheek with a soft paw when she wants attention. She drapes herself across my shoulders while I work. She is physically, persistently, wonderfully affectionate. She is also demanding and vocal but the affection she gives makes every demand worthwhile. I am completely devoted to her."),
            (4, "Striking appearance", "My Colorpoint Shorthair has a lynx point pattern in a beautiful cream and grey combination. She is one of the most striking cats I have ever seen and people always comment on her. She presents herself beautifully and her blue eyes are extraordinary. Her personality matches her appearance in intensity and beauty. A genuinely magnificent cat."),
            (5, "Perfect for working from home", "My Colorpoint Shorthair is the ideal work-from-home companion. He sits on my desk, narrates my video calls, and ensures I take regular breaks by demanding play. He keeps me company through long working days and makes the isolation of remote work much more manageable. He is vocal and present and completely wonderful. I could not imagine my workday without him."),
        ],
    },
    "Cymric": {
        "description": (
            "The Cymric is the longhaired variety of the Manx cat, sharing the same tailless or stumpy-tailed characteristic with a full, flowing coat. "
            "Playful, intelligent, and dog-like in their loyalty, Cymrics are devoted companions who enjoy being involved in household activities. "
            "They have a distinctive rounded appearance and a quiet, gentle temperament that makes them well-suited to family life."
        ),
        "pros": [
            "Gentle, loyal, and devoted to family",
            "Playful and dog-like in personality",
            "Good with children and other pets",
            "Quiet and undemanding",
        ],
        "cons": [
            "Longhaired coat requires regular grooming",
            "Some individuals prone to Manx syndrome (spinal issues)",
            "Tailless cats may have litter box challenges",
            "Relatively rare breed",
        ],
        "reviews": [
            (5, "The most dog-like cat I have owned", "My Cymric plays fetch without fail, comes when called, and greets me at the door every evening. He is quietly loyal in a way that feels more canine than feline. He follows me through the house with a rounded, stub-tailed dignity that is utterly charming. He is gentle with my children and patient with the dog. His flowing coat needs regular brushing but he is otherwise wonderfully easy to care for."),
            (4, "Unique and beautiful", "My Cymric's complete absence of tail is striking. She is fully rounded from every angle and moves with a characteristic rolling gait that I find charming. Her coat is long and silky and needs brushing every other day. She is gentle, quiet, and affectionate. She is not as vocal or demanding as some breeds and is easy to live with. A genuinely unique and beautiful companion."),
            (5, "Perfect gentle companion", "My Cymric is the quietest, gentlest cat I have ever owned. She is present and affectionate without being demanding. She seeks contact regularly but does not insist. She is patient with children, tolerant of the dog, and peaceful in every situation. She has made my home calmer simply by being in it. Her rounded tailless form and flowing coat are beautiful and distinctive."),
            (4, "Playful and entertaining", "My Cymric plays with toys with real enthusiasm and has invented games with household objects that entertain us both. He is interactive and engaging without being high-maintenance. He plays fetch consistently with small balls and brings them back with evident satisfaction. His dog-like qualities in a cat-sized package are a wonderful combination. His health has been excellent in five years."),
            (3, "Health check essential before buying", "My Cymric developed mild Manx syndrome at two years old affecting her hind mobility slightly. It is managed but the condition was distressing to discover. Any prospective Cymric or Manx owner should research Manx syndrome thoroughly and choose a reputable breeder who screens carefully for spinal issues. With good breeding the incidence is much lower. Breed from a tested line."),
            (5, "Quiet home companion", "My Cymric is the ideal companion for my quieter lifestyle. She is undemanding, serene, and content. She greets me when I come home, keeps me company in the evenings, and sleeps at my feet. She does not need constant entertainment or interaction. She is present and warm and peaceful. After years of higher-maintenance cats she is a wonderful relief. A truly harmonious companion."),
            (4, "Devoted and affectionate", "My Cymric has chosen me as her person and demonstrates it consistently. She sleeps pressed against me, follows me at a distance, and seeks me out when she needs contact. Her devotion is genuine and consistent. She is also independent enough not to be anxious when I am away. The balance of devotion and self-sufficiency is ideal."),
            (5, "Best family cat", "My Cymric has been our family cat for seven years and has been wonderful throughout. She is patient with the children, accepts the dog, and is affectionate with all family members without having a favourite. She is adaptable, calm, and wonderful. She has aged gracefully and is still active and engaged at seven. The perfect family companion."),
        ],
    },
    "European Shorthair": {
        "description": (
            "The European Shorthair is a natural cat breed from continental Europe, one of the oldest and most genetically diverse domestic cat populations. "
            "Hardy, adaptable, and balanced in temperament, European Shorthairs make excellent companions who are neither too demanding nor too aloof. "
            "They are excellent hunters with a natural robustness and an adaptable nature that suits both indoor and outdoor lifestyles."
        ),
        "pros": [
            "Hardy, healthy, and naturally robust",
            "Well-balanced, adaptable temperament",
            "Excellent hunter with natural instincts",
            "Generally long-lived and low-maintenance",
        ],
        "cons": [
            "May be too independent for owners wanting a very clingy cat",
            "Strong hunting instinct if allowed outdoors",
            "Less predictable temperament than purpose-bred breeds",
            "Availability varies significantly by region",
        ],
        "reviews": [
            (5, "The perfect natural cat", "My European Shorthair is the most naturally balanced cat I have ever owned. She is affectionate without being demanding, active without being destructive, and curious without being anxious. She has adapted to every change in our household without stress. She is healthy at twelve and shows it in her bright eyes and active lifestyle. She is the quintessential companion cat."),
            (4, "Hardy and independent", "My European Shorthair has been the easiest cat to care for in my twenty years of cat ownership. He is rarely unwell, adapts to any living situation, and is perfectly calibrated between affection and independence. He does not demand constant attention but he is warmly present when I am home. He is the ideal cat for a moderately busy lifestyle."),
            (5, "Excellent health record", "My European Shorthair is ten years old and has had one veterinary visit for anything other than routine care. The natural genetic diversity of this breed contributes to genuine hybrid vigour. He is robust, vital, and healthy in a way that purpose-bred cats sometimes are not. His longevity is a genuine gift. He is everything a companion cat should be."),
            (4, "Good with the whole family", "My European Shorthair accepts every member of my family at face value and interacts with each according to how they engage with her. She is playful with the children when they initiate play, calm with my elderly mother when she visits, and quietly present with me when I work. Her adaptability to different people and contexts is impressive."),
            (3, "Not as interactive as I hoped", "My European Shorthair is lovely but more independent than I wanted. She is affectionate on her schedule, which is not as frequent as I would prefer. She is pleasant company and never a problem but she does not seek contact often. She is a good companion for someone who appreciates a more self-sufficient cat. For someone who wants frequent interaction she might leave you wanting more."),
            (5, "Natural and authentic", "There is a naturalness to my European Shorthair that I appreciate deeply. She has not been bred for exaggerated features or extreme conformations. She is a naturally evolved, balanced cat who has adapted alongside humans for centuries. She is healthy, balanced in temperament, and genuinely harmonious to live with. She represents what a domestic cat can be at its best."),
            (4, "Excellent hunter", "My European Shorthair patrols the garden and has completely resolved the mouse situation that plagued us for years before we got her. She is a confident, efficient hunter with sharp instincts. She presents her catches with visible pride. Her hunting ability is one of the most practical benefits of owning this breed. Indoors she channels the same focused intelligence into toy play and puzzle feeders."),
            (5, "Long-lived and consistently wonderful", "My European Shorthair is fourteen years old and still going strong. He is slower and sleeps more than he did at two but he is still engaged with life. He sits in the garden in the mornings, investigates interesting smells, and still wants his interactive play sessions. The longevity of this breed is remarkable. Fourteen wonderful years and I hope for more."),
        ],
    },
    "Havana Brown": {
        "description": (
            "The Havana Brown is a rare, strikingly beautiful breed with a rich, warm chocolate-brown coat and vivid green eyes. "
            "Developed in England in the 1950s, Havana Browns are affectionate, curious, and quietly sociable cats who form close bonds with their families. "
            "They are known for exploring with their paws rather than their noses, reaching into things to investigate their environment."
        ),
        "pros": [
            "Affectionate and bonded to their family",
            "Curious and playful but not hyperactive",
            "Quiet and gentle temperament",
            "Strikingly beautiful coat and eye colour",
        ],
        "cons": [
            "Extremely rare, very few breeders available",
            "Can be reserved with strangers",
            "Needs companionship and does not do well alone",
            "Gene pool relatively narrow, potential health concerns",
        ],
        "reviews": [
            (5, "The most beautiful cat in the world", "My Havana Brown has a coat the colour of dark chocolate and eyes like polished jade. She is genuinely one of the most beautiful animals I have ever seen. Her personality matches her appearance. She is warm, curious, and deeply affectionate. She investigates everything with her paws in a way that is utterly charming. She is a genuinely rare and remarkable companion."),
            (4, "Curious and interactive", "My Havana Brown reaches into bags, boxes, and drawers to investigate their contents with his front paws. He touches everything before he looks at it. This habit is endearing and occasionally inconvenient. He is interactive, engaged, and curious without being destructive. He is affectionate with family and reserved with strangers until he has assessed them. A quietly wonderful companion."),
            (5, "Quiet and devoted", "My Havana Brown is the quietest, most devoted cat I have ever owned. She is present without being demanding. She follows me through the house at a discreet distance and seeks contact several times a day without insisting on it constantly. She is warm and gentle and deeply bonded to my household. Her chocolate coat is stunning and requires minimal care."),
            (3, "Very difficult to find", "My experience with my Havana Brown has been wonderful but the process of finding a reputable breeder took eighteen months of searching. The breed is critically rare and there are very few breeders. If you are drawn to this breed be prepared for a significant wait. It was worth it but the process was more difficult than I anticipated."),
            (4, "Gentle and family-friendly", "My Havana Brown has integrated beautifully into our family with children and another cat. She is gentle with the children and has established a peaceful coexistence with our other cat. She is not a dramatic, demanding cat. She is quietly present, warmly affectionate, and easy to live with. Her rarity makes her feel even more special."),
            (5, "Explores with paws, not nose", "The paw-first investigation habit of this breed is one of its most charming characteristics. My Havana Brown reaches into everything with exploratory paws before committing his nose to the investigation. He has a tactile relationship with the world that I find fascinating. He is intelligent, curious, and interactive in a very particular and delightful way."),
            (4, "Rare and wonderful", "Owning a Havana Brown feels like a privilege given their rarity. My girl is healthy, beautiful, and has been a wonderful companion for seven years. I was careful to choose a reputable breeder who tests for health conditions. Her gene pool concerns are real and breeding program health is important to research. A responsible approach yields a wonderful, healthy cat."),
            (5, "My most distinctive cat", "Of all the cats I have owned over the years my Havana Brown stands out as the most distinctive and memorable. Her chocolate coat, jade eyes, and paw-first curiosity are unique among all the cats I have known. She has been a genuinely special companion and I recommend this breed wholeheartedly to anyone who can find a reputable breeder."),
        ],
    },
    "Japanese Bobtail": {
        "description": (
            "The Japanese Bobtail is an ancient breed from Japan, known for its distinctive bunny-like bobbed tail and its role as a symbol of good luck in Japanese culture. "
            "Active, intelligent, and vocal, Japanese Bobtails are engaged companions who love to play and talk. "
            "The famous Maneki-neko, the waving lucky cat figurine, is modelled on this breed."
        ),
        "pros": [
            "Active, playful, and engaging personality",
            "Generally healthy with a diverse gene pool",
            "Sociable and good with children and other pets",
            "Comes in a wide variety of colours and patterns",
        ],
        "cons": [
            "Can be vocal and demanding of attention",
            "High activity level needs environmental enrichment",
            "May be challenging to find outside of Japan or specialist breeders",
            "Longhaired variety needs regular brushing",
        ],
        "reviews": [
            (5, "My lucky cat is truly lucky", "My Japanese Bobtail has been the most fortunate addition to my life. She is playful, vocal, and genuinely funny. She carries her bobbed tail upright like a flag and it bounces when she moves. She is an active, engaging presence in my home and has made me laugh every day for five years. She is healthy, energetic, and the embodiment of good fortune. I consider myself very lucky to have her."),
            (4, "Active and entertaining", "My Japanese Bobtail plays more actively than any cat I have previously owned. He chases, leaps, retrieves, and invents new games daily. His bobtail is distinctive and he carries it with apparent pride. He is vocal in a sing-song way that I find charming rather than annoying. He is genuinely entertaining to live with and has made my home feel livelier and more joyful."),
            (5, "Good luck charm personified", "My Japanese Bobtail is the living version of the Maneki-neko figure and she brings that same energy of warmth and good fortune to our home. She is sociable, affectionate, and genuinely joyful in her engagement with life. She gets on well with my children and my other cat. She is a beautiful, healthy, happy cat who has enriched our family life in every way."),
            (4, "Healthy and robust", "My Japanese Bobtail has been remarkably healthy in eight years. The natural gene pool of this ancient breed contributes to genuine robustness. She has had no significant health issues and is still active and engaged as she ages. The breed's longevity and health are genuine assets. She is a reliable, long-term companion who gives me confidence in continued years together."),
            (5, "Distinctive and beautiful", "My Japanese Bobtail's tricolour pattern and distinctive bobbed tail are beautiful and unique. She carries herself with elegant confidence and is immediately distinctive in appearance. Her tail puffs up when she is excited and gives her a permanently cheerful expression. She is as beautiful inside as out, gentle and sociable and warm."),
            (3, "More vocal than expected", "My Japanese Bobtail is a wonderful cat but he is more vocal than I anticipated. He narrates his activities, asks for things persistently, and talks back when I speak to him. I have grown fond of the communication but it was unexpected. If you prefer a quiet cat this breed needs careful consideration. If you enjoy conversation with your cat he is delightful."),
            (4, "Playful with my children", "My Japanese Bobtail is the ideal play companion for my children. She matches their energy when they want to play, signals clearly when she is done, and never resorts to claws. She is patient within reasonable limits and has taught my children to read her signals. She is a wonderful, active companion for a family with children."),
            (5, "Ancient breed, timeless companion", "My Japanese Bobtail connects me to a long tradition of human-cat companionship in Japan. She is a healthy, balanced cat who has evolved alongside humans for centuries. She is affectionate, active, and well-calibrated as a companion. Her distinctively bobbed tail and her good-natured personality make her a daily source of pleasure and I am grateful for every year with her."),
        ],
    },
    "Khao Manee": {
        "description": (
            "The Khao Manee is a rare Thai breed considered a symbol of good luck and traditionally kept by Thai royalty. "
            "Their name means white gem and they are distinguished by their pure white coat and distinctive odd-coloured or blue eyes. "
            "Active, sociable, and curious, Khao Manees are communicative cats who bond closely with their families."
        ),
        "pros": [
            "Strikingly beautiful white coat and unusual eye colours",
            "Sociable, curious, and interactive personality",
            "Generally good health when bred responsibly",
            "Bonds closely with family",
        ],
        "cons": [
            "White cats with blue eyes can be prone to deafness",
            "Extremely rare outside of Thailand",
            "High activity and stimulation needs",
            "Can be very vocal",
        ],
        "reviews": [
            (5, "The white gem lives up to her name", "My Khao Manee has a pure white coat that gleams and odd eyes, one blue and one gold, that are absolutely striking. She looks like a magical creature and has the personality to match. She is curious, sociable, and deeply affectionate. She treats every visitor as a new opportunity and approaches life with bright-eyed enthusiasm. She is genuinely one of the most beautiful and engaging cats I have ever owned."),
            (4, "Rare and remarkable", "Finding my Khao Manee took two years of searching and importing from Thailand. The process was involved but the cat I ended up with is extraordinary. He is striking in appearance, sociable in nature, and intelligent beyond my expectations. He is also tested as fully hearing despite his blue eyes, which is essential to verify with this breed. A genuinely rare and wonderful companion."),
            (5, "Royal cat indeed", "There is something genuinely regal about a Khao Manee. My girl carries herself with the calm confidence of a cat who has always known she was valued. She is sociable without being demanding, beautiful without being fragile, and intelligent without being mischievous. She is the most graceful cat I have owned and the most visually striking."),
            (3, "Deafness was a concern", "My Khao Manee is deaf in one ear due to the white coat gene. We discovered this at her first vet visit. She manages perfectly well with the assistance of visual cues and vibrations but it is worth knowing that deafness is a genuine risk in this breed, particularly with blue or odd eyes. Always have a Khao Manee hearing-tested by a vet before confirming purchase."),
            (4, "Sociable and interactive", "My Khao Manee is the most sociable cat I have owned. She greets everyone who enters my home with confident curiosity. She is not timid or reserved. She investigates new people and new things with bright enthusiasm. She is vocal and communicative and keeps me entertained with her commentary. A genuinely interactive, engaging companion."),
            (5, "Good luck cat brings good luck", "My Khao Manee arrived in the same week that several good things happened in my life. Coincidence perhaps but I am happy to credit her. She is a wonderful cat, healthy and bright and affectionate. She is a beautiful, positive presence in my home and I genuinely feel fortunate to have her. The legend of her good luck feels apt."),
            (4, "Beautiful and healthy", "My Khao Manee is six years old and completely healthy. She was hearing-tested clear before purchase and her pure white coat is immaculate. She is active, bright, and engaged with life. The breed is generally healthy when bred responsibly and my experience confirms this. She is a wonderful, long-term companion who I hope to enjoy for many more years."),
            (5, "My most unusual and beautiful cat", "Of all the cats I have owned my Khao Manee is the most striking. Her pure white coat and odd eyes draw comment everywhere she is seen in photos. She is as beautiful in personality as in appearance, warm, curious, and deeply affectionate. She has been a source of daily delight and I recommend this breed wholeheartedly to anyone who can find a responsible breeder."),
        ],
    },
    "Korat": {
        "description": (
            "The Korat is one of the oldest and rarest natural cat breeds, originating in Thailand where it is considered a symbol of good luck and prosperity. "
            "With their distinctive silver-blue coat and heart-shaped face with large luminous green eyes, Korats are unique in appearance and intensely devoted in temperament. "
            "They are known for their strong bonds with their chosen person and their quiet, gentle demeanour."
        ),
        "pros": [
            "Devoted and deeply bonded to their person",
            "Quiet, gentle, and undemanding",
            "Naturally healthy and robust constitution",
            "Beautiful distinctive appearance",
        ],
        "cons": [
            "Can be possessive of their chosen person",
            "May not tolerate other cats easily",
            "Sensitive to loud environments",
            "Relatively rare outside of specialist breeders",
        ],
        "reviews": [
            (5, "Silver blue perfection", "My Korat is quite simply perfect. Her silver-blue coat and luminous green eyes are stunning. She has chosen me as her person and demonstrates it with quiet, consistent devotion. She is not a demanding cat but she is always present, always near, always available for contact. She is gentle, undemanding, and quietly wonderful. I have never owned a cat with such a specific and profound bond."),
            (4, "Devoted to one person", "My Korat is mine and tolerates the rest of my family politely but without particular warmth. He follows me specifically, sleeps on my side of the bed, and greets only my return from work with enthusiasm. He is not hostile to others, simply uninterested. For a single person or a couple where he can choose a primary person he is extraordinary. In a large family where he is expected to bond broadly he might be less satisfying."),
            (5, "Most beautiful eyes of any breed", "My Korat's luminous green eyes are described as peridot and the comparison is apt. They are large, expressive, and extraordinary. She is striking to look at from every angle. Her personality is as beautiful as her appearance. She is gentle, devoted, and quietly loving. She is everything I wanted in a companion cat and more."),
            (3, "Does not tolerate other cats", "My Korat is wonderful with me but she has been unable to accept our other cat despite eighteen months of careful introduction. She is not aggressive but she is persistently stressed by the presence of another cat in her space. We now manage them separately which is manageable but not ideal. If you have or plan to have multiple cats this breed may not be the best choice."),
            (4, "Quiet and serene companion", "My Korat is one of the quietest cats I have owned. He vocalises occasionally but does not demand attention verbally. His communication is through presence and physical contact rather than sound. He is a calming presence in my home and has the quality of making a room feel more peaceful simply by being in it. A wonderful companion for a quieter lifestyle."),
            (5, "Traditional good luck personified", "My Korat is the traditional good luck cat of Thailand and she feels like it. She is healthy, beautiful, and a genuinely positive presence in my home. She has been uncomplicated to care for, requiring minimal veterinary attention in seven years. She is a serene, devoted companion who has enriched my daily life. I consider myself fortunate to have her."),
            (4, "Beautiful and healthy", "My Korat has been remarkably healthy throughout her life. The breed is known for robust natural health and my experience confirms it. She has had no significant health issues in nine years. She is active, bright, and engaged. Her silver-blue coat is easy to maintain and always beautiful. A low-maintenance, long-lived companion."),
            (5, "Most bonded cat I have ever had", "The bond my Korat has formed with me is unlike anything I have experienced with a cat. He is present and attentive in a way that feels deeply intentional. He sleeps with me, follows me through the house, and sits next to me whenever I am still. He is not clingy or anxious, just fundamentally attached. Living with him feels like a genuine partnership and I treasure it."),
        ],
    },
    "LaPerm": {
        "description": (
            "The LaPerm is a unique curly-coated cat breed that originated from a natural mutation in Oregon in 1982. "
            "Their distinctive wavy or curly coat ranges from loose waves to tight ringlets and is remarkably low-shedding for a longhaired cat. "
            "LaPerms are affectionate, curious, and moderately active cats known for their gentle nature and adaptability."
        ),
        "pros": [
            "Curly coat is low-shedding and relatively allergy-friendly",
            "Affectionate and gentle temperament",
            "Curious and moderately active without being high-maintenance",
            "Good with children and other pets",
        ],
        "cons": [
            "Curly coat needs careful grooming to prevent matting",
            "Relatively rare breed",
            "Can be attention-seeking",
            "Some individuals have variable curl quality",
        ],
        "reviews": [
            (5, "The most unique coat I have ever seen", "My LaPerm's coat is extraordinary. Tight ringlets fall from her head to her tail and she has a magnificent curly ruff. When you part the fur you find waves all the way to the skin. She is genuinely unique in appearance and people always reach out to touch her before they have been introduced. She is gentle and affectionate and accepts this attention graciously. An extraordinary, beautiful cat."),
            (4, "Good for mild allergies", "My husband has mild cat allergies and my LaPerm is the only cat he does not react to significantly. We tested carefully before committing and three years later he remains reaction-free around her. Her low-shedding curly coat genuinely makes a difference. Beyond the allergy benefit she is a wonderful cat, affectionate and gentle and moderately active. An ideal allergy-friendly companion."),
            (5, "Gentle and adaptable", "My LaPerm has adapted to every change in our household without stress. New babies, a house move, a new dog, all met with calm curiosity and rapid adjustment. She is the most adaptable cat I have owned. She is affectionate with everyone in the household and integrates new members smoothly. Her gentle nature makes her ideal for a family environment that changes and grows."),
            (4, "Unique conversation starter", "My LaPerm is the most commented-on cat I have ever owned. Her curly coat is so distinctive that every visitor wants to touch it and photograph it. She is patient with the attention and genuinely seems to enjoy being admired. She is sociable and friendly with visitors and has been a wonderful social icebreaker. Beyond her unusual appearance she is a warm, affectionate companion."),
            (3, "Grooming more complex than expected", "The curly coat requires more careful grooming than I anticipated. Standard brushing can damage the curl pattern. I had to learn specific techniques for curly coats to maintain hers properly. Once I adjusted my approach she has been fine but it was a learning curve. The coat is beautiful but research curly-coat grooming before getting this breed."),
            (5, "Gentle with my shy children", "My children are quite shy and my LaPerm's gentle, non-pushy approach has been perfect for them. She approaches slowly, waits for them to engage, and does not demand attention. Over time she has won over both children who now seek her out for cuddles. Her patience and gentleness have made her an excellent companion for shy, hesitant children."),
            (4, "Moderately active and manageable", "My LaPerm is neither hyperactive nor sedentary. She plays enthusiastically when offered interaction and rests contentedly between sessions. She does not demand entertainment or become destructive when left to herself. She is the ideal companion for a moderately busy lifestyle, engaged and interactive when I am available and perfectly content when I am not."),
            (5, "A living work of art", "My LaPerm is a living work of art. Her curls cascade beautifully and her movement has a fluid grace that her unusual coat enhances. She is the most visually distinctive cat I have ever had the pleasure of living with. Her personality is as beautiful as her appearance, warm and gentle and genuinely engaged with the people around her."),
        ],
    },
    "Lykoi": {
        "description": (
            "The Lykoi is a relatively new and strikingly unusual cat breed whose name means wolf in Greek, reflecting its partially hairless, werewolf-like appearance. "
            "A natural mutation was discovered in domestic cat populations and selectively bred from 2011. "
            "Despite their eerie appearance, Lykois are affectionate, playful, and highly loyal to their families."
        ),
        "pros": [
            "Unique and striking appearance",
            "Affectionate and loyal to family",
            "Playful and energetic personality",
            "Generally sociable once comfortable",
        ],
        "cons": [
            "Patchy coat requires special skin care",
            "Can be initially wary of strangers",
            "Moults almost completely periodically",
            "Relatively new breed with limited health history",
        ],
        "reviews": [
            (5, "My little werewolf is wonderful", "My Lykoi looks like a creature from a horror film and behaves like the warmest, most affectionate companion imaginable. The contrast is one of the most delightful things about this breed. He moults periodically and becomes almost hairless before growing back into his spooky coat. He is loyal, playful, and deeply bonded to me. I love his unusual appearance and his wonderful personality equally."),
            (4, "Unique and captivating", "My Lykoi is the most unusual cat I have ever owned. Her partial hairlessness and roan coloration give her an appearance that makes people look twice. She is initially wary of strangers which contributes to the werewolf impression, but she warms up quickly and becomes genuinely friendly once she has assessed someone as safe. With our family she is warm, playful, and affectionate."),
            (5, "Most loyal cat I have owned", "My Lykoi is loyal in a way I associate more with dogs than cats. He follows me everywhere, greets my return enthusiastically, and is distressed when I am away for more than a day. He is deeply bonded to me specifically and less engaged with other members of my household, though he is friendly with them. His loyalty is one of the most remarkable and touching aspects of the breed."),
            (3, "Skin care is ongoing", "My Lykoi's partially hairless skin requires regular care. The exposed skin can get oily and needs wiping weekly. During moulting periods she can appear almost completely bald which was surprising the first time. She is healthy and the skin care is manageable but it was not something I fully appreciated before getting her. New owners should research Lykoi skin care needs thoroughly."),
            (4, "Playful and energetic", "My Lykoi plays with an intensity that belies his unusual appearance. He is fast, focused, and highly motivated by interactive toys. His play style is more hunting-oriented than most cats I have owned, stalking and pouncing with genuine predatory focus. He channels this into play effectively and is never destructive. He is a genuinely engaging, active companion."),
            (5, "Conversation starter cat", "My Lykoi is the most unusual cat in our neighbourhood and she generates conversation everywhere. Photos of her on social media get enormous engagement. In person she is initially alarming to some people but her warm personality quickly wins them over. She has made me more approachable and social through the curiosity she generates. A wonderful, unique companion."),
            (4, "New breed with good temperament", "My Lykoi is from a responsible breeder who has been carefully health-testing from the beginning. As a newer breed the health history is shorter than established breeds but responsible breeders are building that track record carefully. My cat has been healthy in four years. The breed seems robust and the temperament is genuinely wonderful. Worth researching breeders carefully for this newer breed."),
            (5, "Love him exactly as he is", "My Lykoi is not conventionally beautiful. He is strange-looking and people sometimes recoil at his appearance. I love every unusual inch of him. His patchy coat, his yellow eyes, his periodic moulting. He is completely himself and completely wonderful. He has taught me to look past the surface and find the warmth beneath. A genuinely special, extraordinary cat."),
        ],
    },
}

BREED_DATA.update(_BREED_DATA_CATS1)

_BREED_DATA_CATS2: dict = {
    "Nebelung": {
        "description": (
            "The Nebelung is a rare, long-haired variant of the Russian Blue with a shimmering blue-grey coat and striking green eyes. "
            "Their name means creature of the mist in German, reflecting their ethereal, shimmering appearance. "
            "Nebelungs are reserved, gentle, and deeply devoted to their close family while being cautious with strangers."
        ),
        "pros": [
            "Gentle, devoted, and loyal to their family",
            "Beautiful shimmering blue-grey coat",
            "Quiet and undemanding",
            "Generally good health",
        ],
        "cons": [
            "Reserved with strangers, can take time to warm up",
            "Semi-long coat requires regular brushing",
            "Can be sensitive to changes in routine",
            "Relatively rare",
        ],
        "reviews": [
            (5, "The most ethereal cat I have owned", "My Nebelung truly looks like a creature of the mist. Her blue-grey coat shimmers in certain light and her green eyes are extraordinary. She is reserved with strangers but deeply devoted to me and my household. She follows me quietly, seeks contact on her terms, and purrs with remarkable resonance when content. She is beautiful, serene, and genuinely special. I am completely devoted to her."),
            (4, "Reserved but deeply loyal", "My Nebelung took six weeks to fully trust me after I brought him home. He approached with increasing confidence as he settled. Now he is my most devoted companion, sleeping near me every night and seeking contact regularly. He is still cautious with strangers but that is part of his nature. His trust once earned is absolute and deeply rewarding."),
            (5, "Quiet and serene", "My Nebelung is the most peaceful cat I have ever owned. She vocalises rarely, does not demand attention, and is simply beautifully present in my home. She sits in the window watching the world with luminous green eyes. She is the living definition of quiet companionship. For someone who wants presence without noise or demand she is perfectly calibrated."),
            (4, "Shimmering beauty", "The coat of a Nebelung is genuinely unlike any other. Each hair has a silver tip that catches light and gives the entire coat a shimmering, misty quality. My boy is beautiful in all lights but particularly in the morning sun where his coat appears almost to glow. He is a quiet, gentle companion who is worth the twice-weekly brushing his coat requires."),
            (3, "Slow to warm to strangers", "My Nebelung hides when visitors come and sometimes stays hidden for the duration of a visit. She is wonderful with our immediate family but her caution with strangers is significant. We have worked on gradual introductions and she is better than she was but it is a temperament characteristic rather than something that disappears with training. If you have frequent visitors this breed may find that stressful."),
            (5, "Long-lived and healthy", "My Nebelung is eleven years old and still beautiful and engaged with life. He has had no significant health issues in eleven years. The breed shares the Russian Blue's genetic robustness and it shows. He is slower and sleeps more than he did at three but he is vital and present. Eleven wonderful, quiet years with this beautiful creature and I hope for more."),
            (4, "Perfect for quiet households", "My Nebelung is perfectly suited to my quiet, two-person household. She is content in calm environments, adapts to a predictable routine, and never demands more than gentle, consistent care. She is not the right cat for a busy, unpredictable household. For a calm, settled environment she is a genuinely wonderful companion."),
            (5, "Most beautiful cat I have ever seen", "I have owned many cats over the years and my Nebelung is without question the most beautiful. Her coat is genuinely extraordinary and she carries herself with natural elegance. Her personality is as beautiful as her appearance, gentle and devoted and quietly wonderful. She is everything I could have wanted in a companion cat."),
        ],
    },
    "Ocicat": {
        "description": (
            "The Ocicat is a domestic spotted cat bred to resemble a wild ocelot but with no wild blood in its lineage. "
            "Created from Abyssinian, Siamese, and American Shorthair crosses, Ocicats combine striking spotted beauty with an affectionate, sociable temperament. "
            "They are active, playful, and adaptable cats who are often described as dog-like in their loyalty and trainability."
        ),
        "pros": [
            "Striking spotted coat resembling a wild cat",
            "Friendly, sociable, and adaptable",
            "Trainable and dog-like in loyalty",
            "Active and playful without being hyperactive",
        ],
        "cons": [
            "Needs significant interaction and stimulation",
            "Can be vocal",
            "Does not do well left alone for long periods",
            "Coat can vary in intensity of spotting",
        ],
        "reviews": [
            (5, "Wild looks, domestic heart", "My Ocicat has the spotted coat of an ocelot and the personality of a devoted companion. She is striking in appearance and her spots are beautifully defined. She is sociable, playful, and genuinely interactive. She comes when called, plays fetch reliably, and follows me with the consistency of a dog. She is everything I hoped for in an exotic-looking domestic cat."),
            (4, "Beautiful and trainable", "My Ocicat has learned to sit, shake, and come on command. He retrieves small toys and has learned several behaviours through clicker training. He is sharp and engaged and genuinely enjoys the interaction of training sessions. He is active and needs stimulation but he is not exhausting. A wonderful, intelligent companion with a truly beautiful coat."),
            (5, "Most sociable cat in my experience", "My Ocicat is the most socially engaged cat I have ever owned. She greets every visitor with confident curiosity, investigates everything, and involves herself in all household activities. She is never shy or withdrawn. Her wild appearance combined with her friendly domesticity is one of the great pleasures of this breed. She has made my home more lively and social."),
            (4, "Great with other cats and dogs", "My Ocicat has integrated with my dog and my other cat without drama. She is confident and socially flexible, approaching other animals with curiosity rather than fear. She has established friendly relationships with both. Her adaptability to a multi-pet household is impressive and has made our complex household harmonious."),
            (3, "Needs more company than I expected", "My Ocicat is wonderful when I am home but she struggles with long periods alone. She has been destructive on days when I work late. We have addressed this with a second cat and interactive feeders but her companionship needs are real and ongoing. If you are frequently away for long periods this breed needs additional company or stimulation."),
            (5, "Stunning and engaging", "My Ocicat turns heads wherever she appears in photographs. Her tawny spotted coat is genuinely beautiful and her athletic, muscular build is impressive. In person she is warm, curious, and engaging. She is the most visually striking cat I have owned and has a personality that matches her appearance in warmth and vibrancy."),
            (4, "Active and athletic", "My Ocicat moves with athletic precision and plays with focused intensity. He is not destructive but he needs environmental enrichment to channel his energy. Cat trees, puzzle feeders, and interactive sessions keep him engaged. He is a genuinely athletic cat who is satisfying to watch in motion. His coat is beautiful and his energy is a joy to channel."),
            (5, "Best conversation piece cat", "My Ocicat generates more conversation and compliments than any cat I have previously owned. People cannot believe she has no wild blood. She is a wonderful ambassador for a breed that is genuinely remarkable in appearance and temperament. I have converted several people to Ocicats simply by having them meet mine."),
        ],
    },
    "Oriental Shorthair": {
        "description": (
            "The Oriental Shorthair is a close relative of the Siamese, sharing the same svelte, angular body type but available in over 300 colour and pattern combinations. "
            "Highly intelligent, vocal, and deeply social, Orientals are extraordinarily interactive cats who form intense bonds with their people. "
            "They thrive in busy, engaged households where they can participate fully in daily life."
        ),
        "pros": [
            "Extremely intelligent and trainable",
            "Affectionate and deeply bonded to their person",
            "Available in remarkable variety of colours and patterns",
            "Playful and interactive throughout life",
        ],
        "cons": [
            "Very vocal and demanding of attention",
            "Does not tolerate solitude well",
            "Highly active, needs stimulation",
            "Can be jealous of other pets",
        ],
        "reviews": [
            (5, "The most intelligent cat I have met", "My Oriental Shorthair is the most intelligent cat I have encountered in thirty years of cat ownership. She has learned to open doors, respond to over fifty words, and can solve complex puzzle feeders in seconds. She is always one step ahead. She is also intensely demanding of attention and engagement. Living with her is like having a very clever, slightly demanding child. She is extraordinary."),
            (4, "Vocal and engaging", "My Oriental is the most communicative cat I have owned. He narrates his activities, comments on my behaviour, and tells me exactly what he needs. The volume and frequency of his communication was surprising initially but I have grown to love it. He is deeply affectionate and loyal. His conversations with me are one of the most engaging aspects of living with this breed."),
            (5, "Angular beauty and big personality", "My Oriental Shorthair has the most striking, angular appearance of any cat I have owned. Her large ears, almond eyes, and long, elegant body are perfectly proportioned. She carries herself with theatrical confidence. Her personality is as dramatic as her appearance. She is the most intensely present, engaged companion I have had. She makes every day more interesting."),
            (3, "Too demanding for my lifestyle", "My Oriental is wonderful but he needs more engagement than I consistently have time to provide. He becomes vocal, restless, and occasionally destructive when his needs are not met. He is best suited to a home where someone is present most of the time and genuinely enjoys active interaction. For a busy person who is out frequently he is a poor match."),
            (4, "Incredible variety of colours", "My Oriental Shorthair is a stunning chocolate solid colour that is unlike any cat I have previously owned. The breed comes in hundreds of colour and pattern combinations which makes finding your ideal aesthetic straightforward. The personality is consistent across colour varieties. She is beautiful, engaging, and wonderfully distinctive."),
            (5, "Devoted beyond all expectation", "My Oriental has chosen me as her person and the bond is absolute. She sleeps pressed against me, follows me everywhere, and greets my return with theatrical enthusiasm. Her loyalty and devotion exceed anything I have experienced from any cat. She is intense and demanding but the depth of the bond she offers in return is extraordinary."),
            (4, "Perfect for working from home", "My Oriental is the ideal work-from-home companion because he keeps me engaged, forces me to take breaks for play, and provides constant company. He narrates my video calls, investigates my work, and ensures I am never lonely. For someone who works from home and wants an active, interactive presence, he is genuinely wonderful."),
            (5, "Changed my relationship with cats", "My Oriental Shorthair changed what I thought possible in a human-cat relationship. She is more interactive, more bonded, and more present than any cat I imagined possible. She has made me rethink what I want in a companion animal. She is demanding and extraordinary and I would choose her again every single time."),
        ],
    },
    "Peterbald": {
        "description": (
            "The Peterbald is an elegant, hairless or partly haired Russian breed created in 1994 from a cross between a Donskoy and an Oriental Shorthair. "
            "They inherit the angular, graceful body of the Oriental and the hairless or sparse coat of the Donskoy. "
            "Peterbalds are affectionate, intelligent, and highly social cats who bond intensely with their families."
        ),
        "pros": [
            "Extremely affectionate and bonded to family",
            "Intelligent and interactive",
            "Various coat types from hairless to short brush coated",
            "Sociable with other pets and people",
        ],
        "cons": [
            "Needs regular skin care (oily skin in hairless varieties)",
            "Sensitive to cold and sun",
            "Very social, does not tolerate isolation well",
            "Can be expensive due to rarity",
        ],
        "reviews": [
            (5, "Elegance in a hairless form", "My Peterbald is the most elegant cat I have ever owned. Her angular, graceful body and large ears give her the appearance of a living sculpture. She is also the most affectionate and socially engaged cat I have had. She sleeps under my duvet, follows me everywhere, and participates in every household activity. Her warmth to the touch is remarkable. A genuinely extraordinary companion."),
            (4, "Intensely social and warm", "My Peterbald is never cold in temperature or in personality. He generates remarkable warmth and seeks contact constantly. He sleeps against me for body warmth and for affection in equal measure. He is demanding of interaction but gives affection abundantly in return. His skin needs weekly cleaning but it is manageable. He is one of the most rewarding cats I have owned."),
            (5, "Beautiful and bonded", "My Peterbald is beautiful in an unconventional way. Her sparse, velvety coat and angular features are striking and unique. She bonds intensely with everyone in my household and manages her attachments generously. She is warm, engaged, and wonderfully interactive. Living with her is like having a very elegant, hairless shadow."),
            (3, "Cold weather management required", "My Peterbald struggles in winter. She seeks warm spots obsessively and shivers when temperatures drop below comfortable indoor levels. We keep the house warmer than we otherwise would and she has a heated cat bed. The cold sensitivity is real and requires planning. She is wonderful in warm conditions. Just be prepared to manage the cold season carefully."),
            (4, "Interactive beyond expectation", "My Peterbald plays fetch, comes when called, and has learned several training behaviours with clicker training. She is more interactive than most cats I have owned. Her intelligence is evident in her problem-solving and in the speed with which she learns new things. She is genuinely engaging to live with."),
            (5, "Most responsive cat I have owned", "My Peterbald responds to his name, to tone of voice, and to body language with accuracy that surprises me daily. He anticipates my routine and positions himself accordingly. He knows that certain sounds predict interesting things. He is one of the most responsive, attuned companions I have had in any species. Extraordinary intelligence in an elegant form."),
            (4, "Good with other pets", "My Peterbald has integrated beautifully with our dog and our other cat. She is sociable and confident in multi-pet environments and seems genuinely to enjoy company. She is not territorial or aggressive. She is a warm, adaptable companion who makes multi-pet households harmonious. Her social flexibility is one of her great strengths."),
            (5, "Living sculpture", "My Peterbald is like a living work of art. Her long lines, large ears, and graceful movement are endlessly beautiful to observe. She is also wonderfully warm in personality. She is everything beautiful about cats in a unique, unconventional package. I am devoted to her and to this extraordinary breed."),
        ],
    },
    "Pixiebob": {
        "description": (
            "The Pixiebob is an American breed developed from cats believed to be naturally occurring bobcat hybrids, though no wild DNA has been confirmed. "
            "With a spotted coat, heavy brow, and short or bobbed tail, Pixiebobs have a distinctly wild appearance. "
            "Their temperament is dog-like, loyal, and highly sociable, making them devoted family companions."
        ),
        "pros": [
            "Dog-like loyalty and sociability",
            "Adapts well to leash walking",
            "Good with children and other pets",
            "Polydactyly common and adds charm",
        ],
        "cons": [
            "Large size, not suitable for very small living spaces",
            "Needs significant human interaction",
            "Coat can be high maintenance in longhaired variety",
            "Relatively rare breed",
        ],
        "reviews": [
            (5, "The most dog-like cat I have owned", "My Pixiebob comes on walks on a leash, plays fetch, and waits for me at the door each evening. He is loyal, sociable, and entirely un-catlike in the stereotypical sense. He gets along with my dog and my children equally well. His bobbed tail wags slightly when he is happy. He is a remarkable, unique companion who has completely changed how I think about cats."),
            (4, "Wild appearance, domestic heart", "My Pixiebob's heavy brow, spotted coat, and wild expression make her look like she belongs in a wildlife reserve. Her personality is entirely domestic and warm. She is affectionate with family, tolerant of children, and adaptable to our busy household. She is large and muscular and moves with natural grace. A beautiful and engaging companion."),
            (5, "Perfect family cat", "My Pixiebob has been the ideal family cat. She is large and robust, tolerating the energetic attention of my children with patience. She is sociable with visitors and has integrated perfectly with our dog. She is playful and interactive without being hyperactive. Her dog-like sociability makes her feel more like a part of the family than many cats I have owned."),
            (4, "Leash walking is a genuine joy", "I walk my Pixiebob on a leash every morning and it has been one of the unexpected pleasures of owning this breed. He takes to the harness naturally and explores the neighbourhood with curious confidence. People who see him assume he is a small wild cat and are amazed to learn he is a domestic breed. Our walks are genuinely wonderful and have improved both our daily routines."),
            (3, "Large cat needs space", "My Pixiebob is a large, muscular cat and my small apartment does not suit him well. He needs space to move and explore that my flat does not provide adequately. He is not destructive but he is restless in small spaces. He would be much better suited to a house with outdoor access or at least a large indoor environment. A wonderful cat in the right setting."),
            (5, "Unusual and wonderful", "My Pixiebob is the most distinctive cat I have owned. Her polydactyl paws, bobbed tail, and spotted coat make her genuinely striking. Her personality is open, loyal, and engaging. She has expanded my understanding of what cats can be and do. I am completely devoted to her and would recommend this breed enthusiastically to anyone who wants an extraordinary companion."),
            (4, "Healthy and robust", "My Pixiebob is seven years old and has been remarkably healthy throughout his life. He is a large, solid cat who seems naturally robust. He has had no significant health issues. His longhaired coat requires twice-weekly brushing but is otherwise low-maintenance. He is a reliable, long-term companion who gives me confidence in his continued vitality."),
            (5, "Best decision I ever made", "I researched cats for a year before deciding on a Pixiebob and the research paid off. He has been exactly what I hoped for, loyal, interactive, gentle, and genuinely dog-like in his companionship. He has made my home warmer and my life richer. He is the best pet decision I have made in twenty years of animal ownership."),
        ],
    },
    "Ragamuffin": {
        "description": (
            "The Ragamuffin is a large, fluffy breed closely related to the Ragdoll, developed from Ragdoll breeding stock with additional outcrossing. "
            "Like Ragdolls, Ragamuffins are famous for going limp when held and for their docile, gentle temperament. "
            "They are affectionate, patient, and good-natured cats who are highly adaptable to family life."
        ),
        "pros": [
            "Exceptionally gentle and patient temperament",
            "Good with children and other pets",
            "Luxurious, low-mat coat despite its length",
            "Adapts well to indoor family life",
        ],
        "cons": [
            "Semi-long coat needs regular brushing",
            "Can be prone to obesity without diet management",
            "May not alert to danger due to docile nature",
            "Slower to mature than some breeds",
        ],
        "reviews": [
            (5, "The gentlest cat in existence", "My Ragamuffin goes completely limp when I pick her up. She is a warm, purring, trusting weight in my arms. She accepts everything with absolute calm. She has never scratched or bitten despite my young children's occasionally overwhelming affections. She is the most fundamentally gentle and trusting creature I have ever known. She has made my home feel warmer and calmer simply by being in it."),
            (4, "Fluffy and docile", "My Ragamuffin is enormous, fluffy, and impossibly docile. He adapts to everything without complaint. House move, new baby, new dog, all met with placid equanimity. He is large enough to feel substantial when held but goes completely relaxed in your arms. His coat needs brushing twice a week but it is silky and relatively easy to manage. A wonderful, easygoing companion."),
            (5, "Perfect for my young children", "My children are four and six and my Ragamuffin is the ideal companion for them. She is patient beyond any other animal I have owned, accepting dress-up games, tail examination, and enthusiastic handling with gracious calm. She signals politely when she has had enough by moving away, never by scratching. She has been a truly wonderful family cat."),
            (4, "Beautiful and calm", "My Ragamuffin is genuinely beautiful. Her coat is dense and silky in a warm golden colour that photographers love. She is calm and serene in her daily life, sitting in sunny spots, accepting affection warmly, and moving through the house with unhurried grace. She is the most restful animal I have owned. Living with her lowers my blood pressure noticeably."),
            (3, "Coat is more work than expected", "My Ragamuffin is wonderful but the coat requires more attention than I anticipated from a breed sometimes described as low-maintenance. She mats if I miss brushing sessions and her seasonal blow-outs require daily attention. I now have a dedicated grooming routine and she is fine but new owners should go in with realistic expectations about the coat care commitment."),
            (5, "My therapy cat", "My Ragamuffin has been an unofficial therapy animal for me through a difficult health period. He goes limp in my arms, purrs with extraordinary resonance, and simply stays. He has a quality of calm, warm presence that is genuinely therapeutic. He has made my recovery easier and more bearable. He is the most comforting animal companion I have ever had."),
            (4, "Adaptable and harmonious", "My Ragamuffin has adapted to our multi-pet household without drama. She established peaceful relationships with our two other cats and our dog quickly and without conflict. She seems naturally harmonious and conflict-averse. She is the most diplomatically skilled cat I have owned. She makes communal living easier for everyone in the household."),
            (5, "Wonderful and reliable", "My Ragamuffin is seven years old and has been consistently wonderful throughout. He is healthy, calm, and reliably affectionate. He has never had a difficult phase. He has been exactly what I hoped for from day one and has maintained that standard every year since. He is the most consistent, reliable, and wonderful companion I have ever owned."),
        ],
    },
    "Scottish Straight": {
        "description": (
            "The Scottish Straight is the straight-eared version of the Scottish Fold, sharing the same round face and plush coat but without the folded ear mutation. "
            "Calm, gentle, and adaptable, Scottish Straights have the same lovely temperament as Scottish Folds but without the associated cartilage health concerns. "
            "They are affectionate, sociable, and well-suited to family life."
        ),
        "pros": [
            "Gentle, calm, and adaptable temperament",
            "No folded-ear related health concerns",
            "Good with children and other pets",
            "Plush, beautiful coat",
        ],
        "cons": [
            "Coat requires regular brushing",
            "Can be prone to weight gain",
            "Less distinctive in appearance than the Fold",
            "May be overlooked in favour of the more famous Fold",
        ],
        "reviews": [
            (5, "All the charm without the health concerns", "My Scottish Straight has all the wonderful temperament of the Scottish Fold without the cartilage issues that concern me about the Fold. She is round-faced, calm, and deeply affectionate. She is gentle with everyone and adapts to our household changes without stress. Her straight ears give her a slightly different look but the same gorgeous, round, teddy-bear quality. A perfect choice."),
            (4, "Calm and family-friendly", "My Scottish Straight is the easiest, most harmonious cat I have ever owned. He is calm in all situations, gentle with my children, and tolerant of our boisterous household. He is not demanding or vocal. He seeks affection regularly but does not insist. He has integrated with our dog and other cat beautifully. A genuinely easy, wonderful companion."),
            (5, "Round-faced sweetness", "My Scottish Straight has the most beautifully round face and the most serene expression of any cat I have owned. She looks perpetually content and she genuinely is. She is calm, warm, and regularly delightful. She approaches life with equanimity and seems genuinely at peace with her existence. She has made my home calmer and more pleasant by her presence."),
            (4, "Good health is reassuring", "I specifically chose a Scottish Straight over a Fold because of my concerns about the ear-related health issues in Folds. My Straight is four years old and entirely healthy. I am much more comfortable with the ethics of supporting a cat without an artificially induced health condition. The temperament is identical to what I understand the Fold to be. A wonderful, healthy choice."),
            (3, "Less distinctive looking", "My Scottish Straight is a lovely cat with a wonderful temperament. I chose her specifically to avoid the Fold's health concerns. But I have to acknowledge that she draws fewer comments and less attention than her Fold counterparts. If the distinctive folded ear look is what draws you to the breed, the Straight will be a slight aesthetic compromise. If temperament is your priority she is perfect."),
            (5, "Sweet and undemanding", "My Scottish Straight is the most undemanding cat I have owned. He is present, affectionate, and pleasant without ever being pushy or demanding. He asks for contact occasionally and accepts it warmly. He is content with a calm routine and reliable company. He is the perfect companion for a quieter lifestyle or for someone who wants feline company without high-maintenance emotional needs."),
            (4, "Beautiful plush coat", "My Scottish Straight's coat is dense and plush like a teddy bear. It needs brushing twice a week to maintain its beautiful condition. She is patient during grooming and the sessions are genuinely pleasant for both of us. She enjoys the attention and I enjoy the result. Her coat is one of her most beautiful features and worth the regular care."),
            (5, "Ethical and wonderful", "Choosing a Scottish Straight over a Fold was an ethical decision for me and I am very glad I made it. My cat is healthy, happy, and has all the wonderful qualities associated with the breed without the health compromise. She is the ideal cat for someone who loves the Scottish cat type but wants to make a responsible choice."),
        ],
    },
    "Serengeti": {
        "description": (
            "The Serengeti is a relatively new American breed developed in the 1990s to resemble the African serval without using wild cat blood. "
            "Created from crosses between Oriental Shorthairs and Bengals, Serengetis have a spotted coat, long legs, and large ears that give them a striking wild appearance. "
            "They are active, friendly, and highly social cats who need plenty of stimulation and interaction."
        ),
        "pros": [
            "Striking wild appearance with completely domestic temperament",
            "Friendly and sociable with people and other pets",
            "Active and engaging companion",
            "Healthy due to diverse breeding",
        ],
        "cons": [
            "Very high energy requires significant environmental enrichment",
            "Vocal and communicative",
            "Needs significant interaction",
            "Relatively rare, limited breeders available",
        ],
        "reviews": [
            (5, "The serval without the wild complications", "My Serengeti has the appearance of a small serval with her spots, long legs, and enormous ears. She moves with the grace and athleticism of something wild. Her personality is entirely domestic and warm. She is sociable, friendly, and deeply affectionate with my family. She looks like she belongs in Africa and acts like she belongs on my sofa. The contrast is wonderful."),
            (4, "Athletic and engaging", "My Serengeti is the most athletic cat I have ever owned. She leaps to extraordinary heights from standing, runs circuits of the house with focused speed, and plays with intense predatory focus. She needs significant environmental enrichment to channel all that energy. With adequate stimulation she is a wonderful, engaging companion. Without it she is creatively destructive."),
            (5, "Sociable and warm", "My Serengeti is the most sociable cat I have owned. She greets every visitor with confident curiosity, integrates with other pets easily, and seems genuinely to enjoy company. She is vocal and communicative in a pleasant way. She is warm and present with everyone who enters our home. A genuinely sociable and engaging companion."),
            (3, "Energy level was a challenge initially", "My Serengeti was more active than I anticipated in his first year. He needed more stimulation than I was providing and became destructive when bored. We invested in cat trees, running wheels, and interactive sessions and he settled significantly. He is now wonderful but the energy management required real commitment. Be prepared for a very active cat."),
            (4, "Beautiful spotted coat", "My Serengeti's spotted coat is genuinely beautiful. Her spots are clear, well-defined, and give her a striking, exotic appearance. She catches attention everywhere she appears in photographs. Her coat is short and requires minimal care. She is beautiful and unique looking and her personality is as warm as her appearance is striking."),
            (5, "Wild beauty, gentle soul", "My Serengeti looks like she escaped from a wildlife documentary and behaves like a warm, gentle, devoted companion. The contrast between her wild appearance and her domestic sweetness is one of the great pleasures of this breed. She is loyal to my family, gentle with my children, and playful without being overwhelming. A truly wonderful breed."),
            (4, "Good with my other cats", "My Serengeti has integrated with my existing cats better than I expected. She is socially confident without being aggressive. She established relationships with each cat at their own pace and is now on genuinely friendly terms with both. Her sociability extends to feline companions as well as people. A harmonious addition to a multi-cat household."),
            (5, "Changed my view of domestic cats", "My Serengeti's wild appearance and energetic personality have expanded my appreciation of what domestic cats can be. She is beautiful, athletic, intelligent, and genuinely companionable. She makes me appreciate the depth of what has been achieved in selective breeding. A remarkable, beautiful, wonderful breed."),
        ],
    },
    "Singapura": {
        "description": (
            "The Singapura is the smallest recognised cat breed, originating from Singapore where street cats called drain cats were discovered. "
            "Despite their tiny size, Singapuras have enormous eyes, big ears, and personalities to match their expressive faces. "
            "They are curious, affectionate, and surprisingly active, delighting in climbing and playing well into old age."
        ),
        "pros": [
            "Tiny size is manageable in small living spaces",
            "Curious, playful, and full of energy despite small size",
            "Affectionate and people-oriented",
            "Large expressive eyes and unique appearance",
        ],
        "cons": [
            "Very active for their size, needs stimulation",
            "Can be demanding of attention",
            "Coat is ticked tabby only, no colour variety",
            "Some lines prone to certain genetic conditions",
        ],
        "reviews": [
            (5, "The world's smallest cat with the biggest personality", "My Singapura weighs four pounds and has more personality than cats three times her size. She is curious, bold, and fearlessly investigative. She climbs to the highest points in my home, plays with total commitment, and sleeps pressed against my face. Her enormous eyes observe the world with constant wonder. She is the most adorable and engaging cat I have ever owned."),
            (4, "Tiny but mighty", "My Singapura is the smallest cat I have ever owned but he is fearless. He approaches the dog, investigates every visitor, and has claimed the highest cat tree shelf as his territory. He plays with feather toys until I give up before he does. He is affectionate and demanding in equal measure. His size means he can go anywhere and does."),
            (5, "Perfect apartment cat", "My Singapura is perfectly suited to my small city flat. She is tiny, low impact, and easily satisfied with indoor enrichment. She gets her exercise through climbing, interactive toys, and play sessions with me. She is affectionate and keeps me company without demanding huge amounts of space. A wonderful little cat for urban living."),
            (4, "Enormous eyes are genuinely stunning", "My Singapura's eyes are so large relative to her face that she looks permanently surprised and delighted. They are luminous and expressive and people always comment on them. She uses them to communicate with precision, widening them when excited, narrowing them when content. Her whole face is a constant stream of expressive communication."),
            (3, "More active than her size suggests", "My Singapura is tiny but requires significant enrichment and interaction. She is not a sedentary lap cat. She zooms around the house, leaps extraordinary distances for her size, and demands interactive play every day. She is not destructive but she is persistently active. For someone wanting a calm, quiet companion her energy level was surprising."),
            (5, "Loving and engaging", "My Singapura is the most engaging cat I have owned in thirty years of cat ownership. She is always doing something interesting, always investigating, always curious. She involves herself in everything I do. She is affectionate and present in a way that makes living alone feel genuinely companionable. She is tiny and completely wonderful."),
            (4, "Long-lived for her size", "My Singapura is twelve years old and still as active and curious as she was at three. Small cats often live longer than large ones and my Singapura bears this out beautifully. She is bright, vital, and engaged with the world. Twelve wonderful years with this tiny, remarkable cat and I hope for more."),
            (5, "Best little cat", "My Singapura is the best small cat I have ever owned. She is a bundle of energy, curiosity, and affection in the tiniest possible package. She is the most efficient cat in terms of personality per pound. She has made my home livelier, warmer, and funnier. I could not imagine my flat without her and I would choose her again without a moment's thought."),
        ],
    },
    "Snowshoe": {
        "description": (
            "The Snowshoe is an American breed created from Siamese and American Shorthair crosses, recognisable by its distinctive white-mittened paws and blue eyes. "
            "They combine the pointed colouring of the Siamese with the white markings of the American Shorthair, creating a uniquely beautiful cat. "
            "Snowshoes are sociable, affectionate, and moderately vocal, making them excellent family companions."
        ),
        "pros": [
            "Distinctive and beautiful appearance",
            "Affectionate and sociable without being excessively demanding",
            "Good with children and other pets",
            "Moderately active, suitable for various lifestyles",
        ],
        "cons": [
            "Can be vocal, inheriting Siamese tendencies",
            "White mittened pattern must meet specific standards for showing",
            "Needs companionship, does not do well alone for long",
            "Relatively rare outside the USA",
        ],
        "reviews": [
            (5, "The most beautiful marked cat", "My Snowshoe has the most precise and beautiful markings of any cat I have owned. Her white paws are perfectly symmetrical, her blue eyes are vivid, and her colourpoint pattern is clear and beautiful. She is stunning to look at. She is also wonderfully affectionate and sociable without being demanding. She is everything I hoped for in a companion cat."),
            (4, "Sociable and warm", "My Snowshoe is the most sociable cat I have owned. He greets visitors, integrates with pets, and is genuinely friendly without being pushy. He is moderately vocal, inheriting something of the Siamese expressiveness but in a more moderate form. He is affectionate with my family and has been a wonderful addition to our household. His distinctive paws always draw comment."),
            (5, "Wonderful family cat", "My Snowshoe has been the perfect family companion. She is patient with my children, sociable with their friends, and adapts to our busy household without stress. She is not hyperactive or demanding. She is present, warm, and engaging at a sustainable level. She has been everything I wanted in a family cat and she is beautiful besides."),
            (4, "Moderate temperament is ideal", "My Snowshoe has the ideal moderate temperament for my lifestyle. She is active enough to be engaging, calm enough to be restful. She is vocal enough to be communicative without being overwhelming. She is affectionate without being demanding. She is the ideal middle ground in temperament and I find her a genuinely easy, pleasant companion."),
            (3, "White markings difficult to breed predictably", "My Snowshoe is a wonderful cat but I want to mention that the white mitten markings are notoriously difficult to breed predictably. My girl's markings are slightly asymmetrical which is not a health issue but affects her showability. If you intend to show a Snowshoe, be prepared that perfect markings are not guaranteed. For a pet companion this is entirely irrelevant but worth knowing."),
            (5, "Loyal and affectionate", "My Snowshoe is devoted to my family in a warm, generous way. She is not attached to one person but distributes her affection across the household with apparent pleasure. She sleeps with different family members on different nights, sits with whoever is in the living room, and greets everyone's return from work or school. She is a genuinely warm and inclusive companion."),
            (4, "Blue eyes are extraordinary", "My Snowshoe's blue eyes are as vivid and striking as any cat's eyes I have ever seen. They are a deep, saturated blue that seems to glow in certain light. Combined with her white paws and pointed colouring she is a genuinely beautiful cat. Her personality matches her appearance with warmth and beauty."),
            (5, "Easy to love", "My Snowshoe is the easiest cat I have ever loved. She is not complicated, not demanding, and not high-maintenance. She is simply warm, beautiful, and genuinely pleasant to share a home with. She has made my daily life better in a quiet, consistent way. I am grateful for her every day."),
        ],
    },
    "Sokoke": {
        "description": (
            "The Sokoke is one of the rarest domestic cat breeds in the world, originating from the Arabuko-Sokoke forest in Kenya. "
            "Discovered in the late 1970s from a feral population, Sokokes have a distinctive modified tabby pattern called African tabby. "
            "They are active, agile, and have a wild character that requires experienced cat owners."
        ),
        "pros": [
            "Extremely rare and historically unique breed",
            "Active, athletic, and engaging",
            "Generally good health from diverse gene pool",
            "Unique African tabby coat pattern",
        ],
        "cons": [
            "Extremely rare, very difficult to find outside Scandinavia",
            "Can be reserved with strangers",
            "Needs significant activity and enrichment",
            "Not suitable for very indoor-restricted environments",
        ],
        "reviews": [
            (5, "The rarest and most fascinating cat I have owned", "My Sokoke is one of the rarest cats in the world and owning her feels like a genuine privilege. Her African tabby pattern is unlike any other cat's markings. She is active and engaging, more wild-feeling than most domestic breeds. She is reserved with strangers but deeply bonded to my household. She is a truly extraordinary companion for someone who appreciates rare and genuine breeds."),
            (4, "Wild spirit, domestic heart", "My Sokoke has an energy and presence that feels slightly wild. He moves with a quickness and certainty that is different from other breeds. He is bonded to our family but reserved with strangers. He is active and needs space and stimulation. With the right environment and committed owners he is a fascinating, beautiful companion."),
            (5, "Unique in every way", "My Sokoke's coat pattern is genuinely unlike anything I have seen. The African tabby has a characteristic woody appearance that is stunning. She is athletic and engaged and has a quality that feels ancient and authentic. She is not an easy cat but she is a remarkable one. For an experienced cat owner who wants something truly unusual she is extraordinary."),
            (4, "Healthy and robust", "My Sokoke has been remarkably healthy in five years. The natural gene pool from the Arabuko-Sokoke forest population contributes to genuine hybrid vigour. She is robust and vital and shows none of the health issues that can affect more intensively bred breeds. Her health is one of the great practical benefits of owning a naturally evolved breed."),
            (3, "Very difficult to find", "The search for my Sokoke took over two years and eventually required importing from Scandinavia where most breeding programmes exist. The breed is critically rare and the process of finding a responsible breeder was extended and expensive. The cat herself is wonderful but new owners should be fully prepared for a significant wait and potentially an international purchase."),
            (5, "African forest cat in a domestic setting", "My Sokoke feels like a connection to something ancient and wild. She came from breeding lines that trace to feral cats in a Kenyan forest. She carries that history in her movement and her spirit. She is a genuine domestic cat but with a depth and authenticity that purpose-bred cats sometimes lack. She is one of the most fascinating animals I have ever had the honour of living with."),
            (4, "Bonds deeply with family", "My Sokoke is reserved with strangers but her bond with our family is deep and real. She follows us, seeks contact on her schedule, and is genuinely attached. It took patience to build the relationship but the reward is a deeply bonded companion who has chosen us with intention. Her trust once earned is absolute and precious."),
            (5, "Worth the effort to find", "The two years it took me to find a Sokoke was completely worth it. She is everything I hoped for, rare, beautiful, wild-feeling, and genuinely bonded to me. She is the most extraordinary cat I have ever owned. I urge anyone drawn to this breed to persist in their search. The reward is a companion unlike any other."),
        ],
    },
    "Toyger": {
        "description": (
            "The Toyger is an American designer breed developed from domestic shorthaired cats to resemble a miniature tiger, with bold, branching stripes on an orange-toned background. "
            "Begun in the 1980s, the breed is still being developed with the goal of creating an ever more tiger-like appearance. "
            "Toygers are friendly, intelligent, and easygoing, making them appealing companions as well as striking show cats."
        ),
        "pros": [
            "Striking tiger-like appearance in a domestic cat",
            "Friendly, calm, and easygoing temperament",
            "Trainable and responsive",
            "Good with children and other pets",
        ],
        "cons": [
            "Expensive due to rarity and breeding programme",
            "Still being developed, so appearance can vary",
            "Limited breeder availability outside the USA",
            "Coat pattern quality varies significantly between individuals",
        ],
        "reviews": [
            (5, "My miniature tiger is magical", "My Toyger has the most extraordinary coat I have ever seen on a domestic cat. Her stripes are bold, clear, and have a branching quality that genuinely resembles a tiger's markings. She is beautiful beyond description. Her personality is equally wonderful, friendly, calm, and adaptable. She is the conversation-starting, magazine-cover cat of my dreams. I adore her completely."),
            (4, "Beautiful and friendly", "My Toyger is one of the most beautiful cats I have ever owned. His tiger-striped coat is genuinely spectacular. His personality is equally appealing, calm, friendly, and easy to live with. He is trainable, responds to his name, and adapts easily to our household routine. He is not hyperactive or demanding. He is a beautiful, harmonious companion."),
            (5, "Tiger in my living room", "People who see my Toyger in photographs assume she is a wild cat. In person the illusion is even more convincing. She is genuinely tiger-like in her markings and moves with a fluid grace that enhances the impression. Her personality is entirely domestic and warm. She is affectionate, sociable, and easy to love. She is the most dramatic-looking cat I have owned."),
            (4, "Friendly and adaptable", "My Toyger has been the easiest cat to integrate into my household. He adapted within a week, established peaceful relationships with my other cats, and settled into routine without drama. He is friendly with visitors and calm in varied situations. His temperament is genuinely easygoing and makes him a pleasure to live with."),
            (3, "Expensive with variable markings", "My Toyger cost significantly more than any cat I have previously purchased. The breed is expensive due to the specialised breeding programme. I was also surprised to find that the tiger-like markings vary considerably between individuals and not every Toyger achieves the dramatic look of the best examples. Research specific kittens carefully and be prepared for the cost."),
            (5, "Most striking cat I have owned", "My Toyger is the most visually striking cat in my thirty years of cat ownership. Her coat is genuinely magnificent and her presence in any room is immediately noticed. She is also a wonderful companion, friendly, calm, and genuinely pleasant to live with. Beautiful and good-natured. I could not ask for more."),
            (4, "Trainable and responsive", "My Toyger has learned several behaviours through positive reinforcement training. She comes when called, sits on command, and retrieves small toys. She is more trainable than most cats I have owned. Her intelligence is evident in the speed with which she learns and the reliability of her responses. A genuinely engaging companion to train."),
            (5, "Worth every cent", "My Toyger was the most expensive cat purchase I have made and she has been worth every penny. She is healthy, beautiful, friendly, and genuinely extraordinary to live with. She has enriched my life in ways I did not anticipate. The beauty of her coat, the warmth of her personality, and the pleasure of her daily company have more than justified the investment."),
        ],
    },
    "Tiffanie": {
        "description": (
            "The Tiffanie is a semi-longhaired cat breed developed in the UK from Burmilla breeding, combining a silky, flowing coat with the warm, sociable personality of the Burmese line. "
            "Gentle, affectionate, and intelligent, Tiffanies make excellent companions who are engaged without being hyperactive. "
            "Their beautiful coat and calm temperament make them popular choices for families and individuals alike."
        ),
        "pros": [
            "Gentle, warm, and affectionate personality",
            "Beautiful semi-long silky coat",
            "Sociable without being overly demanding",
            "Good with children and other pets",
        ],
        "cons": [
            "Semi-long coat needs regular brushing",
            "Relatively rare outside the UK",
            "Can be vocal",
            "Needs company and does not thrive in isolation",
        ],
        "reviews": [
            (5, "The most beautiful temperament", "My Tiffanie combines a silky, beautiful coat with a temperament that is warm and gentle without being demanding. She seeks affection regularly and accepts it with gracious pleasure. She is sociable with visitors, patient with children, and harmonious in a multi-pet household. She is the most beautifully balanced cat I have ever owned. Her appearance and personality are equally gorgeous."),
            (4, "Silky beauty with a kind heart", "My Tiffanie's coat is extraordinarily silky and beautiful. It flows and shimmers and makes her look like a cat from a painting. It needs brushing every other day to maintain its condition but it is wonderful to brush. She is affectionate and engaging and has been a wonderful companion. She is not hyperactive or demanding. She is warm, gentle, and consistently lovely."),
            (5, "Perfect family companion", "My Tiffanie has integrated into our family with seamless grace. She is gentle with my children, sociable with visitors, and harmonious with our other cat. She is not a demanding cat but she is warmly present. She seeks affection regularly and gives it generously. She is the ideal balance of engaged companion and self-sufficient cat."),
            (4, "Rare and wonderful", "My Tiffanie was difficult to find and I waited eight months for her. She has been completely worth the wait. She is beautiful, healthy, and has a temperament that is everything I hoped for. The breed is rare and worth seeking out from a responsible breeder who can demonstrate good health records. A truly special, lovely cat."),
            (3, "Coat requires more attention than I expected", "My Tiffanie's silky coat is beautiful but it mats if I miss brushing sessions. I underestimated the grooming commitment. She needs brushing every other day and professional grooming twice a year to keep her coat in good condition. Beyond the coat she is a wonderful cat. New owners should go in with realistic expectations about the grooming time required."),
            (5, "Gentle and sociable", "My Tiffanie is the most naturally harmonious cat I have owned. She fits into every situation without drama or difficulty. She is gentle, warm, and consistently pleasant. She seeks contact regularly and her affection is warm and real. She has made my home more pleasant simply by being in it. A genuinely wonderful breed."),
            (4, "Beautiful indoor companion", "My Tiffanie is a wonderful indoor companion. She is content with indoor life when provided with sufficient enrichment and interaction. She is not restless or destructive. She plays happily with appropriate toys and is content to observe the world from her window perch. She is a calm, beautiful, pleasant indoor cat."),
            (5, "Most loving cat I have had", "My Tiffanie gives love more openly and consistently than any cat I have previously owned. She seeks affection multiple times a day, accepts it with purring contentment, and gives warmth back abundantly. She has made living alone feel genuinely companionable. She is my favourite cat in many years of cat ownership."),
        ],
    },
    "Ukrainian Levkoy": {
        "description": (
            "The Ukrainian Levkoy is a distinctive, hairless cat breed developed in Ukraine in the 2000s from crosses between Scottish Fold and Donskoy cats. "
            "They have a unique appearance with folded ears, a hairless or nearly hairless body, and large, almond-shaped eyes. "
            "Despite their unusual appearance, Levkoys are affectionate, gentle, and sociable cats who bond closely with their families."
        ),
        "pros": [
            "Highly distinctive and unusual appearance",
            "Affectionate and devoted to family",
            "Sociable and good with other pets",
            "Rarely triggers allergies due to minimal coat",
        ],
        "cons": [
            "Skin requires regular cleaning",
            "Sensitive to cold and sun exposure",
            "Extremely rare outside Ukraine and Russia",
            "Folded-ear inheritance may carry health concerns",
        ],
        "reviews": [
            (5, "The most unusual and loving cat", "My Ukrainian Levkoy is the most unusual-looking animal I have ever owned. Her folded ears, wrinkled hairless skin, and large eyes give her an otherworldly appearance that draws comment everywhere. Her personality is entirely warm and ordinary in the best sense. She is affectionate, sociable, and deeply devoted to our family. She is wonderful and unlike anything else I have owned."),
            (4, "Unique and affectionate", "My Levkoy looks like something from another world and behaves like the warmest, most devoted companion. He is hairless with folded ears that give him an alert, curious expression. He is affectionate without being demanding, sociable without being pushy. He needs skin care and temperature management but his personality makes every extra effort worthwhile."),
            (5, "Conversation piece and companion", "My Levkoy generates more curiosity and comment than any cat I have ever owned. Her appearance is genuinely extraordinary. She also happens to be a wonderful companion, warm and affectionate and easy to live with once her skin care needs are accommodated. She is a rare privilege to own and I treasure her daily."),
            (3, "Cold sensitivity is significant", "My Levkoy struggles in cold conditions and requires a heated environment year-round. She shivers below comfortable room temperature and seeks warm spots with determination. We keep our home warmer than we otherwise would and she has a heated bed. The cold management is a real ongoing commitment. In a warm climate or a very warm home this would be much less of an issue."),
            (4, "Good for allergies", "My husband has significant cat allergies but does not react to my Levkoy. Her minimal coat means minimal allergen in the environment. We tested carefully before committing and the results have held for two years. Beyond the allergy benefit she is a wonderful, affectionate, sociable cat who has brought genuine joy to our household."),
            (5, "Rare treasure", "Owning a Ukrainian Levkoy feels like owning something genuinely rare and precious. She is from a newly developed breed with a very small worldwide population. She is healthy, beautiful in her unusual way, and a wonderful companion. I feel privileged to have her and would recommend the breed enthusiastically to anyone who can find a responsible breeder."),
            (4, "Devoted and warm", "My Levkoy is deeply devoted to our family in a warm, generous way. He is not attached to one person but bonds with everyone in the household. He sleeps with different family members, greets everyone's return, and distributes his affection democratically. He is a warm and inclusive companion who has made our household feel more connected."),
            (5, "Beautiful inside and out", "My Levkoy is not conventionally beautiful but she is beautiful to me in every way. Her unusual appearance is unique and distinctive. Her personality is warm, affectionate, and genuine. She has enriched my life and my home with her presence. She is everything I wanted in a companion cat and presented in the most extraordinary-looking package imaginable."),
        ],
    },
    "York Chocolate": {
        "description": (
            "The York Chocolate is a rare American breed developed in the 1980s in New York state from a natural litter of chocolate-coloured kittens. "
            "With their rich chocolate or chocolate and white semi-long coat and affectionate, playful temperament, York Chocolates are charming and devoted companions. "
            "The breed remains very rare and is not formally recognised by all major cat registries."
        ),
        "pros": [
            "Beautiful rich chocolate or bicolour coat",
            "Affectionate and devoted to family",
            "Playful and sociable personality",
            "Generally healthy from diverse background",
        ],
        "cons": [
            "Extremely rare, very few breeders worldwide",
            "Semi-long coat needs regular grooming",
            "Not formally recognised by all registries",
            "Limited health data due to small population",
        ],
        "reviews": [
            (5, "The rarest and most beautiful brown cat", "My York Chocolate has the most beautiful rich, warm brown coat I have ever seen on a cat. The colour is deep and lustrous and unlike any other breed's colouring. She is affectionate, playful, and deeply devoted to our family. Finding her took considerable research and time but she has been absolutely worth every effort. A genuinely rare and beautiful companion."),
            (4, "Warm and devoted", "My York Chocolate is one of the warmest, most devoted cats I have owned. He follows me through the house, seeks contact regularly, and purrs with remarkable frequency. His rich brown coat is beautiful and requires brushing twice a week to maintain. He is a genuinely lovely cat with an unusual and beautiful appearance."),
            (5, "Chocolate perfection", "My York Chocolate is every shade of warm brown possible, from milk chocolate on her points to rich dark chocolate on her back. She is beautiful from every angle. Her personality is equally beautiful, warm, playful, and genuinely affectionate. She is one of the most rewarding cats I have had the pleasure of owning. I am deeply grateful to the breeder who helped me find her."),
            (4, "Playful and sociable", "My York Chocolate is more playful than I expected from a semi-longhaired breed. She plays enthusiastically with toys, chases laser points with focused intensity, and initiates play sessions regularly. She is sociable with visitors and has integrated well with my other cat. She is a genuinely active, engaging companion with a beautiful coat."),
            (3, "Finding a breeder was a genuine challenge", "My York Chocolate search took nearly two years. The breed is critically rare and there are very few breeders. I eventually found one through a specialist cat registry in the USA. The search was extended and frustrating but the cat I eventually brought home is wonderful. Anyone drawn to this breed should be prepared for a very long search and potentially an international purchase."),
            (5, "Rare treasure", "My York Chocolate is one of fewer than a few hundred of her breed in the world. Owning her feels like a genuine privilege and a responsibility. She is healthy, beautiful, and a wonderful companion. I feel connected to something rare and worth preserving. I support her breed through responsible ownership and advocacy for the breed's continuation."),
            (4, "Beautiful coat, great temperament", "My York Chocolate has the most distinctive coat colour of any cat I have owned. His warm chocolate colour is rich and deep. Combined with his affectionate, playful temperament he is the most rewarding cat purchase I have made. He needed grooming attention from the start but his silky coat responds well to regular brushing."),
            (5, "Worth every effort to find", "The eighteen months I spent finding my York Chocolate were completely worth it. She is everything I hoped for, rare, beautiful, affectionate, and healthy. She is a genuine connection to a very rare breed that deserves more recognition and support. She has brought warmth, beauty, and joy to my home. I recommend this breed wholeheartedly to anyone with the patience to find one."),
        ],
    },
}

BREED_DATA.update(_BREED_DATA_CATS2)


def main() -> None:
    import sys
    import os

    # Allow running from any directory by adding the project root to path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, script_dir)

    from app import create_app, db
    from app.models import Subject, Review

    app = create_app("development")

    added_total = 0
    skipped_total = 0
    not_found_total = 0

    with app.app_context():
        for name, data in BREED_DATA.items():
            subject = Subject.query.filter_by(name=name).first()
            if subject is None:
                logger.warning(f"Subject not found in DB: {name!r} — skipping")
                not_found_total += 1
                continue

            # Update description, pros, cons
            subject.description = data["description"]
            subject.pros = "\n".join(data["pros"])
            subject.cons = "\n".join(data["cons"])

            slug = subject.slug
            rng = random.Random(hash(name) % 100000)

            all_reviews = data["reviews"]
            count = rng.randint(5, 12)
            # Sample without replacement if possible
            sample_size = min(count, len(all_reviews))
            picked = rng.sample(all_reviews, sample_size)

            added_for_breed = 0
            for i, (rating, title, body) in enumerate(picked):
                original_url = f"sample-{slug}-{i}"
                existing = Review.query.filter_by(original_url=original_url).first()
                if existing:
                    skipped_total += 1
                    continue

                author = _rnd_name(rng)
                review = Review(
                    subject_id=subject.id,
                    rating=rating,
                    title=title,
                    body=body,
                    author_name=author,
                    source_site="sample",
                    is_published=True,
                    original_url=original_url,
                )
                db.session.add(review)
                added_for_breed += 1
                added_total += 1

            db.session.flush()
            subject.update_stats()
            logger.info(
                f"  {name}: description/pros/cons updated, {added_for_breed} reviews added"
            )

        db.session.commit()

    logger.info(
        f"Done. Added {added_total} reviews, skipped {skipped_total} duplicates, "
        f"{not_found_total} breeds not found in DB."
    )


if __name__ == "__main__":
    main()
