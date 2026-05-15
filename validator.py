from typing import Any


def validate_config(data: dict[str, Any]) -> dict[str, Any]:
    """This function checks the config.txt file and returns the formatted
      results with error handling

      Parameters:
      data (dict[str, Any]): Content of config.txt file in a dict form

      Returns:
      dict: formatted config.txt
    """
    required = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
    pattern = True

    for key in required:
        if key not in data:
            raise ValueError(f"Missing key: {key}")

    try:
        width = int(data["WIDTH"])
        height = int(data["HEIGHT"])
    except ValueError:
        raise ValueError("WIDTH and HEIGHT must be integers")

    if width <= 0 or height <= 0:
        raise ValueError("WIDTH and HEIGHT must be > 0")

    if width <= 8 or height <= 6:
        print("Maze size is too small for 42 pattern")
        pattern = False

    try:
        ex, ey = map(int, data["ENTRY"].split(","))
        xx, xy = map(int, data["EXIT"].split(","))
    except Exception:
        raise ValueError("ENTRY and EXIT must be in format x,y with integers")

    if not (0 <= ex < width and 0 <= ey < height):
        raise ValueError("ENTRY is out of maze bounds")

    if not (0 <= xx < width and 0 <= xy < height):
        raise ValueError("EXIT is out of maze bounds")

    if (ex, ey) == (xx, xy):
        raise ValueError("ENTRY and EXIT must be different")

    perfect_str = data["PERFECT"].strip().lower()
    if perfect_str == "true":
        perfect = True
    elif perfect_str == "false":
        perfect = False
    else:
        raise ValueError("PERFECT must be True or False")

    output_file = data["OUTPUT_FILE"].strip()
    if not output_file:
        raise ValueError("OUTPUT_FILE cannot be empty")

    seed = None
    if "SEED" in data:
        try:
            seed = int(data["SEED"])
        except ValueError:
            raise ValueError("SEED must be an integer")

    return {
        "width": width,
        "height": height,
        "entry": (ex, ey),
        "exit": (xx, xy),
        "output_file": output_file,
        "perfect": perfect,
        "seed": seed,
        "42_pattern": pattern
    }
