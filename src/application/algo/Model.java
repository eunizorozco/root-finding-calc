package application.algo;

import java.util.ArrayList;

import javafx.scene.control.TextField;

public class Model {
	private static ArrayList<RootAlgorithm> algoList;
	private static RootAlgorithm selectedAlgorithm;
	
	//could be replaced by StringBuilder
	public String display;
	public String time;
	public String mem;
	public String iterations;
	
	private static Model This;
	
	//add all Algo here. Should I have used enum?
	private Model() {
		display = "";
		algoList = new ArrayList<>();
		RootAlgorithm newtonR = NewtonRaphson.getAlgo();
		algoList.add(newtonR);
		selectedAlgorithm = algoList.get(0);
		
		//Add more algo:
		RootAlgorithm bisection = BisectionMethod.getAlgo();
		algoList.add(bisection);
		RootAlgorithm secant = SecantMethod.getAlgo();
		algoList.add(secant);
	}
	
	public void solve() {
		selectedAlgorithm.setExpression(display);
		display = "X = " + String.valueOf(selectedAlgorithm.getRoot());
		time = "Time(ms): " + selectedAlgorithm.getRunTime();
		mem = "Mem(KB): " + selectedAlgorithm.getMemory();
		iterations = "Iterations: " + selectedAlgorithm.getNumIterations();
	}
	
	public ArrayList<RootAlgorithm> getAlgoList(){
		return algoList;
	}
	
	public RootAlgorithm getSelectedAlgorithm() {
		return selectedAlgorithm;
	}
	
	public void setSelectedAlgo(RootAlgorithm selectedAlgorithm) {
		this.selectedAlgorithm = selectedAlgorithm;
	}
	
	public static Model getModel() {
		if(This==null) {
			This = new Model();
		}
		return This;
	}

	public void setInitialGuess(double... guesses) {
		selectedAlgorithm.setInitialGuesses(guesses);
	}
}
