import os
from typing import List, Union


MAKEFILE_TEMPLATE = [
    {
        "section_name": "Compiler definition",
        "section_header": "# ---------RULES----------#",
        "fields": [
            {
                "field_name": "CC",
                "prompt": "Please choose a compiling rule\n(You can write your own)\n1 - CC | 2 - GCC | 3 - C++\n",
                "default": "gcc",
                "choices": {
                    '1': 'cc',
                    '2': 'gcc',
                    '3': 'c++',
                }
            },
            {
                "field_name": "CFLAGS",
                "prompt": "Choose a compiling rule\n(You can write your own)\n1 - -Wall | 2 - 42basic (-Wall -Wextra -Werror) | 3 - Debug(-Wall -Wextra -g3)\n",
                "default": "-Wall -Wextra -Werror",
                "choices": {
                    '1': '-Wall',
                    '2': '-Wall -Wextra -Werror',
                    '3': '-Wall -Wextra -g3',
                }
            }
        ]
    }
]


# def getDirList(path: str) -> List[Union[str, List]]:
#     dirList = []
#     if not os.path.isdir(path):
#         return path
#     for name in os.listdir(path):
#         if name == ".git":
#             continue
#         full_path = os.path.join(path, name)
#         if os.path.isdir(full_path):
#             dirList.append(getDirList(full_path))
#         else:
#             dirList.append(name)
#     return [os.path.basename(path)] + dirList


def writeSelector(field: dict) -> str:
    prompt = field["prompt"]
    choices = field["choices"]
    default = field["default"]
    print(f"{prompt} (default: {default})")
    x = input("Selection =>").strip()
    if not x:
        return default
    if x in choices:
        return choices[x]
    return x


def genTemplateMakefile():
    with open("Makefile", 'w') as f:
        for section in MAKEFILE_TEMPLATE:
            f.write(section['section_header'] + "\n")
            print(f"Setup - {section['section_name']}\n")
            for field in section['fields']:
                value = writeSelector(field)
                f.write(f"{field['field_name']} = {value}\n")


def genMakefile():
    print("No Makefile has been found.\nWould you like to generate it ?\n")
    x = input("1 - Yes    |2 - No\nSelection =>")
    if x == '1':
        print("The Makefile will be generated\n")
        genTemplateMakefile()
    elif x == '2':
        print("The Makefile will not be generated\n")
    else:
        print("Invalid input")
        return genMakefile()


dirList = os.walk('.')
print(dirList)
if not "Makefile" in dirList:
    genMakefile()
