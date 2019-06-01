# A simple script that takes as input a text
# file and split its in a train and a test set.
# Used in order to split fileids and
# transciption files.

# Usage: ./splitData.sh <input file> <name1> <name2>

if [ "$#" -ne 3 ]; then
    echo "Illegal number of parameters"
    exit 1
fi

# Split files using 70% ratio.
split -l $[ $(wc -l $1|cut -d" " -f1) * 70 / 100 ] $1

# Rename them.
mv xaa ./$2
mv xab ./$3
