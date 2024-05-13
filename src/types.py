from typing import TypedDict


class IChangeItem(TypedDict):
    beforeHunkStartLine: int
    afterHunkStartLine: int
    hunkLength: int
    removedLines: int
    addedLines: int
    hunk: list[str]
