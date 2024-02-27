@echo off

rem Change directory to the virtual environment and activate it
cd /d C:\Users\R53\vilma-santos-project\vilmavenv\Scripts\Activate

rem Change directory to the git repository and pull the latest changes
cd /d C:\Users\R53\vilma-santos-project
git pull

rem Install requirements from requirements.txt
pip install -r requirements.txt

rem Change directory to your Django project working directory
cd /d C:\Users\R53\vilma-santos-project\vilma

rem Run Django migrations
py manage.py migrate

rem Run Django development server
py manage.py runserver