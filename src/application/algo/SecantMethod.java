package application.algo;

import java.util.StringTokenizer;
import static application.algo.Utilities.evaluate;
public class SecantMethod implements RootAlgorithm{
	private String exp;
	private double[] initGuess;
	
	//<tradeoffs>
	private long runTime = 0;
	private long memory = 0;
	private int numIterations = 0;
	private double accuracy = 0;
	private double convergenceRate = 0;
	//</tradeoffs>
	//tradeoff helper:
	private double errorSum = 0;
	//end tradeoffhelper
	
	
	private double root;
	public final static int REQUIRED_INITGUESS = 2;
	public final static int DIVERGENT_LIMIT = 1000;
	private static RootAlgorithm This;
	
	public static RootAlgorithm getAlgo() {
		if(This==null) {
			This = new SecantMethod();
		}
		return This;
	}	
	//set inaccessible constructor:
	private SecantMethod() {
		
	}	
	@Override
	public long getRunTime() {
		return runTime;
	}

	@Override
	public double getMemory() {
		return memory;
	}

	@Override
	public double getRoot() {
		computeRoot();		
		return root;
	}
	
	//computes root. updates numOf iterations. updates Memory usage
	private void computeRoot() {
		System.gc();
		long startMem = Runtime.getRuntime().freeMemory();
		numIterations = 0;
		memory = 0;
		runTime = 0;			
		double xnMinus1 = 0; 
		double xn = initGuess[0];
		double xnPlus1 = initGuess[1];
		long start = System.nanoTime();	 
		
		do {			
			xnMinus1 = xn;
			xn = xnPlus1;			 
			double fn = evaluate(exp, xn);
			double fnMinus1 = evaluate(exp, xnMinus1);
			xnPlus1 = xn - (fn)*(xn-xnMinus1)/(fn-fnMinus1);			
			numIterations++;
		}while(notStopping(xn, xnPlus1) && numIterations<=DIVERGENT_LIMIT);		
		root = xnPlus1;
		runTime = System.nanoTime() - start;
		memory = startMem - Runtime.getRuntime().freeMemory();
	}

	private boolean notStopping(double x, double xPrevious) {
		return Math.abs(x-xPrevious)>= 0.0000001;
	}

	@Override
	public void setInitialGuesses(double... x) {
		if(x.length!=REQUIRED_INITGUESS) throw new IllegalArgumentException(
				String.format("There must be %d initial guesses", REQUIRED_INITGUESS));
		initGuess = x;
	}
	
	
	@Override
	public void setExpression(String exp) {
		
		this.exp = processExp(exp);
		System.out.println(this.exp);
	}
	
	//processExp returns the right side of the equation when left side is 0
	private String processExp(String exp) {
		String[] expArr = exp.split("=");
		return expArr[1] + "-(" + expArr[0] + ")";
	}

	@Override
	public int getNumIterations() {
		return numIterations;
	}

	@Override
	public String toString() {
		return "Secant Method";
	}

	@Override
	public int getInitGuessNumber() {
		return REQUIRED_INITGUESS;
	}


}
