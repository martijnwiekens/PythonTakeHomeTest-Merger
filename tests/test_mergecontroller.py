import shutil

import pytest

from src.mergecontroller import MergeController


def test_MergeController_CliInputs() -> None:
    # Check if we can find the CLI inputs
    with pytest.raises(ValueError):
        MergeController()


def test_MergeController_FileNotExists() -> None:
    # Test: BeforeFile not found
    with pytest.raises(FileNotFoundError, match="Before file abc.txt does not exist"):
        MergeController(
            "abc.txt", "examples/fileExampleB.txt", "examples/fileExampleC.txt"
        )

    # Test: AfterFile not found
    with pytest.raises(FileNotFoundError, match="After file abc.txt does not exist"):
        MergeController(
            "examples/fileExampleA.txt", "abc.txt", "examples/fileExampleC.txt"
        )

    # Test: TargetFile not found
    with pytest.raises(FileNotFoundError, match="Target file abc.txt does not exist"):
        MergeController(
            "examples/fileExampleA.txt", "examples/fileExampleB.txt", "abc.txt"
        )

    # Test: All files found
    MergeController(
        "examples/fileExampleA.txt",
        "examples/fileExampleB.txt",
        "examples/fileExampleC.txt",
    )


def test_MergeController_Execute() -> None:
    # Copy fileExampleA.txt to temp.txt
    shutil.copy("examples/fileExampleA.txt", "examples/temp.txt")

    # Check if file was changed
    with open("examples/temp.txt", "r", encoding="utf-8") as file:
        assert file.readlines()[0].startswith("Lorem")

    # Execute the merge controller, this is with demo files
    m = MergeController(
        "examples/fileExampleA.txt",
        "examples/fileExampleB.txt",
        "examples/temp.txt",
    )
    m.execute()

    # Check if file was changed
    with open("examples/temp.txt", "r", encoding="utf-8") as file:
        assert file.readlines()[0].startswith("Sed")
