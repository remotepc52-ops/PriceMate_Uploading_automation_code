@echo off

echo Running fairprice_cate...
scrapy crawl fairprice_cate -a retailer=ntuc-fairprice-sg -a region=sg -a Type=eshop -a RetailerCode=ntuc_fairprice_sg

echo Finished category. Running fairprice_pl...
scrapy crawl fairprice_pl -a retailer=ntuc-fairprice-sg -a region=sg -a Type=eshop -a RetailerCode=ntuc_fairprice_sg

echo Finished pl. Running fairprice_pdp...
scrapy crawl fairprice_pdp -a retailer=ntuc-fairprice-sg -a region=sg -a Type=eshop -a RetailerCode=ntuc_fairprice_sg


