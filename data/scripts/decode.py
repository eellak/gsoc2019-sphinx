import argparse
import os
import pickle
import shutil
import sys
import subprocess

if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser(description='''
        Tool that converts a set of sound files to text using the language model of their cluster. The cluster has been
            computed based on the asr output using the general language model
    ''')

    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional argument')
    required.add_argument(
        '--wav', help="Folder that contains the sound files", required=True)
    required.add_argument(
        '--ids', help="Folder that contains the ids file", required=True)
    required.add_argument(
        '--dic', help="Path to the dictionary to be used", required=True)
    required.add_argument(
        '--hmm', help="Path to the acoustic model to be used", required=True)
    required.add_argument(
        '--labels', help="Pickle file that holds the cluster of each file", required=True)
    required.add_argument(
        '--n_clusters', help="Number of clusters", required=True, type=int)
    required.add_argument(
        '--output', help="Folder to save all created files", required=True)
    required.add_argument(
        '--transcription', help="Transription file that contains one email per line", required=True)
    required.add_argument(
        '--clusters', help="Path of the clusters that have been created", required=True)
    optional.add_argument(
        '--merged', help="Use merged language models", action='store_true')

    args = parser.parse_args()
    wav = args.wav
    ids = args.ids
    dic = args.dic
    hmm = args.hmm
    labels_path = args.labels
    n_clusters = args.n_clusters
    output = args.output
    transcription = args.transcription
    clusters = args.clusters
    merged = args.merged

    if not wav.endswith('/'):
        wav = wav + '/'
    if not hmm.endswith('/'):
        hmm = hmm + '/'
    if not output.endswith('/'):
        output = output + '/'
    if not clusters.endswith('/'):
        clusters = clusters + '/'

    if not os.path.exists(output):
        os.makedirs(output)

    # Unpickle labels of the test emails.
    with open(labels_path, 'rb') as f:
        labels = pickle.load(f)

    for i in range(n_clusters):
        if not os.path.exists(os.path.join(output, 'cluster_' + str(i))):
            os.makedirs(os.path.join(output, 'cluster_' + str(i)))

    # Split wav files in the corresponding cluster
    for i in range(n_clusters):
        cluster_path = os.path.join(output, 'cluster_' + str(i))
        if not os.path.exists(os.path.join(cluster_path, 'wav')):
            os.makedirs(os.path.join(cluster_path, 'wav'))

    for email in labels:
        shutil.copy2(os.path.join(wav, email + '.wav'),
                     os.path.join(output + '/cluster_' + str(labels[email]), 'wav'))

    # Split ids in the corresponding cluster
    for i in range(n_clusters):
        cluster_path = os.path.join(output, 'cluster_' + str(i))
        with open(os.path.join(cluster_path, 'fileids'), 'w') as w:
            for email in labels:
                if labels[email] == i:
                    w.write(email)
                    w.write('\n')

    # Split transcriptions file
    with open(transcription, 'r') as r:
        for line in r:
            id = line.split('(')[-1].split(')')[0]
            if id in labels:
                label = labels[id]
            else:
                sys.exit('Error in finding ids')
            cluster_path = os.path.join(
                output, 'cluster_' + str(label))
            with open(os.path.join(cluster_path, 'transription'), 'a') as w:
                w.write(line)

    # Decode each cluster separately
    for i in range(n_clusters):
        wav_path = output + '/cluster_' + str(i) + '/wav'
        id_path = output + '/cluster_' + str(i) + '/fileids'
        if merged:
            lm_path = clusters + '/cluster_' + str(i) + '/merged.lm'
            hyp_path = output + '/cluster_' + str(i) + '/merged.hyp'
        else:
            lm_path = clusters + '/cluster_' + str(i) + '/specific.lm'
            hyp_path = output + '/cluster_' + str(i) + '/specific.hyp'
        command = 'pocketsphinx_batch  -adcin yes  -cepdir ' + wav_path + ' -cepext .wav  -ctl ' + id_path + ' -lm ' + lm_path + \
            ' -dict ' + dic + ' -hmm ' + hmm + ' -hyp ' + hyp_path
        print(command)
        if subprocess.call([command], shell=True):
            sys.exit('Error in cluster ' + str(i))
