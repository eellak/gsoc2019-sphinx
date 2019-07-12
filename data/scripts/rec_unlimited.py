"""Create a recording with arbitrary duration.

PySoundFile (https://github.com/bastibe/PySoundFile/) has to be installed!
Script is taken from https://python-sounddevice.readthedocs.io/en/0.3.13/examples.html.

"""
import argparse
import tempfile
import queue
import sys
import sounddevice as sd
import soundfile as sf
import numpy


def record(dev, samplerate, channels, filename, subtype):
    try:
        if samplerate is None:
            device_info = sd.query_devices(dev, 'input')
            # soundfile expects an int, sounddevice provides a float:
            samplerate = int(device_info['default_samplerate'])
        if filename is None:
            filename = tempfile.mktemp(prefix='delme_rec_unlimited_',
                                       suffix='.wav', dir='')
        q = queue.Queue()

        def callback(indata, frames, time, status):
            """This is called (from a separate thread) for each audio block."""
            if status:
                print(status, file=sys.stderr)
            q.put(indata.copy())
        # Make sure the file is opened before recording anything:
        with sf.SoundFile(filename, mode='x', samplerate=samplerate,
                          channels=channels, subtype=subtype) as file:
            with sd.InputStream(samplerate=samplerate, device=dev,
                                channels=channels, callback=callback):
                print('Recording...')
                print('press Ctrl+C to stop the recording')
                while True:
                    file.write(q.get())
    except KeyboardInterrupt:
        print('\n Recording finished: ' + repr(filename))
        return 0
