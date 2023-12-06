from pathlib import Path


def parse_file_name(file_name: str) -> list[str]:
    file_name = Path(file_name).with_suffix("").name
    args_list = []
    for s in file_name.split("_"):
        try:
            s = int(s)
        except Exception:
            pass
        args_list.append(s)
    return args_list


def add_suffix_to_filename(filename: str, suffix: str) -> str:
    # Create a Path object from the filename
    path = Path(filename)
    # Add the suffix to the stem (the file name without the extension)
    new_stem = f"{path.stem}_{suffix}"
    # Combine the new stem with the extension
    new_filename = path.with_stem(new_stem)
    return str(new_filename)
