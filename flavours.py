"""Flavour knowledge used by build.py: a taste profile per topping, known clashes, and classic sandwiches.

PROFILES: name | ten digits 0..3 | cuisines
  digits, in order: sweet salty sour umami fat heat smoky fresh crunch strength
  cuisines: nl (Dutch deli), snack (Dutch snack bar), sw (sweet breakfast), it, med (Mediterranean/Levant/Spain),
            fr (French/deli cheese board), us (American/BBQ), as (Indonesian/Asian); uni = goes anywhere
"""

DIMS = ["sweet", "salty", "sour", "umami", "fat", "heat", "smoky", "fresh", "crunch", "strength"]

PROFILES = """
Roomboter|0100300001|uni
Halvarine|0100200001|uni
Margarine|0100300001|uni
Kruidenboter|0101300102|fr
Hagelslag melk|3000100011|sw
Hagelslag puur|2000100012|sw
Hagelslag wit|3000100011|sw
Vruchtenhagel|3010000011|sw
Chocoladevlokken melk|3000100001|sw
Chocoladevlokken puur|2000100002|sw
Anijshagel|3000000012|sw
Roze muisjes|3000000022|sw
Blauwe muisjes|3000000022|sw
Gestampte muisjes|3000000002|sw
Chocoladepasta|3000200002|sw
Hazelnootpasta|3000300002|sw
Duo chocoladepasta|3000200002|sw
Witte chocoladepasta|3000200001|sw
Speculoospasta|3000200002|sw
Karamelpasta|3100200002|sw
Kokosbrood|3000100001|sw
Ontbijtkoek|3000000002|sw
Bruine basterdsuiker|3000000011|sw
Kaneelsuiker|3000000012|sw
Aardbeienjam|3010000101|sw
Frambozenjam|3020000102|sw
Kersenjam|3010000101|sw fr
Abrikozenjam|3010000101|sw fr
Bosvruchtenjam|3020000102|sw
Bramenjam|3020000102|sw
Zwarte bessenjam|3020000102|sw
Pruimenjam|3010000101|sw
Rabarberjam|2030000102|sw
Vijgenjam|3000000002|sw fr
Gemberjam|3010010002|sw fr
Sinaasappelmarmelade|2020000102|sw
Lemon curd|3030200102|sw
Appelstroop|3010000002|sw nl
Perenstroop|3000000002|sw nl
Schenkstroop|3000000001|sw
Honing|3000000001|sw fr
Pindakaas|1210300002|sw as
Pindakaas met stukjes|1210300012|sw as
Pindakaas 100%|0110300002|sw as
Cashewnotenpasta|1100300001|sw
Amandelpasta|1000300001|sw
Tahin|0110300002|med
Banaan|2000100101|sw
Appel|2010000221|sw fr
Peer|2010000211|sw fr
Aardbeien|2010000201|sw
Blauwe bessen|2010000201|sw
Frambozen|2020000201|sw
Vijgen|2000000101|sw fr
Ananas|2020000201|sw
Druiven|2010000211|sw fr
Meloen|2000000301|sw
Mango|3010000201|sw as
Gedroogde cranberry's|2020000001|sw
Rozijnen|3000000001|sw
Dadels|3000000001|sw med
Jonge kaas|0201200001|nl
Jong belegen kaas|0202200001|nl
Belegen kaas|0202200002|nl
Extra belegen kaas|0203200002|nl
Oude kaas|0303200013|nl
Overjarige kaas|0303200013|nl
Old Amsterdam|1203200013|nl
Komijnekaas|0202200002|nl
Friese nagelkaas|0202100003|nl
Boerenkaas|0202200002|nl
Edammer|0201200001|nl
Gouda 30+|0201100001|nl
Maasdammer|1101200001|nl
Leerdammer|1101200001|nl
Emmentaler|1101200001|nl fr
Gruyère|0203200002|fr
Cheddar|0212200002|us
Mozzarella|0101200100|it
Parmezaan|0303100013|it
Brie|0101300001|fr
Camembert|0102300002|fr
Geitenkaas zacht|0121200102|fr
Jonge geitenkaas|0211200001|nl fr
Blauwe kaas|0312300003|fr
Feta|0321200102|med
Kruidenkaas|0201200101|nl
Smeerkaas|0201200001|nl
Roomkaas naturel|0110300100|uni
Roomkaas kruiden-knoflook|0111300102|uni
Hüttenkäse|0110100200|uni
Gekookte ham|0202100001|nl
Achterham|0202100001|nl
Beenham|0202101001|nl
Schouderham|0202100001|nl
Rauwe ham|0303100002|fr
Parmaham|1303200002|it
Serranoham|0303100002|med
Kipfilet|0101000100|uni
Gerookte kipfilet|0201002001|nl
Kalkoenfilet|0101000100|uni
Rookvlees|0303002002|nl
Paardenrookvlees|0303002003|nl
Pastrami|0303112003|us
Rosbief|0103100002|us fr
Fricandeau|0102100001|nl
Gebraden gehakt|0202200001|nl
Boterhamworst|0201200001|nl
Cervelaat|0202201002|nl
Salami|0313300002|it
Pepersalami|0313320003|it
Chorizo|0303322003|med
Mortadella|0202300001|it
Leverworst|0203300002|nl
Hamworst|0201200001|nl
Pekelvlees|0302000002|nl
Casselerrib|0202102002|nl
Zult|0232100002|nl
Ontbijtspek|0302302002|nl
Bacon|0303303023|us
Gelderse rookworst|0302303002|nl
Katenspek|0202303002|nl
Ossenworst|0203111002|nl
Metworst|0303202003|nl
Droge worst|0303201002|nl
Grillworst|0202201001|nl
Carpaccio|0103100102|it
Hollandse nieuwe haring|0202300102|nl
Rolmops|1232100013|nl
Gerookte zalm|0202202002|fr
Tonijn|0202100002|uni
Gerookte makreel|0202303003|nl
Gerookte paling|0203302003|nl
Hollandse garnalen|1202000101|nl
Sardines|0303200003|med
Ansjovis|0303100003|it
Surimi|1101000000|uni
Zure haring|1232100103|nl
Bokking|0302203003|nl
Gerookte forel|0202102002|fr
Makreel in tomatensaus|1212200002|nl
Gerookte heilbot|0202202002|nl
Filet americain|0212210002|nl
Eiersalade|0111300001|nl
Tonijnsalade|0212300002|nl
Zalmsalade|0212301002|nl
Krabsalade|1211300001|nl
Kip-kerriesalade|1111310002|nl as
Selderijsalade|1110300111|nl
Huzarensalade|1221300002|nl
Ham-preisalade|0211300101|nl
Komkommersalade|1130000311|nl
Hummus naturel|0211200001|med
Hummus paprika|1211201001|med
Tapenade|0312200003|it med
Groene pesto|0202300203|it
Rode pesto|1212300002|it
Paprikaspread|1111211001|med
Guacamole|0120310201|us
Leverpastei|0203300002|nl fr
Grove paté|0203300002|fr
Tzatziki|0120200302|med
Rundvleessalade|1222300002|nl
Garnalensalade|1212300001|nl
Haringsalade|1222200102|nl
Makreelsalade|0212302002|nl
Pittige kipsalade|0111320002|nl
Baba ganoush|0111203002|med
Mayonaise|0110300001|snack
Fritessaus|1110300000|snack
Truffelmayonaise|0113300003|it
Knoflooksaus|0110300002|med snack
Joppiesaus|2110310002|snack
Tartaarsaus|0120300101|snack
Remouladesaus|0120300101|snack
Cocktailsaus|2110300001|snack
Ketchup|2121000001|snack us
Curry|2121010002|snack
Zigeunersaus|1120010001|snack
Barbecuesaus|2111003002|us
Zaanse mosterd|0120020003|nl
Grove mosterd|0120010012|nl fr
Honingmosterdsaus|2110110002|nl
Mierikswortelsaus|0110220103|nl
Sambal oelek|0211030003|as
Sambal badjak|1201130003|as
Sriracha|1110030003|as us
Zoete chilisaus|3110010001|as
Ketjap manis|3202000002|as
Satésaus|2101310002|as
Piccalilly|1130010112|nl
Mangochutney|3110010002|as
Uienchutney|2111000002|fr
Gekookt ei|0102200001|uni
Gebakken ei|0102300001|uni
Roerei|0102300001|uni
Omelet|0102200001|uni
Komkommer|0000000320|uni
Tomaat|1022000301|uni
Sla|0000000320|uni
IJsbergsla|0000000330|uni
Rucola|0000010302|it
Veldsla|0000000300|uni
Spinazie|0001000200|uni
Rauwe ui|1010020223|nl
Rode ui|1010010222|uni
Lente-ui|0000010311|as
Gebakken uitjes|1201200032|nl
Augurk|1130000222|nl
Zilveruitjes|1130000122|nl
Radijs|0000010331|uni
Paprika|1000000321|uni
Avocado|0000300100|us
Gebakken champignons|0103100001|fr
Tuinkers|0000010301|nl
Alfalfa|0000000310|uni
Bieslook|0000000301|uni
Peterselie|0000000301|uni
Basilicum|1000000302|it
Olijven|0312200002|it med
Jalapeño|0120030112|us
Zongedroogde tomaten|2213100002|it
Rode biet|2010000101|nl
Geraspte wortel|1000000320|uni
Gegrilde courgette|0101102001|it med
Gegrilde aubergine|0102202001|it med
Gegrilde paprika|2101102001|it med
Kroket|0202300031|snack
Bitterballen|0202300031|snack
Frikandel|0202310002|snack
Gehaktbal|0203200002|snack nl
Kibbeling|0202300031|snack
Lekkerbek|0202300031|snack
Shoarma|0203211003|med snack
Kipsaté|2202211002|as
Hamburger|0203301002|us
Kaassoufflé|0202300031|snack
Walnoten|0001200031|fr
Pijnboompitten|1001200021|it
Zonnebloempitten|0101200021|uni
Pompoenpitten|0101200021|uni
Pinda's|0202200031|as
Chips|0301200032|snack
Kroepoek|0202100031|as
Speculaas|3000100032|sw
Poedersuiker|3000000001|sw
Kristalsuiker|3000000021|sw
Rode bessenjam|2020000102|sw fr
Ahornsiroop|3000001002|sw us
Kiwi|2030000201|sw
Perzik|2010000201|sw it
Rookkaas|0202203002|nl
Schapenkaas|0302200002|med
Belegen geitenkaas|0212200002|nl fr
Gorgonzola|0312300003|it
Ricotta|1100200200|it
Burrata|0101300101|it
Brandnetelkaas|0201200101|nl
Mosterdkaas|0211210002|nl
Manchego|0202200002|med
Gegrilde halloumi|0302201012|med
Taugé|0000000320|as
Kappertjes|0331000103|it
Maïs|2100000110|us
Rode peper|0000030213|as
Ingelegde rode ui|2030000212|us
Waterkers|0000020302|uni
Mosterd-dillesaus|2110210102|nl
Samuraisaus|0110320002|snack
Andalousesaus|1110300001|snack
Augurkenrelish|2130000112|us
Kipschnitzel|0201200031|snack
Speklap|0302302012|nl
Bamischijf|1202310032|snack as
Garnalenkroket|0202300031|snack
Kipcorn|0201310031|snack
Pulled pork|2203203002|us
Sesamzaad|0001100021|as
Hazelnoten|1000200031|sw
Cashewnoten|1101200021|as
"""

# Pairs that do NOT work, including the subtle ones a category table gets wrong. (group, group, value)
HERRING = ["Hollandse nieuwe haring", "Zure haring", "Rolmops"]
ITALIAN_FRESH = ["Basilicum", "Groene pesto", "Rode pesto", "Mozzarella", "Burrata", "Zongedroogde tomaten", "Tapenade"]
DUTCH_PUNCH = ["Zaanse mosterd", "Piccalilly", "Appelstroop", "Augurk", "Zilveruitjes", "Mierikswortelsaus"]
ASIAN = ["Sambal oelek", "Sambal badjak", "Ketjap manis", "Satésaus", "Kroepoek", "Taugé"]
SOFT_CHEESE = ["Brie", "Camembert", "Geitenkaas zacht", "Burrata", "Ricotta", "Gorgonzola", "Blauwe kaas"]
FRIED_SNACK = ["Kroket", "Bitterballen", "Frikandel", "Kipcorn", "Kaassoufflé", "Bamischijf"]
CHOC = ["Chocoladepasta", "Hazelnootpasta", "Hagelslag melk", "Hagelslag puur", "Chocoladevlokken melk"]

CLASHES = [
    (HERRING, ["Basilicum", "Groene pesto", "Rode pesto", "Mozzarella", "Burrata", "Zongedroogde tomaten", "Olijven", "Tapenade"], -0.5),
    (HERRING, ["Ketchup", "Curry", "Barbecuesaus", "Satésaus", "Ketjap manis", "Truffelmayonaise"], -0.7),
    (HERRING, ["Avocado", "Rucola", "Tomaat", "Paprika"], -0.2), (HERRING, ["Jonge kaas", "Belegen kaas", "Oude kaas", "Brie"], -0.5),
    (["Katenspek", "Ossenworst", "Metworst", "Droge worst", "Leverworst", "Zult"], ITALIAN_FRESH + ["Kappertjes"], -0.3),
    (["Mozzarella", "Burrata", "Ricotta"], DUTCH_PUNCH + ASIAN, -0.5),
    (SOFT_CHEESE, ["Sambal oelek", "Sambal badjak", "Ketjap manis", "Satésaus", "Ketchup", "Curry", "Mayonaise", "Joppiesaus"], -0.6),
    (SOFT_CHEESE, ["Tonijn", "Tonijnsalade", "Sardines", "Gerookte makreel", "Surimi", "Kroepoek"], -0.5),
    (["Brie", "Camembert"], ["Ossenworst", "Zure haring", "Frikandel", "Kroket"], -0.4),
    (["Pulled pork", "Hamburger"], ["Sambal oelek", "Satésaus", "Ketjap manis", "Mozzarella", "Basilicum", "Groene pesto"], -0.1),
    (["Oude kaas", "Overjarige kaas", "Extra belegen kaas", "Parmezaan"], ["Gerookte zalm", "Gerookte forel", "Hollandse garnalen", "Surimi", "Krabsalade"], -0.5),
    (["Pindakaas", "Pindakaas met stukjes", "Pindakaas 100%"], ["Jonge kaas", "Oude kaas", "Brie", "Mayonaise", "Hollandse nieuwe haring", "Gerookte zalm", "Tomaat", "Mozzarella"], -0.5),
    (CHOC, ["Jonge kaas", "Oude kaas", "Gekookte ham", "Tahin"], -0.6),
    (["Ketchup", "Curry"], ["Gerookte zalm", "Gerookte paling", "Gerookte forel", "Brie", "Parmaham", "Carpaccio", "Gorgonzola"], -0.6),
    (["Tzatziki", "Hummus naturel", "Feta"], ["Ketjap manis", "Satésaus", "Sambal badjak", "Curry"], -0.5),
    (["Satésaus", "Ketjap manis"], ["Gerookte zalm", "Mozzarella", "Parmaham", "Brie", "Feta", "Groene pesto"], -0.6),
    (["Mierikswortelsaus"], ["Mozzarella", "Brie", "Hagelslag melk", "Banaan"], -0.4),
    (FRIED_SNACK, ["Honing", "Parmaham", "Rucola", "Groene pesto", "Brie", "Gerookte zalm"], -0.4),
    (["Kipsaté"], ["Mozzarella", "Parmaham", "Brie", "Groene pesto", "Tzatziki"], -0.5),
    (["Shoarma"], ["Brie", "Honing", "Satésaus", "Ketjap manis"], -0.4),
    (["Leverworst", "Leverpastei"], ["Tonijn", "Gerookte zalm", "Hollandse garnalen", "Avocado"], -0.6),
    (["Filet americain"], ["Aardbeienjam", "Honing", "Brie", "Satésaus"], -0.4),
    (["Taugé"], ["Mozzarella", "Oude kaas", "Brie", "Parmaham"], -0.4),
    (["Hollandse garnalen", "Garnalensalade"], ["Pindakaas", "Oude kaas", "Leverworst"], -0.6),
    (["Gorgonzola", "Blauwe kaas"], ["Sambal oelek", "Ketchup", "Tonijn", "Mayonaise"], -0.6),
    (["Gerookte paling", "Gerookte makreel"], ["Ketchup", "Hagelslag melk", "Honing", "Mozzarella"], -0.7),
    (["Rode peper", "Jalapeño"], ["Brie", "Ricotta", "Gerookte zalm"], -0.3),
    (["Tonijnsalade", "Eiersalade", "Zalmsalade", "Krabsalade"], ["Mayonaise", "Joppiesaus", "Fritessaus"], 0.0),
    (["Sambal oelek"], ["Sambal badjak", "Sriracha"], 0.1),
    (["Ansjovis"], ["Brie", "Hagelslag melk", "Banaan", "Jonge kaas"], -0.5),
]

# Classic sandwiches people actually eat. Used to reward suggestions that are (or extend) a classic.
CLASSICS = [
    ("Broodje gezond", ["Jonge kaas", "Gekookte ham", "Gekookt ei", "Sla", "Tomaat", "Komkommer"]),
    ("Uitsmijter", ["Gebakken ei", "Gekookte ham", "Jonge kaas"]),
    ("Broodje kroket", ["Kroket", "Zaanse mosterd"]),
    ("Broodje bal", ["Gehaktbal", "Zaanse mosterd"]),
    ("Broodje haring", ["Hollandse nieuwe haring", "Rauwe ui", "Augurk"]),
    ("Broodje kibbeling", ["Kibbeling", "Remouladesaus", "Sla"]),
    ("Broodje lekkerbek", ["Lekkerbek", "Tartaarsaus", "Sla"]),
    ("Frikandel speciaal", ["Frikandel", "Curry", "Mayonaise", "Rauwe ui"]),
    ("Broodje shoarma", ["Shoarma", "Knoflooksaus", "Sla", "Komkommer"]),
    ("Broodje kipsaté", ["Kipsaté", "Satésaus", "Gebakken uitjes", "Taugé"]),
    ("Broodje garnalenkroket", ["Garnalenkroket", "Cocktailsaus", "Sla"]),
    ("Caprese", ["Mozzarella", "Tomaat", "Basilicum", "Groene pesto"]),
    ("Broodje burrata", ["Burrata", "Tomaat", "Basilicum", "Parmaham"]),
    ("Broodje carpaccio", ["Carpaccio", "Parmezaan", "Rucola", "Pijnboompitten", "Truffelmayonaise"]),
    ("Italiaanse bol", ["Parmaham", "Rucola", "Parmezaan", "Zongedroogde tomaten", "Groene pesto"]),
    ("Broodje zalm", ["Gerookte zalm", "Roomkaas naturel", "Bieslook", "Kappertjes"]),
    ("Broodje forel", ["Gerookte forel", "Mierikswortelsaus", "Komkommer", "Waterkers"]),
    ("Broodje paling", ["Gerookte paling", "Roerei", "Bieslook"]),
    ("Broodje makreel", ["Gerookte makreel", "Rode ui", "Komkommer"]),
    ("Broodje brie", ["Brie", "Honing", "Walnoten", "Rucola"]),
    ("Broodje geitenkaas", ["Geitenkaas zacht", "Honing", "Walnoten", "Rucola"]),
    ("Peer & gorgonzola", ["Gorgonzola", "Peer", "Walnoten", "Honing"]),
    ("Oude kaas met appelstroop", ["Oude kaas", "Appelstroop"]),
    ("Broodje tartaar", ["Filet americain", "Gekookt ei", "Rauwe ui", "Kappertjes"]),
    ("Broodje ossenworst", ["Ossenworst", "Augurk", "Zilveruitjes", "Zaanse mosterd"]),
    ("Broodje pekelvlees", ["Pekelvlees", "Zaanse mosterd", "Augurk"]),
    ("Broodje katenspek", ["Katenspek", "Zaanse mosterd", "Oude kaas"]),
    ("Broodje gehakt", ["Gebraden gehakt", "Zaanse mosterd", "Augurk"]),
    ("Broodje leverworst", ["Leverworst", "Zaanse mosterd", "Augurk"]),
    ("Broodje tonijnsalade", ["Tonijnsalade", "Sla", "Rode ui", "Kappertjes"]),
    ("Broodje eiersalade", ["Eiersalade", "Tuinkers"]),
    ("Broodje kip-kerrie", ["Kip-kerriesalade", "Sla", "Ananas"]),
    ("Broodje garnalen", ["Hollandse garnalen", "Cocktailsaus", "Sla"]),
    ("Broodje rosbief", ["Rosbief", "Mierikswortelsaus", "Rucola"]),
    ("Club sandwich", ["Kipfilet", "Bacon", "Sla", "Tomaat", "Mayonaise", "Gebakken ei"]),
    ("BLT", ["Bacon", "Sla", "Tomaat", "Mayonaise"]),
    ("Cheeseburger", ["Hamburger", "Cheddar", "Augurk", "Ketchup", "Rode ui"]),
    ("Pulled pork", ["Pulled pork", "Barbecuesaus", "Ingelegde rode ui", "Cheddar"]),
    ("Pastrami", ["Pastrami", "Augurkenrelish", "Grove mosterd", "Emmentaler"]),
    ("Tuna melt", ["Tonijnsalade", "Cheddar", "Rode ui"]),
    ("Broodje hummus", ["Hummus naturel", "Gegrilde paprika", "Komkommer", "Rucola"]),
    ("Broodje halloumi", ["Gegrilde halloumi", "Gegrilde courgette", "Hummus naturel", "Rucola"]),
    ("Manchego & serrano", ["Manchego", "Serranoham", "Olijven"]),
    ("Pindakaas met banaan", ["Pindakaas", "Banaan", "Honing"]),
    ("Pindakaas met sambal", ["Pindakaas", "Sambal oelek", "Komkommer"]),
    ("Pindakaas met hagelslag", ["Pindakaas", "Hagelslag melk"]),
    ("Hazelnoot & banaan", ["Hazelnootpasta", "Banaan"]),
    ("Aardbeien op brood", ["Aardbeien", "Kristalsuiker"]),
    ("Speculaas op brood", ["Speculaas"]),
    ("Kaneel & appel", ["Appel", "Kaneelsuiker"]),
]
