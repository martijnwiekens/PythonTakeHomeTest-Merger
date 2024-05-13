import difflib
import logging

from src.types import IChangeItem


class DiffCreator:
    """Class to create a diff between two files"""

    @classmethod
    def generateChangeList(
        cls, file1Content: list[str], file2Content: list[str], logger: logging.Logger
    ) -> list[IChangeItem]:
        """Create a changelist based on a diff between two files"""
        # Log the action
        logger.info("* Creating a diff between the two files")

        # Create a unified diff between the two files
        unifiedDiff = cls._createDiff(file1Content, file2Content)

        # Parse the unified diff
        changeList = cls._parseUnifiedDiff(unifiedDiff)

        # Log how many changes were found
        logger.info("* Found %i changes" % len(changeList))

        # Return the changelist
        return changeList

    @classmethod
    def _createDiff(cls, file1Content: list[str], file2Content: list[str]) -> list[str]:
        """Create a diff between two files"""
        return list(difflib.unified_diff(file1Content, file2Content))

    @classmethod
    def _parseUnifiedDiff(cls, diff: list[str]) -> list[IChangeItem]:
        # Create a list to store the changes
        changeList: list[IChangeItem] = []

        # Remember for each hunk, the start and end lines
        beforeHunkStartLine = 0
        afterHunkStartLine = 0
        hunk: list[str] = []
        removedLines = 0
        addedLines = 0
        hunkLength = 0

        # Loop through each line in the diff
        for line in diff:
            # Check if the line is unnessary
            if line.startswith("---") or line.startswith("+++"):
                continue

            # Check if the line is a hunk
            if line.startswith("@@"):
                # Check if we started a new hunk
                if len(hunk) > 0:
                    # Add the hunk to the change list
                    changeList.append(
                        {
                            "beforeHunkStartLine": beforeHunkStartLine,
                            "afterHunkStartLine": afterHunkStartLine,
                            "hunkLength": hunkLength,
                            "removedLines": removedLines,
                            "addedLines": addedLines,
                            "hunk": hunk,
                        }
                    )

                    # Reset the hunk
                    hunk = []
                    removedLines = 0
                    addedLines = 0
                    hunkLength = 0

                # Split the line into parts
                parts = line.split()

                # Get the start and end lines of the hunk
                beforeHunkStartLine = int(parts[1][1:].split(",")[0])
                afterHunkStartLine = int(parts[2][1:].split(",")[0])

            else:
                # Check if the line is a removed line
                if line.startswith("-"):
                    # Add to the removed lines
                    removedLines += 1
                    hunkLength -= 1

                # Check if the line is an added line
                elif line.startswith("+"):
                    # Add to the added lines
                    addedLines += 1
                    hunkLength += 1

                else:
                    # Add to the hunk length
                    hunkLength += 1

                # Add to the hunk
                hunk.append(line)

        # Final check if we have a hunk left
        if len(hunk) > 0:
            # Save the last hunk to the change list
            changeList.append(
                {
                    "beforeHunkStartLine": beforeHunkStartLine,
                    "afterHunkStartLine": afterHunkStartLine,
                    "hunkLength": hunkLength,
                    "removedLines": removedLines,
                    "addedLines": addedLines,
                    "hunk": hunk,
                }
            )

        # Return the change list
        return changeList
