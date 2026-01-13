@echo off

echo Running estore_cate...
scrapy crawl estore_cate -a retailer=caring-my -a region=my -a Type=eshop -a RetailerCode=caring_my
scrapy crawl estore_cate -a retailer=caring-my -a region=my -a Type=eshop -a RetailerCode=caring_my

echo Finished category. Running estore_pdp...
scrapy crawl estore_pdp -a retailer=caring-my -a region=my -a Type=eshop -a RetailerCode=caring_my
scrapy crawl estore_pdp -a retailer=caring-my -a region=my -a Type=eshop -a RetailerCode=caring_my

