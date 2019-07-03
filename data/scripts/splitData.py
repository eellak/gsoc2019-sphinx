import argparse
import os
import random
import shutil

if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser(description='''
        Tool that splits a speech dataset in train and test set. Dataset folder should be in Sphinx format.
    ''')

    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument(
        '--wav', help="Folder that contains the recordings", required=True)
    required.add_argument(
        '--ids', help="File that contains the ids of the files", required=True)
    required.add_argument(
        '--data', help="Folder that contains the transcriptions", required=True)
    required.add_argument(
        '--name', help="Name of the dataset. Files in data and wav folder should be name_{id} and name_{id}.wav respectively", required=True)
    required.add_argument(
        '--total', help="Total number of samples", required=True, type=int)

    optional.add_argument(
        '--ratio', help="Ratio between train and test set", type=float, default=0.7)

    args = parser.parse_args()
    wav = args.wav
    ids = args.ids
    data = args.data
    name = args.name
    total = args.total
    ratio = args.ratio

    # Get train and test set ids.
    train = random.sample(range(total), int(ratio * total))
    test = [sample for sample in range(total) if sample not in train]

    # If train or test directory do not exist, create them.
    if not os.path.exists('train'):
        os.makedirs('train')
    if not os.path.exists('test'):
        os.makedirs('test')

    # Split wav files
    if not os.path.exists('train/wav'):
        os.makedirs('train/wav')
    if not os.path.exists('test/wav'):
        os.makedirs('test/wav')
    wav_path = os.path.join(wav, name) + '_'
    for id in range(total):
        if id in train:
            shutil.copy2(wav_path + str(id) + '.wav',
                         os.path.join('train', 'wav'))
        if id in test:
            shutil.copy2(wav_path + str(id) + '.wav',
                         os.path.join('test', 'wav'))

    # Split data files
    if not os.path.exists('train/data'):
        os.makedirs('train/data')
    if not os.path.exists('test/data'):
        os.makedirs('test/data')
    data_path = os.path.join(data, name) + '_'
    for id in range(total):
        if id in train:
            shutil.copy2(data_path + str(id),
                         os.path.join('train', 'data'))
        if id in test:
            shutil.copy2(data_path + str(id),
                         os.path.join('test', 'data'))

    # Split id file
    with open(ids, 'r') as r, open('train/fileids', 'w') as w1, open('test/fileids', 'w') as w2:
        for idx, line in enumerate(r):
            if idx in train:
                w1.write(line)
            if idx in test:
                w2.write(line)
