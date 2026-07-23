## Fresh Install Steps
1. Open vsCode and folder locations
2. Open Terminal
3. run "python3 -m venv .venv" in terminal
4. run the below
  - ".venv\Scripts\Activate.ps1" for Windows.
  - "source .venv/bin/activate" for macOS
5. run "pip install -r requirements.txt"
6. run "pip list" - to check that everything was installed correctly
7. run "python3 main.py"


## Useful Commands
deactivate - manually get out of the virtual environment

## How to use GitHub
Adding new files or changes to github
1. git add .
    - if you're working on changes and don't want to save all the files then instead of a period just write the file names you want added.
2. git commit -m "add notes about what you changed here"
3. git status
    - this checks that all the files you want added are "staged". If you see the file in green then you are good.
4. git push