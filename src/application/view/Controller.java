package application.view;

import application.algo.Model;
import application.algo.RootAlgorithm;
import application.algo.Utilities;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;

public class Controller {

    @FXML
    private Label lblPrecision;

    @FXML
    private Label lblAccuracy;

    @FXML
    private Label lblTime;

    @FXML
    private Label lblMem;

    @FXML
    private Label lblIterations;

    @FXML
    private TextField txtResult;

    @FXML
    private Button btn0;

    @FXML
    private Button btn1;

    @FXML
    private Button btn5;

    @FXML
    private Button btn4;

    @FXML
    private Button btn8;

    @FXML
    private Button btn2;

    @FXML
    private Button btn9;

    @FXML
    private Button btn6;

    @FXML
    private Button btnPeriod;

    @FXML
    private Button btn3;

    @FXML
    private Button btnDel;

    @FXML
    private Button btnMultiply;

    @FXML
    private Button btnPow;

    @FXML
    private Button btnAdd;

    @FXML
    private Button btnAns;

    @FXML
    private Button btnAc;

    @FXML
    private Button btnDivide;

    @FXML
    private Button btnMinus;

    @FXML
    private Button btnEquals;

    @FXML
    private Button btn7;

    @FXML
    private Button btnClose;

    @FXML
    private Button btnSin;

    @FXML
    private Button btnCos;

    @FXML
    private Button btnTan;

    @FXML
    private Button btnOpen;

    @FXML
    private Button btnEqEquals;

    @FXML
    private Button btnSolve;

    @FXML
    private ComboBox<RootAlgorithm> cmbAlgorithms;

    @FXML
    private Button btnX;

    @FXML
    private TextField txtX1;

    @FXML
    private TextField txtX2;

    @FXML
    private TextField txtX3;
    
    Model model;
    
    @FXML
    private void initialize() {
    		model = Model.getModel();
    		initComboBox();
    }

    private void initComboBox() {
    		ObservableList<RootAlgorithm> options = FXCollections.observableArrayList(model.getAlgoList());    	
    		cmbAlgorithms.setItems(options);
    		
    		//add listener
    		cmbAlgorithms.getSelectionModel().selectedItemProperty().addListener(e -> {
    			RootAlgorithm selectedAlgo = (RootAlgorithm)cmbAlgorithms.getSelectionModel().getSelectedItem();
    			hideInitGuessesField(selectedAlgo);
    			model.setSelectedAlgo(selectedAlgo);
    			System.out.println(selectedAlgo);
    		});
    		
    		cmbAlgorithms.getSelectionModel().selectFirst(); 
	}


	private void hideInitGuessesField(RootAlgorithm selectedAlgo) {
		txtX1.setVisible(true);		
		if(selectedAlgo.getInitGuessNumber()>=2) txtX2.setVisible(true);
		else txtX2.setVisible(false);
		if(selectedAlgo.getInitGuessNumber()>=3) txtX3.setVisible(true);
		else txtX3.setVisible(false);
	}

	@FXML
    void btnHandler(ActionEvent event) {
    		Button source = (Button) event.getSource();
    		switch(source.getText()) {
    		case "1":
    			model.display = model.display + "1";    			
    			break;
    		case "2":
    			model.display = model.display + "2";
    			break;
    		case "3":
    			model.display = model.display + "3";
    			break;
    		case "4":
    			model.display = model.display + "4";
    			break;
    		case "5":
    			model.display = model.display + "5";
    			break;
    		case "6":
    			model.display = model.display + "6";
    			break;
    		case "7":
    			model.display = model.display + "7";
    			break;
    		case "8":
    			model.display = model.display + "8";
    			break;
    		case "9":
    			model.display = model.display + "9";
    			break;
    		case "0": 
    			model.display = model.display + "0";
    			break;
    		case ".":
    			model.display = model.display + ".";
    			break;
    		
    		case "X":
    			model.display = model.display + "x";
    			break;
    		case "<=>":
    			model.display = model.display + "=";
    			break;
    		case "Solve": solve();
    			break;    		
    		case "(":
    			model.display = model.display + "(";
    			break;
    		case ")":
    			model.display = model.display + ")";
    			break;
    		case "sin":
    			model.display = model.display + "sin(";
    			break;
    		case "cos":
    			model.display = model.display + "cos(";
    			break;
    		case "tan":
    			model.display = model.display + "tan(";
    			break;    			
    		case "DEL":
    			model.display = model.display.substring(0, model.display.length()-1);
    			break;
    		case "AC":
    			model.display = "";
    			break;
    		case "Ans":
    			model.display = "";
    			break;
    		case "x":
    			model.display = model.display + "*";
    			break;
    		case "÷":
    			model.display = model.display + "÷";
    			break;
    		case "+":
    			model.display = model.display + "+";
    			break;
    		case "-":
    			model.display = model.display + "-";
    			break;
    		case "=":
    			//expression is not supposed to contain X here    			
    			model.display = String.valueOf(Utilities.evaluate(model.display, 0d));    			
    			break;
    		case "^":
    			model.display = model.display + "^";
    			break;
    		default:
    			System.out.println("unpassed");
    			break;
    		}
    		updateUI();
    }

	

	private void solve() {
		model.display = txtResult.getText();
		handleInitGuesses();
		model.solve();
		updateUI();
	}

	private void handleInitGuesses() {
		RootAlgorithm algo = model.getSelectedAlgorithm();
		if(algo.getInitGuessNumber()==3) {
			model.setInitialGuess(Double.parseDouble(txtX1.getText()), Double.parseDouble(txtX2.getText()), Double.parseDouble(txtX3.getText()));
		}else if(algo.getInitGuessNumber()==2) {
			model.setInitialGuess(Double.parseDouble(txtX1.getText()), Double.parseDouble(txtX2.getText()));
		}else if(algo.getInitGuessNumber()==1) {
			model.setInitialGuess(Double.parseDouble(txtX1.getText()));
		}
	}

	private void updateUI() {
		lblTime.setText(model.time);
		lblMem.setText(model.mem);
		lblIterations.setText(model.iterations);
		txtResult.setText(model.display);
	}

}
