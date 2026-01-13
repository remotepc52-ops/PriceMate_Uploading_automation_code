import os
from datetime import datetime
today = datetime.today()
today_str = today.strftime("%Y_%m_%d")
BASE_SAVE_PATH = fr"E:\\Data\\Crawl_Data_Collection\\PriceMate\\{today_str}\\Lazada"
# BASE_SAVE_PATH = r"\\192.168.1.129\e\Kamaram\Crawl_Data_Collection\ADA\12_01_2026\Htmls\lazada"
COOKIES_SAVE_PATH = os.path.join(BASE_SAVE_PATH, "cookies")
CHROMEDRIVER_PATH = r"C:\chromedriver\chromedriver.exe"


SHOP_URLS = [

'https://www.lazada.co.id/shop/royal-canin',
'https://www.lazada.co.id/shop/instinct-pet-food-indonesia',
'https://www.lazada.com.ph/shop/p-g-home-care-official-store/',
'https://www.lazada.sg/shop/darlie',
'https://www.lazada.com.ph/shop/universal-robina',
'https://www.lazada.com.my/shop/heineken-malaysia',
'https://www.lazada.com.my/shop/dugro',
'https://www.lazada.com.ph/shop/mac-cosmetics',
'https://www.lazada.com.ph/shop/silka-skincare-store',
'https://www.lazada.com.my/shop/signature-market',
'https://www.lazada.com.my/shop/carelatex/',
'https://www.lazada.com.my/shop/eureka-popcorn-snack',
'https://www.lazada.com.ph/shop/brilliant-skin-essentials-ncr',
'https://www.lazada.co.id/shop/la-tulipe-store',
'https://www.lazada.com.ph/unilever-beauty',
'https://www.lazada.com.my/shop/s26-gold-progress',
'https://www.lazada.com.my/shop/lotuss-official-store',
'https://www.lazada.com.ph/shop/ajinomoto-ph-official-store',
'https://www.lazada.com.ph/shop/dr-sensitive',
'https://www.lazada.com.my/shop/starbucks-coffee-at-home',
'https://www.lazada.com.ph/shop/p-g-beauty-official-store/?',
'https://www.lazada.com.my/shop/offspring-inc-malaysia',
'https://www.lazada.com.my/shop/lam-soon-edible-oils',
'https://www.lazada.com.my/shop/indomie-store',
'https://www.lazada.com.my/shop/dettol-durex-finish-airwick-gaviscon-vanish-harpic',
'https://www.lazada.com.my/shop/drypers-vinda-dr-p-libresse-tempo-tena',
'https://www.lazada.com.my/shop/bio-pet-products-sdn-bhd',
'https://www.lazada.co.id/shop/godrej-official-store',
'https://www.lazada.com.my/shop/lee-kum-kee',
'https://www.lazada.com.my/shop/wipro-unza-malaysia',
'https://www.lazada.co.id/shop/make-over',
'https://www.lazada.com.ph/shop/ever-bilena',
'https://www.lazada.co.id/shop/nature-republic',
'https://www.lazada.com.ph/shop/natures-spring-water',
'https://www.lazada.sg/shop/kordels',
'https://www.lazada.com.my/shop/aatas-cat',
'https://www.lazada.com.ph/shop/olay-official-store',
'https://www.lazada.com.ph/shop/premier-ws',
'https://www.lazada.co.id/shop/oemah-herborist-official-store',
'https://www.lazada.com.ph/shop/the-face-shop',
'https://www.lazada.com.my/shop/bellamys-flagship-store',
'https://www.lazada.com.my/shop/mamypoko-moony',
'https://www.lazada.com.ph/shop/ardent-world-inc',
'https://www.lazada.com.my/shop/app-petworld',
'https://www.lazada.com.ph/shop/quaker',
'https://www.lazada.com.ph/shop/vice-cosmetics',
'https://www.lazada.sg/shop/loreal-paris',
'https://www.lazada.sg/shop/myeureka-official-store',
'https://www.lazada.com.my/shop/morinaga-malaysia',
'https://www.lazada.co.id/shop/watsons',
'https://www.lazada.co.id/shop/bodyxpert/',
'https://www.lazada.com.ph/shop/l-oreal-paris',
'https://www.lazada.com.my/shop/fernleaf',
'https://www.lazada.co.id/shop/holika-holika/',
'https://www.lazada.com.my/shop/aik-cheong-coffee-roaster-',
'https://www.lazada.com.my/shop/darlie-malaysia',
'https://www.lazada.com.my/shop/ayambrandofficialstore',
'https://www.lazada.com.ph/shop/gt-cosmetics',
'https://www.lazada.com.ph/shop/colourette',
'https://www.lazada.sg/shop/arla',
'https://www.lazada.co.id/shop/dear-klairs/',
'https://www.lazada.co.id/shop/somethinc-official',
'https://www.lazada.com.my/shop/cadbury-oreo-chipsmore-twisties-official-store',
'https://www.lazada.com.ph/shop/unilever-homecare',
'https://www.lazada.co.id/shop/sulwhasoo',
'https://www.lazada.com.my/shop/p-g-malaysia',
'https://www.lazada.com.ph/shop/nutriasia',
'https://www.lazada.co.id/shop/estee-lauder',
'https://www.lazada.com.my/shop/anmum-essential',
'https://www.lazada.com.ph/shop/unilever-foods1632795060',
'https://www.lazada.com.my/shop/maybelline-official-store',
'https://www.lazada.sg/shop/pet-lovers-centre',
'https://www.lazada.com.ph/shop/san-miguel-foods-frozen-chilled-store',
'https://www.lazada.sg/shop/pg',
'https://www.lazada.com.my/shop/mydin-malaysia',
'https://www.lazada.sg/shop/nivea',
'https://www.lazada.com.my/shop/big-pharmacy',
'https://www.lazada.com.my/shop/ajinomoto1627795953',
'https://www.lazada.com.ph/shop/maybelline/',
'https://www.lazada.com.my/shop/petsmore',
'https://www.lazada.com.my/shop/swisse',
'https://www.lazada.com.my/shop/tong-garden',
'https://www.lazada.com.my/shop/boh-tea',
'https://www.lazada.sg/shop/aptamil-dumex',
'https://www.lazada.sg/shop/merries',
'https://www.lazada.co.id/shop/pawsitive-vibes',
'https://www.lazada.sg/shop/nestle',
'https://www.lazada.co.id/shop/missha-indonesia-official',
'https://www.lazada.com.my/shop/probalance-le-gourmet',
'https://www.lazada.com.my/shop/big-three-coffee',
'https://www.lazada.com.my/shop/whiskas-and-pedigree',
'https://www.lazada.sg/shop/durex',
'https://www.lazada.co.id/shop/pet-kingdom-store/',
'https://www.lazada.com.my/shop/loreal-paris-official-store',
'https://www.lazada.com.ph/shop/nature-republic',
'https://www.lazada.co.id/shop/mineral-botanica',
'https://www.lazada.com.my/shop/cetaphil',
'https://www.lazada.com.ph/shop/century-food/',
'https://www.lazada.sg/shop/rascal-friends',
'https://www.lazada.com.ph/shop/coca-cola-flagship-store',
'https://www.lazada.sg/shop/mars-wrigley',
'https://www.lazada.co.id/shop/senka-by-finetoday',
'https://www.lazada.sg/shop/nestle-purina',
'https://www.lazada.sg/shop/laz-mama-shop',
'https://www.lazada.com.my/shop/unicharm-pet',
'https://www.lazada.com.my/shop/sasa-official-store',
'https://www.lazada.sg/shop/drypers-singapore',
'https://www.lazada.com.my/shop/abbott-otc',
'https://www.lazada.com.ph/ul-skin-sciences',
'https://www.lazada.com.my/shop/colgate-palmolive',
'https://www.lazada.sg/shop/eucerin',
'https://www.lazada.com.ph/shop/himalaya',
'https://www.lazada.com.my/shop/wipro-consumer-care-malaysia',
'https://www.lazada.com.ph/shop/frito-lay',
'https://www.lazada.sg/shop/starbucks-at-home',
'https://www.lazada.com.ph/shop/detail-cosmetics/',
'https://www.lazada.com.my/shop/watsons',
'https://www.lazada.com.my/shop/mahnaz-food',
'https://www.lazada.com.ph/shop/san-miguel-foods',
'https://www.lazada.com.my/shop/garnier',
'https://www.lazada.com.my/shop/coca-cola-official',
'https://www.lazada.com.my/shop/power-root-malaysia',
'https://www.lazada.com.ph/shop/sr',
'https://www.lazada.com.my/shop/country-farm-organics',
'https://www.lazada.co.id/shop/the-body-shop',
'https://www.lazada.co.id/shop/cf',
'https://www.lazada.com.my/shop/yew-chian-haw',
'https://www.lazada.co.id/shop/whiskas',
'https://www.lazada.com.my/shop/enfagrow-a',
'https://www.lazada.com.my/shop/wetty',
'https://www.lazada.sg/shop/new-moon-official-store',
'https://www.lazada.com.ph/shop/rfm-foods',
'https://www.lazada.com.my/shop/sunshine-online',
'https://www.lazada.com.my/shop/nestle/',
'https://www.lazada.com.my/shop/ah-huat-',
'https://www.lazada.com.ph/shop/snailwhite',
'https://www.lazada.sg/shop/offspring',
'https://www.lazada.co.id/shop/tempo-store',
'https://www.lazada.com.my/shop/alpro-pharmacy',
'https://www.lazada.sg/shop/himalaya-wellness',
'https://www.lazada.sg/shop/ajinomoto',
'https://www.lazada.sg/shop/garnier',
'https://www.lazada.co.id/shop/pet-kingdom-store',
'https://www.lazada.co.id/shop/mustika-ratu-id',
'https://www.lazada.sg/shop/blackmores',
'https://www.lazada.com.ph/shop/nivea',
'https://www.lazada.com.my/shop/enfagrow-official-store',
'https://www.lazada.com.ph/shop/blk-cosmetics/',
'https://www.lazada.co.id/shop/emina/',
'https://www.lazada.co.id/shop/purina/',
'https://www.lazada.co.id/shop/pedigree',
'https://www.lazada.com.my/shop/sc-johnson',
'https://www.lazada.co.id/shop/unilever-food-solutions/',
'https://www.lazada.co.id/shop/laneige',
'https://www.lazada.com.my/shop/ozpro',
'https://www.lazada.com.my/shop/huggies',
'https://www.lazada.com.my/shop/prodiet-delizios',
'https://www.lazada.com.my/shop/friso-gold',
'https://www.lazada.sg/shop/kao',
'https://www.lazada.com.ph/shop/iwhite-korea',
'https://www.lazada.co.id/shop/dettol-vanish-harpic',
'https://www.lazada.com.my/shop/ferrero-os-malaysia',
'https://www.lazada.com.ph/shop/watsons',
'https://www.lazada.com.my/shop/smartheart/',
'https://www.lazada.com.ph/shop/belo/',
'https://www.lazada.com.ph/shop/zest-o-official-store',
'https://www.lazada.sg/shop/s26',
'https://www.lazada.sg/shop/mamypoko-flagship-store',
'https://www.lazada.sg/shop/swisse',
'https://www.lazada.sg/shop/dettol',
'https://www.lazada.sg/shop/braun',
'https://www.lazada.co.id/shop/frisian-flag',
'https://www.lazada.com.my/shop/mars-wrigley',
'https://www.lazada.sg/shop/unilever',
'https://www.lazada.co.id/shop/revlon',
'https://www.lazada.sg/shop/fonterra',
'https://www.lazada.com.my/shop/unilever',
'https://www.lazada.com.my/shop/jasminefoodos',
'https://www.lazada.co.id/shop/viva-cosmetics-official',
'https://www.lazada.com.my/shop/guardian',
'https://www.lazada.sg/shop/lion',
'https://www.lazada.co.id/shop/wings-flagship-store',
'https://www.lazada.sg/shop/probalance-store',
'https://www.lazada.com.my/shop/happy-dog-happy-cat',
'https://www.lazada.com.my/shop/adabi',
'https://www.lazada.com.my/shop/instinct-pet-food',
'https://www.lazada.sg/shop/kenvue',
'https://www.lazada.co.id/shop/rollover-reaction',
'https://www.lazada.co.id/shop/popmiestore/',
'https://www.lazada.com.my/shop/amelisa-pet-co',
'https://www.lazada.com.my/shop/aunhuat',
'https://www.lazada.com.my/shop/aptamilkid',
'https://www.lazada.com.ph/shop/nestle-store/',
'https://www.lazada.com.my/shop/walls',
'https://www.lazada.sg/shop/haleon',
'https://www.lazada.com.my/shop/nivea-official',
'https://www.lazada.com.my/shop/ur-munchy-s-store',
'https://www.lazada.com.my/shop/kenvue',
'https://www.lazada.co.id/shop/cature-indonesia/',
'https://www.lazada.sg/shop/cetaphil',
'https://www.lazada.com.my/shop/pediasure',
'https://www.lazada.co.id/shop/sk-ii',
'https://www.lazada.sg/shop/bellamys-organic',
'https://www.lazada.com.my/shop/dutch-lady',
'https://www.lazada.co.id/shop/wellness-official',
'https://www.lazada.com.my/shop/rascals-premium-diapers',
'https://www.lazada.co.id/shop/beautyhaul-indonesia',
'https://www.lazada.sg/shop/f-n-sg',
'https://www.lazada.co.id/shop/dancow',
'https://www.lazada.com.my/shop/haleon',
'https://www.lazada.com.ph/shop/monde-nissin',
'https://www.lazada.co.id/shop/nivea',
'https://www.lazada.com.my/shop/nature-s-way',
'https://www.lazada.sg/shop/kimberly-clark1632817711',
'https://www.lazada.com.my/shop/innisfree',
'https://www.lazada.com.my/shop/natures-protection-my',
'https://www.lazada.com.ph/shop/revlon',
'https://www.lazada.co.id/shop/pixy1632881128',
'https://www.lazada.com.ph/shop/kenvue',
'https://www.lazada.sg/shop/natures-way',
'https://www.lazada.com.ph/shop/human-nature1630478979',
'https://www.lazada.sg/shop/friso',
'https://www.lazada.co.id/shop/wardah-ofc-store/',
'https://www.lazada.co.id/shop/pedigree/',
'https://www.lazada.com.my/shop/kao',
'https://www.lazada.sg/shop/brands',
'https://www.lazada.sg/shop/qv',
'https://www.lazada.com.my/shop/nulatex',
'https://www.lazada.com.ph/shop/hello-glow',
'https://www.lazada.com.my/shop/brands-os-official-store',
'https://www.lazada.com.my/shop/dettol',
'https://www.lazada.com.my/shop/etika',
'https://www.lazada.co.id/shop/unilever-flagship-store',
'https://www.lazada.com.my/shop/chemist-warehouse-australia',
'https://www.lazada.com.my/shop/ouji-walch',
'https://www.lazada.com.my/shop/pepsico',
'https://www.lazada.com.my/shop/bio-lifestyle-sdn-bhd',
'https://www.lazada.sg/shop/pampers',
'https://www.lazada.com.ph/shop/ordinary-global-store',
'https://www.lazada.sg/shop/colgate',
'https://www.lazada.com.my/shop/lazada-groceries',
'https://www.lazada.co.id/shop/maybelline',
'https://www.lazada.com.my/shop/f-n-creameries-my',
'https://www.lazada.sg/shop/lam-soon',
'https://www.lazada.sg/shop/innisfree',
'https://www.lazada.com.my/shop/frenche-roast',
'https://www.lazada.sg/shop/hills',
'https://www.lazada.sg/shop/banana-boat',
'https://www.lazada.co.id/shop/l-oreal-paris/',
'https://www.lazada.co.id/shop/kose',
'https://www.lazada.co.id/shop/sc-johnson',
'https://www.lazada.sg/shop/enfagrow',
'https://www.lazada.sg/shop/olly1625144608',
'https://www.lazada.co.id/shop/clinique',
'https://www.lazada.sg/shop/maybelline',
'https://www.lazada.co.id/shop/pg-official-store',
'https://www.lazada.com.ph/shop/happy-skin',
'https://www.lazada.com.my/shop/southern-lion-home',
'https://www.lazada.com.ph/shop/careline/',
'https://www.lazada.co.id/shop/shiseido',
'https://www.lazada.com.my/shop/oldtown-white-coffee',
'https://www.lazada.com.ph/shop/colgate-palmolive',
'https://www.lazada.com.my/shop/purina',
'https://www.lazada.sg/shop/jde-world-of-coffee',
'https://www.lazada.co.id/shop/mayora',
'https://www.lazada.com.my/shop/mamee1629976185',
'https://www.lazada.com.my/shop/hill-s-pet-nutrition-official-store',
'https://www.lazada.com.my/shop/farm-fresh-malaysia-official',
'https://www.lazada.com.my/shop/spritzer',
'https://www.lazada.sg/shop/bioglan',
'https://www.lazada.com.ph/shop/innisfree',
'https://www.lazada.com.my/shop/lider-pet-offical-store',
'https://www.lazada.sg/shop/lee-kum-kee',
'https://www.lazada.sg/shop/carlsberg-official-store1620361782',
'https://www.lazada.com.my/shop/julies',
'https://www.lazada.com.my/shop/blackmores-official-store',
'https://www.lazada.com.my/shop/bdg-express-sabah-sarawak',
'https://www.lazada.com.ph/shop/cetaphil/',
'https://www.lazada.co.id/shop/lt-pro-store',
'https://www.lazada.sg/shop/walch',
'https://www.lazada.com.ph/shop/green-cross',
'https://www.lazada.co.id/shop/mac',
'https://www.lazada.sg/shop/abbotts-nutrition',
'https://www.lazada.com.my/shop/jde-world-of-coffee',
'https://www.lazada.sg/shop/watsons',
'https://www.lazada.com.ph/shop/fresh/',
'https://www.lazada.sg/shop/nutrilife',
'https://www.lazada.co.id/shop/innisfree',
'https://www.lazada.com.my/shop/sin-sing-coffee',
'https://www.lazada.sg/shop/care-latex',
'https://www.lazada.com.my/shop/playsafe-unlimited',
'https://www.lazada.com.ph/shop/cosrx',
'https://www.lazada.sg/shop/bayer-official-store',


]

# SHOP_URLS = [
#     'https://www.lazada.com.ph/shop/nestle-store',
#     'https://www.lazada.com.ph/shop/nestle-wyeth-nutrition',
#     'https://www.lazada.com.ph/shop/nestle-health-science-store',
#     'https://www.lazada.com.ph/shop/lazmart',
#     'https://www.lazada.com.ph/shop/nestle-purina',
#     'https://lazada.com.ph/shop/enfagrow-store',
#     'https://lazada.com.ph/shop/lactum-store',
#     'https://lazada.com.ph/shop/sustagen-adult-nutrition-milk',
#     'https://www.lazada.com.ph/shop/lysol-and-reckitt-home-store',
#     'https://lazada.com.ph/shop/reckitt-health-and-beauty',
#     'https://shopee.ph/reckitthealthofficial',
#     'https://www.lazada.com.my/shop/health-lane-family-pharmacy/?itemId=325277093&channelSource=pdp',
#     'https://www.lazada.com.ph/shop/huggies',
#     'https://www.lazada.com.ph/shop/moony',
#     'https://www.lazada.com.ph/shop/aiwibiphofficialstore',
#     'https://www.lazada.com.ph/shop/kotex',
#     'https://www.lazada.com.ph/shop/sofy',
#     'https://www.lazada.com.ph/shop/abbott1630395516',
#     'https://www.lazada.com.ph/shop/promil',
#     'https://www.lazada.com.ph/shop/nido',
#     'https://www.lazada.com.ph/shop/unilever-foods1632795060',
#     'https://www.lazada.com.ph/shop/ajinomoto-ph-official-store',
#     'https://www.lazada.com.ph/shop/monde-nissin',
#     'https://www.lazada.com.ph/shop/alaska',
#     'https://www.lazada.com.ph/shop/san-miguel-foods',
#     'https://www.lazada.com.ph/shop/century-food',
#     'https://www.lazada.com.ph/shop/rfm-foods',
#     'https://www.lazada.com.ph/shop/cowhead',
#     'https://www.lazada.com.ph/shop/universal-robina',
#     'https://www.lazada.com.ph/shop/ucc-coffee',
#     'https://www.lazada.com.ph/shop/mx3-supplements-ph',
#     'https://www.lazada.com.ph/shop/sante-official',
#     'https://www.lazada.com.ph/shop/ovaltine',
#     'https://www.lazada.com.ph/shop/biggrocer-food-grocery',
#     'https://www.lazada.com.ph/shop/mondelez-ph',
#     'https://www.lazada.com.ph/shop/mondelez-ph-chocolates',
#     'https://www.lazada.com.ph/shop/natures-harvest',
#     'https://www.lazada.com.ph/shop/mars-wrigley',
#     'https://www.lazada.com.ph/shop/raw-bites-ph',
#     'https://www.lazada.com.ph/shop/pedigree-and-whiskas',
#     'https://www.lazada.com.ph/shop/royal-canin',
#     'https://www.lazada.com.ph/shop/vitality',
#     'https://www.lazada.com.ph/shop/san-miguel-animal-health-pet-care',
#     'https://www.lazada.com.ph/kellogg-s-and-pringles-official-store',
#     'https://www.lazada.com.ph/del-monte-ph',
#     'https://www.lazada.com.ph/shop/pet-one-official-store',
#     'https://www.lazada.com.ph/shop/bow-wow-ph',
#     'https://www.lazada.com.ph/shop/fonterra',
#     'https://www.lazada.com.ph/shop/bonavita-philippines',
#     'https://www.lazada.com.ph/shop/hershey-s-philippines',
#     'https://www.lazada.com.ph/shop/kopiko-ph',
#     'https://www.lazada.com.ph/shop/dr-shiba-dog-supplements',
#     'https://www.lazada.com.ph/shop/nutriasia',
#     'https://www.lazada.com.ph/shop/injoyph',
#     'https://www.lazada.com.ph/shop/kreme-city-supplies',
#     'https://www.lazada.com.ph/shop/kalbe-ecossential-international-philippines',
#     'https://www.lazada.com.ph/shop/unilab',
#     'https://www.lazada.com.ph/shop/mega1629966939',
#     'https://lazada.com.ph/shop/p-g-health-official-store',
#     'https://lazada.com.ph/shop/inova-health-store',
#     'https://www.lazada.com.ph/shop/jellytime',
#     'https://www.lazada.com.ph/shop/tenga1632887154',
#     'https://lazada.com.ph/shop/unilever-homecare',
#     'https://lazada.com.ph/shop/sc-johnson',
#     'https://lazada.com.ph/shop/fishermans-friend-jci',
#     'https://lazada.com.ph/shop/nestogrow',
#     'https://www.lazada.com.ph/shop/betadine',
#     'https://lazada.com.ph/shop/just-call-inc-imds',
#     'https://lazada.com.ph/shop/maximus',
#     'https://www.lazada.com.ph/shop/kenvue',
#     'https://www.lazada.com.ph/shop/starbucks',
#     'https://www.lazada.com.ph/shop/nescafe-dolce-gusto',
#     'https://www.lazada.com.ph/shop/oishi',
#     'https://www.lazada.com.ph/shop/dujosoo',
#     'https://www.lazada.com.ph/shop/petmarra',
#     'https://www.lazada.com.ph/shop/topbreed',
#     'https://www.lazada.com.ph/shop/global-winds-corp',
#     'https://www.lazada.com.ph/shop/consumer-care-products-inc',
#     'https://www.lazada.com.ph/shop/personal-collection',
#     'https://www.lazada.com.ph/shop/cov-x-disinfectant',
#     'https://www.lazada.com.ph/shop/hipp-organic',
#     'https://www.lazada.com.ph/shop/nutricia-philippines',
#     'https://www.lazada.com.ph/shop/philusa',
#     'https://www.lazada.com.ph/shop/the-generics-pharmacy-tgp',
#     'https://www.lazada.com.ph/shop/galenx',
#     'https://www.lazada.com.ph/shop/lanbena-beauty',
#     'https://www.lazada.com.ph/shop/abbott-flagship-store',
#     'https://www.lazada.com.ph/shop/sr',
#     'https://www.lazada.com.ph/shop/watsons',
#     'https://www.lazada.com.ph/shop/mondelez-ph-store',
#     'https://www.lazada.com.ph/shop/the-booze-shop1631608599',
#     'https://www.lazada.com.ph/shop/sukigrocermnl',
#     'https://www.lazada.com.ph/shop/naturefood-organics',
#     'https://www.lazada.com.ph/shop/arla-foods',
#     'https://www.lazada.com.ph/shop/rebisco',
#     'https://www.lazada.com.ph/shop/euro-rich',
#     'https://www.lazada.com.ph/shop/cdo-foodsphere-canned-products',
#     'https://www.lazada.com.ph/shop/p-g-home-care-official-store',
#     'https://www.lazada.com.ph/shop/mightyclean',
#     'https://www.lazada.com.ph/shop/megasoft-hygienic-products-inc',
#     'https://www.lazada.com.ph/shop/briteph',
#     'https://www.lazada.com.ph/shop/wincommerce-corporation',
#     'https://www.lazada.com.ph/shop/green-cross',
#     'https://www.lazada.com.ph/shop/3m-official-store',
#     'https://www.lazada.com.ph/shop/unilove',
#     'https://www.lazada.com.ph/shop/sweetbaby-diaper',
#     'https://www.lazada.com.ph/shop/kleenfant',
#     'https://www.lazada.com.ph/shop/gentle-supreme',
#     'https://www.lazada.com.ph/shop/shophygiene-ph',
#     'https://www.lazada.com.ph/shop/colgate-palmolive',
#     'https://www.lazada.com.ph/shop/premier-wash',
#     'https://www.lazada.com.ph/shop/scrubdaddyph',
#     'https://www.lazada.com.ph/shop/anymore-ph',
#     'https://www.lazada.com.ph/shop/southstar-drug-inc',
#     'https://www.lazada.com.ph/shop/indoplas-philippines',
#     'https://www.lazada.com.ph/shop/haleon-ph',
#     'https://www.lazada.com.ph/shop/js-unitrade-adult-care',
#     'https://www.lazada.com.ph/shop/optimum-nutrition',
#     'https://www.lazada.com.ph/shop/omron',
#     'https://www.lazada.com.ph/shop/athlene-nutrition',
#     'https://www.lazada.com.ph/shop/rule-1-proteins',
#     'https://www.lazada.com.ph/shop/met-tathione',
#     'https://www.lazada.com.ph/shop/sinocare-official-store',
#     'https://www.lazada.com.ph/shop/muscletech',
#     'https://www.lazada.com.ph/shop/puritans-pride',
#     'https://www.lazada.com.ph/shop/swanson-vitamins',
#     'https://www.lazada.com.ph/shop/sinocare-ph',
#     'https://www.lazada.com.ph/shop/just-love-ph',
#     'https://www.lazada.com.ph/shop/champion-biotech',
#     'https://www.lazada.com.ph/shop/pureform',
#     'https://www.lazada.com.ph/shop/rascal-friends',
#     'https://www.lazada.com.ph/shop/eq',
#     'https://www.lazada.com.ph/shop/moose-gear-baby',
#     'https://www.lazada.com.ph/shop/tiny-buds',
#     'https://www.lazada.com.ph/shop/hey-tiger',
#     'https://www.lazada.com.ph/shop/pampers-official-store',
#     'https://www.lazada.com.ph/shop/mamypoko',
#     'https://www.lazada.com.ph/shop/cetaphil',
#     'https://www.lazada.com.ph/shop/mustela',
#     'https://www.lazada.com.ph/shop/snack-room-food',
#     'https://www.lazada.com.ph/shop/sharke-mother-baby',
#     'https://www.lazada.com.ph/shop/frito-lay',
#     'https://www.lazada.com.ph/shop/seaways-official-store',
#     'https://www.lazada.com.ph/shop/royo-tissue',
#     'https://www.lazada.com.ph/shop/timsot',
#     'https://www.lazada.com.ph/shop/t-oras',
#     'https://www.lazada.com.ph/shop/goodies-nutrition',
#     'https://www.lazada.com.ph/shop/ichi-ph',
#     'https://www.lazada.com.ph/shop/builtamart',
#     'https://www.lazada.com.ph/shop/mr-squirrel-groceries',
#     'https://www.lazada.com.ph/shop/mapecon-phils-inc',
#     'https://www.lazada.com.ph/shop/icare',
#     'https://www.lazada.com.ph/shop/makukuph',
#     'https://www.lazada.com.ph/shop/farcent-philippines',
#     'https://www.lazada.com.ph/shop/pet-express',
#     'https://www.lazada.com.ph/shop/pet-house-official-store',
#     'https://www.lazada.com.ph/shop/pet-lovers-centre',
#     'https://www.lazada.com.ph/shop/cphn-milk-shop',
#     'https://www.lazada.com.ph/shop/house-of-babies',
#     'https://www.lazada.com.ph/shop/mom-baby-s-nest',
#     'https://www.lazada.com.ph/shop/clickhealthy',
#     'https://www.lazada.com.ph/shop/g-milk',
#     'https://www.lazada.com.ph/shop/keos-push-cart',
#     'https://www.lazada.com.ph/shop/dlexs',
#     'https://www.lazada.com.ph/shop/lauvette',
#     'https://www.lazada.com.ph/shop/secret-corner-ph',
#     'https://www.lazada.com.ph/shop/hnw-shop',
#     'https://www.lazada.com.ph/shop/midoko-official-shop',
#     'https://www.lazada.com.ph/shop/jas-supermart',
#     'https://www.lazada.com.ph/shop/mx8mj7lt',
#     'https://www.lazada.com.ph/shop/edge-marketing-trading',
#     'https://www.lazada.com.ph/glowwell',
#
# ]

import json
import time
import asyncio
import logging
import requests
import pickle
from pathlib import Path
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import undetected_chromedriver as uc

# ==================================================
# CONFIG
# ==================================================

TELEGRAM_BOT_TOKEN = "7992426144:AAGSUbsqjjKR_0k5Url8BPijviNT1QcXNZU"
TELEGRAM_CHAT_ID = "2093836473"

# ==================================================
# LOGGING
# ==================================================
logging.basicConfig(
   level=logging.INFO,
   format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# ==================================================
# TELEGRAM
# ==================================================
# def send_telegram(msg: str):
#    try:
#       requests.post(
#          f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
#          data={"chat_id": TELEGRAM_CHAT_ID, "text": msg},
#          timeout=10
#       )
#    except Exception as e:
#       logger.error(f"Telegram error: {e}")


# ==================================================
# MAIN CLASS
# ==================================================
class LazadaNetworkSaver:

   def __init__(self, urls, base_path=BASE_SAVE_PATH, chrome_path=None):
      self.urls = urls
      self.base_path = base_path
      self.cookies_path = os.path.join(base_path, "cookies")
      self.chrome_path = chrome_path

      os.makedirs(self.cookies_path, exist_ok=True)
      os.makedirs(base_path, exist_ok=True)

      self.driver = None
      self.session = requests.Session()
      self.captcha_solved_once_per_domain = {}
      self.cookies_loaded_domains = set()  # Track domains where cookies were already loaded

   # ------------------------------------------------
   # DRIVER
   # ------------------------------------------------
   def create_driver(self):
      """Create a clean Chrome driver without user data"""
      logger.info("Creating Chrome driver...")
      try:
         # Setup capabilities with logging preferences BEFORE driver creation
         from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
         
         caps = DesiredCapabilities.CHROME
         caps["goog:loggingPrefs"] = {"performance": "ALL"}  # Enable performance logging

         options = uc.ChromeOptions()
         options.add_argument("--start-maximized")
         options.add_argument("--disable-blink-features=AutomationControlled")
         options.add_argument("--no-sandbox")
         options.add_argument("--disable-dev-shm-usage")
         options.add_argument("--disable-gpu")
         options.add_argument("--disable-extensions")
         options.add_argument("--disable-plugins")
         options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

         # Create driver with capabilities - THIS IS IMPORTANT for network logging
         driver = uc.Chrome(options=options, desired_capabilities=caps, use_subprocess=True)
         driver.set_page_load_timeout(60)

         # Enable network tracking from the start
         try:
            driver.execute_cdp_cmd('Network.enable', {})
            logger.info("✅ Chrome DevTools Protocol enabled for network capture")
         except Exception as e:
            logger.warning(f"⚠️  CDP Network.enable failed: {e}")

         logger.info("✅ Chrome driver created successfully")
         return driver
      except Exception as e:
         logger.error(f"❌ Failed to create driver: {e}")
         raise

   def close_driver(self):
      """Safely close driver"""
      if self.driver:
         try:
            self.driver.quit()
            logger.info("✅ Driver closed")
         except:
            pass
         self.driver = None

   # ------------------------------------------------
   # NETWORK CAPTURE
   # ------------------------------------------------
   def capture_network_requests(self, page_num):
      """Capture AJAX requests using CDP with better error handling"""
      time.sleep(2)

      try:
         # Get all network logs
         logs = self.driver.get_log("performance")
         
         if not logs:
            logger.warning(f"[PAGE {page_num}] No performance logs available")
            return None
            
      except Exception as e:
         logger.warning(f"[PAGE {page_num}] Failed to get performance logs: {e}")
         return None

      ajax_responses = []
      request_count = 0
      ajax_urls_found = []  # Track all ajax=true URLs for debugging
      all_response_urls = []  # Track all response URLs for debugging

      for log in logs:
         try:
            msg = json.loads(log["message"])["message"]

            # Capture responses
            if msg["method"] == "Network.responseReceived":
               request_count += 1
               url = msg["params"]["response"]["url"]
               all_response_urls.append(url)

               # Filter for AJAX requests - only ajax=true (NOT ajaxapi)
               if "ajax=true" in url:
                  ajax_urls_found.append(url)  # Track for debugging
                  req_id = msg["params"]["requestId"]

                  try:
                     # Get response body using CDP
                     body_response = self.driver.execute_cdp_cmd(
                        "Network.getResponseBody",
                        {"requestId": req_id}
                     )

                     body = body_response.get("body", "")
                     if body:
                        try:
                           # Parse JSON to ensure it's valid
                           if isinstance(body, str):
                              json_body = json.loads(body)
                           else:
                              json_body = body
                           
                           # Validate response is not a CAPTCHA/error response
                           if self.is_valid_response(json_body):
                              # Add to responses list with URL info
                              ajax_responses.append({
                                 "url": url,
                                 "response": json_body
                              })
                              logger.debug(f"[PAGE {page_num}] Captured AJAX: {url[:80]}...")
                           else:
                              logger.warning(f"[PAGE {page_num}] ⚠️  Skipped error/CAPTCHA response: {json_body.get('ret', 'Unknown error')}")
                        except json.JSONDecodeError:
                           # If not valid JSON, skip it
                           logger.debug(f"[PAGE {page_num}] Response not JSON: {url[:80]}...")

                  except Exception as e:
                     logger.debug(f"[PAGE {page_num}] Could not get body for {url}: {e}")
         except Exception as e:
            logger.debug(f"[PAGE {page_num}] Error parsing log: {e}")

      # Enhanced logging for debugging
      logger.info(f"[PAGE {page_num}] Scanned {request_count} requests, found {len(ajax_urls_found)} ajax=true URLs, captured {len(ajax_responses)} AJAX responses")
      if ajax_urls_found:
         logger.debug(f"[PAGE {page_num}] ajax=true URLs: {ajax_urls_found[:2]}")  # Show first 2
      else:
         # If no ajax=true found, show sample of other URLs for debugging
         sample_urls = [u for u in all_response_urls if 'api' in u.lower() or 'graphql' in u.lower()][:3]
         if sample_urls:
            logger.debug(f"[PAGE {page_num}] No ajax=true URLs. Sample API URLs: {sample_urls}")
      
      return ajax_responses if ajax_responses else None

   def is_valid_response(self, json_data):
      """Check if response contains valid product data (not CAPTCHA/error response)"""
      try:
         if not json_data or not isinstance(json_data, dict):
            return False
         
         # Check for error codes that indicate CAPTCHA or other failures
         error_indicators = [
            'FAIL_SYS_USER_VALIDATE',  # CAPTCHA error
            'RGV587_ERROR',             # CAPTCHA error variant
            'ERROR',                    # Generic error
            'error',                    # Generic error
            'exception',                # Exception
            'Exception',                # Exception
         ]
         
         # Check ret field (main error indicator)
         if json_data.get('ret') in error_indicators:
            logger.debug(f"⚠️  Error response detected: {json_data.get('ret')}")
            return False
         
         # Check if response has actual data
         # if 'data' in json_data and json_data['data']:
         #    return True
         
         # Check if response has productList or items
         if 'productList' in json_data or 'items' in json_data:
            return True
            
         # Check mainInfo exists (product list page structure)
         if 'mainInfo' in json_data:
            return True
         
         logger.debug(f"⚠️  Response has no expected data fields")
         return False
      except Exception as e:
         logger.debug(f"Error validating response: {e}")
         return False

   def check_no_more_pages(self, ajax_responses):
      """Check if noMorePages flag is true in the AJAX response"""
      try:
         # ajax_responses is now a list of dicts with 'url' and 'response' keys
         if not ajax_responses or not isinstance(ajax_responses, list):
            return False
         
         for item in ajax_responses:
            try:
               json_data = item.get('response')
               if not json_data:
                  continue
               
               # Check for noMorePages flag
               if 'mainInfo' in json_data and json_data['mainInfo'].get('noMorePages') == True:
                  logger.info(f"✅ API indicates no more pages (noMorePages=true)")
                  return True
            except:
               pass
         
         return False
      except:
         return False

   def scroll_and_capture(self, start_page=1, max_pages=102):
      """Scroll to load more content and capture AJAX requests with pagination support"""
      pages = {}
      page = start_page

      while page <= max_pages:
         logger.info(f"📄 Capturing page {page}...")

         # Capture AJAX responses with retry for CAPTCHA/errors
         ajax_responses = self.capture_network_requests(page)
         retry_count = 0
         max_retries = 3

         # If no valid responses, retry (might be CAPTCHA not yet solved)
         while not ajax_responses and retry_count < max_retries:
            retry_count += 1
            logger.warning(f"⚠️  No valid responses on page {page} (attempt {retry_count}/{max_retries}). Waiting and retrying...")
            time.sleep(5)  # Wait 5 seconds before retrying
            ajax_responses = self.capture_network_requests(page)

         if not ajax_responses:
            logger.info(f"❌ No AJAX requests found at page {page} after {max_retries} retries")
            if page == 1:
               logger.warning("⚠️  No AJAX data on first page. Check if CAPTCHA was properly solved.")
               # Don't proceed if first page has no data
               break
            else:
               # If subsequent pages fail, stop
               break
         else:
            pages[f"page_{page}"] = ajax_responses
            logger.info(f"✅ Page {page} captured successfully with valid data")
            
            # Check if API says no more pages
            if self.check_no_more_pages(ajax_responses):
               logger.info(f"🛑 Stopping - API indicates no more pages")
               break

         # Try pagination
         try:
            next_button = self.driver.find_element(By.XPATH, "//li[@class='ant-pagination-next']")
            
            # Check if next button is disabled
            if "ant-pagination-disabled" in next_button.get_attribute("class"):
               logger.info("✅ Last page reached - pagination disabled")
               break
            
            # Click next button
            logger.info(f"⬇️  Clicking next page button...")
            self.driver.execute_script("arguments[0].click();", next_button)
            time.sleep(3)
            
         except Exception as e:
            logger.warning(f"No pagination button found or error: {str(e)[:80]}")

            # If no button found and no "noMorePages" flag, try scrolling
            if ajax_responses and not self.check_no_more_pages(ajax_responses):
               logger.info(f"⬇️  Scrolling instead...")
               self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
               time.sleep(3)
            else:
               break

         page += 1

      return pages
   # COOKIES
   # ------------------------------------------------
   def get_domain_from_url(self, url):
      """Extract domain from URL"""
      parsed = urlparse(url)
      return parsed.netloc

   def save_cookies(self, domain):
      """Save cookies to file with retry logic"""
      if not self.driver:
         return

      cookies_file = os.path.join(self.cookies_path, f"{domain}_cookies.pkl")
      try:
         time.sleep(2)  # Wait for driver to stabilize
         cookies = self.driver.get_cookies()
         with open(cookies_file, "wb") as f:
            pickle.dump(cookies, f)
         logger.info(f"💾 Cookies saved for {domain}")
      except Exception as e:
         logger.warning(f"Warning saving cookies: {e} - continuing anyway")

   def load_cookies(self, domain):
      """Load cookies from file"""
      cookies_file = os.path.join(self.cookies_path, f"{domain}_cookies.pkl")
      if os.path.exists(cookies_file):
         try:
            with open(cookies_file, "rb") as f:
               cookies = pickle.load(f)
            return cookies
         except Exception as e:
            logger.error(f"Error loading cookies: {e}")
      return None

   def apply_cookies_to_driver(self, cookies, domain):
      """Apply saved cookies to driver"""
      if not cookies or not self.driver:
         return

      try:
         # First navigate to domain to set cookies
         self.driver.get(f"https://{domain}")
         time.sleep(2)

         for cookie in cookies:
            try:
               # Clean cookie data
               clean_cookie = {
                  'name': cookie.get('name'),
                  'value': cookie.get('value'),
                  'domain': cookie.get('domain', domain),
                  'path': cookie.get('path', '/'),
               }
               self.driver.add_cookie(clean_cookie)
            except Exception as e:
               logger.debug(f"Skipping cookie {cookie.get('name')}: {e}")

         logger.info(f"✅ Cookies applied for {domain}")
         return True
      except Exception as e:
         logger.error(f"Error applying cookies: {e}")
         return False

   # ------------------------------------------------
   # CAPTCHA
   # ------------------------------------------------
   def captcha_present(self):
      """Check if CAPTCHA iframe is present"""
      try:
         elements = self.driver.find_elements(
            By.XPATH,
            "//iframe[contains(@src,'recaptcha') or contains(@src,'punish')]"
         )
         return len(elements) > 0
      except:
         return False

   def wait_captcha_clear(self, timeout=300):
      """Wait for CAPTCHA to be solved"""
      end = time.time() + timeout
      while time.time() < end:
         if not self.captcha_present():
            return True
         time.sleep(2)
      return False

   def handle_manual_captcha(self, domain):
      """Wait for manual CAPTCHA solve"""
      # send_telegram(
      #    "🚨 Lazada CAPTCHA detected.\n"
      #    "Please solve it MANUALLY in the opened browser.\n"
      #    "Do NOT close Chrome."
      # )
      logger.warning("⏳ Waiting for MANUAL CAPTCHA solve...")

      if self.wait_captcha_clear(timeout=300):
         logger.info("✅ Manual CAPTCHA solved")
         time.sleep(3)
         self.save_cookies(domain)
         self.captcha_solved_once_per_domain[domain] = True
         return True
      else:
         raise RuntimeError("Manual CAPTCHA not solved within timeout")

   # ------------------------------------------------
   # FILE MANAGEMENT
   # ------------------------------------------------
   def get_shop_id(self, url):
      """Extract shop ID from URL"""
      # try:
      #    # Try Lazada format first
      #    if "/shop/" in url:
      #       shop_id = url.split("/shop/")[1].split("/")[0]
      #       return shop_id
      # except:
      #    pass

      # Fallback: clean URL to filename
      clean = url.replace('https://', '').replace('http://', '')
      clean = clean.replace('www.', '').split("?")[0]
      clean = clean.strip("/").replace("/", "_")
      return clean

   def get_save_directory(self, shop_id):
      """Get save directory for shop"""
      shop_dir = os.path.join(self.base_path, "HTMLs", shop_id)
      os.makedirs(shop_dir, exist_ok=True)
      return shop_dir

   def get_last_saved_page(self, shop_dir):
      """Check existing pages and return the last page number saved"""
      try:
         # List all files in directory
         files = os.listdir(shop_dir)
         # Filter for page JSON files (e.g., shop_id_page_1.json)
         page_files = [f for f in files if "_page_" in f and f.endswith(".json")]
         
         if not page_files:
            return 0  # No pages saved yet
         
         # Extract page numbers from filenames
         page_numbers = []
         for f in page_files:
            try:
               # Extract number from "shop_id_page_X.json"
               page_num = int(f.split("_page_")[1].split(".")[0])
               page_numbers.append(page_num)
            except:
               pass
         
         if page_numbers:
            last_page = max(page_numbers)
            logger.info(f"✅ Found {len(page_numbers)} existing pages - resuming from page {last_page + 1}")
            return last_page
        
         return 0
      except:
         return 0

   def is_already_saved(self, shop_id):
      """Check if shop data is already saved"""
      shop_dir = self.get_save_directory(shop_id)
      metadata_file = os.path.join(shop_dir, "metadata.json")
      return os.path.exists(metadata_file)

   def is_last_page(self, shop_dir, shop_id,last_saved_page):
      """Check if last page data is already saved"""
      fullpath = os.path.join(shop_dir, f"{shop_id}_page_{last_saved_page}.json")
      if os.path.exists(fullpath):
         response = open(fullpath, 'r', encoding='utf-8').read()
         try:
            loaded_json = json.loads(response)[0]['response']
         except:
            loaded_json = json.loads(response)

         try:noMorePages = loaded_json['mainInfo']['noMorePages']
         except:
            os.remove(fullpath)
            noMorePages = False

         if not noMorePages and len(loaded_json['mods']['listItems']) < 40:
            os.remove(fullpath)
            noMorePages = False
            for i in range(last_saved_page, last_saved_page+10):
               fullpath = os.path.join(shop_dir, f"{shop_id}_page_{i}.json")
               if os.path.exists(fullpath):
                  os.remove(fullpath)
               else:
                  break

         return noMorePages

      return False

   # ------------------------------------------------
   # STORE PROCESSING
   # ------------------------------------------------
   async def process_store(self, url):
      domain = self.get_domain_from_url(url)
      shop_id = self.get_shop_id(url)

      logger.info(f"📍 Processing: {shop_id}")
      shop_dir = self.get_save_directory(shop_id)
      
      # Check how many pages already saved
      last_saved_page = self.get_last_saved_page(shop_dir)

      if self.is_last_page(shop_dir, shop_id, last_saved_page):
         logger.info(f"All Page Saved....{shop_id}")
         return

      last_saved_page = self.get_last_saved_page(shop_dir)
      start_page = last_saved_page + 1


      try:
         # Create driver if needed or closed
         if not self.driver:
            logger.info("Creating new driver...")
            self.driver = self.create_driver()

         # Check if cookies exist and load them FIRST
         saved_cookies = self.load_cookies(domain)

         if saved_cookies and domain not in self.cookies_loaded_domains:
            logger.info(f"✅ Using saved cookies for {domain} - reducing blocking risk")
            self.apply_cookies_to_driver(saved_cookies, domain)
            self.cookies_loaded_domains.add(domain)
         elif not saved_cookies:
            logger.info(f"❌ No saved cookies for {domain} - will save after successful load")

         # Add product page parameters to URL if not already present
         navigation_url = url
         if "pageTypeId=2" not in navigation_url:
            separator = "&" if "?" in navigation_url else "?"
            if start_page > 1:
               navigation_url = f"{url}{separator}from=wangpu&langFlag=en&page={start_page}&pageTypeId=2&q=All-Products&sort=pricedesc".replace('/shop/','/')
            else:
               navigation_url = f"{url}{separator}from=wangpu&langFlag=en&pageTypeId=2&q=All-Products&sort=pricedesc".replace('/shop/','/')

         # Navigate to URL
         logger.info(f"⏳ Navigating to {navigation_url}")
         self.driver.get(navigation_url)
         time.sleep(5)

         # Check for CAPTCHA
         if self.captcha_present():
            logger.warning(f"🚨 CAPTCHA detected for {domain}")

            if domain not in self.captcha_solved_once_per_domain:
               self.handle_manual_captcha(domain)
               # Save cookies after solving CAPTCHA
               self.save_cookies(domain)
            else:
               logger.warning("CAPTCHA appeared again, but already solved once. Trying to continue...")
               # Don't save again, cookies were already saved after first solve
         else:
            # Only save cookies if NOT already loaded (first time)
            if domain not in self.cookies_loaded_domains:
               logger.info(f"💾 Saving new cookies for {domain} (first successful load)")
               self.save_cookies(domain)
               self.cookies_loaded_domains.add(domain)
            else:
               logger.info(f"✅ Reusing cookies for {domain} - no save needed")

         # Scroll and capture AJAX data starting from last saved page
         logger.info(f"📜 Scrolling and capturing AJAX requests (starting page {start_page})...")
         pages_data = self.scroll_and_capture(start_page=start_page, max_pages=102)

         # Save each page separately
         pages_saved = 0
         for page_name, ajax_data in pages_data.items():
            page_file = os.path.join(shop_dir, f"{shop_id}_{page_name}.json")
            with open(page_file, "w", encoding="utf-8") as f:
               json.dump(ajax_data, f, indent=2)
            pages_saved += 1
            logger.info(f"💾 Saved {page_name} - {len(ajax_data)} requests")

         # Count total pages now
         total_pages = self.get_last_saved_page(shop_dir)
         if pages_saved > 0:
            logger.info(f"✅ Completed {shop_id} - Total {total_pages} pages saved")
         else:
            logger.warning(f"⚠️  No new pages captured for {shop_id}")

      except Exception as e:
         logger.error(f"❌ Error processing {shop_id}: {e}", exc_info=True)
         # send_telegram(f"❌ Error: {shop_id}\n{str(e)}")

         # Close driver on error
         self.close_driver()

   # ------------------------------------------------
   # RUN
   # ------------------------------------------------
   async def run(self):
      logger.info(f"🚀 Starting scraping for {len(self.urls)} shops")

      try:
         for url in self.urls:
            await self.process_store(url)
            time.sleep(0)

         logger.info("✅ All shops processed")
      finally:
         self.close_driver()


def run_scraper_thread(urls_batch):
    """Run scraper for a batch of URLs in a separate thread"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        saver = LazadaNetworkSaver(
            urls=urls_batch,
            base_path=BASE_SAVE_PATH,
            chrome_path=CHROMEDRIVER_PATH
        )
        loop.run_until_complete(saver.run())
    finally:
        loop.close()


# ==================================================
# ENTRY
# ==================================================
async def main():
    """Main function - distributes shops across 3 threads"""
    logger.info(f"🚀 Starting scraping with 3 threads for {len(SHOP_URLS)} shops")

    # Split URLs into 3 batches for 3 threads
    num_threads = 2
    batch_size = (len(SHOP_URLS) + num_threads - 2) // num_threads

    batches = []
    for i in range(num_threads):
        start_idx = i * batch_size
        end_idx = start_idx + batch_size
        batch = SHOP_URLS[start_idx:end_idx]
        if batch:
            batches.append(batch)
            logger.info(f"📌 Thread {i + 1}: {len(batch)} shops (indices {start_idx}-{end_idx - 1})")

    # Use ThreadPoolExecutor to run 3 threads
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(run_scraper_thread, batch) for batch in batches]

        for i, future in enumerate(futures, 1):
            try:
                future.result()
                logger.info(f"✅ Thread {i} completed successfully")
            except Exception as e:
                logger.error(f"❌ Thread {i} failed with error: {e}")

    logger.info("✅ All threads completed - Scraping finished!")


if __name__ == "__main__":
   asyncio.run(main())