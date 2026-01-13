@echo off

echo Running myDin_category...
scrapy crawl mydin_cat -a retailer=mydin-my -a region=my -a Type=eshop -a RetailerCode=mydin_my

echo Finished category. Running myDin_pl...
scrapy crawl mydin_pdp -a retailer=mydin-my -a region=my -a Type=eshop -a RetailerCode=mydin_my

