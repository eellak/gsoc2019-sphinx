package speech2text;

import java.io.FileInputStream;
import java.io.IOException;

import edu.cmu.sphinx.api.Configuration;
import edu.cmu.sphinx.api.SpeechResult;
import edu.cmu.sphinx.api.StreamSpeechRecognizer;

public class StreamRecognizer {
public Configuration configuration;
public StreamSpeechRecognizer recognizer;

public StreamRecognizer(){
}

public void setConfiguration(String acousticModel, String phoneticDict, String languageModel) throws IOException {
								this.configuration = new Configuration();
								this.configuration.setAcousticModelPath(acousticModel);
								this.configuration.setDictionaryPath(phoneticDict);
								this.configuration.setLanguageModelPath(languageModel);
								recognizer = new StreamSpeechRecognizer(configuration);

}


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
