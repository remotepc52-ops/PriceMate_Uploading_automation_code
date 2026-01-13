@echo off

echo Running petexp_cate...
scrapy crawl petexp_cate -a retailer=petexpress-ph -a region=ph -a Type=eshop -a RetailerCode=petexpress_ph

echo Finished category. Running petexp_pl...
scrapy crawl petexp_pl -a retailer=petexpress-ph -a region=ph -a Type=eshop -a RetailerCode=petexpress_ph

echo Finished pl. Running petexp_pdp...
scrapy crawl petexp_pdp -a retailer=petexpress-ph -a region=ph -a Type=eshop -a RetailerCode=petexpress_ph


