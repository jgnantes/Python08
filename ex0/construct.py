import sys
import os
import site


def construct() -> str:
    """ """
    in_venv: bool = (
        hasattr(sys, "real_prefix") or
        (hasattr(sys, "base_prefix") and sys.prefix != sys.base_prefix)
    )

    result: str = ""
    if in_venv:
        result += f"Virtual environment detected: {sys.prefix}\n"
        result += f"Environemtn version: {sys.version}\n"
    else:
        result += "No virtual environment detected\n"
        result += "To create one, run the following command on your terminal:"
        result += "\npython -m venv .venv"

    return result




if __name__ == "__main__":
    print(construct())
