@echo off

echo Running snr_cate...
scrapy crawl snr_cate -a retailer=snrshopping-ph -a region=ph -a Type=eshop -a RetailerCode=snrshopping_ph

echo Finished category. Running snr_pl...
scrapy crawl snr_pl -a retailer=snrshopping-ph -a region=ph -a Type=eshop -a RetailerCode=snrshopping_ph

echo Finished pl. Running snr_pdp...
scrapy crawl snr_pdp -a retailer=snrshopping-ph -a region=ph -a Type=eshop -a RetailerCode=snrshopping_ph


