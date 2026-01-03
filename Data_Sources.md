# Complete guide to food safety data sources

The landscape of food safety data spans **over 150 distinct sources** across government agencies, research institutions, NGOs, and commercial providers. For building a consumer-facing platform, the most actionable data comes from a surprisingly small subset: USDA's FoodData Central and Pesticide Data Program, FDA's openFDA APIs, EWG's consumer databases, Monterey Bay Aquarium's Seafood Watch API, and Open Food Facts provide the foundation for comprehensive food safety coverage with programmatic access.

This guide catalogs every significant data source organized by accessibility and data quality, with specific details on APIs, download options, and licensing constraints.

---

## Government sources anchor the most authoritative data

Federal agencies maintain the gold standard for food safety monitoring. The **USDA Pesticide Data Program (PDP)** stands out with **42+ million data points** from testing 126 commodities since 1991—the most comprehensive pesticide residue dataset available anywhere. Data downloads are free in CSV/Access formats at ams.usda.gov/datasets/pdp.

### FDA databases and APIs

| Database | Data Type | Access Method | Update Frequency |
|----------|-----------|---------------|------------------|
| **openFDA Food Enforcement** | Recalls, adverse events | REST API (JSON) | Weekly |
| **Total Diet Study** | Nutrients + contaminants in 307 foods | Excel/PDF downloads | Multi-year cycles |
| **Mercury in Fish** | Mercury PPM for 60+ species | Web tables | Historical (1990-2012) |
| **PFAS Testing Program** | 30 PFAS chemicals in food | PDF analytical results | Ongoing |
| **Import Alerts Database** | Detained products/firms | Web search | Real-time |
| **Pesticide Residue Monitoring** | Pesticide testing on imports/domestic | Annual PDF reports | Annual |

The **openFDA platform** (open.fda.gov) provides the most developer-friendly access with free API keys, JSON responses, and 1,000 requests/hour rate limits. Endpoints cover food enforcement actions, CAERS adverse events, and recall data from 2004-present.

### EPA contaminant databases

EPA's **Integrated Risk Information System (IRIS)** provides toxicity assessments with Reference Doses (RfD) and cancer slope factors for hundreds of chemicals—essential for risk calculations. The **Toxics Release Inventory (TRI)** tracks releases of 800+ chemicals including 172 PFAS compounds, accessible via the EnviroFacts REST API.

Critical gap: The **National Listing of Fish Advisories** contains only historical data through 2011. Current fish advisories must be obtained from individual states—no centralized national database exists.

### USDA comprehensive nutrition and contaminant data

**FoodData Central** (fdc.nal.usda.gov) is the authoritative nutrition database with **300,000+ foods** across Foundation Foods, SR Legacy, FNDDS, and Branded Food Products. The REST API requires a free data.gov key with 1,000 requests/hour limits. Data is CC0 public domain.

The **FSIS Recall API** launched September 2023 provides real-time JSON access to meat, poultry, and egg product recalls—a significant improvement over previous web-only access.

### CDC biomonitoring and outbreak surveillance

**NHANES** provides chemical biomonitoring for 350+ chemicals in representative U.S. populations, including pesticides, heavy metals, PFAS, and PCBs. Public-use files are freely downloadable; restricted data requires Research Data Center access.

| CDC Database | Focus | Access | Notes |
|--------------|-------|--------|-------|
| **FoodNet Fast** | 8 pathogen surveillance | Interactive dashboard | 16% U.S. population coverage |
| **NORS/BEAM Dashboard** | Outbreak reporting | CSV downloads | 12-18 month data lag |
| **National Exposure Report** | 350+ chemical biomonitoring | PDF/web tables | NHANES-derived |

---

## State and international government sources vary dramatically in accessibility

### U.S. state-level databases

**California Proposition 65** maintains the most actionable state database—a searchable list of chemicals known to cause cancer or reproductive toxicity with safe harbor levels (NSRLs/MADLs). Downloadable as Excel at oehha.ca.gov.

Most states do **not** publish food testing databases publicly. Fish consumption advisories exist but require manual collection from individual state health departments.

### European Union leads in public data transparency

The EU offers the most comprehensive publicly accessible food safety databases globally:

| EU Database | URL | Data Type | API Access |
|-------------|-----|-----------|------------|
| **RASFF** | webgate.ec.europa.eu/rasff-window | Real-time food/feed alerts | Limited |
| **EU Pesticides Database** | ec.europa.eu/food/plant/pesticides | MRLs for all pesticides | Yes (JSON/XML) |
| **EFSA OpenFoodTox** | efsa.europa.eu | Toxicology for 5,700+ substances | Excel downloads |
| **EFSA Food Consumption** | efsa.europa.eu | EU population consumption data | Dashboard |

**OpenFoodTox** deserves special mention—it contains ADI/TDI values, NOAELs, BMD values, and genotoxicity data for 5,712 substances evaluated by EFSA, freely downloadable as Excel spreadsheets via Zenodo.

### UK Food Standards Agency API

The **Food Hygiene Rating Scheme API** (api.ratings.food.gov.uk) requires no registration or API key—a rare fully open government API. Returns XML/JSON for all UK food business hygiene ratings with daily updates.

### Canada's open government approach

Canada publishes the **Canadian Total Diet Study** and **CANLINE** surveillance data through the Open Government Portal (open.canada.ca). Data spans 1969-present covering trace elements, pesticides, radionuclides, and industrial chemicals in 160+ food composites. Available as Excel/CSV.

### Australia and New Zealand

**FSANZ** publishes the **Australian Total Diet Study** covering 600+ chemicals in the latest (28th) study. The **Australian Food Composition Database** offers 256 nutrients per food item. Both are free but primarily PDF format rather than API access.

### Japan and China

Japan's MHLW maintains MRL databases for 10,000+ pesticides/veterinary drugs, but detailed data is primarily in Japanese only. China's CFSA publishes Total Diet Study results, but international access is limited—most detailed data requires Chinese language proficiency.

---

## Academic databases require distinguishing subscription from open access

### Free academic resources

| Database | Coverage | Access | Best For |
|----------|----------|--------|----------|
| **PubMed/MEDLINE** | 36M+ citations | Free API via E-utilities | Literature searches |
| **AGRICOLA** (via NAL) | Agricultural citations | Free web search | Agriculture research |
| **PubAg** | 40,000+ USDA articles | Free full-text links | USDA research |
| **FSRIO** | 16,000+ research projects | Searchable database | Tracking funded research |

The **USDA Ag Data Commons** (data.nal.usda.gov) provides free access to USDA research datasets including the Pesticide Data Program in structured formats.

### Subscription databases

**FSTA (Food Science and Technology Abstracts)** is the most specialized for food safety with 2+ million abstracts from 22,675 sources, but requires institutional subscription via Web of Science or EBSCO.

**CAB Abstracts** covers 12+ million records across agriculture and food science from 120+ countries but also requires subscription access.

### Data repositories for research datasets

| Repository | Scope | Access | Deposit Cost |
|------------|-------|--------|--------------|
| **Harvard Dataverse** | General research | Free | Free (up to 1TB) |
| **Zenodo** | CERN-backed | Free | Free |
| **Dryad** | Curated scientific data | Free access | $120 base fee |
| **Figshare** | All formats | Free | Free (up to 5GB) |
| **Ag Data Commons** | USDA agriculture data | Free | N/A |

Harvard Dataverse hosts the **Feed the Future Innovation Lab for Food Safety** datasets—useful for developing country food safety data.

---

## NGO databases fill gaps government sources miss

### Environmental Working Group databases

EWG maintains the largest collection of consumer-accessible food safety databases, though **none offer API access**:

| EWG Database | URL | Update Frequency | Data Type |
|--------------|-----|------------------|-----------|
| **Dirty Dozen/Clean Fifteen** | ewg.org/foodnews | Annual (spring) | Pesticide rankings |
| **Food Scores** | ewg.org/foodscores | Ongoing | 80,000+ products rated |
| **Tap Water Database** | ewg.org/tapwater | Every 2-3 years | 324 contaminants, 50,000 utilities |
| **PFAS Map** | ewg.org/interactive-maps | Ongoing | 4,900+ contamination sites |

EWG's data is derived from USDA PDP testing but adds consumer-friendly risk scoring. For programmatic access, developers have created unofficial scrapers (GitHub: nikodunk/ewg-search), but these aren't officially supported.

### Monterey Bay Aquarium Seafood Watch

The only major NGO with a **documented public API** (api.seafoodwatch.org). Returns sustainability ratings (Best Choice/Good Alternative/Avoid/Certified) for 350+ seafood species in JSON format. The **Super Green list** combines sustainability with low contaminant levels (mercury, PCBs).

PDF pocket guides update twice annually; API data updates more frequently as assessments complete. Commercial use restrictions apply.

### Specialized NGO databases

| Organization | Database | Focus | Access |
|--------------|----------|-------|--------|
| **CSPI** | Chemical Cuisine | Food additive safety ratings | Free web |
| **Clean Label Project** | Certified Products | 200+ contaminants tested | Free web |
| **PAN** | PesticideInfo.org | 15,000+ pesticide chemicals | Free web |
| **Beyond Pesticides** | Disease Database | 2,600+ studies linking pesticides to disease | Free web |
| **Non-GMO Project** | Product Finder | 66,000+ verified products | Free web; spreadsheet by request |
| **Oceana** | Seafood Fraud Reports | DNA testing mislabeling data | PDF reports |
| **Global Fishing Watch** | Vessel Tracking | Satellite fishing activity | **Free API** + R/Python packages |

**Global Fishing Watch** offers the most sophisticated NGO API—free with token authentication, supporting near real-time vessel tracking globally with bulk download options.

**EDF Seafood Selector** has been **discontinued**—EDF now refers users to Seafood Watch.

**PAN's What's On My Food** was **discontinued in 2024**—users are directed to USDA PDP or Hygeia Analytics' Dietary Risk Index.

---

## International organizations provide harmonized global standards

### WHO/FAO integrated platforms

**FOSCOLLAB** (apps.who.int/foscollab) is WHO's integration hub linking JECFA evaluations, JMPR pesticide assessments, GEMS/Food contaminants, and the CIFOCOss consumption database. Free public access via web interface.

**GEMS/Food** (extranet.who.int/gemsfood) contains 8+ million analytical results for chemical contaminants in foods from 70+ countries. Free registration required for detailed data access.

### Codex Alimentarius databases

| Codex Database | URL | Content | Updates |
|----------------|-----|---------|---------|
| **Pesticide Residues** | fao.org/fao-who-codexalimentarius | 6,453 MRLs for pesticide/commodity pairs | Annual after CAC sessions |
| **Veterinary Drugs** | fao.org/fao-who-codexalimentarius | MRLs and risk recommendations | Annual |
| **GSFA (Food Additives)** | fao.org/fao-who-codexalimentarius | Permitted additive conditions | Annual |
| **CXS 193 Contaminants** | PDF standard | Maximum levels for contaminants | Periodic revisions |

### JECFA and JMPR evaluation databases

The **JECFA database** (apps.who.int/food-additives-contaminants-jecfa-database) contains 6,552+ evaluations of food additives, contaminants, and veterinary drugs with ADIs/TDIs. No bulk download available—web interface only.

**JMPR** (apps.who.int/pesticide-residues-jmpr-database) provides ADIs, acute reference doses (ARfDs), and MRL recommendations for pesticides evaluated since 1991.

### Regional food safety networks

| Region | Organization | URL | Coverage |
|--------|--------------|-----|----------|
| **Americas** | PAHO | paho.org/en/topics/food-safety | 35 member states |
| **Asia-Pacific** | AFSN/ARAC | afsn.net, arac-asean.org | 10 ASEAN states |
| **Global** | INFOSAN | who.int | 188 of 194 member states |

**INFOSAN** handles food safety emergencies across 188 countries but is restricted to officially designated national authorities—public access limited to Information Notes.

### IARC carcinogenicity classifications

The **IARC Monographs** (monographs.iarc.who.int) classify 1,000+ agents into carcinogenicity groups (1, 2A, 2B, 3). Food-related classifications include processed meat (Group 1), red meat (Group 2A), and specific chemicals like aflatoxins. Freely downloadable PDF monographs.

---

## Commercial and open data sources enable programmatic access

### Open Food Facts dominates open food data

**Open Food Facts** (world.openfoodfacts.org) offers **4+ million products** from 150 countries under Open Database License (ODbL):

- REST API v2 with no authentication required for reads
- Bulk downloads as CSV, JSONL, JSON, RDF
- Includes Nutri-Score, NOVA groups, Eco-Score, additives, allergens
- Crowdsourced—data quality varies; best for packaged goods

**FoodRepo** (foodrepo.org) is being **retired February 28, 2026**—migrate to Open Food Facts.

### Nutrition API comparison

| API | Foods | Pricing | Rate Limits | Best For |
|-----|-------|---------|-------------|----------|
| **USDA FoodData Central** | 300,000+ | Free | 1,000/hour | Authoritative baseline |
| **Open Food Facts** | 4M+ | Free | Use bulk for heavy loads | Global packaged foods |
| **FatSecret** | 1M+ | Free (basic) | Generous | Consumer apps |
| **Edamam** | 900,000+ | Free tier to $999/mo | 200/min on paid | Recipe analysis |
| **Spoonacular** | 365,000+ | Free tier to $149/mo | Varies | Recipe management |
| **Nutritionix** | 1.2M+ | $299/mo minimum | Enterprise | Commercial apps |
| **Chomp** | 875,000+ | $299/mo + MAU fees | Enterprise | Branded foods + allergens |

**Nutritionix** discontinued its free tier—minimum now $299/month. **CalorieNinjas** is transitioning to API Ninjas.

### Barcode/UPC databases

| Service | Products | Pricing | API |
|---------|----------|---------|-----|
| **GS1 Data Hub** | 360M+ global | Membership required | Yes |
| **Barcode Lookup** | 500M+ | $99/mo minimum | Yes |
| **UPCitemdb** | Large | Free tier (100/day) | Yes |
| **Go-UPC** | 1B+ | Paid tiers | Yes |
| **EAN-Search** | 1B+ | Free basic; paid API | Yes |

**GS1** is the authoritative source for official GTIN/UPC data but requires paid membership.

### Recall monitoring APIs

| Source | Coverage | Access | Format |
|--------|----------|--------|--------|
| **FDA openFDA** | All FDA-regulated | Free API | JSON |
| **USDA FSIS** | Meat/poultry/eggs | Free API (since 2023) | JSON |
| **RASFF (EU)** | EU food/feed alerts | Web search | HTML |
| **CFIA (Canada)** | Canadian recalls | Web + RSS | HTML |

### Sustainability and carbon footprint databases

**Eaternity** maintains the largest food LCA database (950+ ingredients) with CO₂ and water footprint data, but requires paid API access.

**Our World in Data** (ourworldindata.org/explorers/food-footprints) offers free interactive food footprint data with downloadable datasets via GitHub.

**SU-EATABLE LIFE** provides a free research database with 3,349 carbon footprint values published in Nature Scientific Data.

---

## Industry certification databases verify supplier compliance

### GFSI-benchmarked certification directories

| Certification | Directory | Coverage | Access |
|---------------|-----------|----------|--------|
| **SQF** | sqf.etq.com | Global (North America focus) | Free search |
| **BRCGS** | brcgs.com | 35,000+ sites, 130 countries | Free search |
| **FSSC 22000** | Via certification bodies | Global | Registration required |
| **IFS** | ifs-certification.com | Europe focus | Registration required |

None offer public APIs—verification requires web searches or direct certification body contact.

### Seafood traceability standards

The **Global Dialogue on Seafood Traceability (GDST)** (thegdst.org) provides interoperability standards rather than a database. The open-source **Traceability Driver** tool helps implement GDST-compliant data exchange.

Commercial platforms implementing GDST include **Trace Register**, **BlueTrace**, and **Wholechain**.

---

## Priority recommendations for a consumer platform

### Tier 1: Essential free sources with API access

1. **USDA FoodData Central API** - Authoritative nutrition baseline
2. **Open Food Facts API** - Broadest product coverage globally
3. **FDA openFDA APIs** - Recalls and adverse events
4. **Seafood Watch API** - Seafood sustainability ratings
5. **USDA PDP downloads** - Comprehensive pesticide residue data

### Tier 2: Essential free sources requiring web access or downloads

1. **EWG databases** - Consumer-friendly contaminant rankings
2. **EFSA OpenFoodTox** - Toxicological reference values
3. **Codex MRL databases** - International standards
4. **JECFA/JMPR databases** - Safety assessments

### Tier 3: Commercial APIs for enhanced coverage

1. **FatSecret** (free tier) - Additional nutrition data
2. **Edamam** (freemium) - Recipe analysis
3. **Barcode Lookup or UPCitemdb** - Product identification

### Critical data gaps to address

- **State fish advisories**: No centralized database; requires aggregating 50 state sources
- **Microplastics in food**: No comprehensive monitoring database exists
- **Real-time contaminant testing**: Most data has 1-2 year publication lag
- **Global recall aggregation**: No single source covers international recalls

---

## Conclusion

Building comprehensive food safety coverage requires combining approximately **15-20 core sources** from this catalog: government APIs (USDA, FDA, EPA) provide authoritative contaminant and nutrition data; NGO databases (EWG, Seafood Watch) add consumer-friendly risk context; Open Food Facts supplies product-level data at scale; and international sources (Codex, JECFA, EFSA) provide global harmonized standards.

The most significant technical constraint is that most NGO databases lack APIs—EWG's databases, despite their consumer value, require web scraping or manual data collection. The EU's OpenFoodTox and EFSA databases offer superior programmatic access compared to equivalent U.S. sources.

For a consumer-facing platform, prioritize sources with documented APIs and clear licensing (USDA, FDA, Open Food Facts, Seafood Watch), then supplement with manually curated data from web-only sources (EWG, state advisories) where consumer value justifies the maintenance overhead.
