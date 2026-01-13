@echo off
echo ========================================
echo Starting Lazada Shops Scraper
echo ========================================
echo.

REM Kill only lazada_shop spider processes using PowerShell
echo Checking for existing lazada_shop spider processes...
powershell -Command "Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like '*lazada_shop*' } | ForEach-Object { Stop-Process -Id $_.Id -Force }" 2>NUL
echo Cleanup complete.
timeout /t 2 /nobreak
echo.

REM Wait before starting
echo Waiting 3 seconds before starting...
timeout /t 3 /nobreak
echo.

REM Run Lazada Indonesia (eshop)
echo ========================================
echo [1/7] Starting Lazada Indonesia (eshop)...
echo ========================================
start cmd /k "scrapy crawl lazada_shop -a retailer=lazada_id -a region=id -a Type=eshop -a RetailerCode=lazada_watsons_id"
echo Waiting 10 seconds...
timeout /t 10 /nobreak
echo.

REM Run Lazada Malaysia (marketplace)
echo ========================================
echo [2/7] Starting Lazada Malaysia (marketplace)...
echo ========================================
start cmd /k "scrapy crawl lazada_shop -a retailer=lazada_my -a region=my -a Type=marketplace -a RetailerCode=lazada_petsmore_my"
echo Waiting 10 seconds...
timeout /t 10 /nobreak
echo.

REM Run Lazada Philippines (marketplace)
echo ========================================
echo [3/7] Starting Lazada Philippines (marketplace)...
echo ========================================
start cmd /k "scrapy crawl lazada_shop -a retailer=lazada_ph -a region=ph -a Type=marketplace -a RetailerCode=lazada_ph"
echo Waiting 10 seconds...
timeout /t 10 /nobreak
echo.

REM Run Lazada Indonesia (marketplace)
echo ========================================
echo [4/7] Starting Lazada Indonesia (marketplace)...
echo ========================================
start cmd /k "scrapy crawl lazada_shop -a retailer=lazada_id -a region=id -a Type=marketplace -a RetailerCode=lazada_id"
echo Waiting 10 seconds...
timeout /t 10 /nobreak
echo.

REM Run Lazada Malaysia (marketplace - second instance)
echo ========================================
echo [5/7] Starting Lazada Malaysia (marketplace - MY)...
echo ========================================
start cmd /k "scrapy crawl lazada_shop -a retailer=lazada_my -a region=my -a Type=marketplace -a RetailerCode=lazada_my"
echo Waiting 10 seconds...
timeout /t 10 /nobreak
echo.

REM Run Lazada Philippines (marketplace - Watsons)
echo ========================================
echo [6/7] Starting Lazada Philippines (marketplace - Watsons)...
echo ========================================
start cmd /k "scrapy crawl lazada_shop -a retailer=lazada_ph -a region=ph -a Type=marketplace -a RetailerCode=lazada_watsons_ph"
echo.

REM Run Lazada My (marketplace - Watsons)
echo ========================================
echo [7/7] Starting Lazada Philippines (marketplace - Watsons)...
echo ========================================
start cmd /k "scrapy crawl lazada_shop -a retailer=lazada_my -a region=my -a Type=marketplace -a RetailerCode=lazada_watsons_my"
echo.

echo ========================================
echo All scrapers have been started!
echo ========================================
echo.
pause