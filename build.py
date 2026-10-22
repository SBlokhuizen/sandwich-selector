"""Generates data.js: Dutch sandwich toppings and a pairwise pairing score in [-1, 1].

Score = category-pair base + tag rules, clamped, then hand-set overrides for known combos.
Run: python3 build.py
"""
import json

# name | English gloss | category | tags
ITEMS = """
Roomboter|butter|butter|
Halvarine|half-fat margarine|butter|
Margarine|margarine|butter|
Kruidenboter|herb butter|butter|savoury herb garlic
Hagelslag melk|milk chocolate sprinkles|sweet|sprinkle choc
Hagelslag puur|dark chocolate sprinkles|sweet|sprinkle choc
Hagelslag wit|white chocolate sprinkles|sweet|sprinkle choc
Vruchtenhagel|fruit sprinkles|sweet|sprinkle
Chocoladevlokken melk|milk chocolate flakes|sweet|sprinkle choc
Chocoladevlokken puur|dark chocolate flakes|sweet|sprinkle choc
Anijshagel|anise sprinkles|sweet|sprinkle anise
Roze muisjes|pink anise comfits|sweet|sprinkle anise
Blauwe muisjes|blue anise comfits|sweet|sprinkle anise
Gestampte muisjes|crushed anise comfits|sweet|sprinkle anise
Chocoladepasta|chocolate spread|sweet|choc creamy
Hazelnootpasta|hazelnut chocolate spread|sweet|choc creamy
Duo chocoladepasta|two-tone chocolate spread|sweet|choc creamy
Witte chocoladepasta|white chocolate spread|sweet|choc creamy
Speculoospasta|speculoos spread|sweet|creamy
Karamelpasta|caramel spread|sweet|creamy
Kokosbrood|coconut slices|sweet|
Ontbijtkoek|spiced breakfast cake|sweet|
Bruine basterdsuiker|brown sugar|sweet|
Kaneelsuiker|cinnamon sugar|sweet|
Aardbeienjam|strawberry jam|jam|
Frambozenjam|raspberry jam|jam|
Kersenjam|cherry jam|jam|
Abrikozenjam|apricot jam|jam|
Bosvruchtenjam|forest fruit jam|jam|
Bramenjam|blackberry jam|jam|
Zwarte bessenjam|blackcurrant jam|jam|
Pruimenjam|plum jam|jam|
Rabarberjam|rhubarb jam|jam|
Vijgenjam|fig jam|jam|
Gemberjam|ginger jam|jam|
Sinaasappelmarmelade|orange marmalade|jam|
Lemon curd|lemon curd|jam|
Appelstroop|apple syrup spread|jam|stroop
Perenstroop|pear syrup spread|jam|stroop
Schenkstroop|pouring syrup|jam|
Honing|honey|jam|
Pindakaas|peanut butter|nut|peanut
Pindakaas met stukjes|crunchy peanut butter|nut|peanut
Pindakaas 100%|100% peanut butter|nut|peanut
Cashewnotenpasta|cashew butter|nut|
Amandelpasta|almond butter|nut|
Tahin|tahini|nut|sesame
Banaan|banana|fruit|
Appel|apple|fruit|
Peer|pear|fruit|
Aardbeien|strawberries|fruit|
Blauwe bessen|blueberries|fruit|
Frambozen|raspberries|fruit|
Vijgen|figs|fruit|
Ananas|pineapple|fruit|
Druiven|grapes|fruit|
Meloen|melon|fruit|
Mango|mango|fruit|
Gedroogde cranberry's|dried cranberries|fruit|
Rozijnen|raisins|fruit|
Dadels|dates|fruit|
Jonge kaas|young gouda|cheese|mild
Jong belegen kaas|young-matured gouda|cheese|mild
Belegen kaas|matured gouda|cheese|mild
Extra belegen kaas|extra matured gouda|cheese|strong
Oude kaas|old gouda|cheese|strong
Overjarige kaas|vintage gouda|cheese|strong
Old Amsterdam|aged gouda (brand style)|cheese|strong
Komijnekaas|cumin cheese (Leidse)|cheese|strong
Friese nagelkaas|Frisian clove cheese|cheese|strong
Boerenkaas|farmhouse cheese|cheese|strong
Edammer|edam|cheese|mild
Gouda 30+|low-fat gouda|cheese|mild
Maasdammer|maasdam|cheese|mild nutty
Leerdammer|leerdammer|cheese|mild nutty
Emmentaler|emmental|cheese|mild nutty
Gruyère|gruyère|cheese|strong nutty
Cheddar|cheddar|cheese|strong
Mozzarella|mozzarella|cheese|mild italian
Parmezaan|parmesan|cheese|strong italian
Brie|brie|cheese|soft
Camembert|camembert|cheese|soft
Geitenkaas zacht|soft goat cheese|cheese|goat creamy
Jonge geitenkaas|young goat gouda|cheese|goat
Blauwe kaas|blue cheese|cheese|blue strong
Feta|feta|cheese|
Kruidenkaas|herb cheese|cheese|mild herb
Smeerkaas|cheese spread|cheese|mild creamy
Roomkaas naturel|cream cheese|cheese|mild creamy
Roomkaas kruiden-knoflook|garlic & herb cream cheese|cheese|creamy herb garlic
Hüttenkäse|cottage cheese|cheese|mild creamy
Gekookte ham|cooked ham|meat|ham
Achterham|ham (back)|meat|ham
Beenham|bone ham|meat|ham
Schouderham|shoulder ham|meat|ham
Rauwe ham|raw cured ham|meat|cured
Parmaham|parma ham|meat|cured italian
Serranoham|serrano ham|meat|cured
Kipfilet|sliced chicken|meat|
Gerookte kipfilet|smoked chicken|meat|smoky
Kalkoenfilet|sliced turkey|meat|
Rookvlees|smoked beef|meat|smoky cured
Paardenrookvlees|smoked horse meat|meat|smoky cured
Pastrami|pastrami|meat|smoky spicy
Rosbief|roast beef|meat|
Fricandeau|fricandeau|meat|
Gebraden gehakt|meatloaf slices|meat|
Boterhamworst|sandwich sausage|meat|
Cervelaat|cervelat|meat|cured
Salami|salami|meat|cured italian
Pepersalami|pepper salami|meat|cured spicy
Chorizo|chorizo|meat|cured spicy
Mortadella|mortadella|meat|italian
Leverworst|liver sausage|meat|liver
Hamworst|ham sausage|meat|
Pekelvlees|salted beef|meat|
Casselerrib|smoked pork loin|meat|smoky
Zult|head cheese|meat|pickled
Ontbijtspek|breakfast bacon|meat|smoky
Bacon|bacon|meat|smoky fried
Gelderse rookworst|smoked sausage slices|meat|smoky
Hollandse nieuwe haring|raw herring|fish|fishy
Rolmops|pickled herring|fish|fishy pickled
Gerookte zalm|smoked salmon|fish|fishy smoky
Tonijn|canned tuna|fish|fishy
Gerookte makreel|smoked mackerel|fish|fishy smoky
Gerookte paling|smoked eel|fish|fishy smoky
Hollandse garnalen|Dutch shrimp|fish|fishy
Sardines|sardines|fish|fishy
Ansjovis|anchovies|fish|fishy
Surimi|crab sticks|fish|fishy
Filet americain|raw beef spread|salad|creamy
Eiersalade|egg salad|salad|mayo
Tonijnsalade|tuna salad|salad|mayo fishy
Zalmsalade|salmon salad|salad|mayo fishy
Krabsalade|crab salad|salad|mayo fishy
Kip-kerriesalade|chicken curry salad|salad|mayo
Selderijsalade|celery salad|salad|mayo
Huzarensalade|Dutch meat & potato salad|salad|mayo
Ham-preisalade|ham & leek salad|salad|mayo
Komkommersalade|cucumber salad|salad|pickled
Hummus naturel|hummus|salad|creamy
Hummus paprika|red pepper hummus|salad|creamy
Tapenade|olive tapenade|salad|italian
Groene pesto|green pesto|salad|italian herb garlic
Rode pesto|red pesto|salad|italian
Paprikaspread|red pepper spread|salad|creamy
Guacamole|guacamole|salad|creamy
Leverpastei|liver pâté|salad|liver creamy
Grove paté|coarse pâté|salad|liver
Tzatziki|tzatziki|salad|creamy garlic
Mayonaise|mayonnaise|sauce|mayo
Fritessaus|fries sauce|sauce|mayo
Truffelmayonaise|truffle mayo|sauce|mayo
Knoflooksaus|garlic sauce|sauce|mayo garlic
Joppiesaus|joppie sauce|sauce|mayo
Tartaarsaus|tartar sauce|sauce|mayo pickled
Remouladesaus|remoulade|sauce|mayo pickled
Cocktailsaus|cocktail sauce|sauce|mayo
Ketchup|ketchup|sauce|
Curry|curry ketchup|sauce|
Zigeunersaus|paprika sauce|sauce|
Barbecuesaus|barbecue sauce|sauce|smoky
Zaanse mosterd|Dutch mustard|sauce|mustard
Grove mosterd|wholegrain mustard|sauce|mustard
Honingmosterdsaus|honey mustard|sauce|mustard
Mierikswortelsaus|horseradish sauce|sauce|
Sambal oelek|sambal oelek|sauce|spicy asian
Sambal badjak|sambal badjak|sauce|spicy asian
Sriracha|sriracha|sauce|spicy
Zoete chilisaus|sweet chili sauce|sauce|asian
Ketjap manis|sweet soy sauce|sauce|asian
Satésaus|peanut satay sauce|sauce|asian peanut
Piccalilly|piccalilli|sauce|mustard pickled
Mangochutney|mango chutney|sauce|
Uienchutney|onion chutney|sauce|
Gekookt ei|boiled egg|egg|
Gebakken ei|fried egg|egg|
Roerei|scrambled egg|egg|
Omelet|omelette|egg|
Komkommer|cucumber|veg|fresh
Tomaat|tomato|veg|fresh italian
Sla|lettuce|veg|fresh
IJsbergsla|iceberg lettuce|veg|fresh
Rucola|rocket|veg|fresh italian
Veldsla|lamb's lettuce|veg|fresh
Spinazie|baby spinach|veg|fresh
Rauwe ui|raw onion|veg|onion
Rode ui|red onion|veg|onion
Lente-ui|spring onion|veg|onion fresh
Gebakken uitjes|crispy fried onions|veg|onion fried
Augurk|pickled gherkin|veg|pickled
Zilveruitjes|pickled silverskin onions|veg|pickled onion
Radijs|radish|veg|fresh
Paprika|bell pepper|veg|fresh
Avocado|avocado|veg|creamy
Gebakken champignons|fried mushrooms|veg|
Tuinkers|garden cress|veg|fresh herb
Alfalfa|alfalfa sprouts|veg|fresh
Bieslook|chives|veg|herb onion
Peterselie|parsley|veg|herb
Basilicum|basil|veg|herb italian
Olijven|olives|veg|italian
Jalapeño|jalapeño|veg|spicy pickled
Zongedroogde tomaten|sun-dried tomatoes|veg|italian
Rode biet|beetroot|veg|
Geraspte wortel|grated carrot|veg|fresh
Gegrilde courgette|grilled courgette|veg|italian
Gegrilde aubergine|grilled aubergine|veg|italian
Gegrilde paprika|grilled pepper|veg|italian
Kroket|croquette|hot|fried
Bitterballen|bitterballen|hot|fried
Frikandel|frikandel|hot|fried
Gehaktbal|meatball|hot|
Kibbeling|fried cod bites|hot|fried fishy
Lekkerbek|battered fish fillet|hot|fried fishy
Shoarma|shawarma|hot|spicy
Kipsaté|chicken satay|hot|asian
Hamburger|hamburger|hot|
Kaassoufflé|cheese soufflé snack|hot|fried
Walnoten|walnuts|extra|nutty
Pijnboompitten|pine nuts|extra|nutty italian
Zonnebloempitten|sunflower seeds|extra|nutty
Pompoenpitten|pumpkin seeds|extra|nutty
Pinda's|peanuts|extra|nutty peanut
Chips|crisps|extra|fried
Kroepoek|prawn crackers|extra|asian fried
"""

CATS = ["butter", "sweet", "jam", "nut", "fruit", "cheese", "meat", "fish", "salad", "sauce", "egg", "veg", "hot", "extra"]
# Upper triangle of the category base table, row order = CATS.
BASE = {
    "butter": [-0.3, 0.8, 0.7, 0.2, 0.3, 0.7, 0.6, 0.4, 0.2, 0.0, 0.5, 0.3, 0.4, 0.2],
    "sweet":  [0.2, -0.1, 0.4, 0.4, -0.6, -0.9, -1.0, -0.9, -0.9, -0.7, -0.8, -0.9, 0.1],
    "jam":    [-0.2, 0.5, 0.4, 0.0, -0.6, -0.9, -0.8, -0.7, -0.6, -0.6, -0.8, 0.3],
    "nut":    [-0.1, 0.6, -0.3, -0.5, -0.8, -0.6, -0.4, -0.3, -0.3, -0.6, 0.3],
    "fruit":  [0.3, 0.2, -0.3, -0.6, -0.4, -0.5, -0.5, -0.2, -0.6, 0.4],
    "cheese": [0.0, 0.7, -0.2, 0.1, 0.3, 0.6, 0.5, -0.1, 0.3],
    "meat":   [0.1, -0.6, 0.0, 0.4, 0.6, 0.5, -0.2, 0.0],
    "fish":   [-0.1, 0.0, 0.2, 0.4, 0.5, -0.2, 0.0],
    "salad":  [-0.3, 0.0, 0.2, 0.5, -0.3, 0.1],
    "sauce":  [-0.2, 0.3, 0.3, 0.6, 0.0],
    "egg":    [-0.2, 0.5, -0.1, 0.0],
    "veg":    [0.4, 0.1, 0.2],
    "hot":    [-0.5, 0.0],
    "extra":  [0.0],
}

# (selector, selector, delta); selector "c:x" = category, "t:x" = tag. Applied once per matching pair.
RULES = [
    ("t:savoury", "c:sweet", -1.3), ("t:savoury", "c:jam", -1.2), ("t:savoury", "c:nut", -0.6), ("t:savoury", "c:fruit", -0.7),
    ("t:garlic", "c:sweet", -0.4), ("t:garlic", "c:jam", -0.5), ("t:garlic", "c:fruit", -0.4), ("t:garlic", "c:nut", -0.3),
    ("t:herb", "c:sweet", -0.2), ("t:herb", "c:jam", -0.2),
    ("t:sprinkle", "c:butter", 0.2), ("t:sprinkle", "t:sprinkle", -0.4), ("t:anise", "c:nut", -0.3),
    ("t:choc", "c:fruit", 0.3), ("t:choc", "t:choc", -0.3), ("t:choc", "c:jam", -0.2),
    ("t:mild", "c:jam", 0.4), ("t:strong", "c:jam", -0.3),
    ("t:goat", "c:jam", 0.5), ("t:soft", "c:jam", 0.5), ("t:blue", "c:jam", 0.5),
    ("t:goat", "c:fruit", 0.4), ("t:soft", "c:fruit", 0.4), ("t:blue", "c:fruit", 0.4),
    ("t:goat", "t:nutty", 0.5), ("t:soft", "t:nutty", 0.5), ("t:blue", "t:nutty", 0.5),
    ("t:stroop", "c:cheese", 0.7),
    ("t:ham", "t:mild", 0.3), ("t:ham", "c:egg", 0.3), ("t:ham", "t:mustard", 0.2),
    ("t:mustard", "c:meat", 0.3), ("t:mustard", "c:hot", 0.2), ("t:mustard", "t:strong", 0.4),
    ("t:fishy", "c:cheese", -0.4), ("t:fishy", "t:onion", 0.3), ("t:fishy", "t:herb", 0.2), ("t:fishy", "t:pickled", 0.2),
    ("t:mayo", "t:mayo", -0.4), ("t:creamy", "t:creamy", -0.2), ("t:fried", "t:fried", -0.3),
    ("t:italian", "t:italian", 0.4), ("t:asian", "t:asian", 0.3), ("t:asian", "t:peanut", 0.5),
    ("t:liver", "c:cheese", -0.4), ("t:pickled", "c:meat", 0.2), ("t:sesame", "c:veg", 0.6),
    ("t:nutty", "c:sweet", 0.3),
]

PB = ["Pindakaas", "Pindakaas met stukjes", "Pindakaas 100%"]
HAGEL = ["Hagelslag melk", "Hagelslag puur", "Chocoladevlokken melk", "Chocoladevlokken puur"]
HAM = ["Gekookte ham", "Achterham", "Beenham", "Schouderham"]
MILD = ["Jonge kaas", "Jong belegen kaas", "Belegen kaas", "Edammer", "Gouda 30+"]
OLD = ["Extra belegen kaas", "Oude kaas", "Overjarige kaas", "Old Amsterdam", "Boerenkaas"]
SOFT = ["Brie", "Camembert"]
GOAT = ["Geitenkaas zacht", "Jonge geitenkaas"]
SAMBAL = ["Sambal oelek", "Sambal badjak"]
MUSTARD = ["Zaanse mosterd", "Grove mosterd"]
CHOCO = ["Chocoladepasta", "Hazelnootpasta", "Duo chocoladepasta"]
HUMMUS = ["Hummus naturel", "Hummus paprika"]
GRILLED = ["Gegrilde courgette", "Gegrilde aubergine", "Gegrilde paprika"]
PATE = ["Leverpastei", "Grove paté"]
CURED_HAM = ["Parmaham", "Serranoham", "Rauwe ham"]
STROOP = ["Appelstroop", "Perenstroop"]

# Known combinations: final value, overrides the computed score.
OVERRIDES = [
    # peanut butter
    (PB, "Banaan", 1.0), (PB, SAMBAL, 0.9), (PB, HAGEL, 0.7), (PB, "Honing", 0.8), (PB, "Aardbeienjam", 0.8),
    (PB, "Frambozenjam", 0.7), (PB, "Appel", 0.7), (PB, CHOCO, 0.6), (PB, "Komkommer", 0.4), (PB, "Ketjap manis", 0.5),
    (PB, "Sriracha", 0.6), (PB, "Bacon", 0.4), (PB, "Gebakken uitjes", 0.4), (PB, "Kroepoek", 0.4), (PB, "Karamelpasta", 0.6),
    (PB, "Speculoospasta", 0.5), (PB, "Rozijnen", 0.5), (PB, "Chips", 0.5), (PB, "Pinda's", 0.5), (PB, "Blauwe bessen", 0.5),
    (PB, "Frambozen", 0.6), (PB, "Kipfilet", 0.3), (PB, STROOP, 0.4), (PB, HAM, -0.4), (PB, "Jalapeño", 0.3),
    (["Cashewnotenpasta", "Amandelpasta"], ["Banaan", "Honing"], 0.8),
    ("Amandelpasta", ["Aardbeien", "Frambozenjam", "Kersenjam", "Dadels"], 0.7),
    ("Tahin", "Honing", 0.9), ("Tahin", "Dadels", 0.8), ("Tahin", "Gegrilde aubergine", 0.8), ("Tahin", HUMMUS, 0.4),
    ("Tahin", "Banaan", 0.6), ("Tahin", ["Kipfilet", "Feta"], 0.4),
    # sweet
    ("Roomboter", ["Ontbijtkoek", "Bruine basterdsuiker", "Kaneelsuiker"], 1.0), ("Roomboter", "Kokosbrood", 0.9),
    ("Banaan", HAGEL, 0.7), ("Banaan", CHOCO, 0.9), ("Hazelnootpasta", ["Banaan", "Aardbeien"], 1.0),
    ("Aardbeien", HAGEL, 0.6), ("Aardbeien", CHOCO, 0.9), ("Frambozen", CHOCO, 0.8),
    ("Witte chocoladepasta", ["Frambozen", "Aardbeien", "Blauwe bessen"], 0.8), ("Hagelslag wit", ["Aardbeien", "Frambozen"], 0.6),
    (CHOCO, ["Sinaasappelmarmelade", "Kersenjam", "Frambozenjam"], 0.6), (CHOCO, "Peer", 0.6), (CHOCO, HAGEL, 0.1),
    ("Speculoospasta", "Appel", 0.8), ("Speculoospasta", "Banaan", 0.7), ("Speculoospasta", "Peer", 0.6),
    ("Karamelpasta", ["Appel", "Banaan"], 0.8), ("Karamelpasta", ["Peer", "Walnoten", "Pinda's"], 0.6), ("Karamelpasta", "Chips", 0.4),
    ("Kaneelsuiker", "Appel", 0.9), ("Kaneelsuiker", ["Banaan", "Peer"], 0.7), ("Bruine basterdsuiker", "Aardbeien", 0.7),
    ("Ontbijtkoek", "Appel", 0.4), ("Kokosbrood", "Banaan", 0.5),
    # jam, honey, syrup
    ("Aardbeienjam", ["Roomkaas naturel", "Jonge kaas", "Banaan"], 0.6), ("Abrikozenjam", SOFT, 0.9), ("Abrikozenjam", GOAT, 0.8),
    ("Kersenjam", SOFT + GOAT, 0.7), ("Vijgenjam", SOFT + GOAT, 1.0), ("Vijgenjam", "Blauwe kaas", 0.9), ("Vijgenjam", OLD, 0.7),
    ("Vijgenjam", CURED_HAM, 0.8), ("Vijgenjam", PATE, 0.7), ("Vijgenjam", "Walnoten", 0.8), ("Gemberjam", OLD, 0.7),
    ("Sinaasappelmarmelade", "Roomboter", 0.9), ("Sinaasappelmarmelade", "Cheddar", 0.6),
    (["Zwarte bessenjam", "Rabarberjam"], "Roomkaas naturel", 0.6),
    ("Lemon curd", ["Blauwe bessen", "Frambozen"], 0.8), ("Lemon curd", ["Roomkaas naturel", "Aardbeien"], 0.6),
    ("Honing", SOFT + GOAT, 1.0), ("Honing", ["Blauwe kaas", "Vijgen"], 0.8), ("Honing", "Walnoten", 0.9), ("Honing", "Banaan", 0.8),
    ("Honing", ["Peer", "Feta", "Roomkaas naturel", "Appel"], 0.6), ("Honing", ["Gekookte ham", "Kipfilet", "Bacon"], 0.3),
    ("Honing", "Hüttenkäse", 0.5), ("Honing", "Kaneelsuiker", 0.5), ("Honing", HAGEL, 0.1),
    (STROOP, OLD, 0.9), (STROOP, MILD, 0.8), (STROOP, "Roomboter", 0.9), (STROOP, "Leverworst", 0.6), (STROOP, PATE, 0.6),
    (STROOP, SOFT, 0.6), (STROOP, "Ontbijtspek", 0.5), (["Schenkstroop"], ["Ontbijtspek", "Bacon"], 0.6), ("Schenkstroop", "Banaan", 0.5),
    # fruit
    ("Banaan", MILD + OLD, -0.3), ("Banaan", HAM, -0.5), ("Appel", OLD + ["Cheddar"] + SOFT, 0.7), ("Appel", GOAT + MILD, 0.5),
    ("Peer", "Blauwe kaas", 0.9), ("Peer", SOFT + GOAT + ["Walnoten"], 0.7), ("Peer", OLD + CURED_HAM, 0.6),
    ("Vijgen", GOAT + SOFT, 0.9), ("Vijgen", "Parmaham", 1.0), ("Vijgen", ["Blauwe kaas", "Walnoten"], 0.8),
    ("Ananas", HAM, 0.7), ("Ananas", MILD, 0.6), ("Ananas", ["Kip-kerriesalade", "Hüttenkäse"], 0.7), ("Ananas", ["Kipfilet", "Casselerrib"], 0.5),
    ("Meloen", "Parmaham", 1.0), ("Meloen", "Serranoham", 0.9), ("Meloen", "Rauwe ham", 0.8), ("Meloen", "Feta", 0.7),
    ("Mango", "Kipfilet", 0.7), ("Mango", ["Hollandse garnalen", "Avocado", "Kip-kerriesalade", "Zoete chilisaus"], 0.6),
    ("Druiven", SOFT + ["Blauwe kaas"], 0.6), ("Druiven", OLD, 0.5), ("Druiven", "Kip-kerriesalade", 0.4),
    ("Gedroogde cranberry's", SOFT, 0.9), ("Gedroogde cranberry's", GOAT + ["Kalkoenfilet"], 0.8), ("Gedroogde cranberry's", PATE + ["Walnoten"], 0.6),
    ("Rozijnen", ["Kip-kerriesalade", "Geraspte wortel"], 0.5), ("Dadels", GOAT + ["Bacon"], 0.8), ("Dadels", "Blauwe kaas", 0.7),
    ("Blauwe bessen", "Roomkaas naturel", 0.8), ("Frambozen", "Roomkaas naturel", 0.7), ("Aardbeien", "Roomkaas naturel", 0.7),
    ("Aardbeien", ["Mozzarella", "Basilicum"], 0.4),
    # cheese
    (HAM, MILD + ["Leerdammer", "Maasdammer", "Emmentaler"], 1.0), (HAM, "Gebakken ei", 1.0), (MILD, "Gebakken ei", 0.9),
    ("Mozzarella", ["Tomaat", "Basilicum", "Groene pesto"], 1.0), ("Mozzarella", ["Parmaham", "Zongedroogde tomaten", "Tapenade", "Rode pesto"], 0.8),
    ("Feta", "Olijven", 0.9), ("Feta", "Tomaat", 0.8), ("Feta", ["Komkommer", "Spinazie"], 0.7), ("Feta", ["Rode ui", "Tzatziki"], 0.6),
    ("Parmezaan", ["Rosbief", "Rucola"], 0.9), ("Parmezaan", ["Pijnboompitten", "Groene pesto"], 0.8),
    ("Cheddar", ["Bacon", "Uienchutney", "Hamburger"], 0.9), ("Cheddar", "Mangochutney", 0.8), ("Cheddar", ["Piccalilly", "Augurk", "Jalapeño"], 0.6),
    ("Blauwe kaas", "Walnoten", 0.9), (SOFT, "Walnoten", 0.9), (GOAT, "Walnoten", 0.9),
    (SOFT, ["Rucola", "Gebakken champignons", "Bacon"], 0.7), (SOFT, "Parmaham", 0.6), (SOFT, "Honingmosterdsaus", 0.6),
    (GOAT, ["Rode biet", "Rucola"], 0.8), (GOAT, ["Bacon", "Zongedroogde tomaten", "Rode pesto", "Pijnboompitten"], 0.7), (GOAT, "Pompoenpitten", 0.6),
    ("Gruyère", ["Gebakken champignons", "Gekookte ham"], 0.8), ("Emmentaler", "Pastrami", 0.8),
    ("Smeerkaas", HAM, 0.6), ("Smeerkaas", "Bieslook", 0.6), ("Smeerkaas", ["Komkommer", "Tomaat"], 0.4),
    ("Roomkaas naturel", ["Gerookte zalm"], 1.0), ("Roomkaas naturel", ["Komkommer", "Bieslook", "Radijs", "Zoete chilisaus"], 0.7),
    ("Roomkaas naturel", ["Gerookte kipfilet", "Tuinkers", "Jalapeño", "Lente-ui"], 0.6), ("Roomkaas kruiden-knoflook", "Gerookte zalm", 0.8),
    ("Hüttenkäse", ["Komkommer", "Bieslook", "Radijs", "Gerookte zalm"], 0.6), ("Hüttenkäse", "Tomaat", 0.5),
    # cold meat
    ("Rookvlees", "Gebakken ei", 0.9), ("Rookvlees", "Gekookt ei", 0.8), ("Rookvlees", "Mierikswortelsaus", 0.6), ("Rookvlees", ["Augurk", "Tuinkers"], 0.5),
    (HAM, "Honingmosterdsaus", 0.8), (HAM, "Augurk", 0.5), (CURED_HAM, "Rucola", 0.9),
    ("Rosbief", ["Mierikswortelsaus", "Truffelmayonaise", "Rucola"], 0.9), ("Rosbief", "Remouladesaus", 0.7), ("Rosbief", ["Gebakken uitjes", "Pijnboompitten", "Uienchutney"], 0.6),
    ("Fricandeau", ["Mayonaise", "Piccalilly"], 0.6), ("Fricandeau", "Augurk", 0.5),
    ("Gebraden gehakt", MUSTARD, 0.7), ("Gebraden gehakt", ["Augurk", "Piccalilly"], 0.6), ("Gebraden gehakt", "Mayonaise", 0.5),
    ("Leverworst", "Zaanse mosterd", 0.8), ("Leverworst", "Augurk", 0.6), ("Leverworst", ["Rauwe ui", "Zilveruitjes"], 0.5),
    ("Leverworst", "Pekelvlees", 1.0),  # broodje halfom
    ("Pekelvlees", MUSTARD, 0.8), ("Pekelvlees", "Augurk", 0.6),
    ("Zult", ["Augurk", "Piccalilly", "Zaanse mosterd"], 0.7), ("Zult", "Rauwe ui", 0.6),
    ("Casselerrib", MUSTARD, 0.8), ("Casselerrib", "Appel", 0.5), ("Gelderse rookworst", "Zaanse mosterd", 1.0), ("Gelderse rookworst", "Rauwe ui", 0.5),
    ("Pastrami", ["Grove mosterd", "Augurk"], 0.9), ("Pastrami", "Mierikswortelsaus", 0.6),
    ("Chorizo", "Roerei", 0.8), ("Chorizo", ["Paprika", "Olijven"], 0.6), ("Salami", "Olijven", 0.6), ("Pepersalami", "Roomkaas naturel", 0.6),
    ("Bacon", ["Gebakken ei", "Hamburger"], 1.0), ("Bacon", ["Roerei", "Gebakken champignons"], 0.9), ("Bacon", ["Tomaat", "Sla", "Avocado", "Barbecuesaus"], 0.8),
    ("Bacon", "Ketchup", 0.5), ("Ontbijtspek", "Gebakken ei", 0.9), ("Ontbijtspek", "Roerei", 0.8),
    ("Kipfilet", ["Zoete chilisaus", "Avocado", "Honingmosterdsaus"], 0.8), ("Kipfilet", ["Groene pesto", "Mangochutney", "Zongedroogde tomaten"], 0.7),
    ("Gerookte kipfilet", ["Mango", "Avocado"], 0.7), ("Kalkoenfilet", "Honingmosterdsaus", 0.6),
    # fish
    ("Hollandse nieuwe haring", "Rauwe ui", 1.0), ("Hollandse nieuwe haring", "Augurk", 0.9), ("Hollandse nieuwe haring", "Zilveruitjes", 0.6),
    ("Hollandse nieuwe haring", ["Mayonaise", "Ketchup"], -0.7), ("Rolmops", ["Rauwe ui", "Augurk"], 0.8), (["Hollandse nieuwe haring", "Rolmops"], "Rode biet", 0.5),
    ("Gerookte zalm", ["Roerei", "Bieslook"], 0.9), ("Gerookte zalm", ["Avocado", "Mierikswortelsaus", "Honingmosterdsaus"], 0.8),
    ("Gerookte zalm", ["Komkommer", "Rode ui"], 0.7), ("Gerookte zalm", ["Gekookt ei", "Rucola", "Tuinkers"], 0.6),
    ("Tonijn", ["Rode ui", "Mayonaise"], 0.7), ("Tonijn", ["Gekookt ei", "Cheddar", "Tartaarsaus"], 0.6),
    ("Gerookte makreel", ["Mierikswortelsaus", "Rode biet"], 0.8), ("Gerookte makreel", ["Rode ui", "Roomkaas naturel"], 0.6),
    ("Gerookte paling", "Roerei", 0.9), ("Gerookte paling", "Mierikswortelsaus", 0.7), ("Gerookte paling", "Bieslook", 0.5),
    ("Hollandse garnalen", "Cocktailsaus", 1.0), ("Hollandse garnalen", ["Gekookt ei", "Avocado"], 0.8), ("Hollandse garnalen", ["Mayonaise", "Guacamole"], 0.7),
    ("Hollandse garnalen", ["Sla", "Bieslook", "Zoete chilisaus"], 0.6), ("Surimi", ["Cocktailsaus", "Avocado"], 0.6),
    ("Ansjovis", ["Olijven", "Gekookt ei"], 0.6), ("Ansjovis", ["Tomaat", "Mozzarella"], 0.4), ("Sardines", "Tomaat", 0.6), ("Sardines", "Rode ui", 0.5),
    # salads & spreads
    ("Filet americain", "Rauwe ui", 1.0), ("Filet americain", "Gekookt ei", 0.8), ("Filet americain", ["Augurk", "Zilveruitjes", "Bieslook"], 0.6),
    ("Filet americain", SAMBAL, 0.4),
    ("Eiersalade", "Tuinkers", 0.9), ("Eiersalade", "Bieslook", 0.8), ("Eiersalade", HAM + ["Gerookte zalm", "Bacon"], 0.6),
    ("Tonijnsalade", "Rode ui", 0.7), ("Tonijnsalade", ["Komkommer", "Sla", "Lente-ui"], 0.6), ("Tonijnsalade", "Chips", 0.5),
    ("Zalmsalade", ["Komkommer", "Bieslook"], 0.6), ("Krabsalade", "Avocado", 0.6),
    ("Kip-kerriesalade", "Mangochutney", 0.7), ("Kip-kerriesalade", "Sla", 0.6),
    ("Selderijsalade", ["Walnoten", "Appel"], 0.6), ("Huzarensalade", "Gekookt ei", 0.7), ("Huzarensalade", "Rode biet", 0.6),
    (HUMMUS, ["Paprika", "Komkommer"] + GRILLED, 0.8), (HUMMUS, ["Zongedroogde tomaten", "Pijnboompitten"], 0.7),
    (HUMMUS, ["Tomaat", "Feta", "Rucola", "Spinazie", "Avocado", "Olijven", "Geraspte wortel", "Alfalfa"], 0.6),
    (HUMMUS, ["Kipfilet", "Jalapeño", "Zonnebloempitten", "Pompoenpitten"], 0.5), (HUMMUS, "Mayonaise", -0.4),
    ("Tapenade", ["Tomaat", "Feta"] + GOAT, 0.7), ("Tapenade", ["Gegrilde paprika", "Mozzarella"], 0.8), ("Tapenade", "Olijven", 0.2),
    ("Groene pesto", "Tomaat", 0.9), ("Groene pesto", ["Kipfilet", "Parmezaan", "Zongedroogde tomaten"], 0.8), ("Groene pesto", ["Pijnboompitten", "Rucola"] + GRILLED, 0.7),
    ("Rode pesto", ["Kipfilet"] + GRILLED, 0.7),
    ("Guacamole", ["Tomaat", "Jalapeño"], 0.8), ("Guacamole", ["Rode ui", "Kipfilet", "Bacon"], 0.7), ("Guacamole", ["Feta", "Chorizo", "Gerookte zalm"], 0.5),
    ("Tzatziki", "Shoarma", 0.9), ("Tzatziki", ["Komkommer", "Kipfilet"], 0.6), ("Tzatziki", ["Tomaat", "Rode ui"], 0.5),
    ("Paprikaspread", ["Kipfilet", "Komkommer", "Feta"], 0.6),
    (PATE, "Uienchutney", 0.9), (PATE, "Augurk", 0.7), (PATE, "Zilveruitjes", 0.6),
    # sauces
    ("Mayonaise", "Sriracha", 0.6), ("Mayonaise", MUSTARD, 0.5), ("Mayonaise", "Curry", 0.4), ("Mayonaise", SAMBAL, 0.3),
    (SAMBAL, "Ketjap manis", 0.6), (SAMBAL, "Gebakken ei", 0.7), (SAMBAL, "Satésaus", 0.7),
    ("Satésaus", "Gebakken uitjes", 0.9), ("Satésaus", ["Kroepoek", "Gekookt ei"], 0.7), ("Satésaus", ["Kipfilet", "Pinda's"], 0.6), ("Satésaus", "Komkommer", 0.5),
    ("Ketjap manis", "Gebakken ei", 0.6), ("Ketjap manis", "Kipfilet", 0.5), ("Piccalilly", HAM, 0.6),
    ("Mierikswortelsaus", "Rode biet", 0.7), ("Honingmosterdsaus", "Kipfilet", 0.7),
    ("Truffelmayonaise", ["Gebakken champignons"], 0.8), ("Truffelmayonaise", "Parmezaan", 0.7), ("Truffelmayonaise", ["Rucola", "Roerei"], 0.6),
    ("Mangochutney", SOFT + GOAT, 0.6), ("Uienchutney", OLD + SOFT + GOAT, 0.8), ("Uienchutney", "Hamburger", 0.6),
    ("Zoete chilisaus", ["Komkommer", "Kibbeling", "Kroepoek"], 0.5),
    ("Barbecuesaus", "Hamburger", 0.8), ("Barbecuesaus", ["Kipfilet", "Cheddar", "Gebakken uitjes"], 0.6),
    # eggs
    ("Gekookt ei", "Tuinkers", 0.9), ("Gekookt ei", "Bieslook", 0.8), ("Gekookt ei", "Mayonaise", 0.7), ("Gekookt ei", ["Tomaat", "Sla", "Cocktailsaus"], 0.6),
    ("Gebakken ei", ["Avocado", "Sriracha"], 0.8), ("Gebakken ei", "Gebakken champignons", 0.7), ("Gebakken ei", ["Tomaat", "Lente-ui"], 0.6), ("Gebakken ei", "Ketchup", 0.5),
    ("Roerei", "Bieslook", 0.9), ("Roerei", ["Gebakken champignons", "Avocado"], 0.8), ("Roerei", ["Spinazie", "Tomaat", "Feta"], 0.6),
    ("Omelet", HAM + MILD + ["Bacon"], 0.8), ("Omelet", "Gebakken champignons", 0.7), ("Omelet", ["Paprika", "Spinazie"], 0.6),
    # veg
    ("Tomaat", "Basilicum", 1.0), ("Tomaat", MILD, 0.7), ("Tomaat", "Mayonaise", 0.6), ("Rucola", "Pijnboompitten", 0.8), ("Rucola", "Zongedroogde tomaten", 0.8),
    ("Radijs", "Roomboter", 0.8), ("Radijs", "Bieslook", 0.5), ("Paprika", ["Feta", "Kipfilet"], 0.6),
    ("Avocado", ["Tomaat", "Kipfilet"], 0.8), ("Avocado", ["Feta", "Rode ui", "Mozzarella"], 0.6), ("Avocado", ["Tuinkers", "Alfalfa", "Zonnebloempitten", "Pompoenpitten"], 0.5),
    ("Gebakken champignons", ["Spinazie", "Kipfilet"], 0.5),
    ("Gebakken uitjes", ["Hamburger"], 0.8), ("Gebakken uitjes", "Cheddar", 0.6), ("Gebakken uitjes", "Gebakken ei", 0.4),
    ("Augurk", ["Hamburger", "Filet americain"], 0.8), ("Augurk", OLD + ["Gekookt ei"], 0.5),
    ("Zilveruitjes", OLD, 0.5), ("Olijven", ["Mozzarella", "Hummus naturel"], 0.6),
    ("Jalapeño", "Guacamole", 0.8), ("Jalapeño", "Roomkaas naturel", 0.6), ("Jalapeño", "Hamburger", 0.6),
    ("Zongedroogde tomaten", "Feta", 0.7), ("Rode biet", ["Feta", "Walnoten"], 0.6),
    ("Spinazie", ["Pijnboompitten"] + GOAT, 0.6), (GRILLED, ["Feta", "Mozzarella"] + GOAT, 0.7),
    # hot snacks
    ("Kroket", "Zaanse mosterd", 1.0), ("Kroket", "Grove mosterd", 0.8), ("Kroket", "Honingmosterdsaus", 0.6), ("Kroket", ["Mayonaise", "Fritessaus", "Mierikswortelsaus"], 0.4),
    ("Kroket", ["Ketchup", "Satésaus"], 0.0), ("Kroket", "Chips", -0.3),
    ("Bitterballen", MUSTARD, 1.0), ("Bitterballen", "Ketchup", -0.1),
    ("Frikandel", "Curry", 0.9), ("Frikandel", "Rauwe ui", 0.9), ("Frikandel", "Mayonaise", 0.8), ("Frikandel", "Joppiesaus", 0.7), ("Frikandel", ["Ketchup", "Satésaus"], 0.6),
    ("Gehaktbal", "Zaanse mosterd", 0.8), ("Gehaktbal", "Satésaus", 0.7), ("Gehaktbal", SAMBAL, 0.6), ("Gehaktbal", "Mayonaise", 0.5),
    (["Kibbeling", "Lekkerbek"], ["Tartaarsaus", "Remouladesaus", "Knoflooksaus"], 0.9), (["Kibbeling", "Lekkerbek"], "Ketchup", -0.5), ("Kibbeling", "Cocktailsaus", 0.5),
    ("Shoarma", "Knoflooksaus", 1.0), ("Shoarma", SAMBAL + ["Sla"], 0.8), ("Shoarma", ["Rauwe ui", "Tomaat"], 0.6), ("Shoarma", "Komkommer", 0.5),
    ("Kipsaté", "Satésaus", 1.0), ("Kipsaté", "Gebakken uitjes", 0.9), ("Kipsaté", "Kroepoek", 0.8), ("Kipsaté", "Pinda's", 0.7), ("Kipsaté", "Komkommer", 0.5),
    ("Hamburger", "Ketchup", 0.9), ("Hamburger", ["Rauwe ui", "Sla", "Tomaat"], 0.7), ("Hamburger", "Mayonaise", 0.6), ("Hamburger", "Chips", 0.4),
    ("Kaassoufflé", "Curry", 0.6), ("Kaassoufflé", "Mayonaise", 0.5),
    # extras
    ("Walnoten", ["Banaan", "Rode biet"], 0.6), ("Walnoten", CHOCO + OLD, 0.5), ("Pijnboompitten", ["Mozzarella", "Rosbief"], 0.6),
    ("Chips", MILD + HAM, 0.5), ("Chips", ["Kipfilet", "Eiersalade"], 0.4), ("Chips", CHOCO, 0.2), ("Chips", HAGEL, -0.6),
    ("Kroepoek", "Satésaus", 0.8), ("Kroepoek", SAMBAL, 0.6), ("Kroepoek", "Ketjap manis", 0.4),
    ("Pinda's", ["Banaan", "Chocoladepasta"], 0.6), ("Pinda's", SAMBAL, 0.5),
]


def build():
    items = []
    for line in ITEMS.strip().splitlines():
        name, en, cat, tags = line.split("|")
        assert cat in CATS, line
        items.append({"name": name, "en": en, "cat": cat, "tags": tags.split()})
    names = [it["name"] for it in items]
    assert len(set(names)) == len(names), "duplicate names"
    idx = {n: i for i, n in enumerate(names)}

    base = {}
    for i, a in enumerate(CATS):
        for j, b in enumerate(CATS[i:]):
            base[a, CATS[i + j]] = base[CATS[i + j], a] = BASE[a][j]

    def has(it, sel):
        kind, val = sel.split(":")
        return it["cat"] == val if kind == "c" else val in it["tags"]

    n = len(items)
    M = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            a, b = items[i], items[j]
            s = base[a["cat"], b["cat"]]
            for x, y, d in RULES:
                if (has(a, x) and has(b, y)) or (has(a, y) and has(b, x)):
                    s += d
            M[i][j] = M[j][i] = max(-1.0, min(1.0, s))

    as_list = lambda v: v if isinstance(v, list) else [v]
    for xs, ys, v in OVERRIDES:
        for x in as_list(xs):
            for y in as_list(ys):
                assert x in idx and y in idx, (x, y)
                if x != y:
                    M[idx[x]][idx[y]] = M[idx[y]][idx[x]] = v

    S = [[round(M[i][j] * 10) if i != j else 0 for j in range(n)] for i in range(n)]

    # self-check
    s = lambda a, b: S[idx[a]][idx[b]]
    assert all(S[i][j] == S[j][i] and -10 <= S[i][j] <= 10 for i in range(n) for j in range(n))
    assert s("Roomboter", "Hagelslag melk") == 10
    assert s("Gekookte ham", "Jonge kaas") == 10
    assert s("Hagelslag melk", "Hollandse nieuwe haring") <= -9
    assert s("Kruidenboter", "Aardbeienjam") <= -9
    assert s("Pindakaas", "Sambal oelek") >= 8
    return items, S


if __name__ == "__main__":
    items, S = build()
    with open("data.js", "w", encoding="utf-8") as f:
        f.write("// generated by build.py — scores are integers -10..10 (= -1.0..1.0)\n")
        f.write("const DATA = " + json.dumps({"cats": CATS, "items": items, "S": S}, ensure_ascii=False, separators=(",", ":")) + ";\n")
    flat = [v for i, r in enumerate(S) for j, v in enumerate(r) if i < j]
    print(f"{len(items)} items, {len(flat)} pairs; >=+5: {sum(v >= 5 for v in flat)}, <=-5: {sum(v <= -5 for v in flat)}")
