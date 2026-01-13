@echo off

echo Running south_cate...
scrapy crawl south_cate -a retailer=southstardrug-ph -a region=ph -a Type=eshop -a RetailerCode=southstardrug_ph

echo Finished category. Running south_pl...
scrapy crawl south_pl -a retailer=southstardrug-ph -a region=ph -a Type=eshop -a RetailerCode=southstardrug_ph

echo Finished pl. Running south_pdp...
scrapy crawl south_pdp -a retailer=southstardrug-ph -a region=ph -a Type=eshop -a RetailerCode=southstardrug_ph


