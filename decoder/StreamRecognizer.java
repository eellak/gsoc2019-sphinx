package com.asr.recognizer;

import java.io.FileInputStream;
import java.io.IOException;

import edu.cmu.sphinx.api.Configuration;
import edu.cmu.sphinx.api.SpeechResult;
import edu.cmu.sphinx.api.StreamSpeechRecognizer;

/**
 * Recognizes a speech file based on the acoustic and language model given.
 * @author Panagiotis Antoniadis
 *
 */

public class StreamRecognizer {
/* Holds the paths of each model.*/
Configuration configuration;
StreamSpeechRecognizer recognizer;

/**
 * Creates a new StreamRecognizer with the given models.
 * @param acousticModel
 * @param phoneticDict
 * @param languageModel
 * @throws IOException
 */
public StreamRecognizer(String acousticModel, String phoneticDict, String languageModel) throws IOException {
        /* Set the path of the acoustic model, the phonetic dictionary
           and the language model */
        this.configuration = new Configuration();
        this.configuration.setAcousticModelPath(acousticModel);
        this.configuration.setDictionaryPath(phoneticDict);
        this.configuration.setLanguageModelPath(languageModel);
        recognizer = new StreamSpeechRecognizer(configuration);
}

/**
 * Converts the input .wav file in text and returns the result.
 * @param filename
 * @return
 * @throws IOException
 */
public String recognizeFile(String filename) throws IOException {
        recognizer.startRecognition(new FileInputStream(filename));
        SpeechResult result;
        String resultString = "";
        // Pause recognition process. It can be resumed then with startRecognition(false).
        while ((result = recognizer.getResult()) != null) {
                resultString += result.getHypothesis() + " ";
        }
        recognizer.stopRecognition();
        return resultString;
}
}
