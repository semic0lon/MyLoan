@echo off
cd /d C:\MyLoan

git pull

C:\MyLoan\venv\Scripts\python.exe -m pip install -r requirements.txt

C:\MyLoan\venv\Scripts\python.exe -m flask db upgrade

nssm restart Loan