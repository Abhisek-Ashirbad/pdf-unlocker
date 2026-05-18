# pdf-unlocker
A simple script to remove password from your PDF permanently (provided you've the original password). 

[![codecov](https://codecov.io/github/Abhisek-Ashirbad/pdf-unlocker/graph/badge.svg?token=75IBCT3JAJ)](https://codecov.io/github/Abhisek-Ashirbad/pdf-unlocker)

## Contents

- [Installation](#installation)
  - [From PyPi](#from-pypi)
  - [From CLI](#from-cli)
- [Running the application](#running-the-application)
  - [CLI version](#cli-version)
  - [GUI version](#gui-version)
- [Tests](#tests)
- [Releases](#releases)
- [Builds](#builds)

## Installation

### From PyPi

`pip install pdf-unlocker` 

### From CLI
Create a virtual environment (venv)

`py -m venv venv`

`pip install -r requirements.txt`

## Running the application

### CLI version
Abridged command

`unlock -i="INPUT_PATH" -o="OUTPUT_PATH" -p="PASSWORD"`  

Extended command

`unlock --input_path="INPUT_PATH" --output_path="OUTPUT_PATH" --password="PASSWORD"`

### GUI version
`unlock`

## Tests
To run all the UTs and generate coverage

`pytest --cov=pdf_unlocker --cov-report=html`

## Releases
* 0.0.1 - Initial config and setup
* 0.0.2 - Added custom flags and added modularity to the CLI
* 0.0.3 - Added UI to the app and also UTs (coverage 100%)
* 1.0.0 - Application v1 is finally released with all the specs

## Documentation
Install the documentation dependencies and build the HTML docs from the project root:

`py -m pip install -r requirements.txt`

`py -m sphinx -b html docs docs/_build/html`

Open the generated documentation in your browser from `docs/_build/html/index.html`.

## Builds
### Windows
For creating .exe, execute the below command in the terminal/CMD from the project root.

`pyinstaller --noconfirm --onedir --windowed --name "PDF-Unlocker" --icon="src/pdf_unlocker/assets/unlock_icon_256.ico" --add-data "src/pdf_unlocker;pdf_unlocker" src/pdf_unlocker/app.py`