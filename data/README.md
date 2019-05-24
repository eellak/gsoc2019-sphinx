# Datasets

- __test_paramythi:__ Greek woman speaker reads a fairytale lasting 4 hours.

  Link: https://drive.google.com/open?id=18hErfhgmXmhJ0VraVX4zb4SJ2UOOZl8l

- __test_radio:__ Multiple Greek speakers of the Department of Journalism tell the news lasting 1 hour.

  Link:  https://www.dropbox.com/home/test_radio



# Structure 

- __wav:__ A folder that contains all the recordings under the name {file id}.wav
- __test.fileids:__ A text file that contains in each line a file id.
- __test.transcription:__ A text file that contains in each line the transcription following by the file id in parenthesis.
- __language-models:__ Folder that contains the language model created based on this dataset (using [SRILM](<http://www.speech.sri.com/projects/srilm/>)):
  - specific: Developed using only the transcriptions of the dataset.
  - merged: Developed using both the transcriptions of the dataset and the default language model.
- __test.hyp:__ Contains the hypothesis of the system using the default model.
- __test_specific.hyp:__ Contains the hypothesis of the system using the specific language model.
- __test_merged.hyp:__ Contains the hypothesis of the system using the merged language model.

Structure is based on [Sphinx requirements](https://cmusphinx.github.io/wiki/tutorialtuning/).

