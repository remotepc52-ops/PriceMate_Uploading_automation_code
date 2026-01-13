@echo off
scrapy crawl walter_cate -a retailer=waltermart-ph -a region=ph -a Type=eshop -a RetailerCode=waltermart_ph
scrapy crawl walter_pl -a retailer=waltermart-ph -a region=ph -a Type=eshop -a RetailerCode=waltermart_ph
scrapy crawl walter_pdp -a retailer=waltermart-ph -a region=ph -a Type=eshop -a RetailerCode=waltermart_ph