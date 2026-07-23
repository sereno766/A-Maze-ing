import argparse

def parser_file(path: str) -> dict:
    coords = ["ENTRY", "EXIT"]
    int_set = ["WIDTH", "HEIGHT"]
    str_set = ["OUTPUT_FILE"]
    bool_set = ["PERFECT"]
    settings = {}
    with open(path, "r") as file:
        lines = str(file.read()).split("\n")
    for line in lines:
        key, value = line.split(sep="=")
        if key in coords:
            x, y = value.split(",")
            settings[key] = (int(x), int(y))
        elif key in int_set:
            settings[key] = int(value)
        elif key in str_set:
            settings[key] = str(value)
        elif key in bool_set:
            settings[key] = True if value == "True" else (False if value == "False" else None)
        else:
            del(settings)
            return {"INVALID": True}
    print(settings)
    return settings

def a_maze_ing() -> int:
    parser = argparse.ArgumentParser(description = "")
    parser.add_argument("config.txt", help = "")

    args = parser.parse_args()

    if args.config_txt:
        pfile = find_file("config.txt")
        parser_file(pfile)

parser_file("config.txt")