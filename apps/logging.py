import os

def append_log(content, file_path):
    if not os.path.isfile(file_path):
        f = open(file_path, "w")
        f.close()

    f = open(file_path, "a")
    f.write(str(content) + "\n")
    f.close()

def update_log(list_content, file_path):
    f = open(file_path, "w")
    for obj in list_content:
        f.write(str(obj) + "\n")
    f.close()

def read_log(file_path, counts):
    list_raw = []
    list_content = []

    f = open(file_path, "r")
    list_raw = f.readlines()
    f.close()

    for obj in list_raw:
        list_content.append(obj.rstrip())

    if counts > len(list_content):
        counts = len(list_content)

    if counts == 0:
        return list_content

    return list_content[0:counts]
