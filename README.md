## Project Overview & Research Motivation
 - Project focuses on creating a synthetic EEG signal (15 Hz + 7 Hz) and running it through a standard and truncated QFT of 3 circuit depths (3, 5, 7-Qubits). 
 - The motivation behind this project is to find out if quantum systems can be used to eventually run longer EEG signal windows while still maintaining frequency depiction accuracy. Running the combined signal through a truncated QFT will allow for the reduction of quantum resources. 

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


## Limitations, Improvements, & Experimental Integration
1. Create longer EEG signals to see how trunctions effects accuracy and signal processing (add more Qubits)
2. Add synthetic noise to create a more realistic/controlled signal.
  - Refine code to see if QFT can distingush between simulated hardware noise and the signals present
3. Run code in other quantum software applications such as Quantinnum, IonQ, qBraid, and Inquanto.
  - Run in additional software to see how they will affect the data either positivly/negativley