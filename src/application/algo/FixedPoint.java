package application.algo;

import java.util.StringTokenizer;

public class FixedPoint implements RootAlgorithm{
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
	public final static int REQUIRED_INITGUESS = 1;
	public final static int DIVERGENT_LIMIT = 1000;
	private static RootAlgorithm This;
	
	public static RootAlgorithm getAlgo() {
		if(This==null) {
			This = new FixedPoint();
		}
		return This;
	}	
	//set inaccessible constructor:
	private FixedPoint() {
		
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
		double x = initGuess[0];
		double xPrevious;
		long start = System.currentTimeMillis();
		
		 
		
		do {
			System.out.println(x);
			xPrevious = x;
			x = xPrevious - (Utilities.evaluate(exp, xPrevious)/Utilities.getSlope(exp, xPrevious));
			numIterations++;
		}while(notStopping(x, xPrevious) && numIterations<=DIVERGENT_LIMIT);
		
		
		root = x;
		runTime = System.currentTimeMillis() - start;
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
		return "Newton Raphson Method";
	}

	@Override
	public int getInitGuessNumber() {
		return REQUIRED_INITGUESS;
	}


}
