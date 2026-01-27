@echo off
cd /d C:\MyLoan

call venv\Scripts\activate

git pull

pip install -r requirements.txt
flask db upgrade
nssm restart MyLoanFlask