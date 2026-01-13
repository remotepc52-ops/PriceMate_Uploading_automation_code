@echo off

scrapy crawl klik_cate -a retailer=k24klik-id -a region=id -a Type=eshop -a RetailerCode=k24klik_id

scrapy crawl klik_pdp -a retailer=k24klik-id -a region=id -a Type=eshop -a RetailerCode=k24klik_id

scrapy crawl klik_pdp -a retailer=k24klik-id -a region=id -a Type=eshop -a RetailerCode=k24klik_id