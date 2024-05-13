import logging
import os
import sys
from typing import Optional

from src.diffcreator import DiffCreator
from src.filemerger import FileMerger


class MergeController:
    """Class to control merging of two files"""

    def __init__(
        self,
        beforeFilePath: Optional[str] = None,
        afterFilePath: Optional[str] = None,
        targetFilePath: Optional[str] = None,
    ) -> None:
        """Initialize the merge controller

        Params:
            Can be given to the constructor or will be taken from the sys args
        """
        # Check if we found everything we need
        if beforeFilePath is None or afterFilePath is None or targetFilePath is None:
            # Check the arguments
            if len(sys.argv) < 4:
                raise ValueError("Not enough arguments")

            # Save the file paths
            beforeFilePath = sys.argv[1]
            afterFilePath = sys.argv[2]
            targetFilePath = sys.argv[3]

        # Check if the file paths are valid
        if os.path.exists(beforeFilePath) is False:
            raise FileNotFoundError(f"Before file {beforeFilePath} does not exist")
        if os.path.exists(afterFilePath) is False:
            raise FileNotFoundError(f"After file {afterFilePath} does not exist")
        if os.path.exists(targetFilePath) is False:
            raise FileNotFoundError(f"Target file {targetFilePath} does not exist")

        # Save the file paths
        self.beforeFilePath = beforeFilePath
        self.afterFilePath = afterFilePath
        self.targetFilePath = targetFilePath

    def execute(self) -> None:
        """Execute the merge"""
        # Create the logger
        self.logger = logging.getLogger("MergeController")
        logging.basicConfig(level=logging.INFO)
        self.logger.info(" ---- MergeController - v1.0.0 ----")
        self.logger.info("Starting merging of files...")
        self.logger.info("Before file: %s" % self.beforeFilePath)
        self.logger.info("After file: %s" % self.afterFilePath)
        self.logger.info("Target file: %s" % self.targetFilePath)

        # Create a diff between the before file and the after file
        with open(self.beforeFilePath, "r", encoding="utf-8") as beforeFile, open(
            self.afterFilePath, "r", encoding="utf-8"
        ) as afterFile:
            changeSetBetweenBeforeAndAfter = DiffCreator.generateChangeList(
                beforeFile.readlines(),
                afterFile.readlines(),
                self.logger,
            )

        # Create a diff between the before file and the target file
        with open(self.beforeFilePath, "r", encoding="utf-8") as beforeFile, open(
            self.targetFilePath, "r", encoding="utf-8"
        ) as targetFile:
            changeSetBetweenBeforeAndTarget = DiffCreator.generateChangeList(
                beforeFile.readlines(),
                targetFile.readlines(),
                self.logger,
            )

        # Apply the changelist to a file
        newTargetFileContent = FileMerger.applyChangeset(
            self.targetFilePath,
            changeSetBetweenBeforeAndAfter,
            changeSetBetweenBeforeAndTarget,
            self.logger,
        )

        # Write changes to file
        with open(self.targetFilePath, "w", encoding="utf-8") as file:
            file.writelines(newTargetFileContent)

        # Log the finish
        self.logger.info("Finished merging of files")
