@echo off

echo Running tiptop_cate...
scrapy crawl tiptop_cate -a retailer=tiptop-id -a region=id -a Type=eshop -a RetailerCode=tiptop_id

echo Finished category. Running tiptop_pl...
scrapy crawl tiptop_pl -a retailer=tiptop-id -a region=id -a Type=eshop -a RetailerCode=tiptop_id

scrapy crawl tiptop_pl -a retailer=tiptop-id -a region=id -a Type=eshop -a RetailerCode=tiptop_id

echo Finished pl. Running tiptop_pdp...
scrapy crawl tiptop_pdp -a retailer=tiptop-id -a region=id -a Type=eshop -a RetailerCode=tiptop_id

scrapy crawl tiptop_pdp -a retailer=tiptop-id -a region=id -a Type=eshop -a RetailerCode=tiptop_id


