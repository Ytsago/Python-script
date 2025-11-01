import os
from typing import List, Union


def getDirList(path: str) -> List[Union[str, List]]:
    dirList = []
    if not os.path.isdir(path):
        return path
    for name in os.listdir(path):
        full_path = os.path.join(path, name)
        if os.path.isdir(full_path):
            dirList.append(getDirList(full_path))
        else:
            dirList.append(name)
    return [os.path.basename(path)] + dirList


def genMakefile():
    print("No Makefile has been found.\nWould you like to generate it ?\n")
    x = input("1 - Yes	|2 - No\n")
    if x == 2:
        print("The Makefile will not be generated\n")
    elif x == 1:
    	print("The Makefile will be generated\n")
    else:
    	print("Invalid input")
    	return genMakefile()


dirList = getDirList("./")
if not os.path.isfile(dirList[0] + "MakeFile"):
    genMakefile()
print(dirList)
