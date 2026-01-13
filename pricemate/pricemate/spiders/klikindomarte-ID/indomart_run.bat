@echo off

echo Running klikindo_cate...
scrapy crawl klikindo_cate -a retailer=klikindomaret-id -a region=id -a Type=eshop -a RetailerCode=klikindomaret_id

echo Finished category. Running klikindo_pl...
crapy crawl klikindo_pl -a retailer=klikindomaret-id -a region=id -a Type=eshop -a RetailerCode=klikindomaret_id

crapy crawl klikindo_pl -a retailer=klikindomaret-id -a region=id -a Type=eshop -a RetailerCode=klikindomaret_id

echo Finished pl. Running klikindo_pdp...
scrapy crawl klikindo_pdp -a retailer=klikindomaret-id -a region=id -a Type=eshop -a RetailerCode=klikindomaret_id

scrapy crawl klikindo_pdp -a retailer=klikindomaret-id -a region=id -a Type=eshop -a RetailerCode=klikindomaret_id

scrapy crawl klikindo_pdp -a retailer=klikindomaret-id -a region=id -a Type=eshop -a RetailerCode=klikindomaret_id


