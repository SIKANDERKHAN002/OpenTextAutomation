@echo off
:: ====================================================
:: [Constants / Paths]
:: ====================================================
set ALLURE_RESULTS=reports\allure-results
set ALLURE_HTML=reports\allure-html
set PYTEST_HTML=reports\report.html
:: ====================================================
:: Step 1: Create virtual environment
:: ====================================================
echo Creating Virtual Environment...
python -m venv venv
:: ====================================================
:: Step 2: Activate the virtual environment
:: ====================================================
echo Activating Virtual Environment...
call venv\Scripts\activate.bat
:: ====================================================
:: Step 3: Restart Docker containers (Selenium Grid, etc.)
:: ====================================================
echo Restarting Docker containers...
docker-compose down
docker-compose up -d
:: ====================================================
:: Step 4: Install required Python packages
:: ====================================================
echo Installing/updating required packages...
pip install -r requirements.txt
:: ====================================================
:: Step 5: Clean up previous test reports (Allure + HTML)
:: ====================================================
echo Cleaning previous test reports...
rmdir /s /q %ALLURE_RESULTS%
rmdir /s /q %ALLURE_HTML%
del %PYTEST_HTML%
:: ====================================================
:: Step 6: Run Pytest tests with marker, reruns, parallel, HTML + Allure reporting
:: ====================================================
echo Running tests...
pytest -s -v ^
--reruns=2 --reruns-delay=2 ^
--alluredir=%ALLURE_RESULTS% ^
--html=%PYTEST_HTML% --self-contained-html ^
testCases/test_006_ForgettenPassword.py
:: ====================================================
:: Step 7: Shut down Docker containers
:: ====================================================
echo Shutting down Docker containers...
docker-compose down
:: ====================================================
:: Step 8: Generate and open Allure report
:: ====================================================
echo Generating and opening Allure report...
allure generate %ALLURE_RESULTS% -o %ALLURE_HTML% --clean && allure open %ALLURE_HTML%
