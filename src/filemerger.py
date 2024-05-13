import copy
import logging

from src.types import IChangeItem


class FileMerger:
    """Class to merge two files"""

    @classmethod
    def applyChangeset(
        cls,
        targetFilePath: str,
        changeSetBetweenBeforeAndAfter: list[IChangeItem],
        changeSetBetweenBeforeAndTarget: list[IChangeItem],
        logger: logging.Logger,
    ) -> list[str]:
        # Log the action
        logger.info("* Applying changes to file %s" % targetFilePath)

        # Open the target file and read the contents into a list
        with open(targetFilePath, "r", encoding="utf-8") as file:
            fileContents = file.readlines()

        # Find which lines have been changed in the target file
        changedLines = cls._getChangedLineNumbersByChangeset(
            changeSetBetweenBeforeAndTarget, logger
        )

        # Prepare the variables for the merge
        totalHunks = len(changeSetBetweenBeforeAndAfter)
        appliedHunks = 0
        skippedHunks = 0
        skippedHunkFileOffset = 0
        resultFileLineOffset = 0

        # Walk through the changelist
        for index, changeItem in enumerate(changeSetBetweenBeforeAndAfter):
            # Find the current line number
            currentLineNumber = changeItem["afterHunkStartLine"] - 1

            # Check if the current line number is in the changed lines
            possibleMergeConflictOnLine = 0
            for lineIndex in range(len(changeItem["hunk"])):
                # Calculate the line number to check if this line was changed in the
                # target file.We need to calculate the number based off the changes
                # between before and target, to figure out what the line number should
                # be.
                checkLineNumber = (
                    changeItem["beforeHunkStartLine"]
                    + cls._getLineOffset(
                        changeItem["beforeHunkStartLine"],
                        changeSetBetweenBeforeAndTarget,
                        logger,
                    )
                    + lineIndex
                )

                # Check if the line number is in the changed lines
                if checkLineNumber in changedLines:
                    # This line was changed in the target file, so we can skip this hunk
                    possibleMergeConflictOnLine = checkLineNumber
                    break

            # Check if we found any lines that were changed in the target file
            if possibleMergeConflictOnLine > 0:
                # Log the warning
                logger.warn("  * DANGER at line %i" % currentLineNumber)
                logger.warn(
                    "  * Skipping hunk #%i at line: %i" % (index, currentLineNumber)
                )

                # Skip the hunk, but remember how much it changed the file
                skippedHunks += 1
                skippedHunkFileOffset += (
                    changeItem["addedLines"] - changeItem["removedLines"]
                )
                continue

            # Log the action
            logger.info("  * Apply hunk #%i at line: %i" % (index, currentLineNumber))
            appliedHunks += 1

            # Calculate the line offset for this hunk
            fileLineOffset = cls._getLineOffset(
                changeItem["beforeHunkStartLine"],
                changeSetBetweenBeforeAndTarget,
                logger,
            )

            # Calculate the line number we need to change in the target file
            # We need to calculate the line number based off the changes
            # between before and target, to figure out what the line number
            # should be. We also need to take into account the skipped hunks.
            changeLineNumber = copy.deepcopy(currentLineNumber)
            if fileLineOffset != 0:
                changeLineNumber += fileLineOffset
            if skippedHunkFileOffset != 0:
                changeLineNumber -= skippedHunkFileOffset

            # Walk through the hunk
            for line in changeItem["hunk"]:
                # Check if we need to add extra lines
                while len(fileContents) < changeLineNumber + 1:
                    fileContents.append("")

                # Check if we should remove the lines
                if line.startswith("-"):
                    # Remove the line
                    fileContents.pop(changeLineNumber)

                    # Remember what we did to the file
                    # This action doesnt change the current line number
                    resultFileLineOffset -= 1

                # Check if we should add the lines
                elif line.startswith("+"):
                    # Add the line
                    fileContents.insert(changeLineNumber, line[1:])

                    # Remember what we did to the file
                    # This action doesnt change the current line number
                    resultFileLineOffset += 1
                    changeLineNumber += 1
                else:
                    # Line stays the same, go to next line
                    changeLineNumber += 1

        # Log the changes
        logger.info(" * Applied hunks: %i" % appliedHunks)
        logger.info(" * Skipped hunks: %i" % skippedHunks)
        logger.info(" * Total hunks: %i" % totalHunks)

        # Return the changes
        return fileContents

    @classmethod
    def _getChangedLineNumbersByChangeset(
        cls, changeList: list[IChangeItem], logger: logging.Logger
    ) -> list[int]:
        """Figure out what lines have been changed by a changeset"""
        # Make a list of all the lines that got changed
        changedLineNumbers = []

        # Check all the items
        for changeItem in changeList:
            # Find the line number in the change item
            currentLineNumber = copy.deepcopy(changeItem["beforeHunkStartLine"])

            # Check each line
            for hunk in changeItem["hunk"]:
                # Check if the line is a removed line
                if hunk.startswith("-"):
                    # Check if we found the line number
                    if currentLineNumber not in changedLineNumbers:
                        changedLineNumbers.append(currentLineNumber)

                # Check if the line is an added line
                elif hunk.startswith("+"):
                    # Check if we found the line number
                    if currentLineNumber not in changedLineNumbers:
                        changedLineNumbers.append(currentLineNumber)

                    # Check the next line
                    currentLineNumber += 1

        # Return the list of changed line numbers
        logger.debug("    * Found the following changed lines: %s" % changedLineNumbers)
        return changedLineNumbers

    @classmethod
    def _getLineOffset(
        cls, lineNumber: int, changeList: list[IChangeItem], logger: logging.Logger
    ) -> int:
        """Figure out how much the before file and target file are offset from
        each other
        """
        # Remember the offset
        offset = 0

        # Check each change item
        for changeItem in changeList:
            # Find the line number in the change item
            currentLineNumber = changeItem["beforeHunkStartLine"]

            # Check if the line numbers is too high
            if currentLineNumber > lineNumber:
                # We found the offset
                logger.debug("    * Found line offset: %i" % offset)
                return offset

            # Calculate the offset between the lines
            offset = (
                changeItem["afterHunkStartLine"] - changeItem["beforeHunkStartLine"]
            )
            offset += changeItem["addedLines"] - changeItem["removedLines"]

        # Return the offset
        logger.debug("    * Found line offset: %i" % offset)
        return offset
