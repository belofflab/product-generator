# Startup Application (Sadovod-base parser)
## On MacOS
```bash
python3 -m pip install virtualenv 
python3 -m virtualenv venv 
source venv/bin/activate
pip install -r requirements.txt
python3 -m src
```
## On Windows
```bash
pip install virtualenv 
virtualenv venv 
source venv/bin/activate
pip install -r requirements.txt
python -m src
```

# Stack
1. sqlalchemy (Database)
2. pandas (Excel)
3. requests (main lib)
extras: bs4, lxml, openpyxl.

# Soon...
1. Add Aiogram 
2. Add Apscheduler

# Ngrok
```bash
ngrok http --domain=loudly-guided-bear.ngrok-free.app 8000
```