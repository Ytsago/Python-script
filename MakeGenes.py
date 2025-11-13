import os
from typing import List, Union


MAKEFILE_TEMPLATE = [
    {
        "section-name": "Color definition",
        "section-header": "# -----------COLOR-----------#",
        "mode": "Optional",
        "prompt": "Would you like to include colors ?\n1 - Yes  |  2 - No\n",
        "default": "False",
        "choices": {
            '1': 'True',
            '2': 'False',
        },
        "fields": [
            {
                "mode": "Preset",
                "field_name": "GREEN",
                "default":  "\\033[32m\nYELLOW = \\033[33m\nBLUE   = \\033[34m\nRED    = \\033[31m\nRESET  = \\033[0m",
            }
        ]
    },
    {
        "mode": "Default",
        "section-name": "Compiler definition",
        "section-header": "# -----------RULES-----------#",
        "fields": [
            {
                "mode": "Manual",
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
                "mode": "Manual",
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
    },
    {
        "mode": "Default",
        "section-name": "Directories definition",
        "section-header": "# -----------PATHS-----------#",
        "fields": [
            {
                "mode": "Preset",
                "field_name": "SRCDIR",
                "default": "src/",
            },
            {
                "mode": "Preset",
                "field_name": "INCDIR",
                "default": "inc/",
            },
            {
                "mode": "Preset",
                "field_name": "OBJDIR",
                "default": ".obj/",
            },
            {
                "mode": "Optional",
                "field_name": "LIBDIR",
                "prompt": "Would you like to include a lib directory ?\n1 - True  |  2 - False\n",
                "default": "False",
                "value": "libs/",
                "choices": {
                    '1': 'True',
                    '2': 'False',
                }
            }
        ]
    },
    {
        "section-name": "Subdirectories",
        "section-header": "#///////////SUBDIR////////////#",
        "mode": "Auto",
    },
    {
        "section-name": "Other definition",
        "section-header": "# -----------OTHER-----------#",
        "mode": "Default",
        "fields": [
            {
                "mode": "Preset",
                "field_name": "OBJS",
                "default": "$(patsubst $(SRCDIR)%.cpp, $(OBJDIR)%.o, $(SRCS))\n",
            },
            {
                "mode": "Preset",
                "field_name": "DEPS",
                "default": "$(OBJS:.o=.d)\n",
            },
            {
                "mode": "Preset",
                "field_name": "HEADER",
                "default": "$(addprefix $(INCDIR), $(INC))\n",
            },
            {
                "mode": "Preset",
                "field_name": "# LIBS",
                "default": "WIP\n",
            },
            {
                "mode": "Manual",
                "field_name": "NAME",
                "default": "a.out",
                "prompt": "Enter the executable name :\n",
                "choices": {
                    'none': 'none',
                }
            }
        ]

    },
    {
        "section-name": "Compilation Rules",
        "section-header": "# -----------COMPILATION-----------#",
        "mode": "Rules",
        "fields": [
            {
                "field_name": "all",
                "default": "$(NAME)"
            },
            {
                "field_name": "$(NAME)",
                "default": "libs $(OBJS)\n\t$(CC) $(CFLAGS) $(OBJS) $(LIBS) -o $(NAME)\n",
            },
            {
                "field_name": "$(OBJDIR)%.o",
                "default": "$(SRCDIR)%.cpp Makefile | $(OBJDIR)\n\t$(CC) $(CFLAGS) -I $(INCDIR) $(if $(LIBS),-I $(LIBDIR)$(INCDIR)) -c $< -o $@\n"
            },
            {
                "field_name": "$(OBJDIR)",
                "default": "\n\tmkdir -p $(OBJDIR) $(dir $(OBJS))\n",
            },
            {
                "field_name": "libs",
                "default": "\n\t$(MAKE) -C $(LIBDIR) --no-print-directory\n",
            }
        ]
    },
    {
        "section-name": "More rules",
        "section-header": "# -----------UTILS-----------#",
        "mode": "Rules",
        "fields": [
            {
                "field_name": "clean",
                "default": "\n\trm -rf $(OBJDIR)\nifneq ($(LIBS),)\n# WIP for libs\n",
            },
            {
                "field_name": "fclean",
                "default": "clean\n\trm -f $(NAME)\n# WIP for libs\n",
            },
            {
                "field_name": "re",
                "default": "fclean all\n"
            },
            {
                "field_name": ".PHONY",
                "default": "clean fclean, re, all",
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
    default = field["default"]
    mode = field["mode"]
    if mode == "Auto":
        print("This field will be determinate automaticly\n")
        return default
    if mode == "Preset":
        return default
    prompt = field["prompt"]
    choices = field["choices"]
    print(f"{prompt}(default: {default})")
    x = input("Selection => ").strip()
    if not x:
        return default
    if x in choices:
        return choices[x]
    if mode == "Manual":
        return x
    else:
        return "False"


def handleField(section: dict, f):
    delim = " = "
    mode = section["mode"]
    for field in section["fields"]:
        if mode == "Default" or mode == "Optional":
            value = writeSelector(field)
            if field["mode"] == "Optional":
                if value == "False":
                    continue
                else:
                    value = field["value"]
        elif mode == "Rules":
            delim = ": "
            value = field["default"]
        f.write(f"{field['field_name']}{delim}{value}\n")


def handleSection(f):
    for section in MAKEFILE_TEMPLATE:
        if section["mode"] == "Optional":
            value = writeSelector(section)
            if value == "False":
                continue

        elif section["mode"] == "Auto":
            print("This section must be determine automaticly\n")
            continue

        f.write(section["section-header"] + "\n")
        handleField(section, f)
        f.write("\n")


def scanDirectory(Path):
    config = {}
    for root, dirs, files in os.walk(Path):
        if os.path.basename(root).startswith("."):
            continue

        fileLst = [f for f in files if not f.startswith(".")]
        config[root] = fileLst
    return config


def genTemplateMakefile():
    with open("Makefile", 'w') as f:
        handleSection(f)


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


def main():
    makefile = False
    for entry in os.scandir('.'):
        if "Makefile" in entry.name:
            print("Makefile found")
            makefile = True
        else:
            print("No makefile")
    if makefile:
        print("Would you like to update it ?(y/N)\n")
        x = input("Selection => ")
        if x == 'y' or x == 'Y':
            print("Updating makefile")
        else:
            print("Exiting...")
    else:
        genMakefile()


if __name__ == "__main__":
    config = scanDirectory(".")
    for folder, files in config.items():
        print(folder, ":", files)
    main()
