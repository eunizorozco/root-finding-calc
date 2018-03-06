package application;
	
import java.io.IOException;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.stage.Stage;
import javafx.scene.Scene;
import javafx.scene.layout.AnchorPane;
import javafx.scene.layout.BorderPane;


public class Main extends Application {
	private Stage primaryStage;
	private AnchorPane rootLayout;
	
	@Override
	public void start(Stage primaryStage) {
		this.primaryStage = primaryStage;
		this.primaryStage.setTitle("Scientific Calculator");
		initRootLayout();
	}
	
	private void initRootLayout() {
		FXMLLoader loader = new FXMLLoader();
		loader.setLocation(Main.class.getResource("view/View.fxml"));
		try {
			rootLayout = (AnchorPane) loader.load();
			Scene scene = new Scene(rootLayout);
			primaryStage.setScene(scene);
			primaryStage.setResizable(false);
			primaryStage.show();
		} catch (IOException e) {			
			e.printStackTrace();
		}		
	}

	public static void main(String[] args) {
		launch(args);
	}
}
