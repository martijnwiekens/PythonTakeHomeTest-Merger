import copy
import logging

from src.diffcreator import DiffCreator


def test_generateChangeList() -> None:
    """Test the generateChangeList function"""
    # Get content
    with open("examples/fileExampleA.txt", "r", encoding="utf-8") as file:
        fileAContent = file.readlines()
    with open("examples/fileExampleB.txt", "r", encoding="utf-8") as file:
        fileBContent = file.readlines()

    # Test: Generate change list, with both lists
    # Give a copy of a list, just to make sure we don't change the original list
    changeList = DiffCreator.generateChangeList(
        copy.deepcopy(fileAContent),
        copy.deepcopy(fileBContent),
        logging.getLogger(),
    )
    assert len(changeList) == 1

    # Test: Generate change list, with 1 list
    # Give a copy of a list, just to make sure we don't change the original list
    changeList = DiffCreator.generateChangeList(
        copy.deepcopy(fileAContent),
        [],
        logging.getLogger(),
    )
    assert len(changeList) == 1

    # Test: Generate change list, with 1 list
    # Give a copy of a list, just to make sure we don't change the original list
    changeList = DiffCreator.generateChangeList(
        [],
        copy.deepcopy(fileBContent),
        logging.getLogger(),
    )
    assert len(changeList) == 1

    # Test: Generate change list, with 2 empty lists
    changeList = DiffCreator.generateChangeList(
        [],
        [],
        logging.getLogger(),
    )
    assert len(changeList) == 0


def test_createDiff() -> None:
    """Test the createDiff function"""
    # Get content
    with open("examples/fileExampleA.txt", "r", encoding="utf-8") as file:
        fileAContent = file.readlines()
    with open("examples/fileExampleB.txt", "r", encoding="utf-8") as file:
        fileBContent = file.readlines()

    # Test: Generate change list, with both lists
    # Give a copy of a list, just to make sure we don't change the original list
    diff = DiffCreator._createDiff(
        copy.deepcopy(fileAContent), copy.deepcopy(fileBContent)
    )
    assert len(diff) == 18

    # Test: Generate change list, with 1 list
    # Give a copy of a list, just to make sure we don't change the original list
    diff = DiffCreator._createDiff(copy.deepcopy(fileAContent), [])
    assert len(diff) == 13

    # Test: Generate change list, with 1 list
    # Give a copy of a list, just to make sure we don't change the original list
    diff = DiffCreator._createDiff([], copy.deepcopy(fileBContent))
    assert len(diff) == 13

    # Test: Generate diff, with 2 empty lists
    diff = DiffCreator._createDiff([], [])
    assert len(diff) == 0


def test_parseUnifiedDiff() -> None:
    """Test the parseUnifiedDiff function"""
    # Parse empty unified diff
    changeList = DiffCreator._parseUnifiedDiff([])
    assert len(changeList) == 0

    # Parse empty unified diff
    unifiedDiff1 = DiffCreator._createDiff([], [])
    changeList = DiffCreator._parseUnifiedDiff(unifiedDiff1)
    assert len(changeList) == 0

    # Parse single hunk
    with open("examples/fileExampleA.txt", "r", encoding="utf-8") as file:
        fileAContent = file.readlines()
    with open("examples/fileExampleB.txt", "r", encoding="utf-8") as file:
        fileBContent = file.readlines()
    diff = DiffCreator._createDiff(
        copy.deepcopy(fileAContent), copy.deepcopy(fileBContent)
    )
    changeList = DiffCreator._parseUnifiedDiff(diff)
    assert len(changeList) == 1
    assert changeList[0]["beforeHunkStartLine"] == 1
    assert changeList[0]["afterHunkStartLine"] == 1
    assert changeList[0]["hunkLength"] == 5
    assert changeList[0]["removedLines"] == 5
    assert changeList[0]["addedLines"] == 5
    assert len(changeList[0]["hunk"]) == 15

    # Parse multi hunk
    with open("examples/fileExampleE.txt", "r", encoding="utf-8") as file:
        fileEContent = file.readlines()
    with open("examples/fileExampleF.txt", "r", encoding="utf-8") as file:
        fileFContent = file.readlines()
    diff = DiffCreator._createDiff(
        copy.deepcopy(fileEContent), copy.deepcopy(fileFContent)
    )
    changeList = DiffCreator._parseUnifiedDiff(diff)
    assert len(changeList) == 2
