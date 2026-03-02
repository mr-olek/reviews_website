#!/usr/bin/env python3
"""
Replace generic template reviews for Plants & Garden with specific, data-driven
reviews referencing real care tips, seasonal notes, pests, propagation, and
growing contexts.

Usage:
  python3 generate_plant_reviews.py                    # all plant types
  python3 generate_plant_reviews.py --slug roses       # single subcategory
  python3 generate_plant_reviews.py --start-from cacti # resume from subcategory
  python3 generate_plant_reviews.py --count 15         # reviews per subject (default 15)
"""
from __future__ import annotations
import argparse, os, random, sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# Plant-type-specific facts, keyed by subcategory slug
# ---------------------------------------------------------------------------
PLANT_DATA = {
    'roses': {
        'care_tips':  [
            'deep watering at the base rather than overhead',
            'deadheading spent blooms to encourage reblooming',
            'applying rose-specific granular fertiliser in early spring',
            'pruning to an outward-facing bud at a 45-degree angle',
        ],
        'display':    [
            'a sunny south-facing garden border',
            'a cottage garden mixed planting with lavender',
            'a dedicated rose bed with good air circulation',
            'a trellis or pergola for climbing varieties',
            'a large terracotta pot on a sunny patio',
        ],
        'issues':     [
            'black spot fungal disease on the leaves',
            'aphid infestations on new growth',
            'rose dieback from hard winter frosts',
            'powdery mildew in humid summers',
        ],
        'traits':     [
            'repeat-flowering over a long season',
            'exceptional fragrance on warm afternoons',
            'dense double blooms with a classic silhouette',
            'strong disease-resistant root stock',
        ],
        'seasons':    [
            'first flush of blooms in late spring',
            'peak flowering through midsummer',
            'hips forming in autumn for wildlife interest',
            'bare canes in winter showing the plant\'s architecture',
        ],
    },
    'succulents': {
        'care_tips':  [
            'watering only when the soil is completely dry',
            'using a gritty well-draining cactus compost mix',
            'providing at least six hours of bright indirect light',
            'avoiding water on the rosette centre to prevent rot',
        ],
        'display':    [
            'a sunny windowsill in a terracotta pot',
            'a shallow dish garden arrangement',
            'a vertical living wall frame',
            'a fairy garden or miniature landscape',
            'an office desk with a grow light',
        ],
        'issues':     [
            'root rot from overwatering and poor drainage',
            'etiolation from insufficient light',
            'mealybug infestations in leaf crevices',
            'leaf drop in cold or draughty positions',
        ],
        'traits':     [
            'water-storing fleshy leaves in geometric rosettes',
            'extremely low maintenance between waterings',
            'wide range of colours from blue-grey to red',
            'easy propagation from leaf cuttings',
        ],
        'seasons':    [
            'surprising flower spikes in late spring',
            'vivid stress colouring in full summer sun',
            'dormancy and reduced watering in winter',
            'new offsets appearing around the base in spring',
        ],
    },
    'cacti': {
        'care_tips':  [
            'watering sparingly and only in the active growing season',
            'using pure mineral grit for drainage in the soil mix',
            'providing the sunniest window or outdoor position available',
            'protecting from frost below -5°C even for hardy varieties',
        ],
        'display':    [
            'a south-facing windowsill in full sun',
            'a dry garden rockery or gravel bed',
            'a greenhouse or conservatory staging',
            'a grouped desert landscape display',
            'an outdoor container brought in for winter',
        ],
        'issues':     [
            'root rot from any waterlogging in winter',
            'spider mites in warm dry indoor conditions',
            'scarring from cold water splash on the skin',
            'slow growth frustration for impatient growers',
        ],
        'traits':     [
            'architectural sculptural form that needs no flowers to impress',
            'remarkable drought tolerance once established',
            'spectacular but brief blooms that can appear overnight',
            'extremely long-lived with minimal intervention',
        ],
        'seasons':    [
            'flowering in late spring to early summer',
            'rapid growth during the warm summer months',
            'complete dormancy in winter with no watering',
            'offsetting and pup production in spring',
        ],
    },
    'herbs': {
        'care_tips':  [
            'harvesting regularly to prevent plants going to seed',
            'planting in free-draining soil in the sunniest spot',
            'pinching out flower buds on basil to extend leaf production',
            'dividing clumping herbs like chives every two or three years',
        ],
        'display':    [
            'a kitchen windowsill close to the cooking area',
            'a dedicated raised herb bed near the back door',
            'a terracotta pot collection on a sunny patio',
            'an ornamental potager kitchen garden',
            'a hanging basket with trailing herbs like thyme',
        ],
        'issues':     [
            'bolting in hot dry weather especially with cilantro',
            'root rot from overwatering in poorly drained pots',
            'mint spreading invasively through garden beds',
            'powdery mildew on basil in cool damp conditions',
        ],
        'traits':     [
            'dual purpose as ornamental plant and culinary ingredient',
            'aromatic foliage that intensifies in heat',
            'fast growing from seed or small plug plant',
            'attractive to bees and other pollinators when in flower',
        ],
        'seasons':    [
            'sowing and planting out after last frost in spring',
            'peak harvest productivity through summer',
            'drying or freezing surplus growth in late summer',
            'overwintering woody perennials like rosemary with minimal protection',
        ],
    },
    'orchids': {
        'care_tips':  [
            'watering by soaking the pot then letting it drain fully',
            'providing bright indirect light away from direct afternoon sun',
            'feeding with a half-strength orchid fertiliser weekly in summer',
            'repotting into fresh bark medium every two or three years',
        ],
        'display':    [
            'a bright bathroom with natural humidity',
            'a north or east-facing windowsill',
            'a conservatory shelf with filtered light',
            'a decorative cachepot for a formal living room',
            'a grouping with other tropical plants for humidity',
        ],
        'issues':     [
            'crown rot from water sitting in the leaf crown',
            'aerial root desiccation in dry centrally heated rooms',
            'failure to rebloom without a temperature drop trigger',
            'scale insects on pseudobulbs and undersides of leaves',
        ],
        'traits':     [
            'extraordinary bloom longevity lasting weeks to months',
            'spectacular flower forms that rival almost any plant',
            'pseudobulbs that store water and nutrients',
            'wide hybridisation resulting in an almost unlimited colour range',
        ],
        'seasons':    [
            'triggering a new flower spike with cooler autumn nights',
            'peak bloom display through winter and spring',
            'rest period in summer with focus on leaf and root growth',
            'repotting best done just after flowering finishes',
        ],
    },
    'ferns': {
        'care_tips':  [
            'maintaining consistent moisture without waterlogging',
            'misting the fronds in dry centrally heated rooms',
            'positioning in shade or dappled light away from direct sun',
            'removing dead fronds cleanly at the base in spring',
        ],
        'display':    [
            'a shaded north-facing border under trees',
            'a hanging basket in a cool bathroom',
            'a woodland garden understorey planting',
            'a fern wall or vertical garden in a shaded courtyard',
            'a humid conservatory in a decorative pot',
        ],
        'issues':     [
            'frond browning and crisp tips in dry air',
            'scale insects on the undersides of fronds',
            'crown death from frost on tender varieties',
            'root bound stunting in pots left too long without repotting',
        ],
        'traits':     [
            'prehistoric elegance with delicate layered fronds',
            'exceptional ability to thrive in deep shade',
            'dramatic unfurling fiddle-head growth in spring',
            'wide range from compact table plants to large architectural specimens',
        ],
        'seasons':    [
            'spectacular new crozier unfurling in spring',
            'full lush canopy through summer',
            'frond dieback in winter for deciduous species',
            'early emergence from the soil before most other plants in spring',
        ],
    },
    'vegetables': {
        'care_tips':  [
            'thinning seedlings to give each plant adequate space',
            'consistent deep watering rather than frequent shallow watering',
            'feeding with a high-potassium fertiliser once flowering begins',
            'rotating crops each year to prevent soil-borne disease build-up',
        ],
        'display':    [
            'a raised bed in full sun with good-quality compost',
            'a grow bag on a paved patio or balcony',
            'an allotment plot with companion planting',
            'a greenhouse or polytunnel for season extension',
            'a decorative potager with flowers and vegetables mixed',
        ],
        'issues':     [
            'slug and snail damage on young seedlings',
            'blight in warm wet summers especially on tomatoes',
            'aphid colonies on brassicas and soft growth',
            'blossom end rot from irregular watering and calcium deficiency',
        ],
        'traits':     [
            'satisfaction of harvesting food you grew yourself',
            'far superior flavour versus supermarket produce',
            'full control over growing methods and chemical use',
            'productive over a long season with successive sowing',
        ],
        'seasons':    [
            'sowing under cover from late winter for early crops',
            'planting out and establishing after last frost',
            'peak harvest in mid to late summer',
            'clearing beds and preparing soil with compost in autumn',
        ],
    },
    'fruit-trees': {
        'care_tips':  [
            'formative pruning in the first three years to build good structure',
            'thinning fruitlets in early summer to improve individual fruit size',
            'mulching around the base to retain moisture and suppress weeds',
            'checking and adjusting tree ties and stakes annually',
        ],
        'display':    [
            'a sheltered south or west-facing garden wall as an espalier',
            'an orchard with mixed varieties for cross-pollination',
            'a large half-barrel container on a sunny patio',
            'a fan-trained shape on a warm boundary fence',
            'a specimen tree as a garden focal point',
        ],
        'issues':     [
            'fireblight bacterial disease affecting pears and apples',
            'codling moth larvae in fruit at harvest',
            'biennial bearing producing a heavy crop every other year',
            'late frost damage to blossom in exposed positions',
        ],
        'traits':     [
            'blossom spectacle in spring before any other ornamental value',
            'harvest of home-grown fruit with exceptional fresh flavour',
            'long productive lifespan of decades with good management',
            'dual ornamental and productive value in a garden',
        ],
        'seasons':    [
            'blossom opening in spring requiring frost protection',
            'fruitlet setting and development through summer',
            'harvest from late summer through autumn depending on variety',
            'winter pruning while the tree is dormant',
        ],
    },
    'tropical-plants': {
        'care_tips':  [
            'maintaining temperatures above 15°C throughout the year',
            'providing high humidity through pebble trays or regular misting',
            'watering generously in summer and reducing in winter',
            'protecting from cold draughts and air conditioning vents',
        ],
        'display':    [
            'a warm humid conservatory or heated greenhouse',
            'a bright living room away from draughts',
            'a summer patio with shelter from wind and cold nights',
            'a bathroom with high natural light and steam humidity',
            'a hotel lobby-style statement interior display',
        ],
        'issues':     [
            'leaf browning from low humidity in centrally heated rooms',
            'spider mite infestations in hot dry conditions',
            'yellowing leaves from overwatering or cold root temperatures',
            'failure to flower indoors without sufficient light intensity',
        ],
        'traits':     [
            'dramatic large leaves or flowers that create an instant impact',
            'fast growth in warm humid conditions',
            'exotic appearance that transforms any indoor or outdoor space',
            'natural air-purifying properties noted in indoor conditions',
        ],
        'seasons':    [
            'active growth flush when moved outdoors in early summer',
            'flowering period in peak summer heat',
            'bringing back indoors before first autumn frost',
            'reduced watering rest period in winter',
        ],
    },
    'bonsai': {
        'care_tips':  [
            'watering daily in summer as bonsai pots dry out fast',
            'wiring branches during the growing season while wood is flexible',
            'repotting every two to three years with root pruning',
            'styling with the front and viewing angle in mind from day one',
        ],
        'display':    [
            'a purpose-built outdoor bonsai bench with correct height',
            'a bright indoor shelf for tropical species only',
            'a Japanese-inspired garden display with gravel and stone',
            'a dedicated display stand at eye level for appreciation',
            'a seasonal rotation on display when looking its best',
        ],
        'issues':     [
            'drying out and death from missing a day\'s watering in summer',
            'over-wiring causing wire bite scarring on branches',
            'root bound decline from leaving in the same pot too long',
            'spider mite and scale in stressful growing conditions',
        ],
        'traits':     [
            'living art form that reflects decades of patient cultivation',
            'seasonal change including blossom, foliage colour, and bare winter silhouette',
            'deeply personal relationship between artist and tree',
            'miniaturisation of full-grown tree characteristics',
        ],
        'seasons':    [
            'repotting temperate species in early spring before buds break',
            'vigorous growing season requiring wiring and pinching',
            'autumn colour on deciduous species before leaf fall',
            'winter rest with protection from extreme frost for most species',
        ],
    },
    'wildflowers': {
        'care_tips':  [
            'sowing directly into poor soil as rich soil encourages weeds',
            'scarifying or scratching the soil before sowing for seed contact',
            'allowing plants to set seed before cutting at the end of season',
            'avoiding any fertiliser which would favour grasses over flowers',
        ],
        'display':    [
            'a wildflower meadow replacing lawn areas',
            'a naturalistic border at the edge of a garden',
            'a wildlife pond margin planting',
            'a roadside or verge planting in a community space',
            'a container with a meadow mix for a balcony',
        ],
        'issues':     [
            'annual weed competition overwhelming slow-establishing flowers',
            'poor germination in compacted or clay soils',
            'dog walkers or trampling on unmown meadow areas',
            'rabbits and slugs targeting young seedlings',
        ],
        'traits':     [
            'exceptional wildlife value for bees, butterflies, and hoverflies',
            'self-seeding and naturalising without annual replanting',
            'naturalistic aesthetic that suits modern ecological gardens',
            'wide seasonal succession from spring to autumn',
        ],
        'seasons':    [
            'early spring bulbs and annual seedling germination',
            'peak flowering from early to midsummer',
            'seed setting and dispersal in late summer',
            'cutting back meadow areas in autumn to remove thatch',
        ],
    },
    'bamboo': {
        'care_tips':  [
            'installing a root barrier for running bamboo before planting',
            'watering heavily in the first season to establish the root system',
            'removing the oldest and most congested canes each spring',
            'feeding with a high-nitrogen fertiliser in early spring',
        ],
        'display':    [
            'a privacy screen along a boundary fence',
            'a focal point specimen in a large container',
            'a Japanese or contemporary minimalist garden design',
            'a windbreak planting in an exposed position',
            'a poolside or water feature surrounding planting',
        ],
        'issues':     [
            'running bamboo spreading beyond its intended boundary',
            'new canes not reaching full height in the first year',
            'yellowing leaves from drought or nitrogen deficiency',
            'die-back after mass flowering which occurs once per lifetime',
        ],
        'traits':     [
            'rapid establishment and fast vertical growth',
            'year-round evergreen screening and architectural presence',
            'beautiful sound of canes moving in wind',
            'exceptional tensile strength in the cane structure',
        ],
        'seasons':    [
            'new shoot emergence in spring growing at remarkable speed',
            'cane hardening and leafing out through summer',
            'foliage refresh as older leaves shed in late winter',
            'best container division and replanting in spring',
        ],
    },
    'palms': {
        'care_tips':  [
            'avoiding cutting healthy green fronds as this stresses the plant',
            'feeding with a palm-specific slow-release fertiliser in spring',
            'wrapping the crown with fleece in winter for borderline hardy species',
            'planting in free-draining soil to prevent crown rot',
        ],
        'display':    [
            'a sheltered sunny courtyard or walled garden',
            'a large decorative pot as a patio centrepiece',
            'a Mediterranean or exotic themed garden border',
            'a warm conservatory or bright atrium',
            'a poolside or coastal garden planting',
        ],
        'issues':     [
            'red palm weevil damage in warmer European regions',
            'crown damage and death in severe or prolonged frost',
            'root bound decline in pots left too long without repotting',
            'slow recovery from transplant shock when moved as large specimens',
        ],
        'traits':     [
            'instantly transformative architectural presence in any setting',
            'remarkable toughness once properly established',
            'long-lived structure that becomes more impressive over decades',
            'association with warmth and holiday destinations worldwide',
        ],
        'seasons':    [
            'fastest growth during the warmest summer months',
            'new frond production visible in spring and early summer',
            'cold weather protection needed in winter for tender varieties',
            'best planting and repotting in late spring as soil warms',
        ],
    },
    'vines-climbers': {
        'care_tips':  [
            'training new growth to the support structure while still flexible',
            'pruning at the correct season for the specific variety',
            'providing a robust support structure before planting',
            'feeding with a high-potassium fertiliser in summer to encourage flowering',
        ],
        'display':    [
            'a pergola or arch creating a garden feature',
            'a boundary wall or fence for screening and softening',
            'a trellis panel as a garden divider',
            'a house wall with appropriate fixings for support',
            'a tree stump or old structure being naturalised',
        ],
        'issues':     [
            'pruning at the wrong time removing next season\'s flower buds',
            'support structure failing under the weight of mature growth',
            'roots disturbing foundations if planted too close to buildings',
            'slow establishment in the first season before taking off',
        ],
        'traits':     [
            'vertical growing habit maximising space in small gardens',
            'dramatic seasonal transformations from bare stems to full cover',
            'ability to soften hard architectural features naturally',
            'many varieties offering fragrance, colour, and wildlife value',
        ],
        'seasons':    [
            'bud break and rapid early growth in spring',
            'peak flowering display in summer',
            'autumn foliage colour on deciduous species before leaf fall',
            'bare structure in winter revealing the interesting stem framework',
        ],
    },
    'bulbs': {
        'care_tips':  [
            'planting at three times the depth of the bulb',
            'leaving foliage to die back naturally after flowering',
            'lifting and drying tender bulbs before autumn frosts',
            'adding grit to the planting hole in heavy clay soils',
        ],
        'display':    [
            'a naturalised lawn planting for a wild spring effect',
            'a container for a doorstep or patio display',
            'a mixed border with later-emerging perennials to hide dying foliage',
            'a formal bedding scheme for maximum visual impact',
            'a cut flower garden for fresh indoor arrangements',
        ],
        'issues':     [
            'squirrel and mouse predation on newly planted bulbs',
            'bulb rot from waterlogging in poorly drained soil',
            'blindness with no flowers produced from weak or immature bulbs',
            'narcissus fly larvae tunnelling into the base of the bulb',
        ],
        'traits':     [
            'remarkable energy stored underground for a reliable annual performance',
            'some of the earliest colour in the garden after winter',
            'wide range of flower forms, heights, and flowering times',
            'increasing clump size year on year when well established',
        ],
        'seasons':    [
            'earliest crocuses and snowdrops emerging in late winter',
            'peak spring bulb display from tulips and daffodils',
            'summer bulbs like gladiolus and allium extending the season',
            'planting new bulbs in autumn for next year\'s display',
        ],
    },
    'shrubs': {
        'care_tips':  [
            'pruning at the right time of year for the specific species',
            'mulching around the base annually to feed and retain moisture',
            'watering in dry spells in the first two seasons after planting',
            'deadheading where appropriate to extend the flowering season',
        ],
        'display':    [
            'a mixed shrub border providing year-round structure',
            'a low-maintenance foundation planting around a house',
            'a wildlife garden with berrying and nectaring shrubs',
            'a formal clipped topiary or box hedge',
            'a large container for a terrace or courtyard',
        ],
        'issues':     [
            'leggy and open growth habit from insufficient light',
            'box blight and box moth caterpillar on Buxus species',
            'dieback from harsh winters on marginally hardy varieties',
            'failure to flower when pruned at the wrong time',
        ],
        'traits':     [
            'permanent woody structure providing year-round garden framework',
            'multi-season interest from flowers, berries, bark, and autumn colour',
            'wide range from ground-covering species to large specimens',
            'generally low maintenance once established',
        ],
        'seasons':    [
            'early spring flowering on bare branches before leaves appear',
            'summer flowering on the current season\'s growth',
            'autumn berries and foliage colour',
            'winter bark and evergreen foliage interest',
        ],
    },
    'aquatic-plants': {
        'care_tips':  [
            'planting in aquatic baskets with specialist pond compost',
            'positioning at the correct water depth for the species',
            'dividing overcrowded plants every two or three years in spring',
            'removing dying foliage in autumn before it rots and reduces water quality',
        ],
        'display':    [
            'a formal ornamental pond with clear water and reflections',
            'a natural wildlife pond with naturalistic marginal planting',
            'a half-barrel water garden for a small patio',
            'a stream edge or bog garden',
            'an indoor water feature with appropriate species',
        ],
        'issues':     [
            'blanketweed algae competing for nutrients in established ponds',
            'overrunning the pond surface in productive warm summers',
            'root-eating by water lily aphids or china mark moth',
            'frost damage on tender varieties left in shallow water',
        ],
        'traits':     [
            'essential habitat and breeding ground for pond wildlife',
            'natural filtration improving water clarity and quality',
            'extraordinary flower forms rising above or floating on the water',
            'cooling visual effect and microclimate benefit in summer',
        ],
        'seasons':    [
            'first leaf pads emerging at the water surface in spring',
            'peak flowering period in midsummer',
            'foliage die-back and pond tidying in autumn',
            'overwintering dormancy in the pond bed',
        ],
    },
    'air-plants': {
        'care_tips':  [
            'soaking in water for 20 to 30 minutes once or twice a week',
            'shaking off excess water after soaking to prevent rot at the base',
            'providing bright indirect light or outdoor shade in summer',
            'misting more frequently in hot dry indoor conditions',
        ],
        'display':    [
            'a decorative driftwood or cork bark mount',
            'a glass globe or terrarium with open ventilation',
            'a wire frame or macrame hanging display',
            'grouped together in a bowl as a centrepiece',
            'attached to a seashell or stone for a natural arrangement',
        ],
        'issues':     [
            'base rot from water not drying within four hours of soaking',
            'dehydration shown by rolled or curled leaves',
            'scale insects or mealybug in the leaf bases',
            'bleaching and burning from direct summer sun',
        ],
        'traits':     [
            'completely soil-free growth from atmospheric moisture and nutrients',
            'extraordinary architectural forms from spiralling to globe-shaped',
            'surprisingly tough once watering rhythm is established',
            'flowers only once in a lifetime but produces offsetting pups after',
        ],
        'seasons':    [
            'flowering triggered by lengthening days in spring or summer',
            'pup production after flowering creating a new clump',
            'most vigorous growth in warm humid summer months',
            'reduced watering needed in cool winter months indoors',
        ],
    },
    'houseplants': {
        'care_tips':  [
            'checking soil moisture before watering rather than watering on a fixed schedule',
            'wiping dusty leaves with a damp cloth to improve light absorption',
            'rotating pots a quarter turn each week for even growth',
            'repotting only when roots are visibly emerging from the drainage holes',
        ],
        'display':    [
            'a bright indirect windowsill away from heating vents',
            'a plant shelf or bookcase as a green interior feature',
            'a hanging planter for trailing varieties',
            'a grouped arrangement for a humidity-raising effect',
            'an office desk with a grow light supplement',
        ],
        'issues':     [
            'overwatering causing yellowing leaves and root rot',
            'fungus gnats in consistently damp potting compost',
            'brown leaf tips from low humidity or fluoride in tap water',
            'leggy growth reaching toward insufficient light',
        ],
        'traits':     [
            'air-purifying properties in enclosed indoor spaces',
            'year-round green presence improving mood and productivity',
            'wide range of forms, textures, and light requirements',
            'straightforward propagation by division, cuttings, or offsets',
        ],
        'seasons':    [
            'growth spurt when longer days arrive in spring',
            'summer growth needing more frequent watering and feeding',
            'slowing down in autumn as light levels drop',
            'minimal watering and no feeding through winter',
        ],
    },
    'trees': {
        'care_tips':  [
            'staking correctly with a low stake to allow the trunk to flex and strengthen',
            'formative pruning in the first five years to build a clear leader',
            'keeping a mulch-free collar immediately around the trunk',
            'watering deeply and regularly in the first two growing seasons',
        ],
        'display':    [
            'a garden focal point visible from the house windows',
            'a boundary or avenue planting in a larger space',
            'a specimen on a lawn as a traditional statement tree',
            'a wildlife garden with native species',
            'a small garden with a compact or columnar variety chosen for scale',
        ],
        'issues':     [
            'honey fungus affecting roots especially on stressed trees',
            'root encroachment near drains or house foundations',
            'verticillium wilt causing branch dieback on susceptible species',
            'scale insects or aphids in the canopy attracting sooty mould',
        ],
        'traits':     [
            'multi-decade investment that improves year on year',
            'exceptional seasonal spectacle from blossom through autumn colour',
            'canopy habitat for birds, insects, and wildlife',
            'significant impact on the microclimate and character of a garden',
        ],
        'seasons':    [
            'blossom or leaf burst in spring creating dramatic transformation',
            'full canopy providing shade and habitat in summer',
            'autumn colour and fruit or berry display',
            'bare winter silhouette revealing branch structure and bark',
        ],
    },
}

# ---------------------------------------------------------------------------
# Review templates
# ---------------------------------------------------------------------------
TEMPLATES = [
    {
        'title_tmpl': 'Six months with {name} — what I actually learned',
        'body_tmpl': (
            "I brought {name} home six months ago with high hopes and almost no knowledge. "
            "The first challenge was understanding {care_tip} — something I hadn't expected to matter so much. "
            "Once I got that right, the whole thing settled down.\n\n"
            "I grow it in {display} and the position has been ideal. {trait} is what keeps drawing me back to it. "
            "{season} was the moment that made me glad I persisted through the learning curve. "
            "One honest warning: {issue} caught me off guard in month two. Stay on top of it from the start."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': '{name} finally thriving — the one thing that changed everything',
        'body_tmpl': (
            "I nearly gave up on {name} after three months of mediocre results. Then I focused properly on "
            "{care_tip} and within a few weeks the difference was dramatic.\n\n"
            "It now lives in {display} and has genuinely transformed that spot. {trait} is even more impressive "
            "in person than I expected from photos. {season} was spectacular — worth every bit of patience. "
            "If you're struggling with yours, {care_tip} is almost certainly the issue."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Honest review: {name} is rewarding but {issue} is real',
        'body_tmpl': (
            "{name} is a genuinely satisfying plant to grow, but I want to be upfront about one thing: "
            "{issue}. I've dealt with it twice now and it takes consistent attention to manage.\n\n"
            "Beyond that, {trait} makes it one of my favourites in the collection. I keep it in {display} "
            "which suits it well. Learning about {care_tip} has been essential. {season} is worth waiting for — "
            "the plant really justifies itself then. Four stars because of that persistent issue."
        ),
        'rating': 4,
    },
    {
        'title_tmpl': 'Beginner success with {name} — here is what helped',
        'body_tmpl': (
            "As a complete beginner I was nervous about starting with {name}. It turned out to be more forgiving "
            "than I expected, as long as I paid attention to {care_tip}.\n\n"
            "I grow mine in {display} which is working really well. {trait} was a genuine surprise — I didn't "
            "expect it to look or perform like that. {season} has been the highlight so far. "
            "My biggest mistake early on was ignoring {issue}, which I'd recommend addressing immediately."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Started {name} at the wrong time — lessons learned',
        'body_tmpl': (
            "I planted {name} at entirely the wrong point in the growing calendar and spent the first few months "
            "wondering what I'd done wrong. {issue} didn't help matters. "
            "Once I understood {care_tip} things improved substantially.\n\n"
            "{trait} is what makes this plant worth persisting with. In {display} it finally looks as good as "
            "I'd imagined. {season} redeemed the whole effort. "
            "If you're starting out: do your timing research before you plant."
        ),
        'rating': 4,
    },
    {
        'title_tmpl': 'The propagation success I didn\'t expect with {name}',
        'body_tmpl': (
            "I started with one {name} and now have four, all from propagation. "
            "The process is straightforward once you understand {care_tip} — something I picked up from trial and error "
            "rather than any guide.\n\n"
            "I display them in {display} which shows off {trait} at its best. "
            "{season} is when they're most impressive. {issue} has been my main challenge across all of them, "
            "but it's manageable now that I know what to look for. A genuinely generous plant if you let it be."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Gift that became an obsession — {name}',
        'body_tmpl': (
            "Someone gave me {name} as a birthday gift and I barely knew what it was. Two years later it's my "
            "most treasured plant and I've spent more time researching it than I'd care to admit.\n\n"
            "The key discovery was {care_tip} — once that clicked, the plant transformed. "
            "{trait} is what gets mentioned every time anyone visits. I keep it in {display} which works perfectly. "
            "{season} is when I understand why this plant has such devoted followers. "
            "{issue} is the one ongoing challenge but it's worth the effort."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Container growing {name} — a practical guide from experience',
        'body_tmpl': (
            "I don't have a garden so {display} is my only option for {name}. It absolutely works — "
            "with the right attention to {care_tip} you can get excellent results in containers.\n\n"
            "{trait} is fully achievable even in a pot. {season} is just as impressive in a container as it would "
            "be in the ground, possibly more so because the plant is at closer viewing distance. "
            "The main issue to watch in containers: {issue}. Happens faster than in the ground. "
            "Highly recommend for balcony and patio gardeners."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Pest battle with {name} — and how I won',
        'body_tmpl': (
            "I had a serious problem with {issue} on my {name} earlier this year. Caught it late and had to work "
            "hard to bring the plant back. The experience was frustrating but educational.\n\n"
            "Now that it's healthy again I can fully appreciate {trait}, which is remarkable. "
            "I've repositioned it in {display} and improved my attention to {care_tip}. "
            "{season} was the proof that the plant had fully recovered — genuinely beautiful. "
            "Moral of the story: inspect regularly and catch problems early."
        ),
        'rating': 4,
    },
    {
        'title_tmpl': 'Three things I wish someone had told me before growing {name}',
        'body_tmpl': (
            "After growing {name} for over a year here is what I'd tell a beginner.\n\n"
            "First: {care_tip} is not optional — it's the foundation everything else depends on. "
            "Second: {issue} will happen and you should know how to handle it before it does. "
            "Third: {display} genuinely matters — the right position unlocks {trait} in a way a poor position never will. "
            "{season} is the payoff for getting all of this right. It's worth every bit of effort."
        ),
        'rating': 4,
    },
    {
        'title_tmpl': '{name} seasonal highlights — a year in review',
        'body_tmpl': (
            "I've been growing {name} for a full year now and want to capture what each season offered. "
            "{season} was the clear high point — everything you're told about {name} at that time of year is true. "
            "But the plant has something to offer in every season, which I hadn't expected.\n\n"
            "{trait} is consistent throughout the year, which is one of its real strengths. "
            "I've settled on {display} as the ideal position. {care_tip} was the lesson I took into next year. "
            "{issue} is the only thing that interrupted the enjoyment. Otherwise: excellent."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Good plant, mediocre results — what went wrong with my {name}',
        'body_tmpl': (
            "{name} is clearly a great plant — I can see that from other people's results. Mine has been decent "
            "but not spectacular, and I think I know why.\n\n"
            "I underestimated the importance of {care_tip} in the early stages and paid for it. "
            "{issue} also knocked the plant back at a critical point. It lives in {display} which is probably "
            "not quite right but it's the best I can do in my space. {trait} is visible but muted. "
            "{season} gave me hope — there are glimpses of what it could be. Three stars for now with potential for four."
        ),
        'rating': 3,
    },
    {
        'title_tmpl': 'Slow start but a stunning finish with {name}',
        'body_tmpl': (
            "The first few months with {name} were underwhelming. Almost no visible growth and I questioned my "
            "decision repeatedly. Then something shifted — I think getting {care_tip} right was the turning point.\n\n"
            "{trait} became apparent once the plant found its stride, and it's genuinely impressive. "
            "Displayed in {display} it gets the attention it deserves. "
            "{season} was the moment it stopped being a project and became a pleasure. "
            "One thing to keep on top of: {issue}. Everything else takes care of itself once the basics are solid."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Experienced grower\'s notes on {name}',
        'body_tmpl': (
            "I've been growing plants seriously for over fifteen years and {name} remains a reliable favourite. "
            "For anyone starting out: the most critical thing is {care_tip}. Everything else follows from that.\n\n"
            "{issue} is the challenge that trips up most beginners and some experienced growers too. "
            "I've been growing mine in {display} for three seasons now and the results are consistently good. "
            "{trait} is what makes it worth coming back to year after year. "
            "{season} is when I show it off — it earns its place fully then."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Returned to {name} after a difficult first attempt',
        'body_tmpl': (
            "My first attempt at {name} failed — {issue} got hold of it and I didn't know what I was looking at "
            "until it was too late. I left it alone for a year before trying again.\n\n"
            "The second attempt, with proper attention to {care_tip}, has been completely different. "
            "It's now thriving in {display} and {trait} is on full display. {season} this year was a genuine reward "
            "for starting again. If you failed first time, the plant isn't the problem — the conditions probably were."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'The unexpected joy of growing {name}',
        'body_tmpl': (
            "I planted {name} without expecting much and it's become one of the most satisfying things in my garden. "
            "{trait} is something I couldn't have predicted from looking at it in a nursery. "
            "You only understand it once the plant is established and performing.\n\n"
            "I keep it in {display} which is perfect for it. {care_tip} was the thing I got lucky getting right early. "
            "{season} stopped me in my tracks the first time I saw it. "
            "{issue} is a real thing — just check regularly and deal with it quickly."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Overrated for ease, underrated for beauty — {name}',
        'body_tmpl': (
            "People describe {name} as easy and I'd push back on that slightly. {care_tip} needs consistent attention "
            "and {issue} can undermine progress quickly if ignored.\n\n"
            "Where {name} is genuinely underrated is the beauty. {trait} is extraordinary when you see it in person. "
            "I display it in {display} and it gets comments from everyone who sees it. "
            "{season} is the time to really understand what this plant offers. "
            "Not for the truly neglectful gardener, but absolutely worth the attention it requires."
        ),
        'rating': 4,
    },
    {
        'title_tmpl': 'Wildlife value of {name} — an unexpected bonus',
        'body_tmpl': (
            "I planted {name} primarily for ornamental reasons. What I didn't anticipate was the wildlife it would attract. "
            "{trait} seems to be particularly appealing to bees and butterflies during the main growing period.\n\n"
            "I grow it in {display} which allows me to watch the activity up close. "
            "{season} is the most active period for wildlife visits. {care_tip} is important for keeping the plant "
            "healthy enough to flower well and provide that value. {issue} is the thing to watch — it reduces flowering "
            "and therefore wildlife visits if left unchecked. A plant that earns its place twice over."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Struggling with {name} — would appreciate advice',
        'body_tmpl': (
            "I want to be honest: I'm not getting great results with {name} and I'm not entirely sure why. "
            "{issue} has been a recurring problem despite my attempts to address it. "
            "I've been focusing on {care_tip} based on everything I've read.\n\n"
            "{trait} is there in glimpses, which tells me the plant has potential in my conditions. "
            "I have it in {display} which might not be ideal. {season} showed some improvement. "
            "Two stars for now — not the plant's fault, but not a success yet. "
            "I'll update if things improve."
        ),
        'rating': 2,
    },
    {
        'title_tmpl': 'The care secret that transformed my {name}',
        'body_tmpl': (
            "I'd had {name} for about eight months with acceptable but unremarkable results. "
            "Then I started really paying attention to {care_tip} and the difference over the next two months was dramatic.\n\n"
            "{trait} became much more pronounced. The plant in {display} now looks like a completely different specimen. "
            "{season} confirmed that I'd finally unlocked what this plant can do. "
            "{issue} has been less of a problem since I got the overall conditions right. "
            "If your {name} is underwhelming, look at {care_tip} first."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'A year of growing {name} — detailed seasonal notes',
        'body_tmpl': (
            "Here are my notes from twelve months of growing {name}:\n\n"
            "Spring: {season}. This was the moment that confirmed the whole venture. "
            "I focused on {care_tip} during this period which set up the rest of the year.\n\n"
            "{trait} developed steadily through the warmer months. {issue} appeared in summer and required prompt treatment. "
            "The plant in {display} performed better than I'd expected for the position. "
            "Overall: a rewarding year. The investment of attention is paid back generously."
        ),
        'rating': 4,
    },
    {
        'title_tmpl': 'Comparing {name} varieties — notes from growing several',
        'body_tmpl': (
            "I've grown several varieties within the {name} family and have some observations to share. "
            "{trait} varies noticeably between them, more than catalogue descriptions suggest. "
            "The care fundamentals are shared — {care_tip} applies across all of them.\n\n"
            "{issue} affects some more than others, particularly in adverse conditions. "
            "I grow mine in {display} which works well for most varieties. "
            "{season} is the clearest moment of differentiation between varieties — that's when the character of each comes through. "
            "Worth growing a few side by side if you have the space."
        ),
        'rating': 5,
    },
    {
        'title_tmpl': 'Low-effort approach to {name} — what you can get away with',
        'body_tmpl': (
            "I'm a busy person and can't give every plant the attention the books recommend. Here's what I've learned "
            "about the minimum viable care for {name}.\n\n"
            "{care_tip} is genuinely non-negotiable — skip this and the plant declines noticeably. "
            "Everything else, I've found, has more tolerance than expected. "
            "{issue} will happen if you're inattentive for too long — check occasionally and deal with it quickly. "
            "{trait} holds up even with fairly basic care. {display} has been good because it suits the plant's needs "
            "without me having to compensate with extra intervention. A plant for real life, not ideal conditions."
        ),
        'rating': 4,
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


def make_review(plant_name: str, subcat_slug: str, tmpl: dict) -> tuple | None:
    facts = PLANT_DATA.get(subcat_slug)
    if not facts:
        return None

    care_tip = random.choice(facts['care_tips'])
    display   = random.choice(facts['display'])
    issue     = random.choice(facts['issues'])
    trait     = random.choice(facts['traits'])
    season    = random.choice(facts['seasons'])

    title = tmpl['title_tmpl'].format(
        name=plant_name, care_tip=care_tip, display=display,
        issue=issue, trait=trait, season=season,
    )
    body = tmpl['body_tmpl'].format(
        name=plant_name, care_tip=care_tip, display=display,
        issue=issue, trait=trait, season=season,
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
        cat = Category.query.filter_by(slug='plants').first()
        if not cat:
            print('Category "plants" not found')
            import sys; sys.exit(1)

        if args.slug:
            sc = SubCategory.query.filter_by(category_id=cat.id, slug=args.slug).first()
            if not sc:
                print(f'Subcategory slug "{args.slug}" not found under plants')
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
            # start_from targets a subcategory slug: skip subcategories before it
            sc_slugs = [sc.slug for sc in subcategories]
            if args.start_from in sc_slugs:
                idx = sc_slugs.index(args.start_from)
                remaining_scs = subcategories[idx:]
                all_subjects = []
                for sc in remaining_scs:
                    subjects = Subject.query.filter_by(subcategory_id=sc.id).order_by(Subject.id).all()
                    all_subjects.extend(subjects)
                print(f'Resuming from subcategory "{args.start_from}" ({len(all_subjects)} subjects left)')
            else:
                print(f'--start-from slug "{args.start_from}" not found in subcategories, processing all')

        print(f'Processing {len(all_subjects)} plant subjects, ~{args.count} reviews each')

        for subj in all_subjects:
            subcat_slug = subj.subcategory.slug
            if subcat_slug not in PLANT_DATA:
                print(f'  SKIP {subj.name} — no facts data for subcategory "{subcat_slug}"')
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
                result = make_review(subj.name, subcat_slug, tmpl)
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
            print(f'  {subj.name} [{subcat_slug}]: {reviews_added} reviews (avg {subj.avg_rating:.1f}★, deleted {deleted})')

        print('Done.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--slug', help='Single subcategory slug (e.g. roses)')
    parser.add_argument('--start-from', dest='start_from', help='Resume from this subcategory slug')
    parser.add_argument('--count', type=int, default=15, help='Reviews per subject (default 15)')
    args = parser.parse_args()
    run(args)
