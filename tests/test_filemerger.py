import copy
import logging
import shutil

from src.filemerger import FileMerger
from src.diffcreator import DiffCreator


def test_applyChangeset() -> None:
    """Test applyChangeset"""
    # Create temp file
    shutil.copy("examples/fileExampleA.txt", "examples/temp.txt")

    # Test how many lines will be changed
    result = FileMerger.applyChangeset("examples/temp.txt", [], [], logging.getLogger())
    assert len(result) == 10

    # Check if the file has the same content
    with open(
        "examples/9d4e45c5/target/l2cap_core.cf7zq5cwb", "r", encoding="utf-8"
    ) as file:
        assert len(file.readlines()) == 8581

    # Create a changelist for testing
    with open(
        "examples/9d4e45c5/before/kernel-4.18.0-477.27.1.el8_856gbnlwn",
        "r",
        encoding="utf-8",
    ) as file:
        fileBeforeContent = file.readlines()
    with open(
        "examples/9d4e45c5/after/kernel-4.18.0-513.5.1.el8_92fqrcwu_",
        "r",
        encoding="utf-8",
    ) as file:
        fileAfterContent = file.readlines()
    diffBefore = DiffCreator.generateChangeList(
        fileBeforeContent, fileAfterContent, logging.getLogger()
    )

    # Apply changeset to file, (this does not change the file)
    result = FileMerger.applyChangeset(
        "examples/9d4e45c5/target/l2cap_core.cf7zq5cwb",
        diffBefore,
        [],
        logging.getLogger(),
    )
    assert len(result) == 8605

    # Check if the file has the same content
    with open(
        "examples/9d4e45c5/target/l2cap_core.cf7zq5cwb", "r", encoding="utf-8"
    ) as file:
        assert len(file.readlines()) == 8581


def test_getChangedLineNumbersByChangeset() -> None:
    """Test getChangedLineNumbersByChangeset"""
    # Create a change list
    with open("examples/fileExampleA.txt", "r", encoding="utf-8") as file:
        fileAContent = file.readlines()
    with open("examples/fileExampleB.txt", "r", encoding="utf-8") as file:
        fileBContent = file.readlines()
    changeList = DiffCreator.generateChangeList(
        copy.deepcopy(fileAContent),
        copy.deepcopy(fileBContent),
        logging.getLogger(),
    )

    # Test: Get empty list of line numbers
    changedLines = FileMerger._getChangedLineNumbersByChangeset([], logging.getLogger())
    assert len(changedLines) == 0

    # Test: Get changed line numbers
    changedLines = FileMerger._getChangedLineNumbersByChangeset(
        changeList, logging.getLogger()
    )
    assert len(changedLines) == 5
    assert 1 in changedLines
    assert 2 in changedLines
    assert 3 in changedLines
    assert 4 in changedLines
    assert 5 in changedLines


def test_getLineOffset() -> None:
    """Test get line offset"""
    # Test empty line offset
    assert FileMerger._getLineOffset(1, [], logging.getLogger()) == 0

    # Test line offset
    with open(
        "examples/9d4e45c5/before/kernel-4.18.0-477.27.1.el8_856gbnlwn",
        "r",
        encoding="utf-8",
    ) as file:
        fileBeforeContent = file.readlines()
    with open(
        "examples/9d4e45c5/after/kernel-4.18.0-513.5.1.el8_92fqrcwu_",
        "r",
        encoding="utf-8",
    ) as file:
        fileAfterContent = file.readlines()
    diff = DiffCreator.generateChangeList(
        fileBeforeContent, fileAfterContent, logging.getLogger()
    )
    assert FileMerger._getLineOffset(10, diff, logging.getLogger()) == 0
    assert FileMerger._getLineOffset(1294, diff, logging.getLogger()) == 23
    assert FileMerger._getLineOffset(2300, diff, logging.getLogger()) == 25
