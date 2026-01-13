@echo off
cd /d "%~dp0"

echo Running blibli_farmers.py...
scrapy crawl blibli_farmers -a retailer=farmersmarket_id -a region=id -a Type=marketplace -a RetailerCode=farmersmarket_id
pause