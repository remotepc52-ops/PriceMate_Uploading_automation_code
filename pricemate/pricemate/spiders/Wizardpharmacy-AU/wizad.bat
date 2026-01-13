@echo off

echo Running wizard_category...
scrapy crawl wiz_cate -a retailer=wizardpharmacy-au -a region=au -a Type=eshop -a RetailerCode=wizardpharmacy_au

echo Finished category. Running wizard_pl...
scrapy crawl wiz_pl -a retailer=wizardpharmacy-au -a region=au -a Type=eshop -a RetailerCode=wizardpharmacy_au

echo Finished pl. Running wizard_pdp...
scrapy crawl wizard_pdp -a retailer=wizardpharmacy-au -a region=au -a Type=eshop -a RetailerCode=wizardpharmacy_au

scrapy crawl wizard_pdp -a retailer=wizardpharmacy-au -a region=au -a Type=eshop -a RetailerCode=wizardpharmacy_au

scrapy crawl wizard_pdp -a retailer=wizardpharmacy-au -a region=au -a Type=eshop -a RetailerCode=wizardpharmacy_au
