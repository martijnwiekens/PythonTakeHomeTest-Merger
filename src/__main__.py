from src.mergecontroller import MergeController


# Check if we are executing this file directly or if we are importing this file
if __name__ == "__main__":
    # Execute the merge controller, this is with demo files
    m = MergeController(
        "examples/9d4e45c5/before/kernel-4.18.0-477.27.1.el8_856gbnlwn",
        "examples/9d4e45c5/after/kernel-4.18.0-513.5.1.el8_92fqrcwu_",
        "examples/9d4e45c5/target/l2cap_core.cf7zq5cwb",
    )
    m.execute()

    # Execute the merge controller, this is with CLI input
    m = MergeController()
    m.execute()
