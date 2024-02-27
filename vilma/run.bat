@echo off

rem Change directory to the git repository
cd /d C:\Users\R53\vilma-santos-project

rem Pull the latest changes from the remote repository
git pull

rem Install requirements from requirements.txt
C:\Users\R53\vilma-santos-project\vilmavenv\Scripts\python.exe -m pip install -r requirements.txt

rem Change directory to the Django project
cd /d C:\Users\R53\vilma-santos-project\vilma

rem Apply database migrations
C:\Users\R53\vilma-santos-project\vilmavenv\Scripts\python.exe manage.py migrate

rem Run the Django development server
C:\Users\R53\vilma-santos-project\vilmavenv\Scripts\python.exe manage.py runserver
