import os
from pprint import pprint

filename = 'structure.str'


def create_filesystem_structure(root_dir, structure):
    os.makedirs(root_dir, exist_ok=True)

    for directory, contents in structure.items():
        dir_path = os.path.join(root_dir, directory)
        os.makedirs(dir_path, exist_ok=True)

        for content in contents:
            if content.endswith('.py'):
                with open(os.path.join(dir_path, content), 'w') as f:
                    f.write('# Здесь находится код вашего приложения\n')
            else:
                os.makedirs(os.path.join(dir_path, content), exist_ok=True)


with open(filename, 'r') as f:
    structure_str = f.read()
print(structure_str)


def parse_structure_string(structure_str):
    structure_dict = {}
    current_dir = None
    current_dir_2 = None
    current_dir_3 = None

    def parse_level_0(line):
        nonlocal current_dir
        current_dir = line.strip("- ").strip()
        structure_dict[current_dir] = {}

    def parse_level_2(line):
        nonlocal current_dir_2
        if line.strip("- ").strip()[-1] == "/":
            current_dir_2 = line.strip(" - ").strip()
            structure_dict[current_dir][current_dir_2] = {}
        else:
            structure_dict[current_dir][line.strip(" - ").strip()] = None

    def parse_level_4(line):
        nonlocal current_dir_3
        if line.strip("- ").strip()[-1] == "/":
            current_dir_3 = line.strip(" - ").strip()
            structure_dict[current_dir][current_dir_2][current_dir_3] = {}
        else:
            structure_dict[current_dir][current_dir_2][line.strip(" - ").strip()] = None

    def parse_level_6(line):
        structure_dict[current_dir][current_dir_2][current_dir_3].append(line.strip("- ").strip())

    for line in structure_str.split("\n"):
        if not line.strip():
            continue

        indent_level = len(line) - len(line.lstrip("-"))
        if indent_level == 0:
            parse_level_0(line)
        elif indent_level == 2:
            parse_level_2(line)
        elif indent_level == 4:
            parse_level_4(line)
        elif indent_level == 6:
            parse_level_6(line)

    return structure_dict


def generate_structure(structure_dict, path=""):
    for name, value in structure_dict.items():
        current_path = os.path.join(path, name)
        if value is None:
            file = open(current_path, 'w',encoding="utf-8")

            if file.name.endswith('.py'):
                file.write('# Здесь находится код вашего приложения\n')

            file.close()
        elif isinstance(value, dict):
            os.mkdir(current_path)
            generate_structure(value, current_path)


structure_dict = parse_structure_string(structure_str)
pprint(structure_dict)

# Удаляем пустые значения из словаря
structure_dict = {k: v for k, v in structure_dict.items() if v}

generate_structure( structure_dict , ".")
