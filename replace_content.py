import re

with open('www_sdipresence_com_source.html', 'r', encoding='utf-8') as f:
    html = f.read()

replacements = [
    # ── NAV / HEADER ─────────────────────────────────────────────────────
    ('support-button-text text-size-16-mob">About SDI',
     'support-button-text text-size-16-mob">About Rebis'),

    # ── SOLUTIONS SECTION ─────────────────────────────────────────────────
    ('t-red-medium-16-ls010">OUR SOLUTIONS',
     't-red-medium-16-ls010">OUR TECHNOLOGY'),
    ('heading-black-blue-gradient">Your Priorities, Our Solutions',
     'heading-black-blue-gradient">Patented Plasma Technology — Zero Waste, Maximum Value'),

    # ── CASE STUDIES SECTION → PRODUCTS ───────────────────────────────────
    ('t-red-medium-16-ls010">CASE STUDIES',
     't-red-medium-16-ls010">OUR PRODUCTS'),
    ('heading-black-blue-gradient">Unmatched Technical and Industry Expertise',
     'heading-black-blue-gradient">9 High-Value Materials from a Single Waste Stream'),

    # individual case study titles → product names
    ('heading-black-blue-gradient">IT Managed Services for Large Midwest City',
     'heading-black-blue-gradient">Graphene'),
    ('heading-black-blue-gradient">ServiceNow for One of Nations Largest Port Authorities',
     'heading-black-blue-gradient">Electricity Generation'),
    ('heading-black-blue-gradient">Large Midwest Utility Company - EAM &amp; GIS',
     'heading-black-blue-gradient">Glass Cullet'),
    ('heading-black-blue-gradient">Large West Coast City - Data Strategy',
     'heading-black-blue-gradient">Eco Wool'),
    ('heading-black-blue-gradient">West Coast Community College System \u2013 IT Strategic Plan',
     'heading-black-blue-gradient">Rock Wool'),
    ('heading-black-blue-gradient">Large Midwest Energy Provider - Network Engineering Services',
     'heading-black-blue-gradient">EPS Products'),
    ('heading-black-blue-gradient">Large Energy Provider\u2013 SCADA Disconnect',
     'heading-black-blue-gradient">Combifeed'),
    ('heading-black-blue-gradient">Help Desk for Major Healthcare Provider',
     'heading-black-blue-gradient">Nickel Products'),
    ('heading-black-blue-gradient">Leased Line Optimization for Major Regional Energy Provider',
     'heading-black-blue-gradient">Ferro Silicon'),
    ('heading-black-blue-gradient">Nationwide Healthcare Provider \u2013 Help Desk\xa0',
     'heading-black-blue-gradient">Advanced Carbon Materials'),

    # ── WHY SDI SECTION → WHY REBIS ───────────────────────────────────────
    ('heading-sky-blue-gradient">A trusted partner for mission-critical technology initiatives',
     'heading-sky-blue-gradient">India\u2019s First Plasma-to-Graphene Company'),
    ('text-size-regular-16 t-c-sky-blue">For 30 years, SDI has helped mid-sized and enterprise organizations in regulated and complex industries achieve technology success.',
     'text-size-regular-16 t-c-sky-blue">Rebis Graphene India (CIN: U37002UP2023PTC17820 | DPIIT: DIPP215959) converts municipal and industrial waste into Graphene and 8 other high-value materials using patented Plasma Technology \u2014 achieving zero waste output and green energy as a by-product.'),
    # stats
    ('home-why-grid-item-title">Customer Satisfaction Score (CSAT)',
     'home-why-grid-item-title">Funding Required (CGSS Loan)'),
    ('home-why-item-title heading-sky-blue-gradient">350+',
     'home-why-item-title heading-sky-blue-gradient">\u20b920 Cr'),
    ('home-why-grid-item-title">Utilities and Government Customers',
     'home-why-grid-item-title">Jobs After Commissioning'),
    ('home-why-item-title heading-sky-blue-gradient">475+',
     'home-why-item-title heading-sky-blue-gradient">100+'),
    ('home-why-grid-item-title is-short">Technical Professionals',
     'home-why-grid-item-title is-short">Products from Waste'),
    # "About SDI" button in why section
    ('support-button-text text-size-16-mob">About SDI',
     'support-button-text text-size-16-mob">About Rebis'),

    # ── INDUSTRIES SECTION → MARKETS ──────────────────────────────────────
    ('t-red-medium-16-ls010">INDUSTRIES WE SERVE',
     't-red-medium-16-ls010">MARKETS WE SERVE'),
    ('heading-black-blue-gradient">Expertise You Can Trust Across Critical Sectors',
     'heading-black-blue-gradient">Global Demand Across High-Growth Sectors'),

    # tab labels (appear twice — mobile + desktop)
    ('t-red-medium-16">Government',           't-red-medium-16">Aerospace &amp; Defence'),
    ('t-red-medium-16">Utilities',            't-red-medium-16">Semiconductor Industry'),
    ('t-red-medium-16">Aviation',             't-red-medium-16">Electric Vehicles'),
    ('t-red-medium-16">Transportation',       't-red-medium-16">Solar &amp; Renewable Energy'),
    ('t-red-medium-16">Public Safety Managed Services', 't-red-medium-16">Electronics &amp; Manufacturing'),
    ('t-red-medium-16">Commercial Real Estate',         't-red-medium-16">Research &amp; Universities'),
    ('t-red-medium-16">Banking, Financial Services &amp; Insurance',
     't-red-medium-16">Impact Investors &amp; Green Bonds'),
    ('t-red-medium-16">Manufacturing',        't-red-medium-16">Export Markets'),

    # tab section labels (ls010 variant)
    ('t-red-medium-16-ls010">Government',
     't-red-medium-16-ls010">Aerospace &amp; Defence'),
    ('t-red-medium-16-ls010">Utilities',
     't-red-medium-16-ls010">Semiconductor Industry'),
    ('t-red-medium-16-ls010">Aviation',
     't-red-medium-16-ls010">Electric Vehicles'),
    ('t-red-medium-16-ls010">Transportation',
     't-red-medium-16-ls010">Solar &amp; Renewable Energy'),
    ('t-red-medium-16-ls010">Public Safety Managed Services',
     't-red-medium-16-ls010">Electronics &amp; Manufacturing'),
    ('t-red-medium-16-ls010">Commercial Real Estate',
     't-red-medium-16-ls010">Research &amp; Universities'),
    ('t-red-medium-16-ls010">Banking, Financial Services &amp; Insurance',
     't-red-medium-16-ls010">Impact Investors &amp; Green Bonds'),
    ('t-red-medium-16-ls010">Manufacturing',
     't-red-medium-16-ls010">Export Markets'),

    # slide headings
    ('title-32-500-pop is--black-grad">Helping Government Work Smarter for the People It Serves',
     'title-32-500-pop is--black-grad">Graphene for Aerospace &amp; Defence Applications'),
    ('title-32-500-pop is--black-grad">IT Services &amp; Consulting for Utility Organizations',
     'title-32-500-pop is--black-grad">High-Purity Graphene for Semiconductor Manufacturing'),
    ('title-32-500-pop is--black-grad">IT Services &amp; Consulting for Aviation Safety and Security',
     'title-32-500-pop is--black-grad">Graphene-Enhanced Battery Technology for Electric Vehicles'),
    ('title-32-500-pop is--black-grad">Transforming City Operations with ServiceNow',
     'title-32-500-pop is--black-grad">Graphene in Solar Panels &amp; Renewable Energy Systems'),
    ('title-32-500-pop is--black-grad">Public Safety Managed Services',
     'title-32-500-pop is--black-grad">Advanced Materials for Electronics &amp; Manufacturing'),
    ('title-32-500-pop is--black-grad">Commercial Real Estate',
     'title-32-500-pop is--black-grad">Graphene Supply for Research Institutions &amp; Universities'),
    ('title-32-500-pop is--black-grad">Solutions for Banking, Financial Services, and Insurance',
     'title-32-500-pop is--black-grad">ESG-Aligned Investment Opportunity \u2014 ₹20 Crore CGSS Loan'),
    ('title-32-500-pop is--black-grad">IT Services &amp; Manufacturing',
     'title-32-500-pop is--black-grad">Export-Oriented Graphene Production for Global Markets'),

    # slide descriptions
    ('text-size-regular-14 t-c-grey">Modern government relies on technology to deliver secure services, enable data-driven policy, and operate more efficiently in service of the public.',
     'text-size-regular-14 t-c-grey">Graphene\u2019s ultra-light, ultra-strong properties make it ideal for aerospace composites, satellite components, and next-generation defence materials.'),
    ('text-size-regular-14 t-c-grey">Utility companies rely on advanced technology to manage complex networks, strengthen grid resilience, and ensure reliable, safe service in an increasingly data-driven environment.',
     'text-size-regular-14 t-c-grey">High-purity graphene is a critical enabler for microchips, semiconductors, and advanced electronics \u2014 a market India currently imports and Rebis aims to serve domestically.'),
    ('text-size-regular-14 t-c-grey">Aviation depends on advanced technology to ensure safety, optimize operations, and support real-time coordination across complex air travel systems.',
     'text-size-regular-14 t-c-grey">Graphene dramatically improves EV battery performance \u2014 faster charging, longer range, and longer lifespan. International EV manufacturers are already awaiting commercial production.'),
    ('text-size-regular-14 t-c-grey">Information technology is critical to public transit, enabling real-time tracking, efficient operations, and data-driven planning that improve reliability and rider experience.',
     'text-size-regular-14 t-c-grey">Graphene-coated solar panels achieve higher efficiency and durability. Rebis\u2019s green energy by-product further aligns with renewable energy goals.'),
    ('text-size-regular-14 t-c-grey">Advanced technology solutions designed to recognize, respond, and recover from an incident or emergency swiftly and effectively.',
     'text-size-regular-14 t-c-grey">Our by-products \u2014 Eco Wool, Rock Wool, EPS, Ferro Silicon, Nickel, Glass Cullet, and Combifeed \u2014 serve a wide range of industrial and construction markets.'),
    ('text-size-regular-14 t-c-grey">Real estate data services to maximize revenue, valuation &amp; safety.',
     'text-size-regular-14 t-c-grey">Graphene is one of the most studied materials in the world. We supply research-grade graphene to universities and R&amp;D institutions nationally and globally.'),
    ('text-size-regular-14 t-c-grey">Streamlining operations, modernizing legacy systems, and improving service delivery.',
     'text-size-regular-14 t-c-grey">With DPIIT recognition (DIPP215959) and a CGSS-eligible loan ask of \u20b920 crore, Rebis offers a strong ESG-aligned investment backed by government-approved technology.'),
    ('text-size-regular-14 t-c-grey">Information technology is critical to modern manufacturing, enabling automation and data-driven decisions that improve efficiency, quality, and resilience.',
     'text-size-regular-14 t-c-grey">Overseas offices in Singapore and Europe support international buyer relationships. Export-oriented production positions Rebis to earn significant foreign exchange for India.'),

    # ── BLOG SECTION → IMPACT ─────────────────────────────────────────────
    ('t-red-medium-16-ls010">BLOG',
     't-red-medium-16-ls010">OUR IMPACT'),
    ('heading-black-blue-gradient">Latest Insights from SDI',
     'heading-black-blue-gradient">Social, Environmental &amp; National Impact'),

    # ── CTA FOOTER SECTION ────────────────────────────────────────────────
    ('heading-black-blue-gradient">Looking for Strategic IT Expertise?',
     'heading-black-blue-gradient">Ready to Invest in India\u2019s Green Future?'),

    # ── PAGE TITLE ────────────────────────────────────────────────────────
    ('<title>IT Modernization &amp; Managed Services Provider | SDI Presence</title>',
     '<title>Rebis Graphene India \u2014 Turning Waste into Graphene | CGSS Funding Profile</title>'),
]

for old, new in replacements:
    count = html.count(old)
    html = html.replace(old, new)
    print(f'[{"OK" if count else "MISS"}] ({count}x) {old[:70]}')

with open('www_sdipresence_com_source.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('\nDone.')
