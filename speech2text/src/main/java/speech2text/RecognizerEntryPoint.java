package speech2text;

import py4j.GatewayServer;


public class RecognizerEntryPoint {

StreamRecognizer rec;

public RecognizerEntryPoint() {
	rec = new StreamRecognizer();
}
public StreamRecognizer getStreamRecognizer() {
	return rec;
}

public static void main(String[] args) {
        GatewayServer gatewayServer = new GatewayServer(new RecognizerEntryPoint());
        gatewayServer.start();
        System.out.println("Gateway Server Started");
}

}
