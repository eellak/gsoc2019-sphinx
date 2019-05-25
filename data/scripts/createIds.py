# A python script that creates 'test.fileids' file
# for a certain dataset. This file contains the id
# of each file in the dataset in the form dataset_{id}.

import sys

f = open("test.fileids", 'w')

name = raw_input("Give dataset: ")
if (name != "radio" and name != "paramythi"):
    sys.exit("Wrong dataset (should be either radio or paramythi)")
name = name.strip('\n') + "_"

n = int(input("Give number of examples: "))

for i in range(n):
    if name == "radio_":
        f.write(name + format(i, '02d') + '\n')
    if name == "paramythi_":
        f.write("Paramythi_horis_onoma_" + format(i, '04d') + '\n')
f.close()
