@echo off

echo Running lotte_pl...
scrapy crawl lote_pl -a retailer=lottemartgrosir-id -a region=id -a Type=eshop -a RetailerCode=lottemartgrosir_id

echo Finished category. Running lotte_pl...
scrapy crawl lotte_pdp -a retailer=lottemartgrosir-id -a region=id -a Type=eshop -a RetailerCode=lottemartgrosir_id

