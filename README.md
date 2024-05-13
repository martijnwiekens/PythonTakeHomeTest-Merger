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

* `poetry run -m src <beforefilepath> <afterfilepath> <targetfilepath>`

This application doesn't need any external dependencies. This means the project can also be run without poetry.
* `python -m src <beforefilepath> <afterfilepath> <targetfilepath>`

For example:
* `python -m src examples/9d4e45c5/before/kernel-4.18.0-477.27.1.el8_856gbnlwn examples/9d4e45c5/after/kernel-4.18.0-513.5.1.el8_92fqrcwu_ examples/9d4e45c5/target/l2cap_core.cf7zq5cwb`
