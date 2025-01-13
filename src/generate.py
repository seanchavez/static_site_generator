from os.path import exists, isfile, join
from os import listdir, mkdir
from shutil import rmtree, copy


def copy_static(source, destination):
    if exists(destination):
        rmtree(destination)
    mkdir(destination)
    if isfile(source):
        copy(source, destination)
    else:
        contents = listdir(source)
        for item in contents:
            if isfile(item):
                copy(join(item, source), destination)
            else:
                copy_static(join(source, item), join(destination, item))
