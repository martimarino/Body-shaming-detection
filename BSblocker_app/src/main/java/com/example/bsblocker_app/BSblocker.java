package com.example.bsblocker_app;

import javafx.application.Application;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.control.Alert;
import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.scene.control.ScrollPane;
import javafx.stage.Stage;

import twitter4j.*;
import twitter4j.Status;
import twitter4j.Twitter;
import twitter4j.TwitterException;
import twitter4j.TwitterFactory;
import twitter4j.auth.AccessToken;
import twitter4j.conf.ConfigurationBuilder;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;

public class BSblocker extends Application {

    @FXML
    private ComboBox interval, max_users;
    @FXML
    private Button start, stop;
    @FXML
    private ScrollPane scrollPane;

    static final String CONSUMER_KEY = "ecwQTUJQiCXGNn1PNrA6vEPGI";
    static final String CONSUMER_SECRET = "DRPjvsD6p2M1W6cWAJOxPZTUHN9AURE32kDnkBPmKzBus7nnm6";
    static final String ACCESS_TOKEN = "1387046165426835465-I8fMY7raJXeavEDGklAjBPg3WFxEWv";
    static final String ACCESS_TOKEN_SECRET = "LKyW4E3dje14gmqx0ZgCSp7EjxF56CcyedyqvyIjQEIEi";


    Alert a = new Alert(Alert.AlertType.NONE);



//    ArrayList users = new ArrayList<>();
//    Label list = new Label();
//    ScrollPane scrollPane = (ScrollPane) scene.lookup("#scrollPane");
//    scrollPane.setContent(list);



    @Override
    public void start(Stage stage) throws IOException {

        FXMLLoader fxmlLoader = new FXMLLoader(BSblocker.class.getResource("dm.fxml"));
        Scene scene = new Scene(fxmlLoader.load(), 600, 400);
        stage.setTitle("BSblocker");
        stage.setScene(scene);
        stage.show();

    }

    private String resolvePythonScriptPath(String path){
        File file = new File(path);
        return file.getAbsolutePath();
    }

    public void startScraping() throws IOException {
        String i, u = "";

        if (interval.getValue() == null || max_users.getValue() == null) {
            // set alert type
            a.setAlertType(Alert.AlertType.ERROR);
            a.setContentText("You have to select an interval and how many users to display.");
            // show the dialog
            a.show();
            return;
        }

        i = interval.getValue().toString();
        u = max_users.getValue().toString();
        System.out.println("Interval: " + i);
        System.out.println("Max users: " + u);
        System.out.println("Start collecting...");

       ProcessBuilder processBuilder = new ProcessBuilder("C:\\Users\\matre\\OneDrive - University of Pisa\\Desktop\\Body-shaming-detection\\venv\\Scripts\\python", resolvePythonScriptPath("BSblocker_app/src/main/java/com/example/bsblocker_app/scrape.py"));
        processBuilder.redirectErrorStream(true);

        Process process = processBuilder.start();
        BufferedReader reader =
                new BufferedReader(new InputStreamReader(process.getInputStream()));

        String line;
        while ((line = reader.readLine()) != null) {
            System.out.println(line);
        }

        try {
            int exitCode = process.waitFor();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
//*/
/*        String[] cmd = {
                "python3",
                resolvePythonScriptPath("BSblocker_app/src/main/java/com/example/bsblocker_app/scrape.py")
                //this.arg1,
        };
      Process p = Runtime.getRuntime().exec(cmd);
      System.out.println(p);*/

        /*String pathPython = "scrape.py";
        String [] cmd = new String[2];
        cmd[0] = "python";
        cmd[1] = pathPython;
        //cmd[2] = arg1;
        Runtime r = Runtime.getRuntime();
        Process p = r.exec(cmd);
        System.out.println(p);*/
//        BufferedReader in = new BufferedReader(new InputStreamReader(p.getInputStream()));
//        System.out.println(in);
//
//        String s;
//        while((s = in.readLine()) != null){
//            System.out.println(s);
//        }
        //PythonInterpreter interpreter = new PythonInterpreter();
        //interpreter.exec("import sys\nsys.path.append('pathToModules if they are not there by default')\nimport yourModule");
        //String command = "python scrape.py";
        //Process p = Runtime.getRuntime().exec(command);
        //System.out.println(p);
    }

//    curl --request GET --location 'https://api.twitter.com/2/tweets/search/recent?tweet.fields=context_annotations&max_results=100&query=camping(nature%20OR%20%22outdoor%20actvities%22)' \
//            --header 'Authorization: Bearer $BEARER_TOKEN'

    public void stopScraping() {

        System.out.println("Scraping stopped");

        return;
    }

    public static void main(String[] args) {launch();}
}