package com.asr.recognizer;

import java.io.File;
import java.io.IOException;

public class StreamEvaluator {

	public static void main(String[] args) throws IOException {
		// Create a recognizer based on the default acoustic and language model.
		StreamRecognizer recognizer = new StreamRecognizer("cmusphinx-el-gr-5.2/el-gr.cd_cont_5000", "cmusphinx-el-gr-5.2/el-gr.dic", "cmusphinx-el-gr-5.2/el-gr.lm.bin");
		// Folder that holds the speech data to evaluate
		File dir = new File("data");
		File[] directoryListing = dir.listFiles();
		String output;
		if (directoryListing != null) {
			// Convert each .wav file into text and print it.
		    for (File audioFile : directoryListing) {
		    	output = recognizer.recognizeFile(audioFile.toString());
				System.out.println(output);
		    }
		} else {
		    // Handle the case where dir is not really a directory.
			System.out.println("Not a directory");
		}
	}
}
