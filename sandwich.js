// Side-view SVG of a sandwich: bread, butter, then each topping drawn to look like itself.
// Usable in browser and node (node only for the test).
const Sandwich = (() => {
  // [name pattern, kind, colour(s), accent]; first match wins. Colours may be "a,b" for mixed sprinkles.
  const LOOKS = [
    // butter
    [/^(roomboter|halvarine|margarine)$/, "smear", "#f9e79f"], [/kruidenboter/, "smear", "#f4ecb0", "#2f9e44"],
    // sprinkles, sugar, sweet slices
    [/hagelslag melk|chocoladevlokken melk/, "sprinkle", "#6b3f22"], [/hagelslag puur|chocoladevlokken puur/, "sprinkle", "#3b2314"],
    [/hagelslag wit/, "sprinkle", "#f4ecd8"], [/vruchtenhagel/, "sprinkle", "#e8590c,#f59f00,#e64980,#74b816"],
    [/anijshagel/, "sprinkle", "#f8f9fa,#ced4da"], [/roze muisjes/, "dots", "#f783ac,#ffffff"], [/blauwe muisjes/, "dots", "#74c0fc,#ffffff"],
    [/gestampte muisjes/, "dust", "#f3a6c4"], [/poedersuiker/, "dust", "#ffffff"], [/kristalsuiker/, "dust", "#f1f3f5"],
    [/basterdsuiker/, "dust", "#b07a45"], [/kaneelsuiker/, "dust", "#a0612e"],
    [/duo chocoladepasta/, "smear", "#5a3420,#f3e6cf"], [/witte chocoladepasta/, "smear", "#f3e6cf"],
    [/chocoladepasta|hazelnootpasta/, "smear", "#5a3420"], [/speculoospasta/, "smear", "#b5743b"], [/karamelpasta/, "smear", "#c98a3e"],
    [/kokosbrood/, "slab", "#f6ecda", "#e3d3b5"], [/ontbijtkoek/, "cake", "#8b5a2b", "#6b4220"], [/^speculaas$/, "slab", "#b5743b", "#8a5426"],
    // jam, syrup, honey
    [/aardbeienjam/, "smear", "#d6334a"], [/frambozenjam/, "smear", "#c2255c"], [/kersenjam/, "smear", "#8f1d2c"],
    [/abrikozenjam/, "smear", "#f08c00"], [/bosvruchtenjam/, "smear", "#6b1f4a"], [/bramenjam/, "smear", "#4a1a3a"],
    [/zwarte bessenjam/, "smear", "#3d1430"], [/pruimenjam/, "smear", "#5f2340"], [/rabarberjam/, "smear", "#e8738a"],
    [/vijgenjam/, "smear", "#7a4a3a"], [/gemberjam/, "smear", "#d9a441"], [/marmelade/, "smear", "#f08c00", "#e8590c"],
    [/lemon curd/, "smear", "#f4d03f"], [/appelstroop/, "smear", "#3a1f14"], [/perenstroop/, "smear", "#4a2a18"],
    [/rode bessenjam/, "smear", "#d9282f"], [/schenkstroop/, "drizzle", "#8a4b14"], [/^honing$/, "drizzle", "#f2a900"], [/ahornsiroop/, "drizzle", "#b8651b"],
    // nut butters
    [/pindakaas met stukjes/, "smear", "#b9783f", "#7a4a1e"], [/pindakaas/, "smear", "#b9783f"], [/cashewnotenpasta/, "smear", "#e2c08d"],
    [/amandelpasta/, "smear", "#c99a6b"], [/tahin/, "smear", "#d6b98c"],
    // fruit
    [/banaan/, "discs", "#f6e7a1", "#e9d27a"], [/^appel$/, "discs", "#f4f0c8", "#c92a2a"], [/^peer$/, "discs", "#f1ecc6", "#9bb53d"],
    [/^aardbeien$/, "discs", "#e03131", "#ffc9c9"], [/blauwe bessen/, "dots", "#3b4a8c"], [/^frambozen$/, "dots", "#d6336c"],
    [/^vijgen$/, "discs", "#b06a6a", "#6b2e4f"], [/ananas/, "discs", "#f9d65c", "#f0b429"], [/druiven/, "dots", "#9bc53d"],
    [/meloen/, "discs", "#f7c08a", "#9bb53d"], [/mango/, "discs", "#ffb627", "#f08c00"], [/cranberry/, "dots", "#b0233a"],
    [/rozijnen/, "dots", "#4a2a2a"], [/dadels/, "dots", "#6b3a1e"], [/kiwi/, "discs", "#8bc34a", "#5a4a1a"], [/perzik/, "discs", "#ffb88c", "#e8590c"],
    // cheese
    [/maasdammer|leerdammer|emmentaler/, "slice", "#f7e08a", "#e2c45c"], [/komijnekaas|nagelkaas|mosterdkaas/, "slice", "#f2d675", "#6b4a2b"],
    [/kruidenkaas|brandnetelkaas/, "slice", "#f2e17a", "#4f7d2b"], [/cheddar/, "slice", "#f28c28"], [/rookkaas/, "slice", "#e8b85a", "#8b4a1f"],
    [/extra belegen|oude kaas|overjarige|old amsterdam|boerenkaas|gruy/, "slice", "#f2c14e"], [/manchego/, "slice", "#f1dca0", "#8a6a3a"],
    [/schapenkaas|belegen geitenkaas|jonge geitenkaas/, "slice", "#f5ecd0"], [/jonge kaas|belegen kaas|edammer|gouda/, "slice", "#f9e27a"],
    [/parmezaan/, "dots", "#f3df9a"], [/mozzarella/, "discs", "#fbfaf5", "#e9ecef"], [/burrata|ricotta|hüttenkäse|geitenkaas zacht/, "blob", "#fbfbf6", "#e9ecef"],
    [/brie|camembert/, "soft", "#fbf5e3", "#efe6cf"], [/blauwe kaas|gorgonzola/, "slice", "#f4f1e6", "#4a6fa5"], [/feta/, "dots", "#fbfbf7"],
    [/roomkaas kruiden/, "smear", "#f4f3e6", "#2f9e44"], [/roomkaas|smeerkaas/, "smear", "#fbf1d6"], [/halloumi/, "slab", "#f1e3c0", "#8a6a3a"],
    // cold cuts
    [/^(gekookte ham|achterham|beenham|schouderham)$/, "meat", "#f4a6a6", "#f8c8c8"], [/rauwe ham|parmaham|serranoham/, "meat", "#c0392b", "#f3d6d6"],
    [/gerookte kipfilet/, "meat", "#e2b48a", "#f3dcc4"], [/kipfilet|kalkoenfilet/, "meat", "#f3dcc4", "#fbeee0"], [/casselerrib/, "meat", "#e8a8a0", "#f8d8d0"],
    [/pastrami/, "meat", "#9a3a3a", "#2b2b2b"], [/rookvlees|pekelvlees/, "meat", "#8e2a2a", "#b85a5a"], [/carpaccio/, "meat", "#b02a3a", "#d45a6a"],
    [/rosbief/, "meat", "#a8484a", "#d4787a"], [/fricandeau/, "meat", "#d9a3a0", "#ecc8c4"], [/gebraden gehakt/, "slab", "#8a5a44", "#6b4232"],
    [/^salami$/, "rounds", "#b23a48", "#f6d6d6"], [/pepersalami/, "rounds", "#a33a3a", "#2b2b2b"], [/chorizo/, "rounds", "#c0392b", "#f4b6a0"],
    [/cervelaat/, "rounds", "#b5525a", "#f2d0d0"], [/ossenworst/, "rounds", "#c0392b", "#e8a0a0"], [/metworst/, "rounds", "#8e3a3a", "#e8c0b8"],
    [/droge worst/, "rounds", "#7a2e2e", "#e0b8b0"], [/grillworst/, "rounds", "#c97a6a", "#8a4a3a"], [/rookworst/, "rounds", "#9a4a3a", "#6b2a1a"],
    [/mortadella/, "rounds", "#f2b5b5", "#74b816"], [/leverworst/, "rounds", "#9b7a6a"], [/boterhamworst/, "rounds", "#f2b8b0"], [/hamworst/, "rounds", "#f5a8a8", "#fbd0d0"],
    [/zult/, "slab", "#c08a7a", "#f2e0c8"], [/katenspek/, "strips", "#9a3a2a", "#2b1a14"], [/bacon|ontbijtspek/, "strips", "#c0392b", "#f6d6c8"],
    // fish
    [/gerookte zalm|gerookte forel/, "fish", "#f4845f", "#ffd8c8"], [/heilbot/, "fish", "#f3ece0", "#c9b89a"], [/^gerookte makreel$/, "fish", "#8a7a6a", "#c9c0b0"],
    [/paling/, "fish", "#8a6a4a", "#3a2a1a"], [/bokking/, "fish", "#b08a5a", "#e0c89a"], [/haring$|rolmops/, "fish", "#c9d1d9", "#6c7a89"],
    [/sardines/, "fish", "#9aa5b1", "#5c6670"], [/ansjovis/, "strips", "#8a5a4a", "#c9a090"], [/^tonijn$/, "blob", "#c8a888", "#a88868"],
    [/makreel in tomatensaus/, "blob", "#c0392b", "#8a7a6a"], [/hollandse garnalen/, "dots", "#f4a582"], [/surimi/, "rounds", "#ffffff", "#e8590c"],
    // salads and spreads
    [/filet americain/, "smear", "#d9888a"], [/eiersalade/, "blob", "#f7e3a1", "#ffffff"], [/tonijnsalade/, "blob", "#e8d6b8", "#c8a888"],
    [/zalmsalade/, "blob", "#f7b49a"], [/krabsalade/, "blob", "#f4c7b0", "#e8590c"], [/kip-kerriesalade/, "blob", "#f2c94c", "#f6e3a0"],
    [/selderijsalade/, "blob", "#eef2d0", "#9bb53d"], [/huzarensalade/, "blob", "#f0d9c0", "#c92a2a"], [/ham-preisalade/, "blob", "#f5d0c8", "#74b816"],
    [/komkommersalade/, "discs", "#cfe8b0", "#2f9e44"], [/hummus paprika/, "blob", "#e8a07a"], [/hummus/, "blob", "#e5c99a", "#c9a46a"],
    [/tapenade/, "smear", "#3a3a2a"], [/groene pesto/, "smear", "#4f7d2b", "#8bc34a"], [/rode pesto/, "smear", "#c0533a", "#e8a07a"],
    [/paprikaspread/, "smear", "#e8603a"], [/guacamole/, "blob", "#9bc53d", "#5a8a2a"], [/leverpastei/, "smear", "#a07a6a"],
    [/grove pat/, "slab", "#8a5a4a", "#5a3a2a"], [/tzatziki/, "blob", "#f4f6ee", "#74b816"], [/rundvleessalade/, "blob", "#d9b0a0", "#a06050"],
    [/garnalensalade/, "blob", "#f6c0a8", "#f4a582"], [/haringsalade/, "blob", "#e8c8d0", "#c2255c"], [/makreelsalade/, "blob", "#d9c4a8", "#8a7a6a"],
    [/pittige kipsalade/, "blob", "#f08c4a", "#c92a2a"], [/baba ganoush/, "blob", "#c9ad8a", "#8a6a4a"],
    // sauces
    [/truffelmayonaise/, "drizzle", "#e9dfc0", "#3a3a2a"], [/tartaarsaus|remouladesaus/, "drizzle", "#f4efd6", "#74b816"],
    [/mayonaise|fritessaus|knoflooksaus/, "drizzle", "#fbf3d5"], [/joppiesaus/, "drizzle", "#f2c94c"], [/cocktailsaus/, "drizzle", "#f4a582"],
    [/samuraisaus/, "drizzle", "#f08c4a"], [/andalousesaus/, "drizzle", "#f0a060"], [/ketchup/, "drizzle", "#c92a2a"], [/^curry$/, "drizzle", "#d9480f"],
    [/zigeunersaus/, "drizzle", "#e8590c", "#74b816"], [/barbecuesaus/, "drizzle", "#6b2a1a"], [/zaanse mosterd/, "drizzle", "#e0b11a"],
    [/grove mosterd/, "drizzle", "#c9a227", "#7a5a1a"], [/honingmosterdsaus/, "drizzle", "#e9b949"], [/mosterd-dillesaus/, "drizzle", "#e8c84a", "#2f9e44"],
    [/mierikswortelsaus/, "drizzle", "#f4f1e6"], [/sambal oelek/, "smear", "#c92a2a", "#ffd8a8"], [/sambal badjak/, "smear", "#7a2a1a"],
    [/sriracha/, "drizzle", "#e03131"], [/zoete chilisaus/, "drizzle", "#e8590c", "#c92a2a"], [/ketjap/, "drizzle", "#2a1a10"],
    [/satésaus/, "drizzle", "#b5652b"], [/piccalilly/, "smear", "#f2c11a", "#74b816"], [/mangochutney/, "smear", "#f08c00", "#f9d65c"],
    [/uienchutney/, "smear", "#7a3a2a"], [/augurkenrelish/, "smear", "#74b816", "#c5e384"],
    // eggs
    [/gekookt ei/, "egg slices", "#ffffff", "#f4c430"], [/gebakken ei/, "fried egg", "#ffffff", "#f4b400"], [/roerei/, "blob", "#f7d354", "#f9e79f"],
    [/omelet/, "slab", "#f6d365", "#e9b949"],
    // vegetables and herbs
    [/komkommer/, "discs", "#e6f2c8", "#2b8a3e"], [/^tomaat$/, "discs", "#e03131", "#ff8787"], [/zongedroogde tomaten/, "strips", "#9a2a1a", "#c0533a"],
    [/ijsbergsla/, "leaf", "#b2f2bb"], [/veldsla|waterkers/, "leaf", "#2b8a3e"], [/spinazie/, "leaf", "#2b6a2e"], [/rucola/, "leaf", "#4f7d2b"], [/^sla$/, "leaf", "#74b816"],
    [/ingelegde rode ui/, "rings", "#e64980"], [/rode ui/, "rings", "#a23b72"], [/lente-ui/, "rings", "#74b816"], [/rauwe ui/, "rings", "#e9e1cf"],
    [/gebakken uitjes/, "dots", "#b8732e"], [/zilveruitjes/, "dots", "#f8f9fa"], [/augurk$/, "discs", "#74a03c", "#c5e384"],
    [/radijs/, "discs", "#ffffff", "#e64980"], [/gegrilde paprika/, "strips", "#c92a2a", "#3a1a1a"], [/^paprika$/, "strips", "#e03131", "#ff8787"],
    [/avocado/, "discs", "#c5e17a", "#3a5a1a"], [/champignons/, "discs", "#c9a27a", "#8a6a4a"], [/tuinkers/, "herbs", "#8bc34a"],
    [/alfalfa|taugé/, "herbs", "#eef5d6"], [/bieslook|peterselie|basilicum/, "herbs", "#2f9e44"], [/olijven/, "rings", "#2b2b2b"],
    [/jalape/, "rings", "#2f9e44"], [/rode peper/, "rings", "#e03131"], [/rode biet/, "discs", "#7a1a3a", "#c2255c"], [/wortel/, "dots", "#f08c00"],
    [/courgette/, "discs", "#b5d48c", "#2b6a2e"], [/aubergine/, "discs", "#e8d6b0", "#4a1a4a"], [/kappertjes/, "dots", "#5a7a2a"], [/ma[iï]s/, "dots", "#f4c430"],
    // hot snacks
    [/garnalenkroket/, "log", "#b8732e", "#8a5222"], [/kroket/, "log", "#a0612e", "#7a4520"], [/bitterballen/, "balls", "#8a5222", "#6b3a18"],
    [/gehaktbal/, "ball", "#6b3a1e", "#4a2614"], [/frikandel/, "log", "#6b3a2a", "#4a2a1a"], [/kipcorn/, "log", "#d9952e", "#a8701e"],
    [/kibbeling/, "balls", "#d9a441", "#b07a2a"], [/lekkerbek|kipschnitzel|kaassouffl/, "slab", "#d39a3a", "#a8701e"], [/bamischijf/, "slab", "#e0a020", "#8a5a1a"],
    [/shoarma|speklap|kipsaté|pulled pork/, "strips", "#b5652b", "#7a3a1a"], [/hamburger/, "slab", "#5a3420", "#3a2010"],
    // crunchy extras
    [/walnoten|hazelnoten/, "dots", "#a0703a"], [/pijnboompitten|cashewnoten/, "dots", "#f2e3b3"], [/zonnebloempitten/, "dots", "#8a8a6a"],
    [/pompoenpitten/, "dots", "#5a8a3a"], [/pinda's/, "dots", "#c99a5a"], [/sesamzaad/, "dust", "#f2e6c0"], [/^chips$/, "chips", "#f2c94c", "#e0a020"],
    [/kroepoek/, "chips", "#f6ecd8", "#e3d3b5"],
  ];
  const FALLBACK = { butter: "smear", sweet: "smear", jam: "smear", nut: "smear", fruit: "discs", cheese: "slice", meat: "meat", fish: "fish", salad: "blob", sauce: "drizzle", egg: "slab", veg: "leaf", hot: "slab", extra: "dots" };

  function look(item) {
    const name = item.name.toLowerCase();
    for (const [re, kind, color, accent] of LOOKS) if (re.test(name)) return { kind, color, accent, matched: true };
    return { kind: FALLBACK[item.cat] || "slab", color: "#c9a27a", matched: false };
  }

  const X0 = 20, X1 = 300, W = X1 - X0;
  // seeded so a topping looks the same every time it is drawn
  const rng = (seed) => () => ((seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0) / 4294967296);
  const f = (n) => Math.round(n * 10) / 10;

  // Each kind draws in local coordinates: y = 0 at the top of the layer, y = h at its bottom.
  const KINDS = {
    smear: (c, a, r) => {
      const [c1, c2] = c.split(",");
      let s = `<rect x="${X0 + 3}" y="1" width="${W - 6}" height="6" rx="3" fill="${c1}"/>`;
      if (c2) for (let x = X0 + 10; x < X1 - 10; x += 22) s += `<rect x="${x}" y="1" width="11" height="6" fill="${c2}"/>`;
      for (let k = 0; k < 3; k++) s += `<rect x="${f(X0 + 20 + r() * (W - 40))}" y="4" width="7" height="${f(5 + r() * 4)}" rx="3.5" fill="${c1}"/>`;
      if (a) for (let k = 0; k < 14; k++) s += `<circle cx="${f(X0 + 8 + r() * (W - 16))}" cy="${f(2 + r() * 4)}" r="1.4" fill="${a}"/>`;
      return [7, s];
    },
    drizzle: (c, a, r) => {
      let d = `M${X0 + 6} 4`;
      for (let x = X0 + 6, k = 0; x < X1 - 6; x += 20, k++) d += ` Q${x + 10} ${k % 2 ? 9 : -1} ${Math.min(x + 20, X1 - 6)} 4`;
      let s = `<path d="${d}" fill="none" stroke="${c}" stroke-width="5" stroke-linecap="round"/>`;
      for (let k = 0; k < 3; k++) s += `<circle cx="${f(X0 + 20 + r() * (W - 40))}" cy="${f(8 + r() * 3)}" r="2.6" fill="${c}"/>`;
      if (a) for (let k = 0; k < 12; k++) s += `<circle cx="${f(X0 + 8 + r() * (W - 16))}" cy="${f(3 + r() * 3)}" r="1.1" fill="${a}"/>`;
      return [9, s];
    },
    sprinkle: (c, a, r) => {
      const cs = c.split(",");
      let s = "";
      for (let k = 0; k < 90; k++) {
        const x = X0 + 6 + r() * (W - 12), y = 1 + r() * 5, ang = Math.round(r() * 180);
        s += `<rect x="${f(x)}" y="${f(y)}" width="5" height="1.8" rx="0.9" fill="${cs[k % cs.length]}" transform="rotate(${ang} ${f(x + 2.5)} ${f(y + 0.9)})"/>`;
      }
      return [7, s];
    },
    dots: (c, a, r) => {
      const cs = c.split(",");
      let s = "";
      for (let k = 0; k < 34; k++) s += `<circle cx="${f(X0 + 6 + r() * (W - 12))}" cy="${f(4 + r() * 4)}" r="${f(2.4 + r() * 1.6)}" fill="${cs[k % cs.length]}" stroke="rgba(0,0,0,.12)" stroke-width=".6"/>`;
      return [10, s];
    },
    dust: (c, a, r) => {
      let s = `<rect x="${X0 + 4}" y="2.5" width="${W - 8}" height="2" rx="1" fill="${c}" opacity=".7"/>`;
      for (let k = 0; k < 120; k++) s += `<circle cx="${f(X0 + 4 + r() * (W - 8))}" cy="${f(1 + r() * 3)}" r="0.9" fill="${c}"/>`;
      return [5, s];
    },
    slab: (c, a, r) => {
      let s = `<rect x="${X0 + 4}" y="0" width="${W - 8}" height="12" rx="5" fill="${c}"/>`;
      if (a) for (let k = 0; k < 26; k++) s += `<circle cx="${f(X0 + 10 + r() * (W - 20))}" cy="${f(2 + r() * 8)}" r="1.2" fill="${a}"/>`;
      return [12, s];
    },
    cake: (c, a, r) => {
      let s = `<rect x="${X0 + 6}" y="0" width="${W - 12}" height="16" rx="3" fill="${c}"/><rect x="${X0 + 6}" y="0" width="${W - 12}" height="3" rx="1.5" fill="${a}"/>`;
      for (let k = 0; k < 20; k++) s += `<circle cx="${f(X0 + 12 + r() * (W - 24))}" cy="${f(5 + r() * 9)}" r="1" fill="${a}"/>`;
      return [16, s];
    },
    slice: (c, a, r) => {
      // a cheese slice overhangs the bread with a drooping corner
      let s = `<path d="M${X0 - 8} 0 H${X1 + 6} L${X1 + 14} 9 Q${X1 + 15} 13 ${X1 + 10} 12 L${X1 + 4} 7 H${X0 - 8} Z" fill="${c}"/>`;
      if (a) for (let k = 0; k < 9; k++) s += `<ellipse cx="${f(X0 + 6 + r() * (W - 12))}" cy="3.5" rx="${f(2 + r() * 3)}" ry="1.6" fill="${a}"/>`;
      return [7, s];
    },
    soft: (c, a, r) => [10, `<rect x="${X0 - 2}" y="0" width="${W + 4}" height="10" rx="5" fill="${c}"/><rect x="${X0 - 2}" y="0" width="${W + 4}" height="2.5" rx="1.2" fill="${a}"/><rect x="${X0 - 2}" y="7.5" width="${W + 4}" height="2.5" rx="1.2" fill="${a}"/>`],
    blob: (c, a, r) => {
      let d = `M${X0 + 6} 13`;
      for (let x = X0 + 6; x < X1 - 6; x += 24) d += ` Q${x + 12} ${f(-3 + r() * 5)} ${Math.min(x + 24, X1 - 6)} ${f(3 + r() * 3)}`;
      let s = `<path d="${d} L${X1 - 6} 13 Z" fill="${c}"/>`;
      if (a) for (let k = 0; k < 22; k++) s += `<circle cx="${f(X0 + 14 + r() * (W - 28))}" cy="${f(6 + r() * 6)}" r="1.6" fill="${a}"/>`;
      return [13, s];
    },
    meat: (c, a, r) => {
      // a folded slice, wavy, overhanging both sides
      let top = `M${X0 - 10} 3`, bot = "";
      for (let x = X0 - 10, k = 0; x < X1 + 10; x += 25, k++) top += ` Q${x + 12.5} ${k % 2 ? 6 : -1} ${Math.min(x + 25, X1 + 10)} 3`;
      for (let x = X1 + 10, k = 0; x > X0 - 10; x -= 25, k++) bot += ` Q${x - 12.5} ${k % 2 ? 6 : 13} ${Math.max(x - 25, X0 - 10)} 9`;
      let s = `<path d="${top} L${X1 + 10} 9${bot} Z" fill="${c}"/>`;
      if (a) s += `<path d="M${X0} 5.5 Q${X0 + W / 4} 3 ${X0 + W / 2} 6 T${X1} 5.5" fill="none" stroke="${a}" stroke-width="1.4" opacity=".8"/>`;
      return [10, s];
    },
    rounds: (c, a, r) => {
      let s = "";
      for (let k = 0; k < 5; k++) {
        const x = X0 - 4 + k * 60;
        s += `<rect x="${x}" y="${k % 2 ? 2 : 0}" width="56" height="9" rx="4.5" fill="${c}" stroke="rgba(0,0,0,.15)" stroke-width=".8"/>`;
        if (a) for (let j = 0; j < 4; j++) s += `<circle cx="${f(x + 8 + r() * 40)}" cy="${f(3 + r() * 5)}" r="1.4" fill="${a}"/>`;
      }
      return [11, s];
    },
    strips: (c, a, r) => {
      let s = "";
      for (const [y, dx] of [[0, -6], [5, 8]]) {
        let d = `M${X0 + dx} ${y + 2}`;
        for (let x = X0 + dx, k = 0; x < X1 + dx - 10; x += 30, k++) d += ` Q${x + 15} ${y + (k % 2 ? 5 : -1)} ${x + 30} ${y + 2}`;
        s += `<path d="${d}" fill="none" stroke="${c}" stroke-width="5" stroke-linecap="round"/>`;
        if (a) s += `<path d="${d}" fill="none" stroke="${a}" stroke-width="1.3" stroke-linecap="round" opacity=".9"/>`;
      }
      return [10, s];
    },
    fish: (c, a, r) => {
      let s = `<path d="M${X0 - 6} 2 Q${X0 + W / 3} -2 ${X0 + W / 2} 2 T${X1 + 6} 2 L${X1 + 2} 9 Q${X0 + W / 2} 12 ${X0 - 2} 9 Z" fill="${c}"/>`;
      if (a) for (let x = X0 + 6; x < X1; x += 16) s += `<path d="M${x} 2.5 l6 5" stroke="${a}" stroke-width="1.6" stroke-linecap="round"/>`;
      return [10, s];
    },
    leaf: (c, a, r) => {
      // frilly lettuce edge
      let d = `M${X0 - 14} 10`;
      for (let x = X0 - 14; x < X1 + 14; x += 14) d += ` Q${x + 3.5} ${f(-2 + r() * 4)} ${x + 7} ${f(4 + r() * 3)} Q${x + 10.5} ${f(-1 + r() * 4)} ${x + 14} ${f(5 + r() * 3)}`;
      return [12, `<path d="${d} L${X1 + 14} 12 L${X0 - 14} 12 Z" fill="${c}" stroke="rgba(0,0,0,.12)" stroke-width=".8"/>`];
    },
    herbs: (c, a, r) => {
      let s = "";
      for (let k = 0; k < 46; k++) {
        const x = X0 + 4 + r() * (W - 8), y = 2 + r() * 4;
        s += `<ellipse cx="${f(x)}" cy="${f(y)}" rx="3.4" ry="1.5" fill="${c}" transform="rotate(${Math.round(r() * 180)} ${f(x)} ${f(y)})"/>`;
      }
      return [7, s];
    },
    discs: (c, a, r) => {
      // slices seen from the side: a row of slightly overlapping rounds
      let s = "";
      for (let k = 0; k < 4; k++) s += `<rect x="${X0 + 2 + k * 70}" y="${k % 2 ? 1.5 : 0}" width="68" height="9" rx="4.5" fill="${c}" stroke="${a || "rgba(0,0,0,.15)"}" stroke-width="2"/>`;
      return [11, s];
    },
    "egg slices": (c, a, r) => {
      let s = "";
      for (let k = 0; k < 4; k++) s += `<rect x="${X0 + 2 + k * 70}" y="0" width="68" height="11" rx="5.5" fill="${c}" stroke="rgba(0,0,0,.1)"/><rect x="${X0 + 20 + k * 70}" y="3" width="32" height="5" rx="2.5" fill="${a}"/>`;
      return [11, s];
    },
    "fried egg": (c, a, r) => [14, `<path d="M${X0 - 8} 14 Q${X0 - 6} 6 ${X0 + 40} 7 Q${X0 + W / 2} 4 ${X1 - 30} 7 Q${X1 + 10} 6 ${X1 + 8} 14 Z" fill="${c}" stroke="rgba(0,0,0,.08)"/><ellipse cx="${X0 + W / 2 - 20}" cy="7" rx="24" ry="7" fill="${a}"/>`],
    rings: (c, a, r) => {
      let s = "";
      for (let k = 0; k < 7; k++) s += `<ellipse cx="${f(X0 + 22 + k * 39 + r() * 6)}" cy="${f(3 + r() * 2)}" rx="18" ry="2.6" fill="none" stroke="${c}" stroke-width="2.6"/>`;
      return [7, s];
    },
    log: (c, a, r) => {
      let s = `<rect x="${X0 + 14}" y="0" width="${W - 28}" height="20" rx="10" fill="${c}"/>`;
      for (let k = 0; k < 40; k++) s += `<circle cx="${f(X0 + 20 + r() * (W - 40))}" cy="${f(3 + r() * 14)}" r="1.1" fill="${a}"/>`;
      return [20, s];
    },
    ball: (c, a, r) => [24, `<ellipse cx="${X0 + W / 2}" cy="12" rx="70" ry="12" fill="${c}"/><ellipse cx="${X0 + W / 2 - 18}" cy="7" rx="22" ry="3" fill="${a}" opacity=".6"/>`],
    balls: (c, a, r) => {
      let s = "";
      for (let k = 0; k < 4; k++) s += `<circle cx="${X0 + 38 + k * 68}" cy="11" r="11" fill="${c}"/><circle cx="${X0 + 34 + k * 68}" cy="7" r="3" fill="${a}" opacity=".7"/>`;
      return [22, s];
    },
    chips: (c, a, r) => {
      let s = "";
      for (let k = 0; k < 7; k++) {
        const x = X0 + 18 + k * 41, y = 4 + r() * 3;
        s += `<ellipse cx="${f(x)}" cy="${f(y)}" rx="20" ry="4" fill="${c}" stroke="${a}" stroke-width="1" transform="rotate(${Math.round(-12 + r() * 24)} ${f(x)} ${f(y)})"/>`;
      }
      return [11, s];
    },
  };

  // Layers drawn bottom-up. `fresh` = indices of layers that should drop in (with a stagger), `topDrops` = re-drop the top slice.
  function svg(items, stack, { fresh = [], topDrops = false } = {}) {
    const parts = [];
    let y = 0; // grows upwards, as a negative offset from the bottom
    const add = (h, inner, cls, delay, title) => {
      y -= h;
      parts.push(`<g transform="translate(0 ${y})"><g class="${cls}" style="--d:${delay}ms">${title ? `<title>${title}</title>` : ""}${inner}</g></g>`);
    };
    const esc = (s) => String(s).replace(/[&<>"']/g, (ch) => `&#${ch.charCodeAt(0)};`);
    add(28, `<rect x="${X0}" y="0" width="${W}" height="28" rx="9" fill="#c8843e"/><rect x="${X0 + 5}" y="0" width="${W - 10}" height="21" rx="6" fill="#f3d9a4"/>`, "", 0);
    add(4, `<rect x="${X0 + 6}" y="0" width="${W - 12}" height="5" rx="2.5" fill="#f9e79f"/>`, "", 0, "Butter");
    stack.forEach((i, k) => {
      const lk = look(items[i]), [h, inner] = KINDS[lk.kind](lk.color, lk.accent, rng(i * 7919 + 17));
      const at = fresh.indexOf(k);
      add(h, inner, at >= 0 ? "drop" : "", at * 140, esc(items[i].name));
    });
    add(30, `<path d="M${X0} 30 V14 Q${X0} 0 ${X0 + 24} 0 H${X1 - 24} Q${X1} 0 ${X1} 14 V30 Z" fill="#c8843e"/><rect x="${X0 + 5}" y="22" width="${W - 10}" height="8" rx="3" fill="#f3d9a4"/>`,
      topDrops ? "drop" : "", Math.max(0, fresh.length) * 140, "Bread");
    const H = -y + 14;
    return { height: H, svg: `<svg viewBox="0 ${-H + 8} 320 ${H}" width="320" height="${H}" role="img" aria-label="${esc(["Bread", ...stack.map((i) => items[i].name), "bread"].join(", "))}">${parts.join("")}</svg>` };
  }

  return { look, svg, KINDS };
})();

if (typeof module !== "undefined") module.exports = Sandwich;
