import sys
import os
import argparse
import subprocess
import shutil


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser(description='''
        Tool for adapting an acoustic model based on given transcription
    ''')

    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument(
        '--wav', help="Directory that contains the sound files", required=True)
    required.add_argument(
        '--ids', help="The ids of the sound files", required=True)
    required.add_argument(
        '--hmm', help="Folder that contains the default acoustic model", required=True)
    required.add_argument(
        '--dic', help="The dictionary to be used", required=True)
    required.add_argument(
        '--transcriptions', help="Transcriptions of the sound files", required=True)
    required.add_argument(
        '--output', help="Output directory", required=True)
    required.add_argument(
        '--sphinxtrain', help="Sphinxtrain installation folder", required=True)

    required.add_argument(
        '--adaptation', help="Type of adaptation: map or mllr (default: both of them)")

    args = parser.parse_args()
    wav = args.wav
    ids = args.ids
    hmm = args.hmm
    dic = args.dic
    transcriptions = args.transcriptions
    output = args.output
    sphinxtrain = args.sphinxtrain
    adaptation = args.adaptation

    if not wav.endswith('/'):
        wav = wav + '/'
    if not hmm.endswith('/'):
        hmm = hmm + '/'
    if not output.endswith('/'):
        output = output + '/'
    if not sphinxtrain.endswith('/'):
        sphinxtrain = sphinxtrain + '/'

    print('Generate acoustic model features from recordings')
    feat_params = os.path.join(hmm, 'feat.params')
    mfc_path = os.path.join(output, 'mfc')
    generate_command = 'sphinx_fe -argfile ' + feat_params + ' -samprate 16000 -c ' + \
        ids + ' -di ' + wav + ' -do ' + mfc_path + ' -ei wav -eo mfc -mswav yes'
    if subprocess.call([generate_command], shell=True):
        sys.exit('Error in subprocess')

    print('Collect statistics from the adaptation data')

    # Copy bw, map_adapt and mk_s2sendump scripts.
    shutil.copy2(sphinxtrain + 'bw', output)
    shutil.copy2(sphinxtrain + 'map_adapt', output)
    shutil.copy2(sphinxtrain + 'mk_s2sendump', output)

    mdef_path = os.path.join(hmm, 'mdef')
    counts_path = os.path.join(output, 'counts')
    os.makedirs(counts_path)
    feature_path = os.path.join(hmm, 'feature_transform')
    bw_command = './' + output + 'bw -hmmdir ' + hmm + ' -cepdir ' + mfc_path + ' -moddeffn ' + mdef_path + ' -ts2cbfn .cont. -feat 1s_c_d_dd -cmn batch -agc none \
                        -dictfn ' + dic + ' -ctlfn ' + ids + ' -lsnfn ' + transcriptions + ' -accumdir ' + counts_path + ' -lda ' + feature_path + ' -varnorm no -cmninit 40,3,-1'
    print(bw_command)
    if subprocess.call([bw_command], shell=True):
        sys.exit('Error in subprocess')

    shutil.copy2(sphinxtrain + 'mllr_solve', output)
    means_path = os.path.join(hmm, 'means')
    variance_path = os.path.join(hmm, 'variances')
    mllr_path = os.path.join(output, 'mllr_matrix')
    mllr_command = './' + output + 'mllr_solve -meanfn ' + means_path + ' -varfn ' + variance_path + \
        ' -outmllrfn ' + mllr_path + ' -accumdir ' + counts_path
    if adaptation is None or adaptation == "mllr":
        print('Generate mllr transformation')
        print(mllr_command)
        if subprocess.call([mllr_command], shell=True):
            sys.exit('Error in subprocess')

    if adaptation is None or adaptation == "map":
        hmm_map = os.path.join(output, 'map')
        os.makedirs(hmm_map)
        copytree(hmm, hmm_map)
        map_command = './' + output + 'map_adapt -moddeffn ' + hmm + '/mdef.txt -ts2cbfn .cont. -meanfn ' + \
            hmm + '/means -varfn ' + hmm + '/variances -mixwfn ' + hmm + '/mixture_weights -tmatfn ' + hmm + '/transition_matrices \
            -accumdir ' + counts_path + ' -mapmeanfn ' + hmm_map + '/means -mapvarfn ' + hmm_map + '/variances -mapmixwfn ' + hmm_map + \
            '/mixture_weights -maptmatfn ' + hmm_map + '/transition_matrices'
        print('Generate map adaptation')
        print(map_command)
        if subprocess.call([map_command], shell=True):
            sys.exit('Error in subprocess')
