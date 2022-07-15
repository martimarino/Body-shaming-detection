module com.example.bsblocker_app {
    requires javafx.controls;
    requires javafx.fxml;


    opens com.example.bsblocker_app to javafx.fxml;
    exports com.example.bsblocker_app;
}