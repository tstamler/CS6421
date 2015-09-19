/******************************************************************************
 *
 *  CS 6421 - Simple Conversation
 *  Compilation:  javac OuncesInches.java
 *  Execution:    java OuncesInches port
 *
 *  % java OuncesInches portnum
 ******************************************************************************/

import java.net.Socket;
import java.net.ServerSocket;
import java.io.IOException;
import java.io.PrintWriter;
import java.net.UnknownHostException;
import java.io.BufferedReader;
import java.io.InputStreamReader;

//9.  bananas <-> length in inches

// Malcolm Goldiner
// Group Member: Tim Stamler

public class OuncesInches {
    
    
    public static int conversion(int num, String unit){
        if(unit.equals("ounces")) return num * 8;
        else  return  num / 8; 
    }
    
    

    public static void process (Socket clientSocket) throws IOException {
        // open up IO streams
        BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
        PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);

        /* Write a welcome message to the client */
        out.println("Welcome to the Bananas (ounces) to length in inches (inches) Conversion Server");

        /* read and print the client's request */
        // readLine() blocks until the server receives a new line from client
        String userInput;
        if ((userInput = in.readLine()) == null) {
            System.out.println("Error reading message");
            out.close();
            in.close();
            clientSocket.close();
        }

        System.out.println("Received message: " + userInput);
        //--TODO: add your converting functions here, msg = func(userInput);
        String[] inputArr = userInput.split(" "); 
        
        if((!inputArr[0].equals("inches") && !inputArr[1].equals("ounces"))
        && (!inputArr[0].equals("ounces") && !inputArr[1].equals("inches"))) {
            out.println("Sorry, that conversion isn't supported");
        } else {
            if(inputArr[0].equals("b")) out.println(inputArr[2] + " bananas is " + conversion(Integer.valueOf(inputArr[2]), inputArr[0]) + " inches in length");
            else out.println(inputArr[2] + " inches corresponds to " + conversion(Integer.valueOf(inputArr[2]), inputArr[0]) + " bananas");
        }
        
        // close IO streams, then socket
        out.close();
        in.close();
        clientSocket.close();
    }

    public static void main(String[] args) throws Exception {

        //check if argument length is invalid
        if(args.length != 1) {
            System.err.println("Usage: java ConvServer port");
        }
        // create socket
        int port = Integer.parseInt(args[0]);
        ServerSocket serverSocket = new ServerSocket(port);
        System.err.println("Started server on port " + port);

        // wait for connections, and process
        try {
            while(true) {
                // a "blocking" call which waits until a connection is requested
                Socket clientSocket = serverSocket.accept();
                System.err.println("\nAccepted connection from client");
                process(clientSocket);
            }

        }catch (IOException e) {
            System.err.println("Connection Error");
        }
        System.exit(0);
    }
}
