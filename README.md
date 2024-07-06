# Data-Driven Software Security Assessment

This project provides a software security assessment tool using a data-driven approach.

## Development

### Tools

- Code editor: [VSCode](https://code.visualstudio.com/)
- Python: [3.12](https://www.python.org/downloads/)
- GUI design: [Qt Designer](https://build-system.fman.io/qt-designer-download)

### Getting Started

1. Clone the repository

2. Create and activate a virtual environemnt

   1. `python -m venv venv`
   2. * `source venv/bin/activate` (Unix)
      * `venv\Scripts\activate` (Windows, Command prompt)
      * `venv\Scripts\Activate.ps1` (Windows, PowerShell)
   3. `pip install --upgrade pip`
   4. `pip install -r requirements.txt -r requirements-dev.txt` OR `pip install -e ".[dev]"` (to install from `setup.py`)

3. To use the GUI, run the following from the project's root directory:

   ```bash
   python ./ddssa/frontend/ui.py
   ```

4. To use the CLI, run the following command from the project's root directory:
   ```bash
   python ./ddssa/frontend/ddssa.py
   ```
   In order to see the list of commands that are accepted the following command can be used: 
   ```bash
   python ./ddssa/frontend/ddssa.py --help
   ```
5. To make changes to the user interface, open the [main.ui](./ddssa/frontend/main.ui) in Qt Designer. To synchronize changes to the Python GUI file run `pyuic5 -o ./ddssa/frontend/main.py ./ddssa/frontend/main.ui`.

5. To run tests: `pytest`

6. To make changes to the code, open the project's root directory in VSCode.

### Additional Tools

- [diagrams.net](https://app.diagrams.net/) for diagrams
- Contributions are made through GitHub, on this repository
- GitHub issues are used for task and ticket tracking

## The Team

- [Samuel Gamelin](https://github.com/samuel-gamelin)
- [Mohamed Radwan](https://github.com/mo-5)
- [Khalil Aalab](https://github.com/KhalilAalab)
- [John Breton](https://github.com/john-breton)

## Known issues

Currently, there are no known issues.

> If you notice a bug, please add it to Issues tab. Make sure you include how to recreate the bug!
