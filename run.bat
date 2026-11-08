@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Setting up database...
echo Please make sure MySQL is running and update the database configuration in app.py
echo.

echo Starting the application...
python app.py

pause



