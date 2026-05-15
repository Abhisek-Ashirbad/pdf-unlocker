# pdf-unlocker
A simple script to remove password from your PDF (provided you've the original password). 



## Tests
To run all the UTs and generate coverage
`pytest --cov=pdf_unlocker --cov-report=html`

## Releases
* 0.0.1 - Initial config and setup
* 0.0.2 - Added custom flags and added modularity to the CLI
* 0.0.3 - Added UI to the app and also UTs (coverage 100%)

## Builds
### Windows
For creating .exe, execute the below command in the terminal/CMD from the project root.

`pyinstaller --noconfirm --onedir --windowed --name "PDF-Unlocker" --icon="src/pdf_unlocker/assets/unlock_icon_256.ico" --add-data "src/pdf_unlocker;pdf_unlocker" src/pdf_unlocker/app.py`