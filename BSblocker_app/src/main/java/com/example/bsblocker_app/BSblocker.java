package com.example.bsblocker_app;

import javafx.application.Application;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.stage.Stage;

import java.io.IOException;
import java.util.ArrayList;

public class BSblocker extends Application {

    @FXML
    private ComboBox interval, max_users;
    @FXML
    private Button start, stop;
    @FXML
    private ScrollPane scrollPane;

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


        String[] cmd = {
                "/bin/bash",
                "-c",
                "echo password | python script.py '"/* + packet.toString() + "'"*/  //p packet è per i parametri
        };
        Runtime.getRuntime().exec(cmd);

    }

//    curl --request GET --location 'https://api.twitter.com/2/tweets/search/recent?tweet.fields=context_annotations&max_results=100&query=camping(nature%20OR%20%22outdoor%20actvities%22)' \
//            --header 'Authorization: Bearer $BEARER_TOKEN'

    public void stopScraping() {

        System.out.println("Scraping stopped");

        return;
    }


    public static void main(String[] args) {launch();}
}