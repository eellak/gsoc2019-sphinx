import subprocess

categories_name = ['Αθλητισμός', 'Ελλάδα', 'Επιστήμη', 'Κόσμος',
                   'Οικονομία', 'Περιβάλλον', 'Πολιτική', 'Τέχνες', 'Υγεία', 'Άλλα']


def build_model(categories_name):
    for category in categories_name:
        if subprocess.call(['ngram-count -kndiscount -interpolate -text ./categories/' + category + ' -wbdiscount1 -wbdiscount2 -wbdiscount3 -lm ./categories/' + category + '.lm'], shell=True):
            sys.exit('Error in subprocess')
    print('Language models created')


if __name__ == '__main__':
    build_model(categories_name)
