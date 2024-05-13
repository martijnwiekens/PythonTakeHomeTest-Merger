# Python - Test Task
Programming Test Task for the Python Language. A program to merge files.

## Setup application
Dependencies for this project are managed with Poetry.

1. `poetry install`

### Run application

To run the application you need 3 input variables.
- Before file: The file you want to use as the before.
- After file: The file you want to compare the before file to.
- Apply file: The file you want to apply the changes to. This is optional.

1. `poetry run -m src <beforefilepath> <afterfilepath> <targetfilepath>`
