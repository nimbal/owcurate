from Files.Converters import *
from os import listdir, mkdir
from os.path import isfile, join

input_dir = input("Please enter input directory: ")

out_dir = input("Please enter output directory: ")


files = [f for f in listdir(input_dir) if (isfile(join(input_dir, f)) and ".bin" in f)]
files.sort()

for f in files[18:]:
    curr = GENEActiv()
    curr.read_from_raw(join(input_dir, f))
    mkdir(join(out_dir, f[:-4]))
    GENEActivToEDF(curr, join(out_dir, f[:-4]))

