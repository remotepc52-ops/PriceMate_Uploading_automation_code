@echo off

echo Running yogya_cate...
scrapy crawl yogya_cate -a retailer=yogya-id -a region=id -a Type=eshop -a RetailerCode=yogya_id

echo Finished category. Running yogya_pl...
scrapy crawl yogya_pl -a retailer=yogya-id -a region=id -a Type=eshop -a RetailerCode=yogya_id
scrapy crawl yogya_pl -a retailer=yogya-id -a region=id -a Type=eshop -a RetailerCode=yogya_id

echo Finished pl. Running yogya_pdp...
scrapy crawl yogya_pdp -a retailer=yogya-id -a region=id -a Type=eshop -a RetailerCode=yogya_id
scrapy crawl yogya_pdp -a retailer=yogya-id -a region=id -a Type=eshop -a RetailerCode=yogya_id


