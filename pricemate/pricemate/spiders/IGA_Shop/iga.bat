@echo off

echo Running iga_cate...
scrapy crawl iga_cate -a retailer=iga-au -a region=au -a Type=eshop -a RetailerCode=iga_au

echo Finished category. Running iga_pdp...
scrapy crawl iga_pdp -a retailer=iga-au -a region=au -a Type=eshop -a RetailerCode=iga_au
