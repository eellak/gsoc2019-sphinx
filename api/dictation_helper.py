import re
import os
import subprocess


def get_text_pocketsphinx(out, lmPath, acousticPath, dictPath):
    # Create temp id file.
    ids_path = os.path.join(out, "ids")
    with open(ids_path, 'w') as f:
        f.write('curr_dictation\n')
    command = "pocketsphinx_batch -adcin yes -cepdir " + out + " -cepext .wav  -ctl " + ids_path + \
        " -lm " + lmPath + " -dict " + dictPath + \
        " -hmm " + acousticPath + " -hyp " + os.path.join(out, 'result')
    if subprocess.call([command], shell=True):
        print('Error in subprocess')
    # Read output temp file.
    with open(os.path.join(out, 'result'), 'r') as f:
        decoded_text = f.read()
    decoded_text = re.sub(r'\([^)]*\)$', '',
                          decoded_text).strip('\n').strip(' ')
    # Remove temp files
    os.remove(os.path.join(out, 'result'))
    os.remove(ids_path)
    return decoded_text


def get_text_sphinx4(py4j_relpath, acousticPath, dictPath, lmPath, gateway):
    # Convert speech to text using Java cmuSphinx library.
    stream = gateway.entry_point.getStreamRecognizer()
    stream.setConfiguration(acousticPath, dictPath, lmPath)
    decoded_text = stream.recognizeFile(
        os.path.join(py4j_relpath, "curr_dictation.wav"))
    return decoded_text
