from validator import validate_config
from typing import Any


def load_config(path: str) -> dict[Any, Any]:
    """Reads through the config.txt file, formats it so that it works with
    validate_config calls validate_config and returns the formatted version
    of config.txt

    Parameters:
    path (str): name of the config.txt

    Returns:
    dict: Formatted version of config.txt
    """
    data: dict[str, str] = {}

    with open(path) as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                raise ValueError(f"Invalid line {line_no}: {line}")

            key, value = map(str.strip, line.split("=", 1))
            data[key] = value

    validated = validate_config(data)

    return validated


if __name__ == "__main__":
    data = load_config("config.txt")
    print(data)
