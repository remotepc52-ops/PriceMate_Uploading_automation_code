@echo off

echo Running national_cate...
scrapy crawl national_cate -a retailer=nationalpharmacies-au -a region=au -a Type=eshop -a RetailerCode=nationalpharmacies_au
scrapy crawl national_cate -a retailer=nationalpharmacies-au -a region=au -a Type=eshop -a RetailerCode=nationalpharmacies_au

echo Finished category. Running national_pdp...
scrapy crawl national_pdp -a retailer=nationalpharmacies-au -a region=au -a Type=eshop -a RetailerCode=nationalpharmacies_au

scrapy crawl national_pdp -a retailer=nationalpharmacies-au -a region=au -a Type=eshop -a RetailerCode=nationalpharmacies_au

scrapy crawl national_pdp -a retailer=nationalpharmacies-au -a region=au -a Type=eshop -a RetailerCode=nationalpharmacies_au




