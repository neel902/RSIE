def mkimg(path):
    from pathlib import Path
    import json

    script_dir = Path(__file__).resolve().parent
    file_path = script_dir / "filesystem"

    with open(file_path, "r") as file:
        content = file.read()
    with open(path, "w") as file:
        file.write(content)

if __name__ == "__main__":
    mkimg(input("Output: "))