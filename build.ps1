black *.py
pip freeze > requirements.txt
pyinstaller main.py --onefile --noconsole